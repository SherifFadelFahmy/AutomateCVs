# fetch_publications.py
import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
OUTPUT_JSON = DATA_DIR / "publications.json"
CITATIONS_CSV = DATA_DIR / "citations.csv"

# Optional scholarly-based fetch (can be turned on later)
USE_SCHOLARLY = False
SCHOLAR_ID = "Opi9HcEAAAAJ"


def normalize_from_csv(csv_path: Path):
    df = pd.read_csv(csv_path)

    publications = []
    for _, row in df.iterrows():
        title = str(row.get("Title", "")).strip()
        authors = str(row.get("Authors", "")).strip()
        venue = str(row.get("Publication", "")).strip()
        year = row.get("Year", None)

        try:
            year = int(year) if pd.notna(year) else None
        except (ValueError, TypeError):
            year = None

        pub = {
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
        }
        publications.append(pub)

    # Sort by year descending, then title
    publications.sort(key=lambda p: (p["year"] or 0, p["title"]), reverse=True)
    return publications


def normalize_from_scholarly(author_id: str):
    from scholarly import scholarly  # imported only if used

    author = scholarly.search_author_id(author_id)
    author = scholarly.fill(author, sections=["publications"])

    publications = []
    for pub in author.get("publications", []):
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get("bib", {})

        title = bib.get("title", "").strip()
        authors = bib.get("author", "").strip()
        venue = bib.get("journal", "") or bib.get("booktitle", "")
        venue = (venue or "").strip()

        year = bib.get("year", None)
        try:
            year = int(year) if year else None
        except (ValueError, TypeError):
            year = None

        publications.append(
            {
                "title": title,
                "authors": authors,
                "venue": venue,
                "year": year,
            }
        )

    publications.sort(key=lambda p: (p["year"] or 0, p["title"]), reverse=True)
    return publications


def main():
    DATA_DIR.mkdir(exist_ok=True)

    if CITATIONS_CSV.exists():
        print(f"Using Google Scholar CSV: {CITATIONS_CSV}")
        publications = normalize_from_csv(CITATIONS_CSV)
    elif USE_SCHOLARLY:
        print("Using scholarly to fetch publications...")
        publications = normalize_from_scholarly(SCHOLAR_ID)
    else:
        raise FileNotFoundError(
            f"No {CITATIONS_CSV} found and USE_SCHOLARLY=False. "
            "Export your Google Scholar citations to CSV and place it in the data/ folder."
        )

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(publications, f, ensure_ascii=False, indent=2)

    print(f"Wrote normalized publications to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
