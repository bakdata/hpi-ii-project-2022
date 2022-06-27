import logging
import re
from typing import Sequence

from parsel import Selector

from bakdata.rb.corporate.v1.corporate_pb2 import Corporate
from bakdata.rb.person.v1.person_pb2 import Person
from common.base_extractor import BaseExtractor

PERSON_PATTERN = re.compile(r"(([\w -]+, )([\w -]+, )?([\w.\/ -]+), \*\d{2}.\d{2}.\d{4})(, )?([\w.\/ -]+)?")
log = logging.getLogger(__name__)


class RbPersonExtractor(BaseExtractor):
    def __init__(self, selector: Selector, corporate: Corporate):
        super().__init__(selector)
        self.corporate = corporate

    def extract(self) -> Sequence[Person]:
        raw_text: str = self.selector.xpath("/html/body/font/table/tr[6]/td/text()").get()
        groups = PERSON_PATTERN.findall(raw_text)
        person_list: list = []

        for group in groups:
            person = Person()
            full_officer_info = group[0]
            officer_info_list: list = full_officer_info.split(", ")
            person.first_name = officer_info_list[1]
            person.last_name = officer_info_list[0]
            person.corporate_id = self.corporate.id
            key: str = "rb" + person.first_name + person.last_name + self.corporate.name
            person.id = BaseExtractor.generate_id(key)

            try:
                if "*" in officer_info_list[2]:
                    person.birthday = officer_info_list[2]
                    person.birth_location = group[5]
                else:
                    person.birth_location = officer_info_list[2]
                    person.birthday = officer_info_list[3]
            except IndexError:
                log.error("Cannot extract birthday and birth location")
                continue

            person.birthday = person.birthday.replace("*", "")
            person_list.append(person)

        return person_list
