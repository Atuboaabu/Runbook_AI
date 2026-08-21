from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from docparse.base import DocumentParser

class TextParser(DocumentParser) :
    @property
    def supported_suffixes(self) -> set[str]:
        return {".txt"}
    
    def parse(self, path: Path) -> list[Document]:
        loader = TextLoader(
            file_path = str(path),
            encoding = "utf-8",
            autodetect_encoding = True,
        )
        documents = loader.load()
        for document in documents:
            document.metadata.update(
                {
                    "filename": path.name,
                    "file_type": "text",
                }
            )
        return documents