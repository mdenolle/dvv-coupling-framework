"""Build a Quarto HTML website from the Markdown manuscript.

This is the third render target (alongside the Markdown source and the JGR
tex+PDF build). It reuses the same manuscript extractor as ``build_jgr_pdf.py``
so all three formats stay in sync with one source of truth:
``paper/paper_dvv_unified_framework.md``.

Outputs a self-contained Quarto website under ``paper/site/``:

* ``index.qmd``      — the full paper (abstract, body, Figures 1-7, tables).
* ``supplement.qmd`` — Supporting Information (Figures S1-S12, Table S1).
* ``_quarto.yml``    — website project config (navbar, theme, MathJax).

The HTML pages use ``embed-resources: true`` so figures are inlined and each
page is portable (no external asset folder needed for deployment).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

from build_jgr_pdf import (  # reuse the single-source extractor
    REPO_ROOT,
    SOURCE_MD,
    SUPP_INFO_MD,
    extract_manuscript,
)

SITE_DIR = Path(__file__).resolve().parent / "site"

# Full main-text figure set for the web version (includes Figure 7).
# Figure number -> file (citation order). Figures are embedded inline in the
# canonical Markdown; this map is kept only as a reference/sanity list.
MAIN_FIGURES = {
    "Figure 1": "fig01_unified_workflow.png",
    "Figure 2": "fig02_hydrological_competition.png",
    "Figure 3": "fig03_material_sensitivity.png",
    "Figure 4": "fig04_rheology_diagnostics.png",
    "Figure 5": "fig05_anisotropy_fabric.png",
    "Figure 6": "fig06_depth_kernels.png",
    "Figure 7": "fig07_three_site_synthesis.png",
}

# Figures live at repo/figures; the qmd files live at repo/paper/site.
FIG_REL = "../../figures"


def normalize_for_quarto(text: str) -> str:
    """Convert LaTeX-only compact shorthands to plain symbols for HTML/MathJax."""
    return text.replace("$\\sim$", "~").replace("$>$", ">").replace("$<$", "<")


def yaml_quote(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def figure_block(label: str, caption: str, rel_path: str) -> str:
    """A plain image + bold-caption paragraph (robust to special chars)."""
    caption = caption.removeprefix(f"{label}. ").strip()
    return (
        f"![]({rel_path}){{width=95%}}\n\n"
        f"**{label}.** {caption}\n"
    )


def build_index_qmd(
    title: str,
    abstract: str,
    keywords: str,
    body: str,
    figure_captions: dict[str, str],
    table_captions: dict[str, str],
) -> str:
    front = f"""---
title: {yaml_quote(title)}
author:
  - name: "Marine A. Denolle"
    affiliations:
      - "Department of Earth and Space Sciences, University of Washington, Seattle, WA, USA"
    email: "mdenolle@uw.edu"
format:
  html:
    toc: true
    toc-depth: 3
    toc-location: left
    number-sections: false
    theme: cosmo
    embed-resources: true
    html-math-method: mathjax
    fig-cap-location: bottom
---

"""

    abstract_block = f"## Abstract\n\n{abstract}\n\n**Keywords:** {keywords}\n\n"

    # Figures and table captions are already INLINE in the canonical Markdown.
    # Only rebase the figure image paths for the site directory
    # (canonical uses ../figures relative to paper/; the qmd lives in paper/site).
    body = body.replace("](../figures/", f"]({FIG_REL}/")

    return front + abstract_block + body.strip() + "\n"


def parse_supporting_figures(text: str) -> list[tuple[str, str, str]]:
    """(label, markdown caption, repo-relative figure path) from supporting_information.md."""
    entries = re.findall(
        r"\*\*((?:Figure|Table) S\d+)\.\*\*\s*(.*?)Corresponds to `([^`]+)`",
        text,
        flags=re.DOTALL,
    )
    out: list[tuple[str, str, str]] = []
    for label, caption, path in entries:
        caption = " ".join(caption.split()).rstrip(". ")
        out.append((label, caption, path))
    return out


def build_supplement_qmd(title: str, supporting_text: str) -> str:
    front = f"""---
title: "Supporting Information"
subtitle: {yaml_quote(title)}
format:
  html:
    toc: true
    toc-depth: 2
    toc-location: left
    number-sections: false
    theme: cosmo
    embed-resources: true
    html-math-method: mathjax
    fig-cap-location: bottom
---

These supporting figures use synthetic $\\delta v/v$ with physically realistic
shapes to illustrate the framework's forward predictions and diagnostics.

"""
    blocks = []
    for label, caption, path in parse_supporting_figures(supporting_text):
        # path is repo-relative (e.g. figures/notebooks/...); rebase to site dir.
        rel = f"{FIG_REL}/{path.split('figures/', 1)[1]}" if "figures/" in path else path
        blocks.append("\n" + figure_block(label, f"{label}. {caption}", rel))
    return front + "\n".join(blocks) + "\n"


def build_quarto_yml(title: str) -> str:
    return f"""project:
  type: website
  output-dir: _site

website:
  title: "dv/v Unified Framework"
  reader-mode: true
  navbar:
    left:
      - href: index.qmd
        text: "Paper"
      - href: supplement.qmd
        text: "Supporting Information"

format:
  html:
    theme: cosmo
    toc: true
    embed-resources: true
    html-math-method: mathjax
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-render", action="store_true", help="Write .qmd files but skip `quarto render`."
    )
    args = parser.parse_args()

    SITE_DIR.mkdir(parents=True, exist_ok=True)

    source = normalize_for_quarto(SOURCE_MD.read_text(encoding="utf-8"))
    title, abstract, keywords, body, figure_captions, table_captions = extract_manuscript(source)
    supporting_text = normalize_for_quarto(SUPP_INFO_MD.read_text(encoding="utf-8"))

    (SITE_DIR / "index.qmd").write_text(
        build_index_qmd(title, abstract, keywords, body, figure_captions, table_captions),
        encoding="utf-8",
    )
    (SITE_DIR / "supplement.qmd").write_text(
        build_supplement_qmd(title, supporting_text), encoding="utf-8"
    )
    (SITE_DIR / "_quarto.yml").write_text(build_quarto_yml(title), encoding="utf-8")

    print(f"Wrote Quarto sources to {SITE_DIR}")

    if args.no_render:
        print("Skipped render (--no-render). Run: quarto render paper/site")
        return

    if shutil.which("quarto") is None:
        print("quarto not found on PATH; wrote .qmd sources only. Install quarto to render.")
        return

    subprocess.run(["quarto", "render", str(SITE_DIR)], cwd=REPO_ROOT, check=True)
    index_html = SITE_DIR / "_site" / "index.html"
    print(f"Rendered website: {index_html}")


if __name__ == "__main__":
    main()
