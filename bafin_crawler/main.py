import logging
import os
from time import sleep

import click
import requests
from parsel import Selector

from bafin_crawler.extractor.bafin_corporate_extractor import BafinCorporateExtractor
from bafin_crawler.extractor.bafin_person_extractor import BafinPersonExtractor
from bafin_crawler.extractor.bafin_trade_extractor import BafinTradeExtractor
from bafin_crawler.producer.bafin_corporate_producer import BafinCorporateProducer
from bafin_crawler.producer.bafin_error_producer import BafinErrorProducer
from bafin_crawler.producer.bafin_person_producer import BafinPersonProducer
from bafin_crawler.producer.bafin_trade_producer import BafinTradeProducer
from bakdata.common.error.v1.crawl_error_pb2 import CrawlError

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)
BAFIN_BASE_URL = "https://portal.mvp.bafin.de/database/DealingsInfo"


@click.command()
@click.option("-i", "--id", "message_id", type=int, help="The message_id to initialize the crawl from")
def run(message_id: int):
    corporate_producer = BafinCorporateProducer()
    person_producer = BafinPersonProducer()
    trade_producer = BafinTradeProducer()
    error_producer = BafinErrorProducer()

    while True:
        try:
            selector = send_request(message_id=message_id)

            corporate_extractor = BafinCorporateExtractor(selector)
            corporate = corporate_extractor.extract()
            corporate_producer.produce_to_topic(corporate)

            person_extractor = BafinPersonExtractor(selector, corporate)
            person = person_extractor.extract()
            person_producer.produce_to_topic(person)

            trade_extractor = BafinTradeExtractor(selector, message_id, corporate.bafin_id, person.id)
            trade = trade_extractor.extract()
            trade_producer.produce_to_topic(trade)

            message_id = message_id + 1
        except Exception as ex:
            log.error(f"Skipping {message_id}")
            log.error(f"Cause: {ex}")
            crawl_error = CrawlError()
            crawl_error.id = f"{message_id}"
            crawl_error.cause = str(ex)
            error_producer.produce_to_topic(crawl_error)
            message_id = message_id + 1
            continue


def send_request(message_id: int) -> Selector:
    overview_url = f"{BAFIN_BASE_URL}/ergebnisListe.do?cmd=loadEmittentenAction&meldepflichtigerId={message_id}#"
    # For graceful crawling! Remove this at your own risk!
    sleep(0.1)
    overview_text = requests.get(url=overview_url).text

    overview_selector = Selector(text=overview_text)

    if overview_selector.xpath("//div[@id='contentError']").get() is not None:
        raise ValueError(f"The current message id {message_id} does not exists anymore. Please use a newer one.")

    bafin_id = overview_selector.xpath(
        "/html/body/div[1]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[2]/text()"
    ).get()

    # For graceful crawling! Remove this at your own risk!
    sleep(0.1)
    detailed_url = f"{BAFIN_BASE_URL}/transaktionListe.do?meldungId={message_id}&emittentBafinId={bafin_id}"
    detailed_text = requests.get(url=detailed_url).text
    selector = Selector(text=detailed_text)
    return selector


if __name__ == "__main__":
    run()
