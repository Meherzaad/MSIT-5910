const csrf = document.querySelector('meta[name=csrf]').content;
async function api(path,method='GET',body) {
 const response=await fetch(path,{method,headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:body===undefined?undefined:JSON.stringify(body)});
 const result=await response.json(); if(!response.ok) throw new Error(result.error); return result;
}
const fixture={cpu_pct:50,memory_pct:60,storage_pct:70,network_mbps:400,temperature_c:55,environment_temp_c:24};
const form=document.querySelector('#analyze');
function load(hot){ for(const [k,v] of Object.entries(fixture))form.elements[k].value=hot&&k==='temperature_c'?90:v; }
document.querySelector('#normal').onclick=()=>load(false);
document.querySelector('#hot').onclick=()=>load(true);
function message(text){document.querySelector('#message').textContent=text;}
async function refresh(){
 const rows=await api('/api/observations');const tbody=document.querySelector('#records');tbody.replaceChildren();
 for(const r of rows){const tr=document.createElement('tr');
  for(const v of [r.id,r.created_at,r.baseline_anomaly?'Alert':'Normal',r.status]){const td=document.createElement('td');td.textContent=v;tr.append(td);}
  const td=document.createElement('td');if(r.status==='open'){const b=document.createElement('button');b.textContent='Acknowledge';b.onclick=async()=>{try{await api(`/api/observations/${r.id}/acknowledge`,'POST',{});message(`Observation ${r.id} acknowledged for investigation.`);await refresh();}catch(e){message(e.message);}};td.append(b);}tr.append(td);tbody.append(tr);
 }
}
form.addEventListener('submit',async event=>{
 event.preventDefault();const body=Object.fromEntries([...new FormData(form)].map(([k,v])=>[k,Number(v)]));
 try{const r=await api('/api/analyze','POST',body);message(`Observation ${r.id} saved. Status: ${r.status}.`);
 const out=document.querySelector('#result');out.replaceChildren();
 for(const text of [`Threshold baseline: ${r.baseline_anomaly?'INVESTIGATE':'NORMAL'}`,`Experimental forest: ${r.experimental_forest_anomaly?'unusual':'typical'}`,...r.reasons,`Configuration: ${r.config_version}`,`Model: ${r.model_version}`]){const p=document.createElement('p');p.textContent=text;out.append(p);}await refresh();}catch(e){message(e.message);}
});
document.querySelector('#logout').onclick=async()=>{try{await api('/logout','POST',{});location.assign('/login');}catch(e){message(e.message);}};
async function start(){try{await refresh();const metrics=await api('/api/metrics');document.querySelector('#metrics').textContent=Object.entries(metrics).map(([name,m])=>`${name}: precision ${m.precision.toFixed(3)}, recall ${m.recall.toFixed(3)}, F1 ${m.f1.toFixed(3)}`).join(' | ');}catch(e){message(e.message);}}
load(false);start();
