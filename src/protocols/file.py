from typing import Protocol
from src.data_types import File, FileType
from src.protocols.embeddings import Embedder
from src.protocols.search import ClusterMap

class FileBuffer(Protocol):
    @property
    def supported_endings(self) -> list[FileType]:
        ...

    def read(self, path: str) -> str:
        ...

    def check_file(self, path) -> bool:
        ...


class FileFactory(Protocol):
    @property
    def file_type(self) -> FileType:
        ...

    def get_reader(self, path: str) -> FileBuffer:
        ...


class FileBuilder(Protocol):
    def read(self, path: str) -> "FileBuilder":
        ...

    def embed(self, embedder: Embedder) -> "FileBuilder":
        ...

    def assign_cluster(self, clusters: ClusterMap) -> "FileBuilder":
        ...

    def get_file(self) -> File:
        ...
