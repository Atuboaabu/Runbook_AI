from runbook_ai.docparse.registry import DocumentParserRegistry
from runbook_ai.ingestion.scanner import DirectoryScanner

def main() -> None:
    registry = DocumentParserRegistry()
    scanner = DirectoryScanner(
        directory="data/runbooks",
        supported_suffixes= {".md", ".txt"},
    )

    for path in scanner.iter_files():
        documents = registry.parse(path)

        for document in documents:
            print(document.metadata)
