# ESP32 / Wokwi integration

Keep your existing sensor/OLED/LED/servo logic. Add Wi-Fi and HTTPS POST after each slot's stable state is calculated. Endpoint: `https://YOUR-VERCEL-DOMAIN/api/ingest`.

Payload:
```json
{"device_id":"wokwi-esp32-01","slot_id":"S1","distance_cm":23.4,"occupied":true,"sensor_ok":true}
```
Headers: `Content-Type: application/json` and `Authorization: Bearer YOUR_DEVICE_INGEST_TOKEN`.

Helper (adapt to your existing sketch):
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
const char* WIFI_SSID = "Naresh";
const char* WIFI_PASSWORD = "9597asdf";
const char* API_URL = "https://YOUR-VERCEL-DOMAIN/api/ingest";
const char* DEVICE_TOKEN = "bcce6aa050a30a3e94542d64c064d4541c401408ea4112268d2b22449aedae6";

void connectParkingWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long start=millis();
  while(WiFi.status()!=WL_CONNECTED && millis()-start<15000) delay(250);
}
void postSlotReading(const char* slotId,float cm,bool occupied) {
  if(WiFi.status()!=WL_CONNECTED)return;
  HTTPClient http; http.begin(API_URL);
  http.addHeader("Content-Type","application/json");
  http.addHeader("Authorization",String("Bearer ")+DEVICE_TOKEN);
  String body="{\"device_id\":\"wokwi-esp32-01\",\"slot_id\":\""+String(slotId)+"\",\"distance_cm\":"+String(cm,1)+",\"occupied\":"+(occupied?"true":"false")+",\"sensor_ok\":true}";
  int code=http.POST(body); Serial.printf("POST %s -> %d\\n",slotId,code); http.end();
}
```
Call `connectParkingWiFi()` in setup and `postSlotReading("S1", distance, occupied)` for each slot at a sensible interval (e.g. 5–10 seconds) or when a stable occupancy transition occurs. Repeat for S1–S8. Do not post every raw reading. Replace placeholders with your deployed URL and token.

**Security:** embedding a shared bearer token in firmware is demo-only. Use per-device credentials/signatures for production. Physical HC-SR04 ECHO is typically 5V; use a divider/level shifter because ESP32 GPIO is not 5V tolerant. Trigger sensors sequentially in physical hardware to reduce ultrasonic cross-talk. Do not disable TLS verification in production.
