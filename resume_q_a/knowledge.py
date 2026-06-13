import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    title: str
    body: str


def load_documents(path: Path) -> list[Document]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [Document(title=row["title"], body=row["body"]) for row in rows]


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def search_documents(query: str, documents: list[Document], limit: int = 3) -> list[Document]:
    query_terms = tokenize(query)
    if not query_terms:
        return documents[:limit]

    scored: list[tuple[int, Document]] = []
    for document in documents:
        haystack = tokenize(f"{document.title} {document.body}")
        score = len(query_terms & haystack)
        if score:
            scored.append((score, document))

    scored.sort(key=lambda item: (-item[0], item[1].title))
    return [document for _, document in scored[:limit]] or documents[:limit]
