from pathlib import Path

import pytest
from langchain_core.documents import Document

from runbook_ai.docparse.base import DocumentParser
from runbook_ai.docparse.registry import DocumentParserRegistry


class StubParser(DocumentParser):
    def __init__(self, suffixes: set[str], marker: str) -> None:
        self._suffixes = suffixes
        self._marker = marker

    @property
    def supported_suffixes(self) -> set[str]:
        return self._suffixes

    def parse(self, path: Path) -> list[Document]:
        return [Document(page_content=self._marker, metadata={"source": str(path)})]


def test_registry_aggregates_and_deduplicates_parser_suffixes() -> None:
    registry = DocumentParserRegistry(
        parsers=[
            StubParser({".md", ".shared"}, "first"),
            StubParser({".txt", ".shared"}, "second"),
        ]
    )

    assert registry.supported_suffixes == {".md", ".txt", ".shared"}


def test_registry_copies_the_parser_list() -> None:
    parsers: list[DocumentParser] = [StubParser({".md"}, "markdown")]
    registry = DocumentParserRegistry(parsers=parsers)

    parsers.append(StubParser({".txt"}, "text"))

    assert registry.supported_suffixes == {".md"}


def test_registry_routes_to_matching_parser_case_insensitively(
    tmp_path: Path,
) -> None:
    registry = DocumentParserRegistry(
        parsers=[
            StubParser({".md"}, "markdown"),
            StubParser({".txt"}, "text"),
        ]
    )
    file_path = tmp_path / "RUNBOOK.MD"
    file_path.write_text("content", encoding="utf-8")

    documents = registry.parse(file_path)

    assert documents[0].page_content == "markdown"


def test_registry_rejects_missing_file(
    tmp_path: Path,
) -> None:
    registry = DocumentParserRegistry()
    with pytest.raises(FileNotFoundError):
        registry.parse(tmp_path / "missing.md")


def test_registry_rejects_directory(
    tmp_path: Path,
) -> None:
    registry = DocumentParserRegistry()
    with pytest.raises(ValueError, match="Expected file"):
        registry.parse(tmp_path)


def test_registry_rejects_unsupported_suffix(
    tmp_path: Path,
) -> None:
    registry = DocumentParserRegistry()
    file_path = tmp_path / "signals.json"
    file_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type: .json"):
        registry.parse(file_path)
