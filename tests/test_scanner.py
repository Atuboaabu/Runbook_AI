from pathlib import Path

import pytest

from runbook_ai.ingestion.scanner import DirectoryScanner


def test_scan_recursively_filters_and_sorts_supported_files(tmp_path: Path) -> None:
    nested = tmp_path / "platforms" / "8295"
    nested.mkdir(parents=True)
    (nested / "deploy.TXT").write_text("deploy", encoding="utf-8")
    (tmp_path / "cluster.md").write_text("# Cluster", encoding="utf-8")
    (tmp_path / "ignore.json").write_text("{}", encoding="utf-8")

    scanner = DirectoryScanner(
        tmp_path,
        supported_suffixes={"md", ".txt"},
    )

    assert [path.relative_to(tmp_path).as_posix() for path in scanner.scan()] == [
        "cluster.md",
        "platforms/8295/deploy.TXT",
    ]


def test_scan_can_be_limited_to_top_level(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    (tmp_path / "top.md").write_text("top", encoding="utf-8")
    (nested / "nested.md").write_text("nested", encoding="utf-8")

    scanner = DirectoryScanner(
        tmp_path,
        supported_suffixes={".md"},
        recursive=False,
    )

    assert scanner.scan() == [tmp_path / "top.md"]


def test_scan_ignores_configured_directory_names(tmp_path: Path) -> None:
    ignored = tmp_path / "generated"
    ignored.mkdir()
    (ignored / "hidden.md").write_text("hidden", encoding="utf-8")
    (tmp_path / "visible.md").write_text("visible", encoding="utf-8")

    scanner = DirectoryScanner(
        tmp_path,
        supported_suffixes={".md"},
        ignored_names={"generated"},
    )

    assert scanner.scan() == [tmp_path / "visible.md"]


def test_scan_ignores_default_cache_and_repository_directories(
    tmp_path: Path,
) -> None:
    for directory_name in (".git", ".venv", "__pycache__"):
        ignored = tmp_path / directory_name
        ignored.mkdir()
        (ignored / "hidden.md").write_text("hidden", encoding="utf-8")
    visible = tmp_path / "visible.md"
    visible.write_text("visible", encoding="utf-8")

    scanner = DirectoryScanner(tmp_path, supported_suffixes={".md"})

    assert scanner.scan() == [visible]


def test_scan_excludes_symlinks_by_default_and_can_include_them(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.md"
    target.write_text("target", encoding="utf-8")
    link = tmp_path / "linked.md"
    link.symlink_to(target)

    default_scanner = DirectoryScanner(tmp_path, supported_suffixes={".md"})
    following_scanner = DirectoryScanner(
        tmp_path,
        supported_suffixes={".md"},
        follow_symlinks=True,
    )

    assert default_scanner.scan() == [target]
    assert following_scanner.scan() == [link, target]


def test_scan_rejects_missing_directory(tmp_path: Path) -> None:
    scanner = DirectoryScanner(
        tmp_path / "missing",
        supported_suffixes={".md"},
    )

    with pytest.raises(FileNotFoundError, match="Directory does not exist"):
        scanner.scan()


def test_scan_rejects_file_as_directory(tmp_path: Path) -> None:
    file_path = tmp_path / "runbook.md"
    file_path.write_text("content", encoding="utf-8")
    scanner = DirectoryScanner(file_path, supported_suffixes={".md"})

    with pytest.raises(NotADirectoryError, match="Expected directory"):
        scanner.scan()
