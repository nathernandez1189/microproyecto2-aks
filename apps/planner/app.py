import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from common.observability import instrument

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
instrument(app, 'planner')
database = os.getenv('DATABASE_PATH', '/data/planner.db')
Path(database).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def connect():
    connection = sqlite3.connect(database, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


with connect() as connection:
    connection.execute('PRAGMA journal_mode=WAL')
    connection.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, '
                       'course TEXT NOT NULL, status TEXT NOT NULL DEFAULT "pendiente", '
                       'created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/healthz')
def health():
    return jsonify(status='ok')


@app.get('/readyz')
def ready():
    try:
        with connect() as connection:
            connection.execute('SELECT id FROM tasks LIMIT 1').fetchall()
        return jsonify(status='ready', storage='sqlite', pod=os.getenv('HOSTNAME', 'local'))
    except sqlite3.Error:
        return jsonify(status='unavailable'), 503


@app.get('/api/tasks')
def list_tasks():
    with connect() as connection:
        tasks = [dict(row) for row in connection.execute('SELECT * FROM tasks ORDER BY id DESC')]
    return jsonify(tasks=tasks)


@app.post('/api/tasks')
def create_task():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify(error='Envía un objeto JSON.'), 400
    title, course = body.get('title'), body.get('course', 'General')
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
        return jsonify(error='La actividad debe tener entre 1 y 120 caracteres.'), 400
    if not isinstance(course, str) or not 1 <= len(course.strip()) <= 60:
        return jsonify(error='La asignatura debe tener entre 1 y 60 caracteres.'), 400
    with connect() as connection:
        cursor = connection.execute('INSERT INTO tasks(title, course) VALUES (?, ?)', (title.strip(), course.strip()))
        task = dict(connection.execute('SELECT * FROM tasks WHERE id=?', (cursor.lastrowid,)).fetchone())
    return jsonify(task), 201


@app.patch('/api/tasks/<int:task_id>')
def update_task(task_id):
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or body.get('status') not in ('pendiente', 'en-curso', 'completada'):
        return jsonify(error='Estado permitido: pendiente, en-curso o completada.'), 400
    with connect() as connection:
        cursor = connection.execute('UPDATE tasks SET status=? WHERE id=?', (body['status'], task_id))
        if not cursor.rowcount:
            return jsonify(error='Actividad no encontrada.'), 404
        task = dict(connection.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone())
    return jsonify(task)


@app.delete('/api/tasks/<int:task_id>')
def delete_task(task_id):
    with connect() as connection:
        cursor = connection.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    if not cursor.rowcount:
        return jsonify(error='Actividad no encontrada.'), 404
    return '', 204


@app.errorhandler(413)
def too_large(_):
    return jsonify(error='La solicitud supera el límite permitido.'), 413
