# Member 2 — Onboarding and Diagnostic UI

Assigned student: Sandra Suresh Panicker

## Files to push

- `web/index.html`
- `web/onboarding.js`

The Member 2 files were copied into the shared repository while preserving the original directory structure. The complete application requires the contributions from all four members.

## Understand, verify and develop your module

1. The onboarding page collects the initial learner information before starting the lesson.

2. The learner profile includes:
- Python experience level
- Learning preference
- Device type

3. The diagnostic section contains three short Python questions to get an initial idea of the learner's understanding.

4. All three diagnostic questions are required, and an “I don’t know” option is provided so that the learner can continue without guessing.

5. The selected profile information and diagnostic answers are collected when the form is submitted and passed to the application.

6. The `question()` function is used to generate the diagnostic questions with the same radio-button structure.

Verification: `The onboarding and diagnostic files were reviewed in VS Code. The learner profile fields, three diagnostic questions, required options, “I don’t know” choices, form submission data, and error handling were checked in the source code. Full browser and integration verification will be completed after all four member contributions are available.`

## Contribution record

- Changes I made: Added the Member 2 onboarding and diagnostic UI using `web/index.html` and `web/onboarding.js`. Added the learner profile fields for experience level, learning preference, and device type, along with three diagnostic questions and the form submission handling.

- Requirements I verified: Confirmed that the learner profile fields are available and that all three diagnostic questions require a selection. Checked that an “I don’t know” option is available for the diagnostic questions and that the selected values are collected during form submission.

- Checks run and outcomes: Reviewed `index.html` and `onboarding.js` in VS Code. Checked the profile fields, diagnostic questions, radio-button options, reusable question function, form submission data, and error message handling. No immediate issues were identified during the source-code review.

- Problems I fixed: No additional defects were identified during the current source-code review.

- Pull request / commit references: Commit `bc7411e` — `Implement learner onboarding and diagnostic UI`. Pull request #1 was created from the `Sandra_Suresh_Panicker` branch to `main`.

- Remaining work: Complete browser-level and integration testing after all four members' contributions are combined. This includes testing the different profile options, checking the diagnostic questions, and verifying the complete onboarding flow with the other members' modules.
