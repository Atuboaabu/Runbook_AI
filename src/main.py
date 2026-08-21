from docparse.registry import DocumentParserRegisty
from ingestion.scanner import DirectoryScanner

registry = DocumentParserRegisty()

scanner = DirectoryScanner(
    directory="data/runbooks",
    supported_suffixes= {".md", ".txt"},
)

for path in scanner.iter_files():
    documents = registry.parse(path)

    for document in documents:
        print(document.metadata)