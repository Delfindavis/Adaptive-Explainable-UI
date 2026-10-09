import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from http.server import HTTPServer
from core import Store
from server import make_handler, ROOT


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.http = HTTPServer(('127.0.0.1', 0), make_handler(Store(Path(cls.temp.name) / 'test.db'), ROOT))
        cls.base = 'http://127.0.0.1:' + str(cls.http.server_port)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def post(self, path, body):
        req = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as response:
            return json.load(response)

    def test_end_to_end(self):
        for path in ('/', '/app.js', '/lesson.js', '/onboarding.js', '/styles.css', '/api/dataset'):
            with urllib.request.urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
        session = self.post('/api/start', dict(experience_level='beginner',learning_preference='example',device_type='desktop',answers=[1,0,1]))
        sid = session['session_id']
        for variant in ('hint','example','concise','challenge'):
            changed = self.post('/api/variant', dict(session_id=sid,ui_variant=variant))
            self.assertEqual(changed['ui_variant'], variant)
        result = self.post('/api/complete', dict(session_id=sid,answers=[1,0,1]))
        self.assertEqual(result['result']['correct'], 2)
        with urllib.request.urlopen(self.base + '/api/download/interactions') as response:
            text = response.read().decode()
            self.assertIn('prototype_interaction', text)
            self.assertNotIn('synthetic_simulated_event', text)

    def test_invalid_request_and_private_files(self):
        with self.assertRaises(urllib.error.HTTPError) as err:
            self.post('/api/start', {})
        self.assertEqual(err.exception.code, 400)
        for path in ('/server.py', '/runtime/demo.sqlite3', '/api/session/missing'):
            with self.assertRaises(urllib.error.HTTPError) as err:
                urllib.request.urlopen(self.base + path)
            self.assertEqual(err.exception.code, 404)
