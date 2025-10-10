import time
import paho.mqtt.client as mqtt
from .mosquitto_controller import controller_on_connect, controller_on_message
from config.config import Config

BROKER = Config.MQTT_BROKER
PORT = Config.MQTT_PORT


def start():
    # isso aqui mudou minha vida, simplesmente incrivel, ele mostra todos os logs q um ser humano precisa para trabalah com isso
    # def on_log(client, userdata, level, buf):
    #     print("LOG:", buf)
    # client.on_log = lambda c,u,l,s: print("LOG:", s)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = controller_on_connect
    client.on_message = controller_on_message

    while True:
        try:
            print(f"MOSQUITTO: Tentando conectar em {BROKER}:{PORT} ...")
            client.connect(BROKER, PORT, keepalive=60)
            break
        except Exception as e:
            print(f"MOSQUITTO: Falha ao conectar: {e}. Nova tentativa em 5 s...")
            time.sleep(5)

    client.loop_forever(retry_first_connection=True)
