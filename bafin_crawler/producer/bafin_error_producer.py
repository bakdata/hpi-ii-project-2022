from bakdata.common.error.v1.crawl_error_pb2 import CrawlError
from common.base_producer import BaseProducer


class BafinErrorProducer(BaseProducer):
    TOPIC = "bafin-errors"

    def __init__(self):
        super().__init__(BafinErrorProducer.TOPIC, CrawlError)

    def get_key(self, crawl_error: CrawlError):
        return crawl_error.id
