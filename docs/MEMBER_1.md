# Member 1 — Synthetic data

Assigned student: Kavya S Nair

## Files to push

- `dataset/`
- `data/`
- `tests/test_dataset.py`

Copy the contents of your member folder into the shared repository root, preserving subdirectories. Read `docs/GITHUB_WORKFLOW.md` in the integrated project for the exact stage/commit instructions. The full app requires all four contributions.

## Understand, verify and develop your module

1. Explain why each field exists and which fields are available before selection.

2. Run generation twice with the same seed; compare the CSVs.

3. Run validation and the dataset tests; inspect outcomes from each UI.

4. Review the simulator assumptions with the guide; document any changes you make.

Verification:
`python -m unittest discover -s tests -p test_dataset.py -v`

## Your contribution record

### Changes I made:

- Added the synthetic learner dataset under `data/`.
- Added `synthetic_learners.csv` and its metadata file.
- Added the synthetic data generation module in `dataset/generate.py`.
- Added dataset validation functionality in `dataset/validate.py`.
- Added `dataset/__init__.py`.
- Added automated dataset tests in `tests/test_dataset.py`.
- Preserved the required repository folder structure for Member 1.
- Removed Python `__pycache__` files before committing.


  ### Requirements I verified:

- Confirmed that the required Member 1 folders/files are present:
  - `dataset/`
  - `data/`
  - `tests/test_dataset.py`
- Verified the synthetic dataset contains 1000 generated learner records.
- Verified that the dataset passes the validation checks.
- Verified reproducibility by generating two datasets with the same seed and confirming that the CSV files were identical.
- Verified dataset bounds, coverage, empty-generation handling, and corruption detection through the automated tests.
- Verified that the generated data uses the expected UI variants and cold-start assumptions.

### Checks run and outcomes:

#### Dataset validation

Command:

`python -m dataset.validate data/synthetic_learners.csv`

Result:

- **PASS: 1000 rows**
- UI variant counts:
  - Hint: 271
  - Concise: 235
  - Challenge: 255
  - Example: 239
- All generated rows passed the validation checks.

#### Dataset tests

Command:

`python -m unittest discover -s tests -p test_dataset.py -v`

Result:

- `test_bounds_and_coverage` — PASS
- `test_corruption_is_detected` — PASS
- `test_no_empty_generation` — PASS
- `test_reproducible_and_seed_changes_output` — PASS
- **4/4 tests passed**
- **Overall result: OK**

#### Reproducibility check

- Generated the synthetic dataset twice with `count=1000` and `seed=16`.
- Compared both generated CSV files using Windows file comparison.
- Result: `FC: no differences encountered`.
- This confirms that generation is reproducible when the same seed is used.



### Problems I fixed:

- Ensured the Member 1 files were copied into the shared repository root with the required directory structure.
- Removed generated Python `__pycache__` and `.pyc` files from the contribution.
- Verified that only the required dataset, generation/validation, and test files were committed.
- Confirmed that temporary files created during reproducibility testing were removed after comparison.

### Pull request / commit references:

- Branch: `Kavya_S_Nair`
- Commit: `a7ded7`
- Commit message: `Add synthetic data generation and validation`
- Remote branch: `origin/Kavya_S_Nair`

### Remaining work:

- Review the simulator assumptions with the project guide and document any agreed changes.
- Inspect the dataset behaviour through the integrated application UI after all four member contributions are merged.
- Create a Pull Request from `Kavya_S_Nair` to the team's integration/main branch.