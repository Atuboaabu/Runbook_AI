from pathlib import Path
from langchain_core.documents import Document

from docparse.base import DocumentParser
from docparse.parsers.markdown_parser import MarkdownParser
from docparse.parsers.text_parser import TextParser

class DocumentParserRegistry:
    def __init__(self) -> None:
        self._parsers: list[DocumentParser] = [
            MarkdownParser(),
            TextParser(),
        ]
    
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