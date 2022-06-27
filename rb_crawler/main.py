import logging
import os
from time import sleep

import click
import requests
from parsel import Selector

from bakdata.rb.announcement.v1.announcement_pb2 import Type
from bakdata.common.error.v1.crawl_error_pb2 import CrawlError
from rb_crawler.constant import State
from rb_crawler.extractor.rb_announcement_extractor import RbAnnouncementExtractor
from rb_crawler.extractor.rb_corporate_extractor import RbCorporateExtractor
from rb_crawler.extractor.rb_person_extractor import RbPersonExtractor
from rb_crawler.extractor.utils import get_announcement_type
from rb_crawler.producer.rb_announcement_producer import RbAnnouncementProducer
from rb_crawler.producer.rb_corporate_producer import RbCorporateProducer
from rb_crawler.producer.rb_error_producer import RbErrorProducer
from rb_crawler.producer.rb_person_producer import RbPersonProducer

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)


@click.command()
@click.option("-i", "--id", "rb_id", type=int, help="The rb_id to initialize the crawl from")
@click.option("-s", "--state", type=click.Choice(State), help="The state ISO code")
def run(rb_id: int, state: State):
    if state == State.SCHLESWIG_HOLSTEIN:
        if rb_id < 7830:
            error = ValueError("The start rb_id for the state SCHLESWIG_HOLSTEIN (sh) is 7831")
            log.error(error)
            exit(1)

    corporate_producer = RbCorporateProducer()
    person_producer = RbPersonProducer()
    announcement_producer = RbAnnouncementProducer()
    error_producer = RbErrorProducer()

    while True:
        try:
            selector = send_request(rb_id=rb_id, state=state)
            corporate_extractor = RbCorporateExtractor(selector)
            announcement_type = get_announcement_type(selector)
            announcement_extractor = RbAnnouncementExtractor(selector, rb_id, state, announcement_type)
            if announcement_type == Type.TYPE_NEW_ENTRY:
                announcement = announcement_extractor.extract()
                announcement_producer.produce_to_topic(announcement)

                corporate = corporate_extractor.extract()
                corporate_producer.produce_to_topic(corporate)

                person_extractor = RbPersonExtractor(selector, corporate)
                person_list = person_extractor.extract()
                for person in person_list:
                    person_producer.produce_to_topic(person)
            elif announcement_type == Type.TYPE_UPDATE:
                announcement = announcement_extractor.extract()
                announcement_producer.produce_to_topic(announcement)

                corporate = corporate_extractor.extract()
                corporate_producer.produce_to_topic(corporate)
            rb_id = rb_id + 1
        except Exception as ex:
            log.error(f"Skipping {rb_id} in state {state}")
            log.error(f"Cause: {ex}")
            crawl_error = CrawlError()
            crawl_error.id = f"{state}_{rb_id}"
            crawl_error.cause = str(ex)
            error_producer.produce_to_topic(crawl_error)
            rb_id = rb_id + 1
            continue


def send_request(rb_id: int, state: str) -> Selector:
    url = f"https://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?rb_id={rb_id}&land_abk={state}"
    # For graceful crawling! Remove this at your own risk!
    sleep(0.5)
    text = requests.get(url=url).text
    return Selector(text=text)


if __name__ == "__main__":
    run()
