# AdaptLearn — Explainable Cold-Start Adaptive UI

**Phase I Academic Prototype**  
*Group 16 · NSS College of Engineering, Palakkad*

AdaptLearn is an academic prototype that explores how an online learning interface can adapt to a learner's initial context and interaction feedback. It is a local web application built using Python, HTML, CSS, JavaScript and SQLite.

The project demonstrates synthetic educational data generation, learner onboarding, diagnostic assessment, four learning-interface presentation styles, LinUCB-based adaptive UI selection, reward-based model updates and local persistence.

## 🚀 Quick Start

### Requirements

- Python 3.10 or later
- A modern web browser
- No third-party Python packages or `npm` installation required for the standard prototype

### 1. Generate the synthetic dataset

From the repository root, run:

```bash
python3 -m dataset.generate --count 1000 --seed 16
```

This generates 1,000 simulated records using a reproducible random seed.

### 2. Start the application

```bash
python3 server.py
```

### 3. Open the application

Navigate to:

`http://127.0.0.1:8000`

### 4. Run the automated tests

```bash
python3 -m unittest discover -s tests -v
```

Run the tests on the exact version being submitted before reporting the final passing-test count.

## ✨ Key Features

### 1. Synthetic Data Engine

- Generates a reproducible dataset of simulated learners and interaction events.
- Supports dataset generation using a specified random seed.
- Validates generated data.
- Provides dataset exploration and CSV download.
- Keeps the synthetic dataset separate from records collected during prototype interactions.

The synthetic dataset is intended for demonstration and software validation. It does not represent a controlled study of real learners.

### 2. Learner Onboarding and Diagnostic Assessment

- Collects learner experience level, learning preference and device information.
- Provides a diagnostic quiz to estimate initial knowledge.
- Validates learner inputs and assessment responses.
- Supplies contextual information for adaptive interface selection.

### 3. Four Learning-Interface Variants

AdaptLearn presents learning content using four different styles:

- **Hint-heavy:** Emphasises hints and step-by-step guidance.
- **Example-driven:** Emphasises worked examples.
- **Concise:** Presents information in a compact format.
- **Challenge-oriented:** Emphasises attempting tasks and solving problems.

The application also supports manually previewing the available presentation styles.

### 4. LinUCB Contextual-Bandit Selection

The adaptive learning flow uses the LinUCB contextual-bandit algorithm to select a presentation style based on the learner's context.

The current live LinUCB context includes:

- Experience level
- Learning preference
- Device type
- Diagnostic quiz score
- An intercept feature

The implementation maintains a separate linear model for each UI variant. Selection balances predicted reward with an exploration term to support learning from interaction feedback.

The dataset specification includes an initial-engagement field, but initial engagement is not used as an input feature by the current live LinUCB model.

### 5. Assessment and Reward-Based Model Updates

After the learner completes the assessment, the prototype calculates a reward based on assessment performance and task completion:

```text
reward = 0.8 * (quiz_correct / quiz_total)
         + 0.2 * task_completed
```

Where:
- `quiz_correct` is the number of correct answers.
- `quiz_total` is the total number of assessment questions.
- `task_completed` is `1` if the task is completed and `0` otherwise.

The reward is constrained to the range `[0, 1]`.

For an eligible LinUCB-selected session, the observed reward updates the model associated with the selected UI variant and learner context. The implementation prevents the same completed assessment from updating the model repeatedly.

The reward function is a prototype design choice. It has not been validated as a measure of long-term learning, knowledge retention or educational effectiveness.

### 6. SQLite Persistence

The application stores session information, completed assessment results and LinUCB model state in a local SQLite database:

`runtime/demo.sqlite3`

The database is ignored by Git. The application can save and restore the serialized LinUCB model state, allowing the model to retain its learned state across application restarts.

The implementation also supports exporting completed prototype interaction records to CSV. These records are distinct from the synthetic dataset.

Anonymous random session IDs are used; the application does not request a learner's name or email address.

Refreshing the page can resume a session through browser session storage. Closing the browser tab removes the browser's resume pointer but does not automatically delete the stored database record.

Deleting `runtime/demo.sqlite3` removes the locally persisted session records and LinUCB model state. Stop the server before deleting the database.

### 7. Selection Explanations

The prototype displays information about how the interface was selected.

For LinUCB, the interface provides selection-related information, including predicted reward and exploration. The explanation describes aspects of the selection mechanism; it is not a feature-attribution result from an advanced explainable-AI method.

**SHAP and LIME feature-attribution explanations are not implemented in the current prototype.** Implementing and evaluating advanced explanations remain future work.

## 🧠 Selection Modes

The prototype supports three selection modes:

| Mode | Description | Updates LinUCB? |
|---|---|---|
| `linucb` | LinUCB selects a presentation style using the learner context. | Yes, after an eligible completed assessment. |
| `fixed_demo_rule` | A transparent, predefined rule selects a style for demonstration. | No. |
| `manual_preview` | The user manually switches between presentation styles. | No. |

Manual-preview sessions are not treated as clean observations of a single algorithm-selected style. Only eligible LinUCB-selected sessions update the model.

## 🧪 Testing and Verification

The automated test suite covers implemented functionality such as:

- Synthetic dataset generation and validation.
- LinUCB selection and model updates.
- Invalid input and reward validation.
- LinUCB model-state serialization and restoration.
- Session and assessment handling.
- SQLite persistence.
- Backend and HTTP integration.

Run the tests using:

```bash
python3 -m unittest discover -s tests -v
```

Automated tests help verify that the implemented functionality behaves as expected. They do not, by themselves, demonstrate that LinUCB outperforms a static interface or improves real-world learning outcomes.

## 👥 Team & Module Contributions

The project was developed collaboratively by four members, with each member contributing to specific modules and integration activities.

| Module / Area | Owner | Responsibilities |
|---|---|---|
| `dataset/`, `data/` | **Kavya S Nair (Member 1)** | Synthetic learner-data generation, distribution, dataset management and validation. |
| `web/index.html`, `web/onboarding.js`, `linucb.py`, LinUCB integration and related tests | **Sandra Suresh Panicker (Member 2)** | Application shell, learner onboarding, learner-context collection, diagnostic quiz interface, LinUCB contextual-bandit selection, reward-based model updates, model-state serialization and restoration integration, and tests for selection, updates and persistence. |
| `web/lesson.js`, `web/styles.css` | **Mrudhula Mohan (Member 3)** | Four learning-interface presentation styles, lesson presentation, assessment interface and responsive styling. |
| `core.py`, `server.py`, `web/app.js` | **Delfin Davis (Member 4)** | Backend HTTP API, session management, core application logic, SQLite session and assessment persistence, and frontend-backend integration. |

The modules are integrated into the complete AdaptLearn prototype, combining learner onboarding, adaptive UI selection, assessment, reward-based updates and persistent session records.

## ⚠️ Limitations and Future Work

Although the current prototype implements contextual UI selection and reward-based model updates, several research and evaluation tasks remain.

Planned future work includes:

- Investigating SHAP/LIME-based feature-level explanations.
- Evaluating the faithfulness, clarity and usefulness of selection explanations.
- Comparing LinUCB with a static-interface or other appropriate baseline.
- Evaluating adaptive selection across additional learner contexts.
- Conducting controlled evaluations of learning outcomes.
- Validating the approach with real learners, subject to appropriate approval and consent.
- Reporting model performance using suitable evaluation methods.

The synthetic dataset is designed for reproducible demonstration and software validation. It does not establish real-world learner behaviour or educational effectiveness.

Similarly, the implementation of LinUCB updates demonstrates that the model can learn from the defined reward signal; it does not prove that future recommendations will improve learning outcomes.

The server binds to loopback and is intended for local demonstration. It is not an authenticated production hosting service.

## 📚 Documentation

- [System Architecture and API](https://github.com/Delfindavis/Adaptive-Explainable-UI/blob/main/docs/ARCHITECTURE.md)
- [Data Dictionary](https://github.com/Delfindavis/Adaptive-Explainable-UI/blob/main/docs/DATA_DICTIONARY.md)
- [Presentation and Demo Script](https://github.com/Delfindavis/Adaptive-Explainable-UI/blob/main/docs/DEMO_SCRIPT.md)
- [Phase II Roadmap](https://github.com/Delfindavis/Adaptive-Explainable-UI/blob/main/docs/PHASE_II.md)

---

**Project:** Explainable Cold-Start Adaptive User Interface for Online Learning  
**Team:** Group 16  
**Institution:** NSS College of Engineering, Palakkad