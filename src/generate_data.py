import csv, random
from pathlib import Path

def generate(path, n=12000, seed=5910):
    if not isinstance(n, int) or n < 1:
        raise ValueError('n must be a positive integer')
    rng = random.Random(seed)
    fields=["cpu_pct","memory_pct","storage_pct","network_mbps","temperature_c","environment_temp_c","is_anomaly"]
    rows=[]
    for _ in range(n):
        anomaly=1 if rng.random()<0.08 else 0
        cpu=max(1,min(100,rng.gauss(52,13)))
        mem=max(1,min(100,rng.gauss(61,12)))
        storage=max(1,min(100,rng.gauss(68,10)))
        net=max(1,min(1000,rng.gauss(420,160)))
        temp=max(20,min(100,rng.gauss(55,7)))
        env=max(15,min(45,rng.gauss(24,3)))
        if anomaly:
            kind=rng.randrange(5)
            if kind==0: cpu=rng.uniform(93,100)
            elif kind==1: mem=rng.uniform(95,100)
            elif kind==2: storage=rng.uniform(96,100)
            elif kind==3: net=rng.uniform(945,1000)
            else: temp=rng.uniform(83,96)
        rows.append([round(cpu,2),round(mem,2),round(storage,2),round(net,2),round(temp,2),round(env,2),anomaly])
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(fields); w.writerows(rows)
    return rows

if __name__=="__main__":
    generate("data/synthetic_telemetry.csv")
