from bakdata.rb.person.v1.person_pb2 import Person
from common.base_producer import BaseProducer


class RbPersonProducer(BaseProducer):
    TOPIC = "rb-persons"

    def __init__(self):
        super().__init__(RbPersonProducer.TOPIC, Person)

    def get_key(self, person: Person):
        return person.id
