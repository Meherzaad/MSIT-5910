"""Real serial HTTP protocol; no browser or Docker claims."""
import http.cookiejar
import json
import math
import os
import secrets
import statistics
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from werkzeug.security import generate_password_hash

ROOT=Path(__file__).resolve().parents[2]
PASSWORD=secrets.token_urlsafe(24)
DATABASE=ROOT/'data/revalidation.db'
if DATABASE.exists(): DATABASE.unlink()
env=dict(os.environ,APP_SECRET_KEY=secrets.token_hex(32),
         DEMO_PASSWORD_HASH=generate_password_hash(PASSWORD),DATABASE_PATH=str(DATABASE))
log=(ROOT/'results/unit6/server_revalidation.txt').open('w')
process=subprocess.Popen([sys.executable,'-m','gunicorn','--chdir','src',
                         '--bind','127.0.0.1:8765','--workers','1','app:create_app()'],
                         cwd=ROOT,env=env,stdout=log,stderr=log)
base='http://127.0.0.1:8765'
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def request(path,body=None,headers=None):
    data=None if body is None else json.dumps(body).encode()
    req=urllib.request.Request(base+path,data=data,headers=dict({'Content-Type':'application/json'},**(headers or {})))
    with opener.open(req,timeout=5) as response:
        return response.status,response.read().decode()
try:
    for _ in range(100):
        try: request('/health');break
        except OSError: time.sleep(0.1)
    _,raw=request('/login',dict(username='technician',password=PASSWORD))
    token=json.loads(raw)['csrf'];headers={'X-CSRF-Token':token}
    row=dict(cpu_pct=50,memory_pct=60,storage_pct=70,network_mbps=400,temperature_c=55,environment_temp_c=24)
    normal_status,normal=request('/api/analyze',row,headers)
    hotrow=dict(row,temperature_c=90)
    hot_status,hot=request('/api/analyze',hotrow,headers)
    hot=json.loads(hot)
    ack_status,ack=request(f"/api/observations/{hot['id']}/acknowledge",{},headers)
    _,html=request('/')
    for _ in range(10): request('/api/analyze',hotrow,headers)
    batches=[]
    for batch in range(3):
        latencies=[];start=time.perf_counter()
        for _ in range(100):
            one=time.perf_counter();status,raw=request('/api/analyze',hotrow,headers)
            latencies.append((time.perf_counter()-one)*1000)
            assert status==201 and json.loads(raw)['baseline_anomaly']==1
        elapsed=time.perf_counter()-start
        batches.append(dict(batch=batch+1,median_ms=statistics.median(latencies),
                            p95_ms=sorted(latencies)[math.ceil(.95*len(latencies))-1],
                            throughput_per_second=100/elapsed,successful=100))
    from sqlite3 import connect
    with connect(DATABASE) as db:
        records=db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]
        audit=db.execute('SELECT observation_id,actor,action FROM audit').fetchall()
    result=dict(protocol='Ten warmups; three batches of 100 serial authenticated loopback HTTP requests; one Gunicorn worker',
                normal=dict(status=normal_status,response=json.loads(normal)),hot=dict(status=hot_status,response=hot),
                acknowledged=dict(status=ack_status,response=json.loads(ack)),
                dashboard_html_verified='Analyze an observation' in html,
                batches=batches,database_records=records,audit=audit,
                browser_reexecuted=False,docker_executed=False)
    (ROOT/'results/unit6/http_revalidation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
finally:
    process.terminate();process.wait(timeout=10);log.close()
