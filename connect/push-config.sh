#!/bin/bash

BASE_CONFIG=${1:-"$(dirname $0)/elastic-corporate-sink.json"}
KAFKA_CONNECT_ADDRESS=${2:-localhost}
KAFKA_CONNECT_PORT=${3:-8083}
KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

data=$(cat $BASE_CONFIG | jq -s '.[0]')
curl -X POST $KAFKA_CONNECT_API --data "$data" -H "content-type:application/json"
