import logging
import os

from tr_crawler.tr_extractor import TrExtractor

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

def run():

    TrExtractor().extract()

if __name__ == "__main__":
    run()