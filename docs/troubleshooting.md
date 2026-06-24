# Troubleshooting & FAQ

## Installation / imports

**`ModuleNotFoundError: No module named 'analysis'`**
Run Python from the repository root, or install the package in editable mode:
```bash
pip install -e .
```
Notebooks inside `analysis/` use flat imports (`from poroelastic_framework import ...`);
they work as long as the notebook's working directory is `analysis/`.

**`ModuleNotFoundError: No module named 'pydantic'` (or `yaml`)**
The config schema requires `pydantic` and `pyyaml`. Install them with
`pixi install`, or `pip install -e ".[test]"`.

## Configuration errors

**`pydantic.ValidationError` when building a `SiteConfig`**
The schema enforces physical bounds. Common causes:
| Field | Constraint |
|-------|-----------|
| `Vs`, `rho`, `mu_prime`, `perm`, `depth` | must be > 0 |
| `nu` | 0 ≤ ν < 0.5 |
| `alpha_B`, `B_skemp`, `phi` | in [0, 1] |

Read the error message: it names the offending field and the violated rule.

**`SiteConfig` won't let me reassign a field**
`SiteConfig` and `AnalysisConfig` are frozen (immutable). Build a new instance
with `model_copy(update={...})` instead of mutating in place.

## Figures

**Figures aren't where I expected / permission error writing figures**
Output defaults to `figures/coupling/`. Override the location:
```bash
export DVV_FIGDIR=/path/to/output
```

**Matplotlib backend / display errors in headless environments (CI, servers)**
Force a non-interactive backend before importing the modules:
```bash
export MPLBACKEND=Agg
```

## Reproducibility

**Synthetic results differ between runs**
The synthetic generators use NumPy's global RNG. Pin the seed first:
```python
import numpy as np
np.random.seed(42)
```

## Tests

**`pytest` reports it cannot collect tests**
Run from the repo root: `pixi run test` or `pytest tests/`. The test
configuration (`testpaths`) is defined in `pyproject.toml`.
