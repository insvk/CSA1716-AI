import { createClient } from "@supabase/supabase-js";
const slots=new Set(["S1","S2","S3","S4","S5","S6","S7","S8"]);
const send=(res,status,data)=>res.status(status).setHeader("Content-Type","application/json").send(JSON.stringify(data));
export default async function handler(req,res){
 if(req.method!=="POST"){res.setHeader("Allow","POST");return send(res,405,{error:"POST required"});}
 const token=process.env.DEVICE_INGEST_TOKEN,url=process.env.SUPABASE_URL,key=process.env.SUPABASE_SERVICE_ROLE_KEY;
 if(!token||!url||!key)return send(res,500,{error:"Server environment variables missing"});
 if(req.headers.authorization!==`Bearer ${token}`)return send(res,401,{error:"Unauthorized"});
 const b=req.body;if(!b||typeof b!=="object"||Array.isArray(b))return send(res,400,{error:"JSON object required"});
 const device_id=String(b.device_id||"").trim(),slot_id=String(b.slot_id||"").toUpperCase(),distance_cm=Number(b.distance_cm),occupied=b.occupied,sensor_ok=b.sensor_ok!==false,dt=b.recorded_at?new Date(b.recorded_at):new Date();
 if(!device_id||device_id.length>80||!slots.has(slot_id)||!Number.isFinite(distance_cm)||distance_cm<0||distance_cm>1000||typeof occupied!=="boolean"||!Number.isFinite(dt.getTime())||Math.abs(Date.now()-dt.getTime())>300000)return send(res,400,{error:"Invalid device_id, slot_id, distance_cm, occupied or recorded_at"});
 const supabase=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false}}),recorded_at=dt.toISOString();
 const {error:e1}=await supabase.from("sensor_readings").insert({device_id,slot_id,distance_cm,occupied,sensor_ok,recorded_at});
 if(e1)return send(res,500,{error:"Sensor reading save failed",detail:e1.message});
 const {data:old}=await supabase.from("parking_slots").select("occupied").eq("slot_id",slot_id).maybeSingle();
 const {error:e2}=await supabase.from("parking_slots").upsert({slot_id,device_id,distance_cm,occupied,sensor_ok,updated_at:recorded_at},{onConflict:"slot_id"});
 if(e2)return send(res,500,{error:"Current slot update failed",detail:e2.message});
 if(!old||old.occupied!==occupied){const {error}=await supabase.from("parking_events").insert({device_id,slot_id,event_type:occupied?"vehicle_detected":"slot_freed",details:`Distance ${distance_cm.toFixed(1)} cm`,recorded_at});if(error)console.error(error.message);}
 if(slot_id==="S8"){const {data:all}=await supabase.from("parking_slots").select("occupied,sensor_ok,updated_at");if(all?.length===8&&all.every(s=>s.sensor_ok&&s.occupied!==null&&Date.now()-new Date(s.updated_at).getTime()<120000)){const n=all.filter(s=>s.occupied).length;const {error}=await supabase.from("occupancy_snapshots").insert({occupied_count:n,available_count:8-n,utilization_percent:n/8*100,recorded_at});if(error)console.error(error.message);}}
 return send(res,200,{ok:true,slot_id,recorded_at});
}
