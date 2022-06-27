import hashlib
from abc import ABC, abstractmethod
from typing import TypeVar

from parsel import Selector

T = TypeVar("T")


class BaseExtractor(ABC):

    def __init__(self, selector: Selector):
        self.selector = selector

    @abstractmethod
    def extract(self) -> T:
        pass

    @classmethod
    def generate_id(cls, key: str) -> str:
        sha_hash = hashlib.sha256()
        sha_hash.update(key.lower().replace(" ", "").encode("utf-8"))
        return sha_hash.hexdigest()
