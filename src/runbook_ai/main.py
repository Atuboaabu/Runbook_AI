from docparse.registry import DocumentParserRegistry
from ingestion.scanner import DirectoryScanner

registry = DocumentParserRegistry()

scanner = DirectoryScanner(
    directory="data/runbooks",
    supported_suffixes= {".md", ".txt"},
)

for path in scanner.iter_files():
    documents = registry.parse(path)

    for document in documents:
        print(document.metadata)