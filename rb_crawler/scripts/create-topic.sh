#!/bin/bash

KAFKA_REST_ADDRESS=${1:-localhost}
KAFKA_REST_PORT=${2:-8082}
KAFKA_REST_API="$KAFKA_REST_ADDRESS:$KAFKA_REST_PORT/v3/clusters"
TOPIC_NAME="corporate-events"

status="$(curl -Is $KAFKA_REST_API | head -1)"
validate=($status)
if [ ${validate[-2]} != "200" ]; then
  echo "Failed to connect to Kafka-Rest Proxy on port ${KAFKA_REST_PORT} check your connection to the cluster."
  exit 1
fi

CLUSTER_ID=$(curl --silent -X GET $KAFKA_REST_API | jq -r '.data | .[0] | .cluster_id')
curl --silent -X POST -H "Content-Type: application/json" --data "{\"topic_name\": \"${TOPIC_NAME}\", \"partitions_count\": 1}" "$KAFKA_REST_API"/"$CLUSTER_ID"/topics | jq
