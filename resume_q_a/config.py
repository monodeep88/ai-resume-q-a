from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    project_type: str = 'RAG'
    project_subject: str = 'Resume Q&A'
    package_dir: Path = Path(__file__).resolve().parent

    @property
    def data_dir(self) -> Path:
        return self.package_dir / "data"

    @property
    def knowledge_file(self) -> Path:
        return self.data_dir / "knowledge_base.json"


CONFIG = AppConfig()
