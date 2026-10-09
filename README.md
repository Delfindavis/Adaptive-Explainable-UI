# AdaptLearn — Group 16 Phase I

**Explainable Cold-Start Adaptive User Interface for Online Learning**

NSS College of Engineering, Palakkad. This is an AI-assisted academic prototype, prepared from the team's first-review presentation and the Phase I dataset/UI scope. Owners are assigned by the team; no author names are embedded in the generated code.

## Run

Requires **Python 3.10+** and a modern browser. Uses Python's standard library and plain HTML/CSS/JavaScript; no third-party dependencies.

From this repository's root:

```bash
python server.py
```

Open http://127.0.0.1:8000. On Windows use `py` if `python` is unavailable; on macOS/Linux use `python3`.

```bash
python -m dataset.generate --count 1000 --seed 16
python -m dataset.validate data/synthetic_learners.csv
python -m unittest discover -s tests -v
```

The included dataset has 1,000 fictional learners/events. Regeneration overwrites only the specified CSV and its metadata JSON. The app automatically generates a default dataset if the CSV is missing. To change the port: `python server.py --port 8001`.

## Demo flow

1. Open Synthetic dataset to inspect and download simulated data.
2. Open Learning demo and select experience, preference and device.
3. Answer three diagnostic questions. The server grades them.
4. Read the selected version of a Python conditionals lesson.
5. Use the style selector to preview all four presentations.
6. Complete the identical three-question assessment.
7. Inspect the score, reward and explanations of correct answers.
8. Download local interaction records separately from synthetic data.

The fixed demo rule uses diagnostic score and preference. Experience and device are collected for future model features but do not affect the current rule. Initial engagement is explicitly unavailable.

## Persistence

Records are stored at `runtime/demo.sqlite3`, ignored by Git. Anonymous random session IDs are used; no name or email is requested. Refreshing the page resumes the session through browser session storage. Closing the browser tab loses that resume pointer but does not delete the stored record. Clearing local demonstration data means stopping the server and deleting that local database, then restarting.

Successful resubmission of the same answers returns the same stored result; different answers or variant changes after completion are rejected. Incomplete sessions are stored but not included in the completed-interaction CSV. A single task cannot establish learning improvement. Style-preview sessions are flagged `manual_preview` and should not be used as single-style treatment observations.

## Repository modules

| Module | Owner | Role |
|---|---|---|
| `dataset/`, `data/` | Kavya S Nair (Member 1) | Synthetic generation and validation |
| `web/index.html`, `web/onboarding.js` | Sandra Suresh Panicker (Member 2) | Shell, learner details and diagnostic quiz |
| `web/lesson.js`, `web/styles.css` | Mrudhula Mohan (Member 3) | Four lesson presentations, assessment UI, responsive styling |
| `core.py`, `server.py`, `web/app.js` | Delfin Davis (Member 4) | Selection rules, persistence, HTTP API and app integration |

## Implemented / next semester

The implemented Phase I covers UI and synthetic data. UI selection is a fixed rule and manual preview; reward is calculated but does not update a model. The selection explanation is the actual rule, not a SHAP/LIME output.

Next semester: replace selection behind the existing API with LinUCB, track model versions and decisions, implement safe reward updates, evaluate explanations, compare with a static baseline and validate with real users if permitted. See `docs/PHASE_II.md`.

See `docs/DATA_DICTIONARY.md`, `docs/ARCHITECTURE.md`, `docs/DEMO_SCRIPT.md`, `docs/GITHUB_WORKFLOW.md` and the four member handovers.
