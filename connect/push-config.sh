#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
BASE_CONFIG=${3:-"$(dirname $0)/elastic-sink.json"}
KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

data=$(cat $BASE_CONFIG | jq -s '.[0]')
curl -X POST $KAFKA_CONNECT_API --data "$data" -H "content-type:application/json"
