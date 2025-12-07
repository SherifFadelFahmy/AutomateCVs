import csv
import sys
from pathlib import Path

from scholarly import scholarly


def fetch_publications_to_csv(author_id: str, output_csv: str = "citations.csv"):
    """
    Fetch publications for a Google Scholar author ID and save as CSV.
    Columns are similar to the downloadable Google Scholar CSV.
    """
    print(f"Fetching author with id={author_id} ...")
    author = scholarly.search_author_id(author_id)
    author = scholarly.fill(author, sections=["publications"])

    pubs = author.get("publications", [])
    print(f"Found {len(pubs)} publications (before filling details).")

    # Define CSV columns (similar to Google Scholar export)
    fieldnames = [
        "Authors",
        "Title",
        "Publication",
        "Volume",
        "Number",
        "Pages",
        "Year",
        "Publisher",
    ]

    output_path = Path(output_csv)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, pub in enumerate(pubs, start=1):
            # Fill each publication to get full bib info
            try:
                pub_filled = scholarly.fill(pub)
            except Exception as e:
                print(f"  [!] Error filling publication {i}: {e}")
                continue

            bib = pub_filled.get("bib", {})

            title = bib.get("title", "").strip()
            authors = bib.get("author", "").strip()
            year = bib.get("year", "")
            venue = bib.get("journal", "") or bib.get("booktitle", "")
            volume = bib.get("volume", "")
            number = bib.get("number", "")
            pages = bib.get("pages", "")
            publisher = bib.get("publisher", "")

            row = {
                "Authors": authors,
                "Title": title,
                "Publication": venue,
                "Volume": volume,
                "Number": number,
                "Pages": pages,
                "Year": year,
                "Publisher": publisher,
            }

            writer.writerow(row)
            print(f"  [{i}/{len(pubs)}] {title[:60]}...")

    print(f"\nDone. Wrote CSV to: {output_path.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_scholar_to_csv.py <AUTHOR_ID> [output_csv]")
        print("Example: python fetch_scholar_to_csv.py Hfkr1LkAAAAJ citations_professor.csv")
        sys.exit(1)

    author_id = sys.argv[0 + 1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[0 + 2]
    else:
        output_file = "citations.csv"

    fetch_publications_to_csv(author_id, output_file)
