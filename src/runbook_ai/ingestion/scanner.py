# src/ingestion/scanner.py

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


class DirectoryScanner:
    """递归扫描目录中的知识文档。"""

    def __init__(
        self,
        directory: str | Path,
        *,
        supported_suffixes: set[str],
        recursive: bool = True,
        follow_symlinks: bool = False,
        ignored_names: set[str] | None = None,
    ) -> None:
        self.directory = Path(directory)
        self.supported_suffixes = {
            self._normalize_suffix(suffix)
            for suffix in supported_suffixes
        }
        self.recursive = recursive
        self.follow_symlinks = follow_symlinks
        self.ignored_names = ignored_names or {
            ".git",
            ".venv",
            "__pycache__",
        }

    def scan(self) -> list[Path]:
        """扫描并返回排序后的文件路径。"""
        return list(self.iter_files())

    def iter_files(self) -> Iterator[Path]:
        """逐个返回符合条件的文件路径。"""
        self._validate_directory()

        pattern = "**/*" if self.recursive else "*"

        paths = sorted(
            self.directory.glob(pattern),
            key=lambda path: path.as_posix(),
        )

        for path in paths:
            if self._should_include(path):
                yield path

    def _validate_directory(self) -> None:
        if not self.directory.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {self.directory}"
            )

        if not self.directory.is_dir():
            raise NotADirectoryError(
                f"Expected directory, got: {self.directory}"
            )

    def _should_include(self, path: Path) -> bool:
        if not path.is_file():
            return False

        if path.is_symlink() and not self.follow_symlinks:
            return False

        if self._contains_ignored_name(path):
            return False

        return (
            path.suffix.lower()
            in self.supported_suffixes
        )

    def _contains_ignored_name(self, path: Path) -> bool:
        try:
            relative_path = path.relative_to(self.directory)
        except ValueError:
            return True

        return any(
            part in self.ignored_names
            for part in relative_path.parts
        )

    @staticmethod
    def _normalize_suffix(suffix: str) -> str:
        normalized = suffix.lower().strip()

        if not normalized.startswith("."):
            normalized = f".{normalized}"

        return normalized