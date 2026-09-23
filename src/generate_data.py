import csv, random
from pathlib import Path

def generate(path, n=12000, seed=5910):
    random.seed(seed)
    fields=["cpu_pct","memory_pct","storage_pct","network_mbps","temperature_c","environment_temp_c","is_anomaly"]
    rows=[]
    for _ in range(n):
        anomaly=1 if random.random()<0.08 else 0
        cpu=max(1,min(100,random.gauss(52,13)))
        mem=max(1,min(100,random.gauss(61,12)))
        storage=max(1,min(100,random.gauss(68,10)))
        net=max(1,min(1000,random.gauss(420,160)))
        temp=max(20,min(100,random.gauss(55,7)))
        env=max(15,min(45,random.gauss(24,3)))
        if anomaly:
            kind=random.randrange(5)
            if kind==0: cpu=random.uniform(93,100)
            elif kind==1: mem=random.uniform(95,100)
            elif kind==2: storage=random.uniform(96,100)
            elif kind==3: net=random.uniform(945,1000)
            else: temp=random.uniform(83,96)
        rows.append([round(cpu,2),round(mem,2),round(storage,2),round(net,2),round(temp,2),round(env,2),anomaly])
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(fields); w.writerows(rows)
    return rows

if __name__=="__main__":
    generate("data/synthetic_telemetry.csv")
