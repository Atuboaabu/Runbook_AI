from pathlib import Path

import pytest

from runbook_ai.docparse.base import DocumentParser
from runbook_ai.docparse.parsers.markdown_parser import MarkdownParser
from runbook_ai.docparse.parsers.text_parser import TextParser


@pytest.mark.parametrize(
    ("parser", "filename", "content", "expected_type"),
    [
        (MarkdownParser(), "cluster.md", "# QNX Cluster\n\n部署说明", "markdown"),
        (MarkdownParser(), "cluster.markdown", "# QNX Cluster", "markdown"),
        (TextParser(), "deploy.txt", "8295 deployment", "text"),
    ],
)
def test_parser_loads_content_and_file_metadata(
    tmp_path: Path,
    parser: DocumentParser,
    filename: str,
    content: str,
    expected_type: str,
) -> None:
    file_path = tmp_path / filename
    file_path.write_text(content, encoding="utf-8")

    documents = parser.parse(file_path)

    assert len(documents) == 1
    assert documents[0].page_content == content
    assert documents[0].metadata == {
        "source": str(file_path),
        "filename": filename,
        "file_type": expected_type,
    }
