# HPI information integration project SoSe 2022

This repository provides a code base for the information integration course in the summer semester of 2022. Below you
can find the documentation for setting up the project.

## Prerequisites

- Install [Poetry](https://python-poetry.org/docs/#installation)
- Install [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
- Install [Protobuf compiler (protoc)](https://grpc.io/docs/protoc-installation/). If you are using windows you can
  use [this guide](https://www.geeksforgeeks.org/how-to-install-protocol-buffers-on-windows/)
- Install [jq](https://stedolan.github.io/jq/download/)

## Architecture

![](architecture.png)

## Components

### RB website

The [Registerbekanntmachung website](https://www.handelsregisterbekanntmachungen.de/index.php?aktion=suche) contains
announcements concerning entries made into the companies, cooperatives, and
partnerships registers within the electronic information and communication system. You can search for the announcements.
Each announcement can be requested through the link below. You only need to pass the query parameters `rb_id`
and `land_abk`. For instance, we chose the state Rheinland-Pfalz `rp` with an announcement id of `56267`, the
new entry of the company BioNTech.

```shell
export STATE="rp" 
export RB_ID="56267"
curl -X GET  "https://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?rb_id=$RB_ID&land_abk=$STATE"
```

### RB crawler

The Registerbekanntmachung crawler (rb_crawler) sends a get request to the link above with parameters (`rb_id`
and `land_abk`) passed to it and extracts the information from the response.

We use [Protocol buffers](https://developers.google.com/protocol-buffers)
to define our [schema](proto/bakdata/rb/announcement/v1/announcement.proto).
The crawler uses the generated model class (i.e., `Announcement` class) from
the [protobuf schema](proto/bakdata/rb/announcement/v1/announcement.proto).
We will explain further how you can generate this class using the protobuf compiler.

The compiler creates an `Announcement` object with the fields defined in the schema.
The crawler fills the object fields with the extracted data from the website.
It then serializes the `Announcement` object to bytes so that Kafka can read it and produces it to
the `rb-announcements`topic.

After that, it increments the `rb_id` value and sends another GET request.
This process continues until the end of the announcements is reached, and the crawler will stop automatically.

### rb-announcements topic

The `rb-annourncements` topic holds all the announcements produced by the `rb_crawler`. Each message in a Kafka topic
consist of a key and value.

The key type of this topic is `String`. The `rb_crawler generates the key`. The key
is a combination of the `land_abk` and the `rb_id`. If we consider the `rb_id` and `land_abk` from the example above,
the key will look like this: `rp_56267`.

The value of the message contains more information like `event_name`, `event_date`, and more. Therefore, the value type
is complex and needs a schema definition.

### rb-corporates topic

This topic contains the extracted information about the corporates of the Registerbekanntmachung. The key is a self
generated hash from the corporate name and the value is a
[complex schema type](proto/bakdata/rb/corporate/v1/corporate.proto).

### rb-persons topic

This topic contains the extracted information about the persons of the Registerbekanntmachung. The key is a self
generated hash from the source(i.e., rb), firstname, lastname, and corporate name. The value is a
[complex schema type](proto/bakdata/rb/person/v1/person.proto).

### BaFin website

The Federal Financial Supervisory Authority [(BaFin)](https://www.bafin.de/EN/Homepage/homepage_node.html) brings
together under one roof the supervision of banks and
financial services providers, insurance undertakings and securities trading.
The website also contains registered announcements of managers’ transactions pursuant to Article 19 of the MAR.
These announcements describe the transaction details that an executive director (manager) of a company did in the
stocks. The website holds the transaction information in a one-year time window.
The first announcement has a message ID of `17987` at the time of this writing.

### BaFin crawler

This crawler extracts the information from the BaFin portal and fills the model objects with the extracted data.
Moreover, it serializes the objects and produces each of them to the desired topic.

The crawler is initialized with a `message_id` at the beginning of the crawl and sends a request to the portal URL of
BaFin. This process is demonstrated in the script below:

```shell
export MESSAGE_ID="17987"
curl -X GET  https://portal.mvp.bafin.de/database/DealingsInfo/ergebnisListe.do?cmd=loadEmittentenAction&meldepflichtigerId=$MEESAGE_ID
```

After retrieving the HTML of the page, the crawler extracts the `BaFin-ID` in the table and
sends another request to retrieve the detailed transaction information. This is demonstrated with a shell script:

```shell
export MESSAGE_ID="17987"
export BAFIN_ID=40002082
https://portal.mvp.bafin.de/database/DealingsInfo/transaktionListe.do?cmd=loadTransaktionenAction&emittentBafinId=$BAFIN_ID&meldungId=$MESSAGE_ID&KeepThis=true&TB_iframe=true&modal=true
```

The crawler uses the HTML response and extracts the information, and produces them for each topic.
It then increases the `message_id` and repeats this process.

### bafin_trades topic

This topic contains all the transaction information a person made.
The key is a self-generated string from the message-id and the BaFin id.
The value is a [complex schema type](proto/bakdata/bafin/trade/v1/trade.proto).

### bafin_corporates topic

The `bafin_corporates` topic contains all the information about a corporate.
The key is a self-generated hash from the corporate name.
The value is a [complex schema type](proto/bakdata/bafin/corporate/v1/corporate.proto).

### bafin_persons topic

This topic contains the extracted information about the persons who made a transaction. The key is a self-generated hash from the source (i.e., BaFin), first name, last name, and corporate name. The value is a
[complex schema type](proto/bakdata/bafin/person/v1/person.proto).

### Kafka Connect

[Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html) is a tool to move large data sets into
(source) and out (sink) of Kafka.
Here we only use the Sink connector, which consumes data from a Kafka topic into a secondary index such as
Elasticsearch.

We use the [Elasticsearch Sink Connector](https://docs.confluent.io/kafka-connect-elasticsearch/current/overview.html)
to move the data from the `coporate-events` topic into the Elasticsearch.

## Setup

This project uses [Poetry](https://python-poetry.org/) as a build tool.
To install all the dependencies, just run `poetry install`.

This project uses Protobuf for serializing and deserializing objects.
You can find these schemas under the [`proto`](proto) folder.
Furthermore, you must generate the Python code for the model class from the proto file.
To do so run the [`generate-proto.sh`](./generate-proto.sh) script.
This script uses the [Protobuf compiler (protoc)](https://grpc.io/docs/protoc-installation/) to generate the model class
under the [`bakdata`](bakdata) folder.

## Run

### Infrastructure

Use `docker-compose up -d` to start all the services: [Zookeeper](https://zookeeper.apache.org/)
, [Kafka](https://kafka.apache.org/), [Schema
Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
, [Kafka REST Proxy]((https://github.com/confluentinc/kafka-rest)), [Kowl](https://github.com/redpanda-data/kowl),
[Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html),
and [Elasticsearch](https://www.elastic.co/elasticsearch/). Depending on your system, it takes a couple of minutes
before the services are up and running. You can use a tool
like [lazydocker](https://github.com/jesseduffield/lazydocker) to check the status of the services.

**NOTE:** Kafka Connect start time for the Apple silicon is more than 5 minutes!
You can start using Kafka Connect whenever the status of the container is `running (healthy)`.

### Kafka Connect

After all the services are up and running, you need to configure Kafka Connect to use
the Elasticsearch or the Neo4j sink connector.
The config file is a JSON formatted file. We provided the sink configuration for the different topics under the
[`connect`](./connect) folder.

You can find more information about the configuration properties for the Elasticsearch sink on
the [official documentation page](https://docs.confluent.io/kafka-connect-elasticsearch/current/overview.html).
Details on configuring the Neo4j sink connector are available on the
[official documentation page](https://neo4j.com/labs/kafka/4.0/kafka-connect/).

To start the connector, you must push the JSON config file to Kafka. You can use the UI dashboard in Kowl or
the [bash script provided](./connect/push-config.sh). It is possible to remove a connector by deleting it
through Kowl's UI dashboard or calling the deletion API in the [bash script provided](./connect/delete-config.sh).

### RB crawler

You can start the crawler with the command below:

```shell
poetry run python rb_crawler/main.py --id $RB_ID --state $STATE
```

The `--id` option is an integer, which determines the initial event in the Handelsregisterbekanntmachungen to be
crawled.

The `--state` option takes a string (only the ones listed above). This string defines the state where the crawler should
start from.

You can use the `--help` option to see the usage:

```
Usage: main.py [OPTIONS]

Options:
  -i, --id INTEGER                The rb_id to initialize the crawl from
  -s, --state [bw|by|be|br|hb|hh|he|mv|ni|nw|rp|sl|sn|st|sh|th]
                                  The state ISO code
  --help                          Show this message and exit.
```

### BaFin crawler

You can start the crawler with the command below:

```shell
poetry run python rb_crawler/main.py --id $MESSAGE_ID
```

The `--id` option is an integer, which determines the initial event in the BaFin portal to be
crawled.

You can use the `--help` option to see the usage:

```
Usage: main.py [OPTIONS]

Options:
  -i, --id INTEGER  The message_id to initialize the crawl from
  --help            Show this message and exit.
```

## Query data

### Kowl

[Kowl](https://github.com/redpanda-data/kowl) is a web application that helps you manage and debug your Kafka workloads
effortlessly. You can create, update, and delete Kafka resources like Topics and Kafka Connect configs.
You can see Kowl's dashboard in your browser under http://localhost:8080.

### Elasticsearch

To query the data from Elasticsearch, you can use
the [query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl.html) of elastic. For example:

```shell
curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match": {
            <field>
        }
    }
}
'
```

`<field>` is the field you wish to search. For example:

```
"first_name":"Sussane"
```

## Teardown

You can stop and remove all the resources by running:

```shell
docker-compose down
```
