-- Review before running on any existing project. Intended as a starter schema.
create table if not exists public.parking_slots(
 slot_id text primary key check(slot_id in('S1','S2','S3','S4','S5','S6','S7','S8')),
 device_id text,distance_cm double precision,occupied boolean,sensor_ok boolean not null default true,updated_at timestamptz
);
create table if not exists public.sensor_readings(
 id bigint generated always as identity primary key,device_id text not null,
 slot_id text not null check(slot_id in('S1','S2','S3','S4','S5','S6','S7','S8')),
 distance_cm double precision not null,occupied boolean not null,sensor_ok boolean not null default true,
 recorded_at timestamptz not null default now()
);
create index if not exists sensor_readings_time_idx on public.sensor_readings(recorded_at desc);
create table if not exists public.parking_events(
 id bigint generated always as identity primary key,device_id text,slot_id text,event_type text not null,details text,recorded_at timestamptz not null default now()
);
create index if not exists parking_events_time_idx on public.parking_events(recorded_at desc);
create table if not exists public.gate_events(
 id bigint generated always as identity primary key,device_id text not null,state text not null check(state in('open','closed','fault','unknown')),recorded_at timestamptz not null default now()
);
create table if not exists public.occupancy_snapshots(
 id bigint generated always as identity primary key,occupied_count integer not null check(occupied_count between 0 and 8),
 available_count integer not null check(available_count between 0 and 8),utilization_percent double precision not null check(utilization_percent between 0 and 100),recorded_at timestamptz not null default now()
);
create table if not exists public.parking_predictions(
 id bigint generated always as identity primary key,model_name text not null,model_version text not null,slot_id text,
 horizon_minutes integer not null check(horizon_minutes in(15,30)),availability_probability double precision not null check(availability_probability between 0 and 1),
 predicted_for timestamptz not null,created_at timestamptz not null default now(),metrics jsonb
);
-- Read-only anonymous telemetry is suitable only for a public demo. Tighten policies for private facilities.
do $$ declare t text; begin
 foreach t in array array['parking_slots','sensor_readings','parking_events','gate_events','occupancy_snapshots','parking_predictions'] loop
  execute format('alter table public.%I enable row level security',t);
  execute format('grant select on public.%I to anon, authenticated',t);
  execute format('drop policy if exists public_read_demo on public.%I',t);
  execute format('create policy public_read_demo on public.%I for select to anon, authenticated using (true)',t);
 end loop;
end $$;
-- Enable these tables under Database > Publications > supabase_realtime if not already enabled.
alter publication supabase_realtime add table public.parking_slots;
alter publication supabase_realtime add table public.sensor_readings;
alter publication supabase_realtime add table public.parking_events;
alter publication supabase_realtime add table public.gate_events;
alter publication supabase_realtime add table public.occupancy_snapshots;
