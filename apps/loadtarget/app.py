import hashlib
from flask import Flask, jsonify

app = Flask(__name__)


@app.get('/')
def work():
    # A bounded CPU operation per request makes HPA behavior reproducible.
    hashlib.pbkdf2_hmac('sha256', b'demostracion', b'no-es-una-clave', 200_000)
    return jsonify(status='ok', operation='cpu-demo')


@app.get('/healthz')
def health():
    return jsonify(status='ok')
