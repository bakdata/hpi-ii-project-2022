from bakdata.rb.corporate.v1.corporate_pb2 import Corporate
from common.base_producer import BaseProducer


class RbCorporateProducer(BaseProducer):
    TOPIC = "rb-corporates"

    def __init__(self):
        super().__init__(RbCorporateProducer.TOPIC, Corporate)

    def get_key(self, corporate: Corporate):
        return corporate.id
