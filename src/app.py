"""Restricted local research application; not a production identity service."""
import hmac
import os
import secrets
import sqlite3
from datetime import timedelta
from functools import wraps
from pathlib import Path
from flask import Flask, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash
from service import DetectionService
from store import Store

ROOT = Path(__file__).resolve().parents[1]

def create_app(overrides=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get('APP_SECRET_KEY'),
        DEMO_PASSWORD_HASH=os.environ.get('DEMO_PASSWORD_HASH'),
        DEMO_USER=os.environ.get('DEMO_USER', 'technician'),
        DATABASE_PATH=os.environ.get('DATABASE_PATH', str(ROOT / 'data/monitor.db')),
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Strict',
        SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE', '0') == '1',
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30), MAX_CONTENT_LENGTH=16384)
    app.config.update(overrides or {})
    if not app.config['SECRET_KEY'] or not app.config['DEMO_PASSWORD_HASH']:
        raise RuntimeError('APP_SECRET_KEY and DEMO_PASSWORD_HASH are required')
    store = Store(app.config['DATABASE_PATH'])
    engine = DetectionService(ROOT)
    app.extensions.update(store=store, engine=engine)

    def protected(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not session.get('user'):
                return jsonify(error='Authentication required'), 401
            supplied = request.headers.get('X-CSRF-Token', '')
            if request.method == 'POST' and not hmac.compare_digest(supplied, session.get('csrf', '')):
                return jsonify(error='Invalid request token'), 403
            return fn(*args, **kwargs)
        return wrapper

    @app.after_request
    def headers(response):
        response.headers.update({'Cache-Control':'no-store','X-Content-Type-Options':'nosniff',
            'X-Frame-Options':'DENY','Content-Security-Policy':"default-src 'self'; "
            "script-src 'self'; style-src 'self'; frame-ancestors 'none'; form-action 'self'"})
        return response

    @app.errorhandler(sqlite3.Error)
    def storage_failure(error):
        app.logger.warning('Storage operation failed')
        return jsonify(error='Storage unavailable; retry later'), 503

    @app.get('/health')
    def health():
        store.check()
        return jsonify(status='ready')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return jsonify(error='Invalid credentials'), 401
        origin = request.headers.get('Origin')
        if origin and origin != request.host_url.rstrip('/'):
            return jsonify(error='Origin rejected'), 403
        password = body.get('password', '')
        if (not isinstance(password, str) or
            not check_password_hash(app.config['DEMO_PASSWORD_HASH'], password) or
            body.get('username') != app.config['DEMO_USER']):
            return jsonify(error='Invalid credentials'), 401
        session.clear()
        session.update(user=app.config['DEMO_USER'], csrf=secrets.token_hex(24))
        session.permanent = True
        return jsonify(csrf=session['csrf'])

    @app.get('/')
    def dashboard():
        if not session.get('user'):
            return redirect('/login')
        return render_template('dashboard.html', csrf=session['csrf'])

    @app.post('/api/analyze')
    @protected
    def analyze():
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return jsonify(error='A JSON object with six telemetry fields is required'), 400
        try:
            result = engine.analyze(body)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(store.save(result)), 201

    @app.get('/api/observations')
    @protected
    def observations():
        return jsonify(store.recent())

    @app.get('/api/metrics')
    @protected
    def metrics():
        return jsonify(engine.evaluation)

    @app.post('/api/observations/<int:identifier>/acknowledge')
    @protected
    def acknowledge(identifier):
        if not store.acknowledge(identifier, session['user']):
            return jsonify(error='Observation is absent or not open'), 409
        return jsonify(id=identifier, status='acknowledged')

    @app.post('/logout')
    @protected
    def logout():
        session.clear()
        return jsonify(status='signed out')
    return app
