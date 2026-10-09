# Member 4 — Integration, persistence and testing

Assigned student: Delfin Davis

## Files to push

- `server.py`
- `core.py`
- `web/app.js`
- `tests/test_core.py`
- `tests/test_server.py`
- `README.md`
- `.gitignore`
- `docs/`

Copy the contents of your member folder into the shared repository root, preserving subdirectories. Read `docs/GITHUB_WORKFLOW.md` in the integrated project for the exact stage/commit instructions. The full app requires all four contributions.

## Understand, verify and develop your module

1. Trace the start, variant and completion API calls.
2. Explain why the current selection rule is not a bandit.
3. Run all tests, repeat a submission and restart the server to verify persistence.
4. Check all four teammates can run the combined project and rehearse the demo.

Verification: `python -m unittest discover -s tests -v`

## Your contribution record

- Changes I made: Integrated the local prototype with scoring, persistence, and checks. Added `server.py` for API routes, `core.py` for SQLite database logic, and `app.js` for front-end integration. Updated the main `README.md` with team assignments.
- Requirements I verified: Verified the HTTP API flow (start, variant, complete) and CSV export functionality. Confirmed that the current selection uses a fixed demo rule, not a bandit algorithm yet.
- Checks run and outcomes: Ran `python -m unittest discover -s tests -v`. All 10 tests passed successfully. Verified that repeated identical submissions return the stored result without duplicating.
- Problems I fixed: Ensured SQLite database properly initializes and persists data across server restarts.
- Pull request / commit references: Branch `Delfin_Davis` to main.
- Remaining work: Transition fixed demo rules to LinUCB/Thompson Sampling in Phase II.