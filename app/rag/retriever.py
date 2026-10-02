from pathlib import Path


GUIDELINES_DIR = Path(__file__).parent / "guidelines_data"


def load_guidelines():
    documents = []

    for file_path in GUIDELINES_DIR.glob("*.txt"):
        documents.append(
            {
                "filename": file_path.name,
                "content": file_path.read_text(encoding="utf-8"),
            }
        )

    return documents

def search_guidelines(query: str):
    documents = load_guidelines()

    query_words = set(query.lower().split())

    best_document = None
    best_score = 0

    for document in documents:
        content_words = set(document["content"].lower().split())

        score = len(query_words & content_words)

        if score > best_score:
            best_score = score
            best_document = document

    if best_document is None:
        return None

    return {
        "filename": best_document["filename"],
        "score": best_score,
        "content": best_document["content"],
    }