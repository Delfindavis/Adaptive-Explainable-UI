# One repository, four contributors

## 1. Bootstrap (Member 4)

Create one GitHub repository and invite all three teammates as collaborators. Grant the guide the appropriate access for evaluation. Create the initial README through GitHub so that the repository has a main branch. This requires the team's GitHub accounts; this ZIP has not created a remote repository.

Do not upload the entire ZIP under one student's account if you intend to review each member's work separately.

## 2. Each student clones and creates a branch

Replace the URL below with the actual repository URL:

```bash
git clone https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
git switch -c member-1-dataset
```

Other branch names: `member-2-onboarding`, `member-3-ui-variants`, `member-4-integration`.

Configure Git with your own name and your own verified or GitHub-provided no-reply email. Do not use another student's identity.

## 3. Copy assigned contents into the clone

Copy everything INSIDE your `member N` folder into the repository root. Preserve the nested `web/`, `tests/`, `docs/`, etc. paths. Merge directories when prompted. The contribution folders have no conflicting file paths, except Member 4's README replaces the bootstrap README intentionally.

Review the files, run the integrated version locally, and make an actual improvement or verify an assigned requirement. Record your verification and changes in your member handover. This is an AI-assisted starting implementation; committing a generated module alone is not evidence of having independently written it.

## 4. Stage only owned files

Member 1:
```bash
git add dataset data tests/test_dataset.py docs/MEMBER_1.md
git commit -m "Add synthetic data generator and validate simulation records"
git push -u origin member-1-dataset
```

Member 2:
```bash
git add web/index.html web/onboarding.js docs/MEMBER_2.md
git commit -m "Add learner onboarding and diagnostic quiz interface"
git push -u origin member-2-onboarding
```

Member 3:
```bash
git add web/lesson.js web/styles.css docs/MEMBER_3.md
git commit -m "Add four lesson presentation styles and shared assessment"
git push -u origin member-3-ui-variants
```

Member 4:
```bash
git add server.py core.py web/app.js tests/test_core.py tests/test_server.py .gitignore README.md docs/ARCHITECTURE.md docs/DATA_DICTIONARY.md docs/DEMO_SCRIPT.md docs/GITHUB_WORKFLOW.md docs/PHASE_II.md docs/TEST_REPORT.md docs/MEMBER_4.md
git commit -m "Integrate local prototype with scoring persistence and checks"
git push -u origin member-4-integration
```

## 5. Open and review pull requests

Each student opens a pull request into `main` and describes:
- What the module does.
- What they personally reviewed or changed.
- Which checks they ran and their results.
- AI assistance used and remaining limitations, following college policy.

Another teammate checks each PR. Merge Member 1, Member 2, Member 3, then Member 4. The app becomes fully runnable after all four are merged. Earlier branches are partial contributions; use the locally assembled full project when checking integration.

Use merge commits if retaining original commit authors is desired. Do not change authors or backdate commits. After merging:

```bash
git switch main
git pull origin main
python -m unittest discover -s tests -v
python server.py
```

Keep generated local databases and environment folders out of Git. The bundled synthetic CSV is safe to commit because it contains fictional records. Commit subsequent work in small, meaningful changes; do not generate empty commits for contribution counts.
