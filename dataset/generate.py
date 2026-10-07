"""Run from repository root: python -m dataset.generate --count 1000 --seed 16."""
import argparse
import csv
import json
import random
from pathlib import Path

VARIANTS = ('hint', 'example', 'concise', 'challenge')
FIELDS = ('learner_id', 'diagnostic_score', 'experience_level', 'learning_preference',
          'device_type', 'initial_engagement', 'ui_variant', 'action_probability',
          'quiz_correct', 'quiz_total', 'task_completed', 'reward', 'data_source')


def generate(count=1000, seed=16):
    """One fictional learner and one randomly assigned, simulated task per row.

    Relationships below are explicit simulation assumptions, not research findings.
    Only the assigned arm's outcome is recorded; there are no observed counterfactuals.
    """
    if count < 1:
        raise ValueError('count must be positive')
    rng = random.Random(seed)
    rows = []
    for i in range(count):
        experience = rng.choice(('beginner', 'intermediate', 'advanced'))
        mean = {'beginner': 30, 'intermediate': 55, 'advanced': 75}[experience]
        score = round(max(0, min(100, rng.gauss(mean, 18))))
        preference = rng.choice(VARIANTS)
        device = rng.choice(('mobile', 'desktop', 'tablet'))
        # No interaction history exists at this initial decision.
        arm = rng.choice(VARIANTS)
        probability = 0.25 + 0.004 * score
        probability += 0.10 if arm == preference else 0
        if arm == 'hint' and score < 50:
            probability += 0.10
        if arm == 'challenge' and score < 40:
            probability -= 0.12
        if arm == 'challenge' and score >= 70:
            probability += 0.05
        probability = max(0.05, min(0.95, probability))
        completed = int(rng.random() < (0.72 + 0.18 * score / 100))
        correct = sum(rng.random() < probability for _ in range(3)) if completed else 0
        reward = round(0.8 * (correct / 3) + 0.2 * completed, 4)
        rows.append(dict(zip(FIELDS, (
            f'SYN-{i+1:05d}', score, experience, preference, device, 'unavailable',
            arm, 0.25, correct, 3, completed, reward, 'synthetic_simulated_event'))))
    return rows


def write_dataset(output, count=1000, seed=16):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = generate(count, seed)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    output.with_suffix('.metadata.json').write_text(json.dumps({
        'count': count, 'seed': seed, 'generator_version': '1.0',
        'data_source': 'synthetic_simulated_event',
        'policy': 'uniform random UI assignment; probability 0.25 per UI',
        'reward': '0.8 * quiz_correct / quiz_total + 0.2 * task_completed',
        'limitations': 'Assumed learner behaviour. Does not establish educational effectiveness.'
    }, indent=2), encoding='utf-8')
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--count', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=16)
    parser.add_argument('--output', default='data/synthetic_learners.csv')
    args = parser.parse_args()
    write_dataset(args.output, args.count, args.seed)
    print(f'Generated {args.count} simulated rows: {args.output}')
