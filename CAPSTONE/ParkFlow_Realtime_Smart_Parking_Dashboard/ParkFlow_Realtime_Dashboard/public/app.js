import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm";
const $=id=>document.getElementById(id), IDS=Array.from({length:8},(_,i)=>`S${i+1}`), STALE=60000;
let db=null,slots=new Map(),events=[],history=[],gate=null,lastAt=null,channel=null;
const date=v=>v&&Number.isFinite(new Date(v).getTime())?new Date(v):null;
const ago=v=>{const d=date(v);if(!d)return "No reading";const s=Math.max(0,Math.floor((Date.now()-d)/1000));return s<5?"Just now":s<60?`${s}s ago`:s<3600?`${Math.floor(s/60)}m ago`:`${Math.floor(s/3600)}h ago`};
const fresh=s=>!!(s&&s.occupied!==null&&s.sensor_ok!==false&&date(s.updated_at)&&Date.now()-date(s.updated_at)<=STALE);
const state=s=>!fresh(s)?"stale":s.occupied?"occupied":"available";
function health(id,val){$(id).textContent=val}
function toast(t){$("toast").textContent=t;$("toast").classList.add("show");setTimeout(()=>$("toast").classList.remove("show"),3000)}
function render(){
 $("slots").innerHTML="";
 IDS.forEach(id=>{const s=slots.get(id),st=state(s),dist=s?.distance_cm==null?"—":`${Number(s.distance_cm).toFixed(1)}<small> cm</small>`;
 const el=document.createElement("article");el.className=`slot ${st}`;
 el.innerHTML=`<div class="slottop"><b>${id}</b><span class="badge">${st==="stale"?"Unknown":st==="occupied"?"Occupied":"Available"}</span></div><div class="distance">${dist}</div><div class="slotmeta"><span>${s?.sensor_ok===false?"Sensor fault":st==="stale"?"Stale / no data":"Sensor online"}</span><span>${ago(s?.updated_at)}</span></div>`;
 $("slots").append(el)});
 const known=IDS.map(id=>slots.get(id)).filter(fresh),all=known.length===8,occ=known.filter(s=>s.occupied).length,free=known.filter(s=>!s.occupied).length;
 $("free").innerHTML=all?`${free} <small>/ 8</small>`:"— <small>/ 8</small>";$("occupied").innerHTML=all?`${occ} <small>/ 8</small>`:"— <small>/ 8</small>";
 $("util").textContent=all?`${Math.round(occ/8*100)}%`:"—";$("utilBar").style.width=all?`${occ/8*100}%`:"0%";
 $("freeSub").textContent=all?`${free} confirmed available`:`${known.length}/8 fresh readings`;$("occSub").textContent=all?`${occ} confirmed occupied`:"Waiting for fresh readings";$("utilSub").textContent=all?"Based on current confirmed states":"Requires all eight fresh readings";
 const gateFresh=gate&&date(gate.recorded_at)&&Date.now()-date(gate.recorded_at)<=STALE;
 $("gate").textContent=gateFresh?String(gate.state).toUpperCase():"UNKNOWN";$("gate").style.color=gateFresh?(gate.state==="open"?"var(--mint)":"var(--red)"):"var(--muted)";
 $("gateSub").textContent=gateFresh?`Updated ${ago(gate.recorded_at)}`:"No fresh gate event";
 $("lastUpdate").textContent=lastAt?new Date(lastAt).toLocaleTimeString():"Waiting for telemetry";
 $("deviceStatus").textContent=lastAt&&Date.now()-new Date(lastAt).getTime()<=STALE?"ESP32 connected":"Device offline / waiting";
 $("deviceSeen").textContent=lastAt?`Last data ${ago(lastAt)}`:"No telemetry yet";$("deviceDot").classList.toggle("online",!!(lastAt&&Date.now()-new Date(lastAt).getTime()<=STALE));
 $("banner").className="banner"+(all?" good":known.length?" warn":"");$("banner").innerHTML=all?"<b>✓ &nbsp; Live occupancy data received</b><p>All eight slots have fresh confirmed readings from the cloud database.</p>":`<b>ⓘ &nbsp; ${known.length?"Partial sensor data":"Awaiting real sensor data"}</b><p>${known.length} of 8 slots have fresh readings. Unknown/stale sensors are not counted as available.</p>`;
 const candidates=IDS.map(id=>slots.get(id)).filter(s=>fresh(s)&&s.occupied===false).sort((a,b)=>(b.distance_cm??-1)-(a.distance_cm??-1));
 $("best").textContent=candidates[0]?.slot_id||"—";$("reason").textContent=candidates.length?`Fresh available slot; greatest measured distance (${Number(candidates[0].distance_cm).toFixed(1)} cm).`:"No fresh confirmed available slot.";
 $("prediction").textContent="Not available — connect a trained and validated ML model.";
 $("eventList").innerHTML=events.length?events.slice(0,8).map(e=>`<div class="event"><b>${String(e.event_type||"parking event").replaceAll("_"," ")}</b><span>${[e.slot_id,e.details,ago(e.recorded_at)].filter(Boolean).join(" · ")}</span></div>`).join(""):"No saved events yet.";
 health("dbHealth","Connected");health("espHealth",lastAt?ago(lastAt):"Waiting");health("historyHealth",history.length?`${history.length} records`:"No history yet");
 drawChart();$("mode").textContent="Cloud-connected";
}
function drawChart(){
 const c=$("chart"),ctx=c.getContext("2d"),r=c.getBoundingClientRect(),dpr=devicePixelRatio||1;c.width=Math.max(1,r.width*dpr);c.height=200*dpr;ctx.scale(dpr,dpr);ctx.clearRect(0,0,r.width,200);
 const pts=history.filter(x=>Number.isFinite(Number(x.occupied_count))).slice(-24);$("chartEmpty").style.display=pts.length>1?"none":"block";if(pts.length<2)return;
 const w=r.width,h=170,p={l:25,r:8,t:12,b:15},cw=w-p.l-p.r,ch=h-p.t-p.b;
 ctx.strokeStyle=getComputedStyle(document.body).getPropertyValue("--line");ctx.fillStyle=getComputedStyle(document.body).getPropertyValue("--muted");ctx.font="10px DM Sans";
 for(let i=0;i<=4;i++){let y=p.t+ch*i/4;ctx.beginPath();ctx.moveTo(p.l,y);ctx.lineTo(w-p.r,y);ctx.stroke();ctx.fillText(String(8-i*2),3,y+3)}
 const x=i=>p.l+i*cw/(pts.length-1),y=v=>p.t+ch-(Math.max(0,Math.min(8,Number(v)))/8)*ch;
 ctx.beginPath();pts.forEach((q,i)=>i?ctx.lineTo(x(i),y(q.occupied_count)):ctx.moveTo(x(i),y(q.occupied_count)));ctx.strokeStyle="#5de0bb";ctx.lineWidth=2.5;ctx.stroke();
}
async function load(){
 const results=await Promise.all([
 db.from("parking_slots").select("slot_id,occupied,distance_cm,updated_at,device_id,sensor_ok"),
 db.from("sensor_readings").select("slot_id,occupied,distance_cm,recorded_at,device_id,sensor_ok").order("recorded_at",{ascending:false}).limit(8),
 db.from("parking_events").select("event_type,slot_id,details,recorded_at").order("recorded_at",{ascending:false}).limit(8),
 db.from("gate_events").select("state,recorded_at").order("recorded_at",{ascending:false}).limit(1),
 db.from("occupancy_snapshots").select("occupied_count,recorded_at").order("recorded_at",{ascending:false}).limit(24)
 ]);
 const [sr,rr,er,gr,hr]=results;for(const res of results)if(res.error)throw res.error;
 (sr.data||[]).forEach(s=>slots.set(s.slot_id,s));
 (rr.data||[]).forEach(r=>{const s={...r,updated_at:r.recorded_at};if(!slots.has(s.slot_id)||new Date(s.updated_at)>new Date(slots.get(s.slot_id).updated_at||0))slots.set(s.slot_id,s);if(!lastAt||new Date(r.recorded_at)>new Date(lastAt))lastAt=r.recorded_at});
 events=er.data||[];gate=gr.data?.[0]||null;history=(hr.data||[]).reverse();render();
}
async function init(){
 const url=window.SUPABASE_URL,key=window.SUPABASE_ANON_KEY;
 if(!url||!key||url.includes("YOUR_PROJECT")||key.includes("YOUR_SUPABASE")){$("connection").textContent="● Setup required";health("dbHealth","Not configured");health("rtHealth","Not configured");$("mode").textContent="Configuration required";return}
 try{
 db=createClient(url,key);await load();channel=db.channel("parkflow-live")
 .on("postgres_changes",{event:"*",schema:"public",table:"parking_slots"},p=>{if(p.new?.slot_id)slots.set(p.new.slot_id,p.new);render()})
 .on("postgres_changes",{event:"INSERT",schema:"public",table:"sensor_readings"},p=>{const r=p.new,s={...r,updated_at:r.recorded_at};if(s.slot_id)slots.set(s.slot_id,s);if(!lastAt||new Date(s.updated_at)>new Date(lastAt))lastAt=s.updated_at;render()})
 .on("postgres_changes",{event:"INSERT",schema:"public",table:"parking_events"},p=>{events.unshift(p.new);events=events.slice(0,8);render()})
 .on("postgres_changes",{event:"INSERT",schema:"public",table:"gate_events"},p=>{gate=p.new;render()})
 .on("postgres_changes",{event:"INSERT",schema:"public",table:"occupancy_snapshots"},p=>{history.push(p.new);history=history.slice(-24);render()})
 .subscribe(status=>{const ok=status==="SUBSCRIBED";$("connection").textContent=ok?"● Realtime connected":`● ${status}`;$("connection").classList.toggle("ok",ok);health("rtHealth",status);});
 }catch(e){console.error(e);$("connection").textContent="● Connection error";health("dbHealth","Error");health("rtHealth","Not connected");$("banner").innerHTML="<b>Cloud connection failed</b><p>Check browser console, Supabase config, SQL schema, grants and Realtime publication.</p>";toast("Could not load cloud data. Check configuration.");}
}
$("theme").onclick=()=>document.body.classList.toggle("light");
$("refresh").onclick=async()=>{if(!db)return toast("Configure Supabase first");try{const {data,error}=await db.from("parking_events").select("event_type,slot_id,details,recorded_at").order("recorded_at",{ascending:false}).limit(8);if(error)throw error;events=data||[];render();toast("Events refreshed");}catch(e){toast(e.message)}};
window.addEventListener("resize",drawChart);setInterval(render,10000);init();
