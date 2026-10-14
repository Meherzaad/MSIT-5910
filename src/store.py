"""Persistent observations and atomic acknowledgement audit."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY, created_at TEXT NOT NULL,
                    payload TEXT NOT NULL, anomaly INTEGER NOT NULL,
                    status TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY, observation_id INTEGER NOT NULL,
                    actor TEXT NOT NULL, action TEXT NOT NULL, created_at TEXT NOT NULL,
                    FOREIGN KEY(observation_id) REFERENCES observations(id));
            ''')

    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        return db

    def save(self, result):
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as db:
            cursor = db.execute('INSERT INTO observations(created_at,payload,anomaly,status)'
                                ' VALUES(?,?,?,?)', (now, json.dumps(result),
                                 result['baseline_anomaly'], result['status']))
            identifier = cursor.lastrowid
        return dict(result, id=identifier, created_at=now)

    def recent(self):
        with self.connect() as db:
            rows = db.execute('SELECT * FROM observations ORDER BY id DESC LIMIT 50').fetchall()
        return [dict(json.loads(r['payload']), id=r['id'], created_at=r['created_at'],
                     status=r['status']) for r in rows]

    def acknowledge(self, identifier, actor):
        with self.connect() as db:
            changed = db.execute("UPDATE observations SET status='acknowledged' "
                                 "WHERE id=? AND status='open'", (identifier,)).rowcount
            if not changed:
                return False
            db.execute('INSERT INTO audit(observation_id,actor,action,created_at) VALUES(?,?,?,?)',
                       (identifier, actor, 'acknowledged', datetime.now(timezone.utc).isoformat()))
        return True

    def check(self):
        with self.connect() as db:
            db.execute('SELECT id FROM observations LIMIT 1').fetchall()
