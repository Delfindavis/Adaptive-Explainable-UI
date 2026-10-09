# Data contract v1

The synthetic CSV contains one independently generated learner and one uniformly assigned simulated task per row. There is no historical interaction sequence or real learner data. The simulator assumes relationships; it does not learn them.

| Column | Values / meaning |
|---|---|
| learner_id | Unique SYN-prefixed fictional identifier; never a model feature |
| diagnostic_score | Integer 0–100, known before UI selection |
| experience_level | beginner / intermediate / advanced |
| learning_preference | hint / example / concise / challenge |
| device_type | mobile / desktop / tablet |
| initial_engagement | unavailable: no history is assumed |
| ui_variant | The one randomly assigned UI for this simulated event |
| action_probability | 0.25; uniform random assignment, not a bandit policy |
| quiz_correct | Integer 0–3; zero for simulated abandonment |
| quiz_total | 3 |
| task_completed | 0 or 1 |
| reward | 0.8 × quiz_correct / quiz_total + 0.2 × task_completed |
| data_source | synthetic_simulated_event |

The generated metadata JSON records seed, row count, generator version, policy and reward definition. The exact equations are readable in `dataset/generate.py`. Diagnostic values use clipped normal distributions with means 30/55/75 by experience and standard deviation 18. Quiz success probability starts at `0.25 + 0.004 * score`, gains 0.10 for a preference match, gains 0.10 for hints below 50, loses 0.12 for challenge below 40 and gains 0.05 for challenge at 70+. It is clipped to [0.05, 0.95]. Completion probability is `0.72 + 0.18 * score / 100`. On completion, three Bernoulli outcomes are sampled. These numbers are design assumptions for this prototype.

Only pre-decision context may become model input in Phase II. Quiz outcomes, completion and reward are post-decision feedback and must never be fed into the same decision. Device currently has no simulated effect. Avoid interpreting preference as a proven learning style.

## Separate local UI records

`prototype_interactions.csv` uses anonymous session_id, actual diagnostic/assessment answers graded on the server, context, final UI, selection_method and reward. Its label is `prototype_interaction`, not synthetic. It exports only completed tasks. Records from developers testing the UI are demonstrations, not a controlled educational study. Incomplete sessions are not automatically classified as abandonment.

The current backend keeps only the final presentation choice and flags any manual preview. Phase II must log every decision/exposure if analysing switches. The engagement feature remains unavailable; duration alone should not be treated as beneficial engagement.
