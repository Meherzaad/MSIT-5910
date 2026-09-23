import csv,json,time
from pathlib import Path
from baseline import predict,metrics

def run():
    with open("data/synthetic_telemetry.csv",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    thresholds=json.load(open("config/thresholds.json",encoding="utf-8"))
    y=[int(r["is_anomaly"]) for r in rows]
    start=time.perf_counter(); p=[predict(r,thresholds) for r in rows]
    result=metrics(y,p)
    result["mean_detection_latency_ms"]=(time.perf_counter()-start)*1000/len(rows)
    result["observations"]=len(rows)
    Path("results").mkdir(exist_ok=True)
    json.dump(result,open("results/baseline_metrics.json","w"),indent=2)
    return result
if __name__=="__main__": print(json.dumps(run(),indent=2))
