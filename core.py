"""Member 4: shared validation, demo selection, scoring, and local persistence."""
import json
import sqlite3
import uuid
from datetime import datetime, timezone

VARIANTS = ('hint', 'example', 'concise', 'challenge')
DIAGNOSTIC_KEY = (1, 0, 1)
ASSESSMENT_KEY = (1, 1, 1)


def validate_answers(answers, sizes):
    if not isinstance(answers, list) or len(answers) != len(sizes):
        raise ValueError('Answer all three questions.')
    if any(type(a) is not int or not 0 <= a < size for a, size in zip(answers, sizes)):
        raise ValueError('Invalid answer choice.')
    return answers


def score(answers, key):
    return sum(a == b for a, b in zip(answers, key))


def reward(correct, total=3, completed=1):
    if total <= 0 or not 0 <= correct <= total or completed not in (0, 1):
        raise ValueError('Invalid reward input.')
    return round(0.8 * correct / total + 0.2 * completed, 4)


def choose_demo_variant(context):
    # Deliberately transparent fixed rules, not a trained model or an XAI output.
    if context['diagnostic_score'] < 34:
        return 'hint', 'The fixed demo rule offers hints when the diagnostic score is below 34%.'
    preference = context['learning_preference']
    if preference == 'challenge' and context['diagnostic_score'] < 67:
        return 'example', 'The fixed demo rule offers examples before challenges when the diagnostic score is below 67%.'
    return preference, 'The fixed demo rule follows the presentation preference you selected.'


class Store:
    def __init__(self, path):
        self.path = str(path)
        with self.connect() as con:
            con.execute('CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, context TEXT NOT NULL, ui_variant TEXT NOT NULL, reason TEXT NOT NULL, selection_method TEXT NOT NULL, result TEXT)')

    def connect(self):
        return sqlite3.connect(self.path)

    def get(self, session_id):
        with self.connect() as con:
            row = con.execute('SELECT id, created_at, context, ui_variant, reason, selection_method, result FROM sessions WHERE id=?', (session_id,)).fetchone()
        if row is None:
            raise KeyError('Session not found. Start a new learner demo.')
        return dict(session_id=row[0], created_at=row[1], context=json.loads(row[2]),
                    ui_variant=row[3], reason=row[4], selection_method=row[5],
                    result=json.loads(row[6]) if row[6] else None)

    def start(self, payload):
        allowed = {'experience_level': ('beginner','intermediate','advanced'),
                   'learning_preference': VARIANTS, 'device_type': ('desktop','mobile','tablet')}
        context = {}
        for field, options in allowed.items():
            if payload.get(field) not in options:
                raise ValueError(f'Invalid {field}.')
            context[field] = payload[field]
        answers = validate_answers(payload.get('answers'), (4, 3, 4))
        context['diagnostic_score'] = round(100 * score(answers, DIAGNOSTIC_KEY) / 3, 2)
        context['initial_engagement'] = 'unavailable'
        variant, reason = choose_demo_variant(context)
        session_id = uuid.uuid4().hex
        with self.connect() as con:
            con.execute('INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, NULL)',
                        (session_id, datetime.now(timezone.utc).isoformat(), json.dumps(context), variant, reason, 'fixed_demo_rule'))
        return self.get(session_id)

    def change_variant(self, session_id, variant):
        if variant not in VARIANTS:
            raise ValueError('Unknown presentation style.')
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            row = con.execute('SELECT result FROM sessions WHERE id=?', (session_id,)).fetchone()
            if row is None:
                raise KeyError('Session not found.')
            if row[0]:
                raise ValueError('This lesson is complete. Start another demo to switch styles.')
            con.execute('UPDATE sessions SET ui_variant=?, reason=?, selection_method=? WHERE id=?',
                        (variant, 'You manually selected this style to preview the Phase I interface.', 'manual_preview', session_id))
        return self.get(session_id)

    def complete(self, session_id, answers):
        answers = validate_answers(answers, (3, 3, 3))
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            row = con.execute('SELECT result FROM sessions WHERE id=?', (session_id,)).fetchone()
            if row is None:
                raise KeyError('Session not found.')
            if row[0]:
                old = json.loads(row[0])
                if old['answers'] != answers:
                    raise ValueError('This session already has a submitted result. Start another demo to retry.')
            else:
                correct = score(answers, ASSESSMENT_KEY)
                result = dict(answers=answers, correct=correct, total=3, task_completed=1,
                              reward=reward(correct), completed_at=datetime.now(timezone.utc).isoformat(),
                              data_source='prototype_interaction',
                              correct_answers=list(ASSESSMENT_KEY))
                con.execute('UPDATE sessions SET result=? WHERE id=?', (json.dumps(result), session_id))
        return self.get(session_id)

    def export_rows(self):
        with self.connect() as con:
            ids = [r[0] for r in con.execute('SELECT id FROM sessions WHERE result IS NOT NULL ORDER BY created_at')]
        for session_id in ids:
            session = self.get(session_id)
            result = session['result']
            yield { 'session_id': session_id, 'created_at': session['created_at'],
                    **session['context'], 'ui_variant': session['ui_variant'],
                    'selection_method': session['selection_method'], 'quiz_correct': result['correct'],
                    'quiz_total': result['total'], 'task_completed': 1, 'reward': result['reward'],
                    'data_source': 'prototype_interaction' }
