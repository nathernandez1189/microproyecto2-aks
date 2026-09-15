"""Real HTTP tests. Start Compose, then: python3 -m unittest discover -s tests -v."""
import json
import http.client
import os
from pathlib import Path
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

CLASSIFIER = os.getenv('CLASSIFIER_URL', 'http://127.0.0.1:8081')
PLANNER = os.getenv('PLANNER_URL', 'http://127.0.0.1:8082')


def call(base, path, method='GET', data=None, headers=None):
    if isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
        headers = {'Content-Type': 'application/json'}
    try:
        response = urlopen(Request(base + path, data=data, headers=headers or {}, method=method), timeout=90)
    except HTTPError as error:
        response = error
    content = response.read()
    result = response.code, content, response.headers
    response.close()
    return result


def upload(content, filename='dog.jpg'):
    boundary = 'mp2-boundary-2026'
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="img"; filename="{filename}"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n').encode() + content + f'\r\n--{boundary}--\r\n'.encode()
    return call(CLASSIFIER, '/predict', 'POST', body, {'Content-Type': f'multipart/form-data; boundary={boundary}'})


class ClassifierTests(unittest.TestCase):
    def test_readiness_model(self):
        status, body, _ = call(CLASSIFIER, '/readyz')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['classes'], 1000)

    def test_real_inference_dog(self):
        status, body, _ = upload((Path(__file__).parent / 'fixtures/dog.jpg').read_bytes())
        result = json.loads(body)
        self.assertEqual(status, 200, result)
        predictions = result['predictions']
        self.assertEqual(len(predictions), 5)
        self.assertEqual(predictions[0]['label'], 'Samoyed')
        scores = [p['score'] for p in predictions]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertTrue(all(0 <= p <= 1 for p in scores))
        self.assertLessEqual(sum(scores), 1.00001)
        self.assertGreater(result['inference_ms'], 0)

    def test_missing_image(self):
        self.assertEqual(call(CLASSIFIER, '/predict', 'POST', b'')[0], 400)

    def test_invalid_image(self):
        self.assertEqual(upload(b'not an image')[0], 400)

    def test_oversized_upload(self):
        # Gunicorn rejects oversized Content-Length before consuming the body.
        # Sending only headers avoids the expected early-close BrokenPipe on urllib.
        url = urlsplit(CLASSIFIER)
        connection = http.client.HTTPConnection(url.hostname, url.port, timeout=10)
        connection.putrequest('POST', '/predict')
        connection.putheader('Content-Length', str(6 * 1024 * 1024))
        connection.putheader('Content-Type', 'multipart/form-data; boundary=test')
        connection.endheaders()
        response = connection.getresponse()
        self.assertEqual(response.status, 413)
        self.assertIn('error', json.loads(response.read()))
        connection.close()

    def test_metrics_include_predictions(self):
        upload(b'invalid')
        status, body, _ = call(CLASSIFIER, '/metrics')
        self.assertEqual(status, 200)
        self.assertIn(b'app_requests_total', body)
        self.assertIn(b'route="/predict"', body)


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.ids = []

    def tearDown(self):
        for identifier in self.ids:
            call(PLANNER, f'/api/tasks/{identifier}', 'DELETE')

    def create(self, title='Prueba de integración'):
        status, body, _ = call(PLANNER, '/api/tasks', 'POST', {'title': title, 'course': 'Computación en la Nube'})
        self.assertEqual(status, 201)
        result = json.loads(body)
        self.ids.append(result['id'])
        return result

    def test_crud(self):
        task = self.create()
        identifier = task['id']
        status, body, _ = call(PLANNER, '/api/tasks')
        self.assertEqual(status, 200)
        self.assertIn(identifier, [t['id'] for t in json.loads(body)['tasks']])
        status, body, _ = call(PLANNER, f'/api/tasks/{identifier}', 'PATCH', {'status': 'completada'})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['status'], 'completada')
        self.assertEqual(call(PLANNER, f'/api/tasks/{identifier}', 'DELETE')[0], 204)
        self.assertEqual(call(PLANNER, f'/api/tasks/{identifier}', 'DELETE')[0], 404)

    def test_sql_special_characters_are_data(self):
        title = "O'Brien'); DROP TABLE tasks; --"
        task = self.create(title)
        self.assertEqual(task['title'], title)
        self.assertEqual(call(PLANNER, '/api/tasks')[0], 200)

    def test_validation(self):
        for payload in ({'title': ''}, {'title': ' '*3}, {'title': 'a'*121}, {'title': 7}, [], {'title': 't', 'course': []}):
            self.assertEqual(call(PLANNER, '/api/tasks', 'POST', payload)[0], 400)

    def test_invalid_status_and_missing_task(self):
        task = self.create()
        self.assertEqual(call(PLANNER, f"/api/tasks/{task['id']}", 'PATCH', {'status': 'inventado'})[0], 400)
        self.assertEqual(call(PLANNER, '/api/tasks/99999999', 'PATCH', {'status': 'completada'})[0], 404)

    def test_ui_and_headers(self):
        for base, title in ((PLANNER, b'Campus Planner'), (CLASSIFIER, b'Visi')):
            status, body, headers = call(base, '/')
            self.assertEqual(status, 200)
            self.assertIn(title, body)
            self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')
            self.assertTrue(headers['X-Request-ID'])

    def test_readiness(self):
        status, body, _ = call(PLANNER, '/readyz')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['storage'], 'sqlite')


if __name__ == '__main__':
    unittest.main()
