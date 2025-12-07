# CV Automation for Sherif Fadel Fahmy

This repository automates generating academic CVs (short and long versions)
from:

- A fixed profile file (`profile.yaml`)
- Google Scholar publications (via `data/citations.csv` or `scholarly`)

Outputs:

- `output/cv_short.tex` and `output/cv_long.tex` (LaTeX)
- `output/cv_short.docx` (Word)

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export your Google Scholar citations to CSV and place the file as:

```text
data/citations.csv
```

(From your Google Scholar profile → three-dot menu → Export → CSV.)

## Usage

1. Normalize publications from Google Scholar:

```bash
python fetch_publications.py
```

This generates:

```text
data/publications.json
```

2. Generate LaTeX CVs (short and long):

```bash
python generate_cv_tex.py
```

You will get:

- `output/cv_short.tex`
- `output/cv_long.tex`

Compile them to PDF with `pdflatex`:

```bash
cd output
pdflatex cv_short.tex
pdflatex cv_long.tex
```

3. Generate a short CV in Word format:

```bash
python generate_cv_docx.py
```

This produces:

- `output/cv_short.docx`

You can open and edit this in Microsoft Word.

## Customization

- Edit `profile.yaml` to change:

  - Contact information
  - Education
  - Positions
  - Teaching
  - Service and committees
  - Awards
  - Skills
  - Publication limits for short vs long CV

- Edit `templates/cv_template.tex.j2` to customize the LaTeX layout.

## Notes

- By default, the system uses `data/citations.csv`.
- If you prefer automatic fetching via `scholarly`, set `USE_SCHOLARLY = True`
  in `fetch_publications.py`, and make sure your Scholar ID is correct.
