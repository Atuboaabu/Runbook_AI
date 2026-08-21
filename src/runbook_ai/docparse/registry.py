from pathlib import Path
from langchain_core.documents import Document

from runbook_ai.docparse.base import DocumentParser
from runbook_ai.docparse.parsers.markdown_parser import MarkdownParser
from runbook_ai.docparse.parsers.text_parser import TextParser

class DocumentParserRegistry:
    def __init__(self, parsers: list[DocumentParser] | None = None) -> None:
        self._parsers = list(parsers) if parsers is not None else [
            MarkdownParser(),
            TextParser(),
        ]

    @property
    def supported_suffixes(self) -> set[str]:
        return {
            suffix
            for parser in self._parsers
            for suffix in parser.supported_suffixes
        }
    
    def parse(self, file_path: str | Path) -> list[Document]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)
        
        if not path.is_file():
            raise ValueError(f"Expected file, got: {path}")
        
        for parser in self._parsers:
            if parser.supports(path):
                return parser.parse(path)
            
        raise ValueError(f"Unsupported file type: {path.suffix}")
