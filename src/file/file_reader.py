import PyPDF2
import docx

from src.data_types import FileType
from src.protocols.file import FileBuffer, FileFactory as FileFactoryProtocol


class FileReader(FileBuffer):
    def __init__(self, supported_endings: list[FileType]) -> None:
        self.supported_endings = supported_endings

    def check_file(self, path: str) -> bool:
        return any(map(lambda x: path.endswith(x.value), self.supported_endings))

    def read(self, path: str) -> str:
        raise NotImplementedError


class RawTextFile(FileReader):
    def __init__(self) -> None:
        super().__init__(supported_endings=[FileType.TEX, FileType.TXT])

    def read(self, path: str) -> str:
        with open(path) as file:
            return file.read()


class PdfFile(FileReader):
    def __init__(self) -> None:
        super().__init__(supported_endings=[FileType.PDF])

    def read(self, path: str) -> str:
        text = []
        with open(path) as file:
            pdf = PyPDF2.PdfFileReader(file)
            for i in range(pdf.numPages):
                page = pdf.getPage(i)
                text.append(page.extract_text())
        return "\nPAGEBREAK\n".join(text)


class OfficeFile(FileReader):
    def __init__(self) -> None:
        super().__init__(supported_endings=[FileType.DOC, FileType.DOCX, FileType.ODF])

    def read(self, path: str) -> str:
        doc = docx.Document(path)
        text = [paragraph.text for paragraph in doc.paragraphs]
        return "\nPARBREAK\n".join(text)


class FileFactory(FileFactoryProtocol):
    readers: list[FileReader] = [PdfFile(), OfficeFile(), RawTextFile()]

    def __init__(self) -> None:
        super().__init__()
        self._type = None

    @property
    def file_type(self) -> FileType:
        return self._type

    def get_reader(self, path: str) -> FileReader:
        for reader in self.readers:
            if reader.check_file(path):
                self._type = list(
                    filter(lambda x: path.endswith(x.value), reader.supported_endings)
                )[0]
                return reader
        self._type = FileType.UNKNOWN
        return RawTextFile()
