import re
from typing import Tuple

from parsel import Selector

from bakdata.rb.announcement.v1.announcement_pb2 import Type

PATTERN = re.compile(r"Amtsgericht (.+) Aktenzeichen: (.+)[ \t]+$")


def extract_company_reference_id(selector: Selector) -> Tuple:
    text = selector.xpath("/html/body/font/table/tr[1]/td/nobr/u/text()").get()
    groups = PATTERN.match(text).groups()
    return groups


def get_announcement_type(selector: Selector) -> Type:
    event_type = selector.xpath("/html/body/font/table/tr[3]/td/text()").get()
    if event_type == "Neueintragungen":
        return Type.TYPE_NEW_ENTRY
    elif event_type == "Veränderungen":
        return Type.TYPE_UPDATE
    elif event_type == "Löschungen":
        return Type.TYPE_DELETE
    return Type.TYPE_UNSPECIFIED
