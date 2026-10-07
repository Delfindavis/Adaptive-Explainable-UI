"""Validate a generated CSV: python -m dataset.validate data/synthetic_learners.csv"""
import csv
import sys
from collections import Counter
from .generate import FIELDS, VARIANTS


def validate_rows(rows):
    errors, seen = [], set()
    for number, row in enumerate(rows, 2):
        try:
            if set(row) != set(FIELDS):
                raise ValueError('unexpected or missing fields')
            learner = row['learner_id']
            if not learner.startswith('SYN-') or learner in seen:
                raise ValueError('invalid or duplicate learner ID')
            seen.add(learner)
            if not 0 <= float(row['diagnostic_score']) <= 100:
                raise ValueError('diagnostic score out of range')
            if row['experience_level'] not in ('beginner', 'intermediate', 'advanced'):
                raise ValueError('invalid experience')
            if row['device_type'] not in ('mobile', 'desktop', 'tablet'):
                raise ValueError('invalid device')
            if row['ui_variant'] not in VARIANTS or row['learning_preference'] not in VARIANTS:
                raise ValueError('invalid UI or preference')
            if row['initial_engagement'] != 'unavailable':
                raise ValueError('cold-start engagement must be unavailable')
            correct, total, completed = (int(row[k]) for k in ('quiz_correct', 'quiz_total', 'task_completed'))
            if total != 3 or not 0 <= correct <= total or completed not in (0, 1):
                raise ValueError('invalid outcome')
            if completed == 0 and correct != 0:
                raise ValueError('abandoned simulated task must have zero correctness here')
            expected = round(0.8 * correct / total + 0.2 * completed, 4)
            if abs(float(row['reward']) - expected) > 0.0001:
                raise ValueError('reward mismatch')
            if float(row['action_probability']) != 0.25:
                raise ValueError('assignment probability must be 0.25')
            if row['data_source'] != 'synthetic_simulated_event':
                raise ValueError('missing synthetic label')
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f'Row {number}: {exc}')
    if not rows:
        errors.append('Dataset is empty')
    return errors


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/synthetic_learners.csv'
    with open(path, newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    errors = validate_rows(rows)
    if errors:
        print('\n'.join(errors[:20]))
        sys.exit(1)
    print(f'PASS: {len(rows)} rows; UI counts: {dict(Counter(r["ui_variant"] for r in rows))}')
