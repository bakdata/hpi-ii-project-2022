from bakdata.rb.corporate.v1.corporate_pb2 import Corporate
from common.base_extractor import BaseExtractor
from rb_crawler.extractor.utils import extract_company_reference_id


class RbCorporateExtractor(BaseExtractor):
    def extract(self) -> Corporate:
        corporate = Corporate()
        raw_text: str = self.selector.xpath("/html/body/font/table/tr[6]/td/text()").get()
        company_name_address = raw_text.split(",")
        court_reference_id = extract_company_reference_id(self.selector)
        corporate.reference_id = court_reference_id[1].replace(" ", "")
        corporate.name = company_name_address[0].replace(f"{court_reference_id[1]}: ", "")
        corporate.street = company_name_address[2]

        postal_code_city = (company_name_address[3].split(".")[0])[1:]
        corporate.postal_code = postal_code_city.split(" ")[0]
        corporate.city = postal_code_city.split(" ")[1]
        corporate.id = self.generate_id(corporate.name)
        return corporate
