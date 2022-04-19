#!/bin/bash

KAFKA_REST_ADDRESS=${1:-localhost}
KAFKA_REST_PORT=${2:-8082}
KAFKA_REST_API="$KAFKA_REST_ADDRESS:$KAFKA_REST_PORT/v3/clusters"
TOPIC_NAME="corporate-events"

CLUSTER_ID=$(curl --silent -X GET $KAFKA_REST_API | jq -r '.data | .[0] | .cluster_id')
curl --silent -X POST -H "Content-Type: application/json" --data "{\"topic_name\": \"${TOPIC_NAME}\", \"partitions_count\": 1}" "$KAFKA_REST_API"/"$CLUSTER_ID"/topics | jq
