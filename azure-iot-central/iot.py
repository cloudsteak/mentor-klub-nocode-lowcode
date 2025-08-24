import os
import json
import math
import random
import signal
import sys
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from azure.iot.device import Message
from azure.iot.device import IoTHubDeviceClient, MethodResponse
from azure.iot.device import ProvisioningDeviceClient

# -- Config --
load_dotenv()
ID_SCOPE = os.getenv("IOTC_ID_SCOPE")
DEVICE_ID = os.getenv("IOTC_DEVICE_ID")
DEVICE_KEY = os.getenv("IOTC_DEVICE_KEY")
SEND_INTERVAL = int(os.getenv("SEND_INTERVAL_SEC", "5"))

if not all([ID_SCOPE, DEVICE_ID, DEVICE_KEY]):
    print("Hiányzó .env érték(ek): IOTC_ID_SCOPE, IOTC_DEVICE_ID, IOTC_DEVICE_KEY")
    sys.exit(1)

_stop = False
def handle_sigterm(signum, frame):
    global _stop
    _stop = True

signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)

def provision_with_dps(id_scope: str, device_id: str, device_key: str):
    """
    IoT Central → DPS (global.azure-devices-provisioning.net) → IoT Hub assignment.
    """
    dps_endpoint = "global.azure-devices-provisioning.net"
    dps_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=dps_endpoint,
        registration_id=device_id,
        id_scope=id_scope,
        symmetric_key=device_key,
    )
    registration_result = dps_client.register()
    if registration_result.status != "assigned":
        raise RuntimeError(f"DPS sikertelen: {registration_result.status}")
    assigned_hub = registration_result.registration_state.assigned_hub
    return assigned_hub

def create_iothub_client(hostname: str, device_id: str, device_key: str):
    return IoTHubDeviceClient.create_from_symmetric_key(
        hostname=hostname,
        device_id=device_id,
        symmetric_key=device_key,
    )

def generate_temperature(t: int, base=22.0):
    """
    Valószerű hőmérséklet:
    - Napi ciklus (sine)
    - Véletlen zaj
    - Lassan vándorló drift
    """
    # napi 24h szimuláció helyett gyorsabb ciklus a demóhoz
    sine = 2.0 * math.sin((t % 3600) / 3600 * 2 * math.pi)  # ~1h ciklus
    noise = random.uniform(-0.15, 0.15)
    drift = 0.002 * (t / 60.0) * math.sin(t / 120.0)  # lassú, kicsi elcsúszás
    return round(base + sine + noise + drift, 2)

def main():
    print("DPS provisioning…")
    hub = provision_with_dps(ID_SCOPE, DEVICE_ID, DEVICE_KEY)
    print(f"Assigned IoT Hub: {hub}")

    print("Connecting IoT Hub…")
    client = create_iothub_client(hub, DEVICE_ID, DEVICE_KEY)
    client.connect()
    print("Connected.")

    start = time.time()
    sent = 0

    # Opcionális: felhő → eszköz direct method példa (pl. mintavételezési intervallum módosítása)
    def handle_method(request):
        global SEND_INTERVAL
        if request.name == "setInterval":
            try:
                payload = request.payload or {}
                new_interval = int(payload.get("seconds", SEND_INTERVAL))
                SEND_INTERVAL = max(1, new_interval)
                resp = MethodResponse.create_from_method_request(
                    request, 200, {"status": "ok", "seconds": SEND_INTERVAL}
                )
            except Exception as e:
                resp = MethodResponse.create_from_method_request(
                    request, 400, {"error": str(e)}
                )
        else:
            resp = MethodResponse.create_from_method_request(
                request, 404, {"error": "unknown method"}
            )
        client.send_method_response(resp)

    client.on_method_request_received = handle_method

    print(f"Küldési intervallum: {SEND_INTERVAL}s. Leállítás: Ctrl+C")
    try:
        while not _stop:
            t = int(time.time() - start)
            temp = generate_temperature(t)

            payload = {
                "deviceId": DEVICE_ID,
                "temperature": temp,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            msg = Message(json.dumps(payload))
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"

            client.send_message(msg)
            sent += 1
            print(f"[{sent}] → {payload}")

            time.sleep(SEND_INTERVAL)
    finally:
        print("Disconnecting…")
        try:
            client.disconnect()
        except Exception:
            pass
        print("Bye.")

if __name__ == "__main__":
    main()
