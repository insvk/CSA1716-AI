# ParkFlow setup guide

## Data flow
ESP32/Wokwi -> HTTPS `POST /api/ingest` -> Supabase PostgreSQL -> Supabase Realtime -> browser dashboard.

## 1. Requirements
Install Node.js LTS, Git and Vercel CLI (`npm install -g vercel`). Have a Supabase project and your Wokwi ESP32 project.

## 2. Supabase setup
1. Check whether tables with these names already exist. Do not run this schema blindly against an existing production database.
2. For a dedicated project, open Supabase SQL Editor and run `supabase/schema.sql`.
3. In Database > Publications, confirm the listed tables are in `supabase_realtime`.
4. Copy project URL and the public anon/publishable key from Supabase API settings.
5. The SQL policy grants public read access to telemetry for this demo. For a private facility, replace these with authenticated, role-based RLS policies before production.

## 3. Browser configuration
Copy `public/config.js.example` to `public/config.js`, then set `SUPABASE_URL` and the public anon/publishable key. Never put a service-role key or device token in browser config.

## 4. Server configuration
Create `.env` from `.env.example`; set `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and a long random `DEVICE_INGEST_TOKEN`. Add these three values to Vercel Project > Settings > Environment Variables. Do not commit `.env`.

Generate a token:
- PowerShell: `[Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))`
- macOS/Linux: `openssl rand -hex 32`

## 5. Local run
From this directory:
```bash
npm install
npx vercel login
npx vercel dev
```
Open the URL shown by Vercel CLI. Make sure `public/config.js` exists first.

## 6. Deploy
Push the repository to GitHub, import it in Vercel, add the server environment variables and deploy. Keep `public/config.js` private to your deployment workflow if you do not want the public project URL/key committed; remember the anon key is designed for browser use but still depends on correct RLS.

## 7. Test API from PowerShell
Replace the URL and token:
```powershell
$body = @{ device_id="manual-test"; slot_id="S1"; distance_cm=22.5; occupied=$true; sensor_ok=$true } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "https://YOUR-VERCEL-DOMAIN/api/ingest" -Headers @{ Authorization="Bearer YOUR_DEVICE_INGEST_TOKEN" } -ContentType "application/json" -Body $body
```
A successful response includes `ok: true`. Repeat for S1–S8 with fresh timestamps/readings. Dashboard counts are shown only when all eight readings are fresh (under 60 seconds).

## 8. Connect Wokwi
Follow `firmware/README.md`. Add Wi-Fi connection and HTTP POST calls to your existing sketch after occupancy state stabilization. The firmware helper is not a complete replacement for your existing sketch. Use the deployed API URL. Wokwi's common network is `Wokwi-GUEST` with no password; check current Wokwi network docs if connection fails.

## 9. Verify end-to-end
1. Open dashboard.
2. POST S1 with 20 cm and occupied=true. Confirm S1 changes in the dashboard.
3. POST S1 with 400 cm and occupied=false. Confirm S1 becomes available.
4. Send fresh readings for all eight slots. Confirm counts and utilization appear.
5. Stop sending readings. After 60 seconds the slots should become unknown/stale rather than being treated as available.
6. Check browser console, Vercel function logs and Supabase logs if anything fails.

## Important limitations
- Gate UI reads `gate_events`, but this starter does not yet send gate-state telemetry. Add a server-validated gate-event path and report actual state, not just servo commands.
- ML prediction is not trained or bundled. It is correctly shown as unavailable until a real model writes prediction records.
- Public-read RLS is demo-only. Use Supabase Auth and tight policies for private installations.
- A token embedded in firmware is demo-only, not strong production device identity.
- Add rate limiting, device identity, alerting and audit controls before public production.
- A physical gate needs local obstruction detection, emergency stop, manual override and a fail-safe design. Do not depend on cloud availability for safety.
- Shared TRIG is a Wokwi pin-saving shortcut; trigger physical ultrasonic sensors sequentially to reduce cross-talk.
- Physical HC-SR04 ECHO is typically 5V; use a voltage divider/level shifter for ESP32 inputs.

## Official docs
- Supabase Realtime: https://supabase.com/docs/guides/realtime
- Supabase RLS: https://supabase.com/docs/guides/database/postgres/row-level-security
- Vercel Functions: https://vercel.com/docs/functions
- Wokwi ESP32 Wi-Fi: https://docs.wokwi.com/guides/esp32-wifi
