from bakdata.bafin.person.v1.person_pb2 import Person
from common.base_producer import BaseProducer


class BafinPersonProducer(BaseProducer):
    TOPIC = "bafin-persons"

    def __init__(self):
        super().__init__(BafinPersonProducer.TOPIC, Person)

    def get_key(self, person: Person):
        return person.id
