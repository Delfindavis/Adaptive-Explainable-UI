# AdaptLearn — Explainable Cold-Start Adaptive UI

**Phase I Academic Prototype**  
*Group 16 · NSS College of Engineering, Palakkad*

This repository contains the Phase I implementation of an explainable, cold-start adaptive user interface for online learning. It is a zero-dependency, local web application built to demonstrate synthetic educational data generation, adaptive UI assignment, and local persistence.

## 🚀 Quick Start

The application requires **Python 3.10+** and a modern web browser. It uses Python's standard library and plain HTML/CSS/JS (no third-party packages or `npm` required).

**1. Generate the synthetic dataset:**
```bash
python -m dataset.generate --count 1000 --seed 16
```

**2. Run the local server:**
```bash
python server.py
```
*On Windows, you may need to use `py server.py`.*

**3. Open the application:**  
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser. 

*(To run tests, use: `python -m unittest discover -s tests -v`)*

## ✨ Key Features (Phase I)

- **Synthetic Data Engine:** Generates a reproducible dataset of fictional learners and simulated interaction events to test the adaptive rules.
- **Diagnostic UI:** Collects cold-start learner context (experience, preference, device) and runs a real-time diagnostic quiz.
- **Adaptive Lesson Variants:** Presents educational content across four distinct pedagogical styles (Hint-heavy, Example-driven, Concise, Challenge-oriented).
- **Local Persistence:** Uses SQLite to store session data, grade assessments, calculate reward metrics, and export local interactions to CSV.

## 👥 Team & Module Ownership

The architecture is split into four distinct, non-overlapping modules managed by the team:

| Module | Owner | Responsibility |
|---|---|---|
| `dataset/`, `data/` | **Kavya S Nair** (Member 1) | Synthetic data generation, distribution rules, and validation. |
| `web/index.html`, `web/onboarding.js` | **Sandra Suresh Panicker** (Member 2) | Application shell, learner profile collection, and diagnostic UI. |
| `web/lesson.js`, `web/styles.css` | **Mrudhula Mohan** (Member 3) | Four dynamic presentation styles, assessment UI, and responsive design. |
| `core.py`, `server.py`, `web/app.js` | **Delfin Davis** (Member 4) | Backend HTTP API, selection rule logic, SQLite persistence, and frontend integration. |

## 📚 Documentation

Detailed documentation has been separated into the `docs/` directory:
- [System Architecture & API](docs/ARCHITECTURE.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Presentation / Demo Script](docs/DEMO_SCRIPT.md)
- [Phase II Roadmap (LinUCB / XAI integration)](docs/PHASE_II.md)
