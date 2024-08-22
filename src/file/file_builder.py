from src.data_types import File, FileType
from src.file.file_reader import FileFactory
from src.embedding.text_transformer import Transform
from src.protocols.embeddings import Embedder
from src.protocols.file import FileBuffer, FileBuilder as FileBuilderProtocol
from src.protocols.search import ClusterMap


class NotATextFileException(Exception):
    ...


class FileBuilder(FileBuilderProtocol):
    def read(self, path: str) -> FileBuilderProtocol:
        self.file_path = path
        factory = FileFactory()
        reader = factory.get_reader(path)
        self.file_type = factory.file_type
        try:
            self.file_content = reader.read(path)
        except Exception as e:
            if factory.file_type == FileType.UNKNOWN:
                raise NotATextFileException(f"{path} cannot be parsed.")
            raise e
        return self

    def clean(self, transfomer: Transform) -> FileBuilderProtocol:
        self.file_content = transfomer.clean(self.file_content)
        return self

    def embed(self, embedder: Embedder) -> FileBuilderProtocol:

        return self

    def assign_cluster(self, clusters: ClusterMap) -> FileBuilderProtocol:
        return self

    def get_file(self) -> File:
        return File(
            path=self.file_path,
            file_type=self.file_type

        )
