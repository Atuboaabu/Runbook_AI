from pathlib import Path

from runbook_ai.docparse.registry import DocumentParserRegistry
from runbook_ai.ingestion.scanner import DirectoryScanner


def test_validation_corpus_loads_all_runbooks() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    runbook_directory = repository_root / "data" / "runbooks"
    registry = DocumentParserRegistry()
    scanner = DirectoryScanner(
        runbook_directory,
        supported_suffixes=registry.supported_suffixes,
    )

    documents = [
        document
        for path in scanner.iter_files()
        for document in registry.parse(path)
    ]

    assert len(documents) == 10
    assert {document.metadata["filename"] for document in documents} == {
        "01-qnx-dev-environment.md",
        "02-8155-cluster-deploy.md",
        "03-8295-cluster-deploy.txt",
        "04-8397-cluster-deploy.md",
        "05-qnx-log-and-crash-analysis.md",
        "06-screen-black-debug-old.md",
        "07-screen-black-debug-current.md",
        "08-can-signal-simulation.md",
        "09-resource-localization-update.md",
        "10-boot-autostart-incident.md",
    }
