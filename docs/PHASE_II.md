# Next semester plan

1. Agree with the guide on lesson scope, reward weights, experimental design and decision timing.
2. Separate feature encoding, policy selection and outcome logging behind stable interfaces.
3. Member 1 expands synthetic scenarios: informative context, weak context, equal arms, noise and distribution changes. Preserve seeds and held-out evaluation scenarios.
4. Member 4 implements LinUCB with Member 1 reviewing the algorithm tests. Record context snapshots, policy/model version, selected arm, predicted reward and uncertainty. Update exactly once per decision outcome.
5. Member 2 adds reliable session/task handling and exposure/event logs. Adapt at task boundaries. Handle unfinished tasks and missing feedback explicitly.
6. Member 3 implements explanations grounded in actual decisions with Member 4. Evaluate the suitability of SHAP/LIME; explain exploration separately from predicted reward.
7. All members compare against a fixed static UI under comparable tasks. Repeat synthetic runs over multiple seeds, report early-interaction and cumulative reward, and separate simulated results from participant outcomes.
8. Conduct permitted user evaluation, improve accessibility, package the demo and prepare the final report.

No performance gain, human trust score or SHAP/LIME correctness is claimed by the Phase I release. Keep all four members responsible for tests and documentation of their own modules.
