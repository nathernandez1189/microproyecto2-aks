import json
import os
import time
import uuid

from flask import Response, g, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUESTS = Counter('app_requests_total', 'Completed HTTP requests', ['app', 'route', 'method', 'status'])
LATENCY = Histogram('app_request_seconds', 'Request duration in seconds', ['app', 'route'])


def instrument(app, name):
    @app.before_request
    def start():
        g.started = time.perf_counter()
        g.request_id = uuid.uuid4().hex

    @app.after_request
    def finish(response):
        elapsed = time.perf_counter() - g.started
        route = request.url_rule.rule if request.url_rule else 'unmatched'
        response.headers['X-Request-ID'] = g.request_id
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-store'
        if route not in ('/healthz', '/readyz', '/metrics', '/static/<path:filename>'):
            REQUESTS.labels(name, route, request.method, str(response.status_code)).inc()
            LATENCY.labels(name, route).observe(elapsed)
            print(json.dumps({'event': 'http_request', 'app': name, 'path': route,
                              'method': request.method, 'status': response.status_code,
                              'duration_ms': round(elapsed * 1000, 2),
                              'request_id': g.request_id, 'pod': os.getenv('HOSTNAME', 'local')}), flush=True)
        return response

    @app.get('/metrics')
    def metrics():
        return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)
