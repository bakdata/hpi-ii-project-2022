from parsel import Selector

from bakdata.bafin.corporate.v1.corporate_pb2 import Corporate
from bakdata.bafin.person.v1.person_pb2 import Person, Role
from common.base_extractor import BaseExtractor


class BafinPersonExtractor(BaseExtractor):
    def __init__(self, selector: Selector, corporate: Corporate):
        super().__init__(selector)
        self.corporate = corporate

    def extract(self) -> Person:
        person = Person()
        first_name: str = self.selector.xpath(f"//table[@id='1']/tbody/tr[2]/td[2]/text()").get("").strip()
        last_name = self.selector.xpath(f"//table[@id='1']/tbody/tr[3]/td[2]/text()").get("").strip()
        bafin_id = self.selector.xpath(f"//table[@id='emittent']/tbody/tr[1]/td[2]/text()").get("")

        person.last_name = last_name
        self.corporate.bafin_id = bafin_id
        if first_name == "":
            raise Exception("The current transaction is not done by a real person.")

        person.title = self.selector.xpath(f"//table[@id='1']/tbody/tr[1]/td[2]/text()").get("").strip()
        person.first_name = first_name
        person.role = Role.ROLE_EXECUTIVE_DIRECTOR

        person.id = self.generate_id("bafin" + person.first_name + person.last_name + self.corporate.name)
        person.corporate_id = self.corporate.id
        return person
