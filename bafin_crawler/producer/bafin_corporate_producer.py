from bakdata.bafin.corporate.v1.corporate_pb2 import Corporate
from common.base_producer import BaseProducer


class BafinCorporateProducer(BaseProducer):
    TOPIC = "bafin-corporates"

    def __init__(self):
        super().__init__(BafinCorporateProducer.TOPIC, Corporate)

    def get_key(self, corporate: Corporate):
        return corporate.id
