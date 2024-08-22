from dataclasses import dataclass
from enum import Enum


@dataclass(kw_only=True)
class Embedding:
    index: int
    version: int


@dataclass(kw_only=True)
class Cluster:
    center: Embedding
    members: list


class FileType(Enum):
    PDF = ".pdf"
    DOC = ".doc"
    DOCX = ".docx"
    ODF = ".odf"
    TXT = ".txt"
    TEX = ".tex"
    UNKNOWN = "unknown"


@dataclass(kw_only=True)
class File:
    path: str
    file_type: FileType
    total_lines: int
    cluster: Cluster
    representation: Embedding
    parts: dict[int, Embedding]


@dataclass(kw_only=True)
class FileLocator:
    regex_pattern: str
    start: int
    end: int
    page: int = None
    paragraph: int = None
