# 4-minute review demo

1. **Dataset (45 sec):** Open Synthetic dataset. Show 1,000 records, seed 16 and the four UI counts. Say: “These are fictional learner contexts and simulated outcomes. We can regenerate them with the same seed. The rules are documented assumptions.”
2. **Cold-start input (45 sec):** Open Learning demo. Choose beginner, worked examples, desktop. Answer `==`, True, and “when the if condition is false”. Say: “We collect information available before the learner starts the lesson. No previous engagement history is assumed.”
3. **Four variants (60 sec):** The selected UI is example-driven. Switch through hint-heavy, concise and challenge-oriented. Say: “All four teach the same conditionals concept and have the same assessment. Selection currently uses a fixed demonstration rule; the drop-down lets us inspect each design.”
4. **Result (45 sec):** Choose Mild day, `score >= 50`, Yes. Finish. Show 3/3 and reward 1.00. Say: “The server grades and saves the result. Repeated submission does not create another result.”
5. **Next stage (45 sec):** “In Phase II we will connect the selection API to LinUCB, update it using feedback and evaluate faithful explanations and performance against a static UI.”

## Each member's explanation

- Member 1: explain the random seed, column meanings and simulation rules.
- Member 2: explain how context and diagnostic answers reach the backend.
- Member 3: demonstrate the four styles and shared assessment.
- Member 4: explain API integration, reward, persistence and tests.

## Likely questions

**Does it already learn?** No. Phase I implements data and the interface; selection is a fixed demo rule.

**Is the dataset real?** No. It is explicitly synthetic and built for controlled development.

**Why do you need a dataset?** To exercise the future bandit pipeline and evaluate algorithms under stated simulation assumptions. It does not replace real-user validation.

**Why four interfaces?** They represent the four predefined presentation/support choices in our proposal.

**Is the explanation SHAP?** No. The displayed reason reflects the fixed rule actually used. The Phase II explanation must reflect the bandit's predicted reward and exploration uncertainty.

**Does high reward prove learning?** No. The reward is a proposed engineering signal; educational validity needs separate evaluation.
