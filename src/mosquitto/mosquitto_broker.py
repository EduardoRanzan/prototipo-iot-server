import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from .mosquitto_controller import controller_on_connect, controller_on_message

load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))

def start():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = controller_on_connect
    client.on_message = controller_on_message
    client.on_disconnect = on_disconnect

    while True:
        try:
            print(f"MOSQUITTO: Tentando conectar em {BROKER}:{PORT} ...")
            client.connect(BROKER, PORT, keepalive=60)
            break
        except Exception as e:
            print(f"MOSQUITTO: Falha ao conectar: {e}. Nova tentativa em 5 s...")
            time.sleep(5)

    client.loop_start()

    while True:
        time.sleep(1)


def on_disconnect(client, userdata, flags, rc, properties):
    print(f"MOSQUITTO: Desconectado! rc={rc}")

    while True:
        print("MOSQUITTO: Tentando reconectar...")
        try:
            client.reconnect()
            return
        except Exception as e:
            print(f"MOSQUITTO: Falha ao reconectar: {e}")
            time.sleep(5)
