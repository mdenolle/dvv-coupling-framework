# Overleaf AGUTeX Template Check

**Date:** 2026-06-20  
**Target journal:** JGR: Solid Earth

## Findings

- Overleaf lists official AGU AGUTeX article templates, including `AGU JGR: Space Physics AGUTeX Article` and `AGU JGR: Atmospheres AGUTeX Article`.
- The visible template source uses `\documentclass[draft]{agujournal2019}` and includes `JGR: Solid Earth` in the allowed `\journalname{...}` list.
- No separate official Overleaf template labeled `JGR: Solid Earth` was found in the Overleaf template index. The correct route is therefore to use the shared AGU/JGR AGUTeX template and set `\journalname{JGR: Solid Earth}`.
- The Overleaf template is configured for `pdflatex` and a TeX Live 2025 image.
- The local TeX installation checked here does not provide `agujournal2019.cls`, and CTAN package metadata checks for `agutex` and `agujournal2019` returned 404. A direct AGU zip URL was blocked by Cloudflare from this environment.

## Repository Action

The manuscript build now produces two outputs:

- `paper/build/paper_dvv_jgr_submission.pdf`: local JGR-style review PDF, compiled with XeLaTeX.
- `paper/build/paper_dvv_agutex_jgr_solid_earth.tex`: AGUTeX source configured for `JGR: Solid Earth`, intended for the official AGU Overleaf template or a TeX installation that provides `agujournal2019.cls`.

## Source Checked

- Official Overleaf AGU JGR template page: <https://www.overleaf.com/latex/templates/agu-jgr-space-physics-agutex-article/jqvttbfdtrjg>
