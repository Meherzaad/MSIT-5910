import csv,json,time
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from baseline import metrics

FEATURES=["cpu_pct","memory_pct","storage_pct","network_mbps","temperature_c","environment_temp_c"]

def run(data_path="data/synthetic_telemetry.csv"):
    with open(data_path,encoding="utf-8") as f: rows=list(csv.DictReader(f))
    X=[[float(r[k]) for k in FEATURES] for r in rows]; y=[int(r["is_anomaly"]) for r in rows]
    cut=int(len(X)*0.8)
    scaler=StandardScaler().fit(X[:cut]); X_train=scaler.transform(X[:cut]); X_test=scaler.transform(X[cut:])
    model=IsolationForest(n_estimators=200,contamination=0.08,random_state=5910); model.fit(X_train)
    start=time.perf_counter(); raw=model.predict(X_test)
    p=[1 if v==-1 else 0 for v in raw]
    result=metrics(y[cut:],p)
    result.update({"mean_detection_latency_ms":(time.perf_counter()-start)*1000/len(X_test),
                   "test_observations":len(X_test),"training_observations":cut,"features":FEATURES})
    Path("results").mkdir(exist_ok=True)
    json.dump(result,open("results/isolation_forest_metrics.json","w"),indent=2)
    return result
if __name__=="__main__": print(json.dumps(run(),indent=2))
