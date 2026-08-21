from abc import ABC, abstractmethod
from pathlib import Path
from langchain_core.documents import Document



class DocumentParser(ABC):
    """
    不同文档格式的文档解析器的统一入口
    """
    @property
    @abstractmethod
    def supported_suffixes(self) -> set[str]:
        """返回支持的文件扩展名"""
    
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.supported_suffixes
    
    @abstractmethod
    def parse(self, path: Path) -> list[Document] :
        """读取文件并转换为LangChain Document""" 