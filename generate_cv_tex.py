# generate_cv_tex.py
import json
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
PROFILE_YAML = BASE_DIR / "profile.yaml"
PUB_JSON = BASE_DIR / "data" / "publications.json"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


def load_profile():
    with open(PROFILE_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_publications():
    if PUB_JSON.exists():
        with open(PUB_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("Warning: publications.json not found; run fetch_publications.py first.")
        return []


def render_tex(profile, publications, short_version: bool):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("cv_template.tex.j2")

    if short_version:
        max_pubs = profile.get("config", {}).get("short_cv", {}).get("max_publications", 8)
        pubs_used = publications[:max_pubs]
        out_file = OUTPUT_DIR / "cv_short.tex"
    else:
        max_pubs = profile.get("config", {}).get("long_cv", {}).get("max_publications", 1000)
        pubs_used = publications[:max_pubs]
        out_file = OUTPUT_DIR / "cv_long.tex"

    tex = template.render(
        profile=profile,
        publications=pubs_used,
        short_version=short_version,
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_file.write_text(tex, encoding="utf-8")
    print(f"Wrote {out_file}")


def main():
    profile = load_profile()
    publications = load_publications()

    # Sort again defensively (year desc)
    publications.sort(key=lambda p: (p.get("year") or 0, p.get("title") or ""), reverse=True)

    render_tex(profile, publications, short_version=True)
    render_tex(profile, publications, short_version=False)


if __name__ == "__main__":
    main()
