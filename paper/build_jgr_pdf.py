"""Build JGR submission artifacts from the Markdown manuscript.

This creates two outputs:

* a locally compiled review PDF using a JGR-style Pandoc template; and
* an AGUTeX source file for the official Overleaf/AGU ``agujournal2019`` class.

The official AGU class is not vendored in this repository, so the AGUTeX source
is generated for Overleaf or for a TeX installation that already provides
``agujournal2019.cls``.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = Path(__file__).resolve().parent
SOURCE_MD = PAPER_DIR / "paper_dvv_unified_framework.md"
TEMPLATE = PAPER_DIR / "agu_jgr_submission_template.tex"
AGUTEX_TEMPLATE = PAPER_DIR / "agutex_overleaf_template.tex"
BUILD_DIR = PAPER_DIR / "build"

FIGURE_FILES = {
    "Figure 1": "figures/main/fig01_unified_workflow.png",
    "Figure 2": "figures/main/fig02_depth_kernels.png",
    "Figure 3": "figures/main/fig03_hydrological_competition.png",
    "Figure 4": "figures/main/fig04_material_sensitivity.png",
    "Figure 5": "figures/main/fig05_anisotropy_fabric.png",
    "Figure 6": "figures/main/fig06_rheology_diagnostics.png",
    "Figure 7": "figures/main/fig07_three_site_synthesis.png",
}

AGU_KEYPOINTS = [
    "A unified framework links seismic velocity changes to stress strain hydrology and rheology",
    "Directional crack fabric explains Parkfield velocity changes tracking axial contraction",
    "Coda window metrics make velocity change processing reproducible for codameter",
]

PLAIN_LANGUAGE_SUMMARY = """Small changes in seismic wave speed can reveal how rocks, sediments, and fluids respond to environmental and tectonic forcing. This paper connects several explanations that are often treated separately, including temperature, groundwater, surface loading, earthquake damage, volcanic pressure changes, and long term tectonic strain. The result is a practical framework for deciding when velocity changes behave like a stress meter, when they behave like a strain meter, and when additional material or hydrological effects must be modeled."""


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def normalize_markdown_for_pandoc(text: str) -> str:
    """Normalize compact inline math shorthands that Pandoc intentionally skips.

    Pandoc does not parse dollar math when the closing dollar is followed by a
    digit. The manuscript uses compact forms such as ``$\\sim$50`` and
    ``$>$0.1%`` in prose, so convert those atomic symbols to ``\\(...\\)``.
    """

    return (
        text.replace("$\\sim$", r"\textasciitilde{}")
        .replace("$>$", r"\textgreater{}")
        .replace("$<$", r"\textless{}")
    )


def latex_caption_from_markdown(label: str, caption: str) -> str:
    caption = caption.removeprefix(f"{label}. ").strip()
    caption = re.sub(r"`([^`]+)`", r"\\texttt{\1}", caption)
    return caption


def extract_manuscript(source: str) -> tuple[str, str, str, str, dict[str, str], dict[str, str]]:
    first_line = source.splitlines()[0]
    if not first_line.startswith("# "):
        raise ValueError("Expected manuscript to start with a level-1 title.")
    title = first_line.removeprefix("# ").strip()

    try:
        _, rest = source.split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("Expected YAML-like separator after title/author block.") from exc

    abstract_match = re.search(
        r"## Abstract\s*\n\n(?P<abstract>.*?)(?:\n\n\*\*Keywords:\*\*\s*(?P<keywords>.*?)\n\n---)",
        rest,
        flags=re.DOTALL,
    )
    if not abstract_match:
        raise ValueError("Could not extract abstract and keywords.")

    abstract = abstract_match.group("abstract").strip()
    keywords = abstract_match.group("keywords").strip()
    body = rest[abstract_match.end() :].lstrip()

    caption_match = re.search(
        r"\n## Main Figure and Table Captions\s*\n\n(?P<captions>.*?)(?=\n---\s*\n\n## References)",
        body,
        flags=re.DOTALL,
    )
    figure_captions: dict[str, str] = {}
    table_captions: dict[str, str] = {}
    if caption_match:
        caption_block = caption_match.group("captions").strip()
        entries = re.findall(
            r"\*\*((?:Figure|Table) \d+)\.\*\*\s*(.*?)(?=\n\n\*\*(?:Figure|Table) \d+\.\*\*|\Z)",
            caption_block,
            flags=re.DOTALL,
        )
        for label, caption in entries:
            full_caption = f"{label}. {' '.join(caption.split())}"
            if label.startswith("Figure"):
                figure_captions[label] = full_caption
            else:
                table_captions[label] = full_caption
        body = body[: caption_match.start()] + "\n" + body[caption_match.end() :]

    return title, abstract, keywords, body, figure_captions, table_captions


def build_submission_markdown(
    title: str,
    abstract: str,
    keywords: str,
    body: str,
    figure_captions: dict[str, str],
    table_captions: dict[str, str],
) -> str:
    metadata = f"""---
title: "{title}"
author: "Marine A. Denolle"
affiliation: "Department of Earth and Space Sciences, University of Washington, Seattle, WA, USA"
corresponding_author: "mdenolle@uw.edu"
---

"""

    front_matter = f"""## Abstract

{abstract}

**Keywords:** {keywords}

"""

    sections: list[str] = [metadata, front_matter, body.strip(), "\n\\clearpage\n\n## Table Captions\n"]
    for label in sorted(table_captions):
        sections.append(f"\n**{label}.** {table_captions[label].removeprefix(label + '. ')}\n")

    sections.append("\n\\clearpage\n\n\\section*{Figure Files}\n")
    for label, figure_path in FIGURE_FILES.items():
        caption = latex_caption_from_markdown(label, figure_captions.get(label, label))
        sections.append(
            f"""
\\clearpage
\\begin{{figure}}[p]
\\centering
\\includegraphics[width=\\textwidth,height=0.72\\textheight,keepaspectratio]{{{figure_path}}}
\\caption{{{caption}}}
\\end{{figure}}
"""
        )

    return "\n".join(sections).strip() + "\n"


def yaml_block(name: str, value: str) -> str:
    indented = "\n".join(f"  {line}" if line else "" for line in value.splitlines())
    return f"{name}: |\n{indented}\n"


def build_agutex_markdown(
    title: str,
    abstract: str,
    keywords: str,
    body: str,
    figure_captions: dict[str, str],
    table_captions: dict[str, str],
) -> str:
    metadata_lines = [
        "---",
        yaml_block("title", title).rstrip(),
        yaml_block("abstract", abstract).rstrip(),
        yaml_block("plain_language_summary", PLAIN_LANGUAGE_SUMMARY).rstrip(),
        yaml_block("keywords", keywords).rstrip(),
        "keypoints:",
        *[f"  - {keypoint}" for keypoint in AGU_KEYPOINTS],
        "---",
        "",
    ]

    sections: list[str] = ["\n".join(metadata_lines), body.strip(), "\n\\clearpage\n\n## Table Captions\n"]
    for label in sorted(table_captions):
        sections.append(f"\n**{label}.** {table_captions[label].removeprefix(label + '. ')}\n")

    sections.append("\n\\clearpage\n\n\\section*{Figure Files}\n")
    for label, figure_path in FIGURE_FILES.items():
        caption = latex_caption_from_markdown(label, figure_captions.get(label, label))
        sections.append(
            f"""
\\clearpage
\\begin{{figure}}[p]
\\centering
\\includegraphics[width=\\textwidth,height=0.72\\textheight,keepaspectratio]{{{figure_path}}}
\\caption{{{caption}}}
\\end{{figure}}
"""
        )

    return "\n".join(sections).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep-going", action="store_true", help="Continue after LaTeX warnings.")
    args = parser.parse_args()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    source = normalize_markdown_for_pandoc(SOURCE_MD.read_text(encoding="utf-8"))
    title, abstract, keywords, body, figure_captions, table_captions = extract_manuscript(source)
    generated_md = build_submission_markdown(
        title=title,
        abstract=abstract,
        keywords=keywords,
        body=body,
        figure_captions=figure_captions,
        table_captions=table_captions,
    )

    md_path = BUILD_DIR / "paper_dvv_jgr_submission.md"
    tex_path = BUILD_DIR / "paper_dvv_jgr_submission.tex"
    pdf_path = BUILD_DIR / "paper_dvv_jgr_submission.pdf"
    agutex_md_path = BUILD_DIR / "paper_dvv_agutex_jgr_solid_earth.md"
    agutex_tex_path = BUILD_DIR / "paper_dvv_agutex_jgr_solid_earth.tex"
    md_path.write_text(generated_md, encoding="utf-8")
    agutex_md_path.write_text(
        build_agutex_markdown(
            title=title,
            abstract=abstract,
            keywords=keywords,
            body=body,
            figure_captions=figure_captions,
            table_captions=table_captions,
        ),
        encoding="utf-8",
    )

    pandoc_from = "markdown+tex_math_dollars+tex_math_single_backslash+raw_tex+pipe_tables+link_attributes"
    resource_path = os.pathsep.join([str(REPO_ROOT), str(REPO_ROOT / "figures/main")])
    run(
        [
            "pandoc",
            str(md_path),
            "--from",
            pandoc_from,
            "--standalone",
            "--shift-heading-level-by=-1",
            "--template",
            str(TEMPLATE),
            "--resource-path",
            resource_path,
            "-o",
            str(tex_path),
        ]
    )
    run(
        [
            "pandoc",
            str(agutex_md_path),
            "--from",
            pandoc_from,
            "--standalone",
            "--shift-heading-level-by=-1",
            "--template",
            str(AGUTEX_TEMPLATE),
            "--resource-path",
            resource_path,
            "-o",
            str(agutex_tex_path),
        ]
    )

    xelatex_cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={BUILD_DIR}",
        str(tex_path),
    ]
    if args.keep_going:
        xelatex_cmd.remove("-halt-on-error")
    run(xelatex_cmd)
    run(xelatex_cmd)

    if not pdf_path.exists():
        raise FileNotFoundError(f"Expected PDF was not created: {pdf_path}")
    print(f"Wrote {pdf_path}")
    print(f"Wrote AGUTeX source for Overleaf: {agutex_tex_path}")


if __name__ == "__main__":
    main()
