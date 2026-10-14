document.querySelector('#login').addEventListener('submit',async event=>{
 event.preventDefault();
 const body=Object.fromEntries(new FormData(event.target));
 const response=await fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 const result=await response.json();
 if(response.ok) location.assign('/');
 else document.querySelector('#message').textContent=result.error;
});
