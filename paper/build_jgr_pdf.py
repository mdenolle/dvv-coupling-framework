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
SUPP_INFO_MD = PAPER_DIR / "supporting_information.md"
TEMPLATE = PAPER_DIR / "agu_jgr_submission_template.tex"
AGUTEX_TEMPLATE = PAPER_DIR / "agutex_overleaf_template.tex"
BUILD_DIR = PAPER_DIR / "build"

# Main-text figure set. The quantitative three-site synthesis (Figure 7) follows
# the data application, which is a placeholder in the main text, so it is moved to
# the Supporting Information together with the detailed application and S-figures.
FIGURE_FILES = {
    "Figure 1": "figures/main/fig01_unified_workflow.png",
    "Figure 2": "figures/main/fig02_depth_kernels.png",
    "Figure 3": "figures/main/fig03_hydrological_competition.png",
    "Figure 4": "figures/main/fig04_material_sensitivity.png",
    "Figure 5": "figures/main/fig05_anisotropy_fabric.png",
    "Figure 6": "figures/main/fig06_rheology_diagnostics.png",
}

# Three-site synthesis figure (moved to Supporting Information with §9).
SUPP_SYNTHESIS_FIGURE = (
    "Figure 7",
    "figures/main/fig07_three_site_synthesis.png",
)

# Placeholder that replaces the detailed §9 data application in the main text.
DATA_APPLICATION_PLACEHOLDER = r"""## 9. Application to Field Observations

*[Data application — placeholder.]* A quantitative application of the framework
to field observations is in preparation. A preliminary reinterpretation of three
contrasting published datasets — Parkfield (strike-slip; Okubo et al., 2024),
Cascadia (subduction; Kidiwela et al., 2026), and Kīlauea (volcanic caldera
collapse; Hotovec-Ellis et al., 2022) — is provided in Text S1 of the Supporting
Information (with its three-site synthesis figure and comparison table). That
preliminary analysis uses only published
$\delta v/v$ measurements, velocity profiles, and geodetic strain constraints
(no new waveform processing) to illustrate how the bridge relation (Eq. 7), the
data-driven drainage regime, and the isotropic-versus-deviatoric diagnostic
operate across settings. A full application with independently reprocessed
$\delta v/v$ records is deferred to future work (§10.5).

"""

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


def split_data_application(body: str) -> tuple[str, str]:
    """Replace the §9 data application with a placeholder; return (body, §9 text).

    The detailed §9 application (Parkfield/Cascadia/Kīlauea) is removed from the
    main body and returned for inclusion in the Supporting Information.
    """
    match = re.search(
        r"(?P<sec>^## 9\. .*?)(?=^## 10\. )",
        body,
        flags=re.DOTALL | re.MULTILINE,
    )
    if not match:
        raise ValueError("Could not locate the §9 data-application section to placeholder.")
    data_application = match.group("sec").strip()
    new_body = body[: match.start()] + DATA_APPLICATION_PLACEHOLDER + body[match.end() :]
    return new_body, data_application


def parse_supporting_figures(text: str) -> list[tuple[str, str, str]]:
    """Parse supporting_information.md into (label, caption, figure_path) tuples."""
    entries = re.findall(
        r"\*\*((?:Figure|Table) S\d+)\.\*\*\s*(.*?)Corresponds to `([^`]+)`",
        text,
        flags=re.DOTALL,
    )
    parsed: list[tuple[str, str, str]] = []
    for label, caption, path in entries:
        caption = " ".join(caption.split()).rstrip(". ")
        caption = re.sub(r"`([^`]+)`", r"\\texttt{\1}", caption)
        parsed.append((label, caption, path))
    return parsed


def _figure_float(figure_path: str, caption: str) -> str:
    return f"""
\\clearpage
\\begin{{figure}}[p]
\\centering
\\includegraphics[width=\\textwidth,height=0.78\\textheight,keepaspectratio]{{{figure_path}}}
\\caption{{{caption}}}
\\end{{figure}}
"""


def build_supplement_markdown(
    title: str,
    data_application: str,
    table_captions: dict[str, str],
    supporting_text: str,
) -> str:
    """Assemble the Supporting Information document (§9 + S-figures + Fig 7)."""
    metadata = f"""---
title: "Supporting Information for: {title}"
author: "Marine A. Denolle"
affiliation: "Department of Earth and Space Sciences, University of Washington, Seattle, WA, USA"
corresponding_author: "mdenolle@uw.edu"
---

"""

    intro = (
        "## Contents of this file\n\n"
        "- Text S1: preliminary application of the framework to three published "
        "datasets (Parkfield, Cascadia, Kīlauea).\n"
        "- Figures S1–S12: supporting forward-model and validity figures "
        "(synthetic $\\delta v/v$ with realistic shapes, illustrating the "
        "framework).\n"
        "- Figure 7: three-site synthesis of the preliminary application.\n"
        "- Tables S1 and 2: parameter overview and three-site comparison.\n\n"
        "All quantitative inputs are traced to their sources in "
        "\\texttt{docs/site\\_analyses/provenance\\_tables.md}.\n"
    )

    # Demote the §9 heading into a "Text S1" supplement section.
    data_app = re.sub(
        r"^## 9\. .*$",
        "## Text S1. Preliminary Application to Field Observations",
        data_application,
        count=1,
        flags=re.MULTILINE,
    )

    sections = [metadata, intro, "\\clearpage\n", data_app]

    # Table 2 (three-site comparison) travels with §9; Table S1 with the figures.
    sections.append("\n\\clearpage\n\n## Supporting Tables\n")
    for label in ("Table S1", "Table 2"):
        if label in table_captions:
            cap = table_captions[label].removeprefix(label + ". ")
            cap = re.sub(r"`([^`]+)`", r"\\texttt{\1}", cap)
            sections.append(f"\n**{label}.** {cap}\n")

    # Figure 7 (three-site synthesis) first, then S-figures.
    sections.append("\n\\clearpage\n\n\\section*{Supporting Figures}\n")
    syn_label, syn_path = SUPP_SYNTHESIS_FIGURE
    syn_caption = latex_caption_from_markdown(
        syn_label, FIGURE_CAPTIONS_CACHE.get(syn_label, syn_label)
    )
    sections.append(_figure_float(syn_path, f"\\textbf{{{syn_label}.}} {syn_caption}"))

    for label, caption, path in parse_supporting_figures(supporting_text):
        sections.append(_figure_float(path, f"\\textbf{{{label}.}} {caption}"))

    return "\n".join(sections).strip() + "\n"


# Filled in main() so the supplement can reuse the parsed Figure 7 caption.
FIGURE_CAPTIONS_CACHE: dict[str, str] = {}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep-going", action="store_true", help="Continue after LaTeX warnings.")
    args = parser.parse_args()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    source = normalize_markdown_for_pandoc(SOURCE_MD.read_text(encoding="utf-8"))
    title, abstract, keywords, body, figure_captions, table_captions = extract_manuscript(source)

    # Cache Figure 7 caption so the supplement can render it.
    FIGURE_CAPTIONS_CACHE.update(figure_captions)

    # Replace §9 with a placeholder; keep the detailed application for the SI.
    body, data_application = split_data_application(body)

    # Main text keeps Table 1; Table 2 (three-site comparison) travels with §9.
    main_table_captions = {k: v for k, v in table_captions.items() if k != "Table 2"}

    generated_md = build_submission_markdown(
        title=title,
        abstract=abstract,
        keywords=keywords,
        body=body,
        figure_captions=figure_captions,
        table_captions=main_table_captions,
    )

    # Supporting Information (Text S1 = §9, S-figures, Figure 7, Table 2).
    supporting_text = normalize_markdown_for_pandoc(
        SUPP_INFO_MD.read_text(encoding="utf-8")
    )
    supplement_md = build_supplement_markdown(
        title=title,
        data_application=data_application,
        table_captions=table_captions,
        supporting_text=supporting_text,
    )

    md_path = BUILD_DIR / "paper_dvv_jgr_submission.md"
    tex_path = BUILD_DIR / "paper_dvv_jgr_submission.tex"
    pdf_path = BUILD_DIR / "paper_dvv_jgr_submission.pdf"
    supp_md_path = BUILD_DIR / "paper_dvv_jgr_supplement.md"
    supp_tex_path = BUILD_DIR / "paper_dvv_jgr_supplement.tex"
    supp_pdf_path = BUILD_DIR / "paper_dvv_jgr_supplement.pdf"
    agutex_md_path = BUILD_DIR / "paper_dvv_agutex_jgr_solid_earth.md"
    agutex_tex_path = BUILD_DIR / "paper_dvv_agutex_jgr_solid_earth.tex"
    md_path.write_text(generated_md, encoding="utf-8")
    supp_md_path.write_text(supplement_md, encoding="utf-8")
    agutex_md_path.write_text(
        build_agutex_markdown(
            title=title,
            abstract=abstract,
            keywords=keywords,
            body=body,
            figure_captions=figure_captions,
            table_captions=main_table_captions,
        ),
        encoding="utf-8",
    )

    pandoc_from = "markdown+tex_math_dollars+tex_math_single_backslash+raw_tex+pipe_tables+link_attributes"
    resource_path = os.pathsep.join(
        [
            str(REPO_ROOT),
            str(REPO_ROOT / "figures/main"),
            str(REPO_ROOT / "figures/notebooks"),
        ]
    )

    def pandoc_to_tex(src_md: Path, out_tex: Path, template: Path) -> None:
        run(
            [
                "pandoc",
                str(src_md),
                "--from",
                pandoc_from,
                "--standalone",
                "--shift-heading-level-by=-1",
                "--template",
                str(template),
                "--resource-path",
                resource_path,
                "-o",
                str(out_tex),
            ]
        )

    pandoc_to_tex(md_path, tex_path, TEMPLATE)
    pandoc_to_tex(supp_md_path, supp_tex_path, TEMPLATE)
    pandoc_to_tex(agutex_md_path, agutex_tex_path, AGUTEX_TEMPLATE)

    def xelatex(target_tex: Path) -> None:
        cmd = [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={BUILD_DIR}",
            str(target_tex),
        ]
        if args.keep_going:
            cmd.remove("-halt-on-error")
        run(cmd)
        run(cmd)

    xelatex(tex_path)
    xelatex(supp_tex_path)

    for produced in (pdf_path, supp_pdf_path):
        if not produced.exists():
            raise FileNotFoundError(f"Expected PDF was not created: {produced}")
    print(f"Wrote main manuscript PDF:  {pdf_path}")
    print(f"Wrote Supporting Info PDF:  {supp_pdf_path}")
    print(f"Wrote AGUTeX source for Overleaf: {agutex_tex_path}")


if __name__ == "__main__":
    main()
