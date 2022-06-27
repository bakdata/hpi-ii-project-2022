from parsel import Selector

from bakdata.bafin.trade.v1.trade_pb2 import Trade
from common.base_extractor import BaseExtractor


class BafinTradeExtractor(BaseExtractor):
    def __init__(self, selector: Selector, message_id: str, bafin_id: str, person_id: str):
        super().__init__(selector)
        self.message_id = message_id
        self.bafin_id = bafin_id
        self.person_id = person_id

    def extract(self) -> Trade:
        trade = Trade()

        trade.id = f"{self.message_id}_{self.bafin_id}"
        trade.instrument_type = self.selector.xpath(f"//table[@id='4']/tbody/tr[1]/td[2]/text()").get("").strip()
        trade.isin = self.selector.xpath(f"//table[@id='4']/tbody/tr[2]/td[2]/text()").get("")
        trade.type = self.selector.xpath(f"//table[@id='4']/tbody/tr[4]/td[1]/text()").get("").strip()
        trade.description = self.selector.xpath(f"//table[@id='4']/tbody/tr[6]/td[1]/text()").get("").strip()
        trade.price = (
            self.selector.xpath(f"//table[@id='transaktion']/tfoot/tr/td/table/tr[2]/td[2]/text()").get("").strip()
        )
        trade.total = (
            self.selector.xpath(f"//table[@id='transaktion']/tfoot/tr/td/table/tr[3]/td[2]/text()").get("").strip()
        )
        trade.date = (
            self.selector.xpath(f"//table[@id='transaktion']/tfoot/tr/td/table/tr[5]/td[1]/text()").get("").strip()
        )
        trade.place = (
            self.selector.xpath(f"//table[@id='transaktion']/tfoot/tr/td/table/tr[7]/td[2]/text()").get("").strip()
        )
        trade.mic = (
            self.selector.xpath(f"//table[@id='transaktion']/tfoot/tr/td/table/tr[8]/td[2]/text()").get("").strip()
        )

        trade.person_id = self.person_id

        return trade
