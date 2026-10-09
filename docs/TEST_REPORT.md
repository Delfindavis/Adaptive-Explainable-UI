# Phase I verification report

Date: 29 September 2026

Executed on the assembled project in a Linux Python environment.

## Passed

- Assembly: all four contribution folders combined with no file-path collisions.
- Synthetic CSV: 1,000 rows passed schema, uniqueness, bounds, label and reward checks.
- UI assignment counts: hint 271, concise 235, challenge 255, example 239.
- Reproducibility: same seed produced identical records; a different seed changed output.
- Corrupt reward and duplicate learner ID were detected.
- Cold-start fixed rule and manual override behaved as specified.
- SQLite data persisted when the store was reopened.
- Repeated identical submission returned the stored result; changed answers and style changes after completion were rejected.
- HTTP flow: start, all four variant changes, complete and CSV export passed.
- Public HTML/CSS/JS and the dataset endpoint returned HTTP 200.
- Invalid input returned 400; private source/database paths and missing sessions returned 404.
- JavaScript syntax checks passed for all three JS modules.

Command: `python -m unittest discover -s tests -v`

Result: **10 tests passed**.

## Browser verification still required locally

A headless browser was unavailable in the build environment and its installation did not complete. No screenshot-based or automated browser rendering result is claimed. Before the review, each team member should:

1. Run the app with the README instructions on their laptop.
2. Complete the form using a keyboard and check that missing answers block submission.
3. Preview all four styles; open hints and worked answers.
4. Complete the assessment and refresh to confirm the result view resumes.
5. Check the dataset view and both CSV downloads.
6. Resize the window to mobile width and use browser zoom to inspect text and controls.

Windows/macOS execution has not been tested in this environment. The implementation uses cross-platform Python standard-library modules and relative project paths; record your own platform checks in your member handover.
