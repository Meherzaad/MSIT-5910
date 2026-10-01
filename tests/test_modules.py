import csv
import json
import random
import pytest
from baseline import predict, metrics
from telemetry import FEATURES, validate, split_rows
from generate_data import generate
from isolation_forest import detect
from evaluate import run

T = {'cpu_pct':92,'memory_pct':94,'storage_pct':95,'network_mbps':940,'temperature_c':82}
R = {'cpu_pct':50,'memory_pct':60,'storage_pct':70,'network_mbps':400,'temperature_c':55,'environment_temp_c':24}

@pytest.mark.parametrize('feature', list(T))
@pytest.mark.parametrize('delta, expected', [(-0.01,0),(0,1),(0.01,1)])
def test_threshold_boundaries(feature, delta, expected):
    assert predict(dict(R, **{feature:T[feature]+delta}), T) == expected

@pytest.mark.parametrize('value', [float('nan'),float('inf'),-1,101,None,'bad'])
def test_invalid_values(value):
    with pytest.raises(ValueError): validate(dict(R,cpu_pct=value))

def test_missing_and_numeric_strings():
    assert validate({k:str(v) for k,v in R.items()}) == R
    with pytest.raises(ValueError): validate({})

def test_metrics_known_confusion():
    result = metrics([1,1,0,0],[1,0,1,0])
    assert result == dict(precision=.5,recall=.5,f1=.5,false_positive_rate=.5,tp=1,fp=1,fn=1,tn=1)

@pytest.mark.parametrize('labels,predictions', [([0,0],[0,0]),([1,1],[0,0]),([1,1],[1,1])])
def test_metric_denominators(labels, predictions):
    assert all(0 <= metrics(labels,predictions)[k] <= 1 for k in ['precision','recall','f1','false_positive_rate'])

@pytest.mark.parametrize('labels,predictions', [([],[]),([2],[1]),([0],[3])])
def test_invalid_metrics(labels,predictions):
    with pytest.raises(ValueError): metrics(labels,predictions)

def test_reproducible_generation_and_rng(tmp_path):
    random.seed(100)
    before = random.getstate()
    a = generate(tmp_path/'a.csv', n=400)
    b = generate(tmp_path/'b.csv', n=400)
    assert a == b and len(a) == 400
    assert random.getstate() == before
    assert (tmp_path/'a.csv').read_bytes() == (tmp_path/'b.csv').read_bytes()
    with open(tmp_path/'a.csv') as f:
        rows = list(csv.DictReader(f))
    assert set(rows[0]) == set(FEATURES + ['is_anomaly'])
    assert set(int(r['is_anomaly']) for r in rows) == {0,1}
    for row in rows: validate(row)

@pytest.mark.parametrize('n',[0,-1,1.5])
def test_invalid_generation(n,tmp_path):
    with pytest.raises(ValueError): generate(tmp_path/'a.csv',n)

def test_split_and_minimum():
    train,test = split_rows(list(range(10)))
    assert train == list(range(8)) and test == [8,9]
    with pytest.raises(ValueError): split_rows([1])

@pytest.mark.parametrize('train,test', [([],[R]),([R],[])])
def test_forest_empty_partitions(train,test):
    with pytest.raises(ValueError): detect(train,test)

def test_forest_separation_and_mapping(monkeypatch):
    calls = {}
    class Scaler:
        def fit(self,rows): calls['fit'] = rows; return self
        def transform(self,rows): return rows
    class Model:
        def __init__(self,**kwargs): calls['settings']=kwargs
        def fit(self,rows): calls['model_fit']=rows
        def predict(self,rows): return [-1,1]
    monkeypatch.setattr('isolation_forest.StandardScaler',Scaler)
    monkeypatch.setattr('isolation_forest.IsolationForest',Model)
    result, latency = detect([R],[dict(R,cpu_pct=99),R])
    assert calls['fit'] == [[R[k] for k in FEATURES]]
    assert calls['model_fit'] == calls['fit']
    assert calls['settings']['random_state'] == 5910
    assert result == [1,0] and latency >= 0

def test_evaluator_contract(tmp_path,monkeypatch):
    path=tmp_path/'telemetry.csv'
    generate(path,10)
    config=tmp_path/'thresholds.json'; config.write_text(json.dumps(T))
    def fake_detect(train,test):
        assert len(train)==8 and len(test)==2
        return [0,0],0.1
    monkeypatch.setattr('evaluate.detect',fake_detect)
    result=run(path,config,tmp_path/'out')
    assert set(result)=={'baseline','isolation_forest'}
    for name in result:
        assert result[name]['test_observations']==2
        saved=json.loads((tmp_path/'out'/f'{name}_metrics.json').read_text())
        assert saved == result[name]
