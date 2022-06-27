from bakdata.bafin.trade.v1.trade_pb2 import Trade
from common.base_producer import BaseProducer


class BafinTradeProducer(BaseProducer):
    TOPIC = "bafin-trades"

    def __init__(self):
        super().__init__(BafinTradeProducer.TOPIC, Trade)

    def get_key(self, trade: Trade):
        return trade.id
