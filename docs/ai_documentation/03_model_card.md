# AI Model Card and Statement of AI Use

## Model Information

| Field | Value |
|-------|-------|
| **Model** | Claude Opus 4 |
| **Provider** | Anthropic |
| **Interface** | claude.ai (web interface) |
| **Date of use** | March 28, 2026 |
| **Session type** | Single multi-turn conversation |
| **Tools used** | Web search, project knowledge search, code execution (Python), file creation |

## Statement of AI Use

This manuscript, its companion Jupyter notebooks, and associated figures were produced through a collaborative human–AI workflow. The human author (M.A. Denolle) provided:

- Scientific direction, problem framing, and research questions
- Selection and curation of the project knowledge base (11 PDF papers)
- Iterative feedback on structure, content, and scientific accuracy
- The key insight to integrate partially saturated media with dynamic capillary effects (Shi et al., 2026)
- The proposal to explore 3D stress/strain inversion from frequency-dependent dv/v

The AI assistant (Claude, Anthropic) provided:

- Literature search and synthesis across project papers and web sources
- Derivation and implementation of forward models in Python
- Generation of 18 publication-quality figures
- Drafting of manuscript text with in-text citations and bibliography
- Repository organization and documentation

All scientific claims in this manuscript are grounded in published, peer-reviewed literature cited in the references. The AI did not generate novel theoretical results; rather, it synthesized and connected existing frameworks (Murnaghan, 1937; Berger, 1975; Roeloffs, 1988; Tromp & Trampert, 2018; Fokker et al., 2021) into a unified presentation with systematic parameter exploration.

The full interaction log, including all human prompts and AI reasoning, is documented in the `docs/ai_documentation/` directory of this repository:

- `01_prompts_log.md` — Complete prompts and response summaries
- `02_chain_of_thought.md` — AI reasoning process and design decisions
- `03_model_card.md` — This file

## Reproducibility

All computational results can be reproduced by executing the Jupyter notebooks in the `notebooks/` directory. The notebooks use only standard Python scientific libraries (NumPy, SciPy, Matplotlib) and contain no proprietary code or data.

## Ethical Considerations

- No personal data was used or generated.
- All cited works are properly attributed.
- The AI documentation is provided for full transparency about the human–AI collaboration.
- This work follows the emerging best practices for responsible AI use in scientific publishing as recommended by major journals and professional societies.
