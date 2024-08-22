from numpy import ndarray
from typing import Iterable, Protocol

from src.data_types import FileLocator


class TextTransform(Protocol):
    def clean(self) -> tuple[Iterable[str], Iterable[FileLocator]]:
        ...

    def generate_batch_finder(self, raw_text, clean_text: str) -> FileLocator:
        ...


class Embedder(Protocol):
    def load_embedder(self) -> None:
        ...

    def embed(self, text_chunk: str) -> ndarray:
        ...

    def batch_embed(self, text: Iterable[str]) -> ndarray:
        ...
