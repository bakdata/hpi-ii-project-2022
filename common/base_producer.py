import logging
from abc import ABC, abstractmethod
from typing import TypeVar
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer

T = TypeVar("T")
log = logging.getLogger(__name__)


class BaseProducer(ABC):
    BOOTSTRAP_SERVER: str = "localhost:29092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"

    def __init__(self, topic, schema):
        self.topic = topic
        schema_registry_conf = {"url": BaseProducer.SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        protobuf_serializer = ProtobufSerializer(
            schema, schema_registry_client, {"use.deprecated.format": True}
        )

        producer_conf = {
            "bootstrap.servers": BaseProducer.BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": protobuf_serializer,
        }

        self.producer = SerializingProducer(producer_conf)

    @abstractmethod
    def get_key(self, message: T):
        pass

    def produce_to_topic(self, message: T):
        self.producer.produce(
            topic=self.topic, partition=-1, key=self.get_key(message), value=message,
            on_delivery=self.delivery_report
        )

        # It is a naive approach to flush after each produce this can be optimised
        self.producer.poll()

    def delivery_report(self, err, msg):
        """
        Reports the failure or success of a message delivery.
        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        Note:
            In the delivery report callback the Message.key() and Message.value()
            will be the binary format as encoded by any configured Serializers and
            not the same object that was passed to produce().
            If you wish to pass the original object(s) for key and value to delivery
            report callback we recommend a bound callback or lambda where you pass
            the objects along.
        """
        if err is not None:
            log.error("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        log.info(
            "Record with key {} successfully produced to {} [{}] at offset {}".format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()
            )
        )
