import re
from src.data_types import FileLocator
from src.protocols.embeddings import TextTransform


class Transform(TextTransform):
    def __init__(self) -> None:
        self.par_pattern = re.compile(r"[\.\!\?]\s*\n+")
        self.pattern = re.compile(r"([\.\!\?]\s*\n+)|(PAGEBREAK|\n|\t|\s)+")

    def clean(self, raw_text: str) -> tuple[list[str], list[FileLocator]]:
        text = re.sub(self.pattern, self._conditional_replace, raw_text.strip())
        chunks = []
        locators = []
        for chunk in text.split(" PARBREAK "):
            chunks.append(chunk.strip())
            locators.append(self.generate_batch_finder(raw_text, chunks[-1]))
        return chunks, locators

    def generate_batch_finder(self, raw_text, clean_text: str) -> FileLocator:
        parts = clean_text.split()
        join_ex = r"(\s+PAGEBREAK\s+|\s+)"
        if len(parts) > 6:
            re_expression = (
                join_ex.join(parts[:3])
                + r"[a-zA-Z\d\s]*"
                + join_ex.join(parts[-3:])
            )
        else:
            re_expression = join_ex.join(parts)
        return self._get_file_locator(raw_text, re_expression)

    @staticmethod
    def _get_file_locator(raw_text: str, re_expression: str) -> FileLocator:
        match = re.search(re_expression, raw_text)
        assert match, re_expression + "\n "+ raw_text
        page_breaks = len(re.findall("PAGEBREAK", raw_text[:match.pos]))
        par_breaks = len(re.findall("PARBREAK", raw_text[:match.pos]))
        return FileLocator(
            regex_pattern=re_expression,
            page=page_breaks if "PAGEBREAK" in raw_text else None,
            paragraph=par_breaks if "PARBREAK" in raw_text else None,
            start=match.start(),
            end=match.end()
        )

    def _conditional_replace(self, match: re.Match) -> str:
        print("g0", match.group(0), "g1", match.group(1))
        if re.search(self.par_pattern, match.group()):
            return " PARBREAK "
        return " "
