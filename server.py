"""Run locally with Python 3.10+: python server.py. No third-party packages."""
import argparse
import csv
import io
import json
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
from core import Store

ROOT = Path(__file__).resolve().parent


def make_handler(store, root=ROOT):
    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self, status, data, content_type, filename=None):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            if filename:
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(data)

        def json_response(self, data, status=200):
            self.send_bytes(status, json.dumps(data).encode(), 'application/json; charset=utf-8')

        def do_GET(self):
            path = urlparse(self.path).path
            try:
                if path.startswith('/api/session/'):
                    return self.json_response(store.get(path.rsplit('/', 1)[-1]))
                if path == '/api/dataset':
                    with (root / 'data/synthetic_learners.csv').open(newline='', encoding='utf-8') as handle:
                        rows = list(csv.DictReader(handle))
                    metadata = json.loads((root / 'data/synthetic_learners.metadata.json').read_text(encoding='utf-8'))
                    return self.json_response({'count': len(rows), 'ui_counts': dict(Counter(r['ui_variant'] for r in rows)), 'preview': rows[:12], 'metadata': metadata})
                if path == '/api/download/synthetic':
                    return self.send_bytes(200, (root / 'data/synthetic_learners.csv').read_bytes(), 'text/csv; charset=utf-8', 'synthetic_learners.csv')
                if path == '/api/download/interactions':
                    fields = ['session_id','created_at','experience_level','learning_preference','device_type','diagnostic_score','initial_engagement','ui_variant','selection_method','quiz_correct','quiz_total','task_completed','reward','data_source']
                    output = io.StringIO(newline='')
                    writer = csv.DictWriter(output, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(store.export_rows())
                    return self.send_bytes(200, output.getvalue().encode(), 'text/csv; charset=utf-8', 'prototype_interactions.csv')
                allowed = {'/': ('index.html','text/html'), '/index.html':('index.html','text/html'),
                           '/styles.css':('styles.css','text/css'), '/app.js':('app.js','text/javascript'),
                           '/onboarding.js':('onboarding.js','text/javascript'), '/lesson.js':('lesson.js','text/javascript')}
                if path not in allowed:
                    return self.json_response({'error': 'Not found'}, 404)
                filename, mime = allowed[path]
                self.send_bytes(200, (root / 'web' / filename).read_bytes(), mime + '; charset=utf-8')
            except KeyError as exc:
                self.json_response({'error': str(exc.args[0])}, 404)
            except FileNotFoundError:
                self.json_response({'error': 'A required file is missing. Combine all four member folders and generate the dataset as described in README.md.'}, 404)

        def do_POST(self):
            try:
                if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                    raise ValueError('Send application/json.')
                length = int(self.headers.get('Content-Length', 0))
                if length < 1 or length > 10000:
                    raise ValueError('Invalid request size.')
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict):
                    raise ValueError('Expected a JSON object.')
                path = urlparse(self.path).path
                if path == '/api/start':
                    result = store.start(payload)
                elif path == '/api/variant':
                    if not isinstance(payload.get('session_id'), str):
                        raise ValueError('Missing session ID.')
                    result = store.change_variant(payload['session_id'], payload.get('ui_variant'))
                elif path == '/api/complete':
                    if not isinstance(payload.get('session_id'), str):
                        raise ValueError('Missing session ID.')
                    result = store.complete(payload['session_id'], payload.get('answers'))
                else:
                    return self.json_response({'error': 'Not found'}, 404)
                self.json_response(result)
            except (ValueError, UnicodeDecodeError) as exc:
                self.json_response({'error': str(exc)}, 400)
            except KeyError as exc:
                self.json_response({'error': str(exc.args[0])}, 404)

    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--db', default=str(ROOT / 'runtime/demo.sqlite3'))
    args = parser.parse_args()
    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    if not (ROOT / 'data/synthetic_learners.csv').exists():
        from dataset.generate import write_dataset
        write_dataset(ROOT / 'data/synthetic_learners.csv')
    server = HTTPServer(('127.0.0.1', args.port), make_handler(Store(args.db)))
    print(f'AdaptLearn Phase I: http://127.0.0.1:{args.port}', flush=True)
    print('Local classroom demo. Press Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
