import logging

from parsel import Selector

from bakdata.rb.announcement.v1.announcement_pb2 import Announcement, Type
from common.base_extractor import BaseExtractor
from rb_crawler.extractor.utils import extract_company_reference_id

log = logging.getLogger(__name__)


class RbAnnouncementExtractor(BaseExtractor):
    def __init__(self, selector: Selector, rb_id: int, state: str, announcement_type: Type):
        super().__init__(selector)
        self.rb_id = rb_id
        self.state = state
        self.announcement_type = announcement_type

    def extract(self) -> Announcement:
        announcement = Announcement()
        announcement.id = f"{self.state}_{self.rb_id}"
        court_reference_id = extract_company_reference_id(self.selector)
        reference_id = court_reference_id[1].strip().replace(" ", "")
        announcement.reference_id = reference_id
        announcement.event_date = self.selector.xpath("/html/body/font/table/tr[4]/td/text()").get()
        raw_text: str = self.selector.xpath("/html/body/font/table/tr[6]/td/text()").get()
        announcement.information = raw_text
        announcement.type = self.announcement_type
        return announcement
