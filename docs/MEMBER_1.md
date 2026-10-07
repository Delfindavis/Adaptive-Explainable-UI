# Synthetic Data Contribution

## Overview

Implemented the synthetic data component for the project, including synthetic learner data generation, dataset validation, and automated testing.

## Work Completed

### Synthetic Data Generation

Implemented the data generation module in:

`dataset/generate.py`

The generator creates synthetic learner records containing:

- Learner ID
- Diagnostic score
- Experience level
- Learning preference
- Device type
- Initial engagement
- UI variant
- Action probability
- Quiz performance
- Task completion
- Reward
- Data source

Generated dataset:

`data/synthetic_learners.csv`

Metadata:

`data/synthetic_learners.metadata.json`

### Cold-Start Data

The simulator represents the initial decision point where no previous interaction history is available.

Therefore, `initial_engagement` is recorded as `unavailable`.

Before UI selection, the available information includes:

- Diagnostic score
- Experience level
- Learning preference
- Device type

The UI variant is then selected as the simulated action. Quiz performance, task completion, and reward are recorded as subsequent outcomes.

### Dataset Validation

Implemented validation in:

`dataset/validate.py`

The validation checks:

- Required fields
- Unique learner IDs
- Diagnostic score range
- Valid experience and device values
- Valid UI variants
- Cold-start engagement value
- Quiz and task outcome consistency
- Reward calculation
- Action probability
- Synthetic data source label
- Empty dataset detection

### Automated Testing

Added:

`tests/test_dataset.py`

The tests cover:

- Dataset bounds and coverage
- Corrupted data detection
- Empty generation handling
- Reproducibility with the same seed
- Different output with different seeds

## Verification

### Dataset Validation

Command:

`python -m dataset.validate data/synthetic_learners.csv`

Result:

**PASS: 1000 rows**

UI variant distribution:

| UI Variant | Records |
|---|---:|
| Hint | 271 |
| Concise | 235 |
| Challenge | 255 |
| Example | 239 |

All generated records passed validation.

### Dataset Tests

Command:

`python -m unittest discover -s tests -p test_dataset.py -v`

Result:

- `test_bounds_and_coverage` — PASS
- `test_corruption_is_detected` — PASS
- `test_no_empty_generation` — PASS
- `test_reproducible_and_seed_changes_output` — PASS

**4/4 tests passed.**

### Reproducibility Check

Generated the dataset twice with:

- Count: `1000`
- Seed: `16`

The generated CSV files were compared.

Result:

`FC: no differences encountered`

This confirms reproducible generation when the same seed is used.

## Simulation Assumptions

The dataset represents simulated learner behaviour and is not intended to represent real learner measurements.

The simulation uses:

- Four UI variants: `hint`, `example`, `concise`, and `challenge`
- Uniform random UI assignment
- Initial action probability of `0.25`
- Experience level influencing diagnostic score
- Learning preference and diagnostic score influencing simulated outcomes
- Simulated quiz performance and task completion
- Reward calculated from quiz correctness and task completion

Only the outcome of the assigned UI variant is recorded; counterfactual outcomes are not generated.

The assumptions are treated as simulation assumptions rather than research findings.

## Problems Addressed

- Organized the synthetic data files into the required repository structure.
- Implemented dataset generation and validation.
- Added automated dataset tests.
- Verified reproducibility using a fixed seed.
- Removed temporary test files and Python cache files.
- Verified the generated dataset against the validation rules.

## Repository References

Branch:

`Kavya_S_Nair`

Commits:

- `a7ded7` — Add synthetic data generation and validation
- `812f80f` — Document Member 1 synthetic data contribution

Files contributed:

```text
data/
├── synthetic_learners.csv
└── synthetic_learners.metadata.json

dataset/
├── __init__.py
├── generate.py
└── validate.py

tests/
└── test_dataset.py