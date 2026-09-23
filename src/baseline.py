def predict(row, thresholds):
    return int(
        float(row["cpu_pct"]) >= thresholds["cpu_pct"] or
        float(row["memory_pct"]) >= thresholds["memory_pct"] or
        float(row["storage_pct"]) >= thresholds["storage_pct"] or
        float(row["network_mbps"]) >= thresholds["network_mbps"] or
        float(row["temperature_c"]) >= thresholds["temperature_c"]
    )

def metrics(y,p):
    tp=sum(a==1 and b==1 for a,b in zip(y,p)); fp=sum(a==0 and b==1 for a,b in zip(y,p))
    fn=sum(a==1 and b==0 for a,b in zip(y,p)); tn=sum(a==0 and b==0 for a,b in zip(y,p))
    precision=tp/(tp+fp) if tp+fp else 0
    recall=tp/(tp+fn) if tp+fn else 0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0
    fpr=fp/(fp+tn) if fp+tn else 0
    return {"precision":precision,"recall":recall,"f1":f1,"false_positive_rate":fpr,"tp":tp,"fp":fp,"fn":fn,"tn":tn}
