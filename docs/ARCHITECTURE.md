# Phase I architecture and contracts

Browser UI uses ES modules. `onboarding.js` renders the profile and diagnostic form; `lesson.js` renders the four lesson styles and assessment. `app.js` handles navigation, network requests, the dataset explorer and results. `styles.css` supplies responsive presentation.

The local Python server serves only an explicit list of public UI files. `core.py` validates context, grades answers, applies fixed demo rules and saves sessions in SQLite. `dataset/` produces a separate synthetic CSV and metadata JSON.

## API

| Method / path | Input | Output |
|---|---|---|
| POST /api/start | experience_level, learning_preference, device_type, answers (three integer indices) | session_id, context, ui_variant, reason, selection_method, result=null |
| POST /api/variant | session_id, ui_variant | updated session, selection_method=manual_preview |
| POST /api/complete | session_id, answers (three integer indices) | session with persisted result |
| GET /api/session/{id} | session ID | session and existing result |
| GET /api/dataset | none | row count, variant counts, first 12 rows, metadata |
| GET /api/download/synthetic | none | synthetic CSV |
| GET /api/download/interactions | none | completed local interaction CSV |

Input errors return HTTP 400; missing records/resources return 404. POST requests require JSON. Scores and rewards are calculated on the server. Repeated identical assessment submission returns the existing result. Replacing an already submitted result is disallowed.

## SDLC evidence

Requirements: dataset generation, shared context fields, four UI variants, quiz flow and integration.
Design: this architecture and the data dictionary.
Implementation: four modules owned by the four team members.
Verification: dataset, core and HTTP integration tests plus manual browser checks.
Release: local ZIP/GitHub review prototype.
Maintenance: issues, reviewed changes and Phase II work plan.
