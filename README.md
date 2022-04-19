# hpi-ii-project-2022

## Architecture

## Setup

This project uses [poetry](https://python-poetry.org/) as a build tool.
To install all the dependencies, just run `peotry install`.

This project uses Protobuf for serializing and deserializing objects. We provided a
simple [protobuf schema](./proto/bakdata/corporate/v1/corporate.proto).
Furthermore, you need to generate the Python code from the proto file.
To do so run the [`generate-proto.sh`](./generate-proto.sh)
script.
This script uses the Protobuf compiler to generate the model class under the `build/gen/bakdata/corporate/v1` folder
with the name `corporate_pb2.py`.

## Run

### Infrastructure

Use `docker-compose up -d` to start all the services: Zookeeper, Kafka, Schema Registry, Kafka Rest Proxy, Kowl,
Kafka Connect, and Elasticsearch.
After all the services are up and running you can use the [`create-topic.sh`](./rb_crawler/scripts/create-topic.sh)
script to create the `corporate-events` topic.
This script uses the [Kafka REST Proxy](https://github.com/confluentinc/kafka-rest) to communicate with Kafka.

### Kafka Connect

After all the services are up and running, you need to configure Kafka Connect to use the Elasticsearch sink connector.
The config file is a JSON formatted file. We provided a [basic configuration file](./connect/elastic-sink.json).
You can find more information about the configuration properties on
the [official documentation page](https://docs.confluent.io/kafka-connect-elasticsearch/current/overview.html).

### RB Crawler

[//]: # (TODO Write commands on how to start the python crawler)
