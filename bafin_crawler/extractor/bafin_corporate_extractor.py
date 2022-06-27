from parsel import Selector

from common.base_extractor import BaseExtractor
from bakdata.bafin.corporate.v1.corporate_pb2 import Corporate


class BafinCorporateExtractor(BaseExtractor):
    def __init__(self, selector: Selector):
        super().__init__(selector)

    def extract(self) -> Corporate:
        corporate = Corporate()
        corporate.bafin_id = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[1]/td[2]/text()").get("")
        corporate.lei = self.selector.xpath(f"//table[@id='3']/tbody/tr[3]/td/text()").get("")
        corporate.name = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[2]/td[2]/text()").get("").strip()
        corporate.street = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[3]/td[2]/text()").get("")
        corporate.postal_code = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[4]/td[2]/text()").get("")
        corporate.city = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[5]/td[2]/text()").get("")
        corporate.country = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[6]/td[2]/text()").get("")
        corporate.id = self.generate_id(corporate.name)
        return corporate
