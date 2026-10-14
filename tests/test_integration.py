"""Integration checks for state, API security and failure consequences."""
import sqlite3
import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from store import Store

NORMAL = dict(cpu_pct=50, memory_pct=60, storage_pct=70, network_mbps=400,
              temperature_c=55, environment_temp_c=24)
PASSWORD = 'synthetic-test-fixture-only'

@pytest.fixture(scope='module')
def application(tmp_path_factory):
    return create_app(dict(TESTING=True, SECRET_KEY='synthetic-test-session-key',
        DEMO_PASSWORD_HASH=generate_password_hash(PASSWORD),
        DATABASE_PATH=str(tmp_path_factory.mktemp('integration') / 'monitor.db')))

@pytest.fixture
def client(application):
    with application.extensions['store'].connect() as db:
        db.execute('DELETE FROM audit')
        db.execute('DELETE FROM observations')
    return application.test_client()

def login(client):
    result = client.post('/login',json=dict(username='technician',password=PASSWORD))
    assert result.status_code == 200
    return {'X-CSRF-Token':result.json['csrf']}

def test_required_secrets(monkeypatch):
    monkeypatch.delenv('APP_SECRET_KEY',raising=False)
    monkeypatch.delenv('DEMO_PASSWORD_HASH',raising=False)
    with pytest.raises(RuntimeError): create_app()

def test_health_and_login_page(client):
    assert client.get('/health').json == {'status':'ready'}
    assert client.get('/').status_code == 302
    response=client.get('/login')
    assert response.status_code==200
    assert response.headers['X-Frame-Options']=='DENY'
    assert 'no-store' in response.headers['Cache-Control']

@pytest.mark.parametrize('body',[None,[],{'password':1},{'username':'technician','password':'wrong'},
                                    {'username':'wrong','password':PASSWORD}])
def test_bad_login(client,body):
    assert client.post('/login',json=body).status_code==401

def test_origin_rejected(client):
    assert client.post('/login',json={'username':'technician','password':PASSWORD},
                       headers={'Origin':'https://other.invalid'}).status_code==403

def test_auth_and_csrf(client):
    assert client.post('/api/analyze',json=NORMAL).status_code==401
    login(client)
    assert client.post('/api/analyze',json=NORMAL).status_code==403

def test_normal_hot_review_and_reopen(client,application):
    headers=login(client)
    assert client.get('/').status_code==200
    assert client.get('/api/metrics').json['baseline']['tp']==174
    normal=client.post('/api/analyze',json=NORMAL,headers=headers)
    assert normal.status_code==201 and normal.json['status']=='normal'
    hot=client.post('/api/analyze',json=dict(NORMAL,temperature_c=90),headers=headers)
    assert hot.status_code==201 and hot.json['baseline_anomaly']==1
    assert hot.json['experimental_forest_anomaly']==0
    assert hot.json['reasons']==['temperature_c: 90 >= 82']
    identifier=hot.json['id']
    route=f'/api/observations/{identifier}/acknowledge'
    assert client.post(route,headers=headers).json['status']=='acknowledged'
    assert client.post(route,headers=headers).status_code==409
    assert client.post('/api/observations/999/acknowledge',headers=headers).status_code==409
    normalroute=f"/api/observations/{normal.json['id']}/acknowledge"
    assert client.post(normalroute,headers=headers).status_code==409
    reopened=Store(application.config['DATABASE_PATH'])
    assert reopened.recent()[0]['status']=='acknowledged'
    with reopened.connect() as db:
        audit=db.execute('SELECT observation_id,actor,action FROM audit').fetchall()
        assert [tuple(x) for x in audit]==[(identifier,'technician','acknowledged')]
    assert len(client.get('/api/observations').json)==2
    assert client.post('/logout',headers=headers).status_code==200
    assert client.get('/api/observations').status_code==401

@pytest.mark.parametrize('body',[[],{},dict(NORMAL,cpu_pct=-1),dict(NORMAL,temperature_c='bad')])
def test_invalid_never_saved(client,body):
    headers=login(client)
    assert client.post('/api/analyze',json=body,headers=headers).status_code==400
    assert client.get('/api/observations').json==[]

def test_storage_error(client,application,monkeypatch):
    headers=login(client)
    def unavailable(result): raise sqlite3.OperationalError('private diagnostic')
    monkeypatch.setattr(application.extensions['store'],'save',unavailable)
    result=client.post('/api/analyze',json=NORMAL,headers=headers)
    assert result.status_code==503
    assert 'private' not in result.json['error']

def test_request_size_limit(client):
    headers=login(client)
    assert client.post('/api/analyze',json={'padding':'x'*20000},headers=headers).status_code==413
