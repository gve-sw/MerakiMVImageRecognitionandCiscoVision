import json
import requests
import time

import paho.mqtt.client as mqtt

from env_var import MERAKI_API_KEY
from img_reko import aws_img_recognition

# Meraki network settings
NETWORK_ID = ""
CAMERA_SERIAL = ""

# mqtt setting
MQTT_SERVER = ""
MQTT_PORT = ""
MQTT_TOPIC = "/merakimv/"+ CAMERA_SERIAL + "/0"

# motion trigger setting
MOTION_ALERT_PEOPLE_COUNT_THRESHOLD = 1

MOTION_ALERT_ITERATE_COUNT = 4

MOTION_ALERT_TRIGGER_PEOPLE_COUNT = 0

MOTION_ALERT_PAUSE_TIME = 15

_MONITORING_TRIGGERED = False

_MONITORING_MESSAGE_COUNT = 0

_MONITORING_PEOPLE_TOTAL_COUNT = 0


def collect_zone_information(topic, payload):
    parameters = topic.split("/")
    serial_number = parameters[2]

    # detect motion
    global _MONITORING_TRIGGERED, _MONITORING_MESSAGE_COUNT, _MONITORING_PEOPLE_TOTAL_COUNT

    # if motion monitoring triggered
    if _MONITORING_TRIGGERED:

        _MONITORING_MESSAGE_COUNT = _MONITORING_MESSAGE_COUNT + 1

        _MONITORING_PEOPLE_TOTAL_COUNT = _MONITORING_PEOPLE_TOTAL_COUNT + payload

        if _MONITORING_MESSAGE_COUNT > MOTION_ALERT_ITERATE_COUNT:

            if _MONITORING_PEOPLE_TOTAL_COUNT >= MOTION_ALERT_TRIGGER_PEOPLE_COUNT:

                # notification
                notify(serial_number)
                # pause
                time.sleep(MOTION_ALERT_PAUSE_TIME)

            # reset
            _MONITORING_MESSAGE_COUNT = 0

            _MONITORING_PEOPLE_TOTAL_COUNT = 0

            _MONITORING_TRIGGERED = False

    if payload >= MOTION_ALERT_PEOPLE_COUNT_THRESHOLD:
        _MONITORING_TRIGGERED = True

    print("payload : " + str(payload) +
          ", _MONITORING_TRIGGERED : " + str(_MONITORING_TRIGGERED) +
          ", _MONITORING_MESSAGE_COUNT : " + str(_MONITORING_MESSAGE_COUNT) +
          ", _MONITORING_PEOPLE_TOTAL_COUNT : " + str(_MONITORING_PEOPLE_TOTAL_COUNT))

def notify(serial_number):
    url = "https://api.meraki.com/api/v0/networks/{1}/cameras/{0}/snapshot".format(serial_number, NETWORK_ID)
    ts = str(time.time()).split(".")[0] + "000"
    #querystring = {"timestamp": ts}

    headers = {
       'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
        "Content-Type": "application/json"
    }
    resp = requests.post(url, headers=headers, json={})
    r = json.loads(resp.text)

    snapshot = str(r["url"])
    url = snapshot.replace(" ", "")

    snapshot_file = "sample_image.png"

    for i in range (0,10):
        resp = requests.get(url, allow_redirects=True)
        if int(resp.status_code /100) ==2:
            with open(snapshot_file, 'wb') as f:
                for chunk in resp:
                    f.write(chunk)
            print('Took a Snapshot, sending to AWS')
            aws_img_recognition(snapshot_file)
            break

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))
    payload = payload["counts"]["person"]
    collect_zone_information(msg.topic, payload)

if __name__ == "__main__":

    MQTT_TOPIC = "/merakimv/"+ CAMERA_SERIAL + "/0"

    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        client.loop_forever()

    except Exception as ex:
        print("[MQTT]failed to connect or receive msg from mqtt, due to: \n {0}".format(ex))
