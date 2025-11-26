import json
from sensors.sensor_controller import post_records
from datetime import datetime

TOPICS = [("sensores/temperatura", 0), ("sensores/umidade", 0)]

def controller_on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("MOSQUITTO: Conectado ao broker!")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"MOSQUITTO: Inscrito no tópico: {topic}")
    else:
        print(f"MOSQUITTO: Falha na conexão, código {rc}")

def controller_on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode().strip()

        data = json.loads(payload)

        value = float(data["value"])
        timestamp_ms = int(data["ts"])

        sensor_type = msg.topic.split("/")[-1]

        post_records(sensor_type, value, timestamp_ms)

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
              f"MOSQUITTO: [{sensor_type}] Valor: {value} | Timestamp: {timestamp_ms}")

    except json.JSONDecodeError:
        print(f"MOSQUITTO: Payload inválido (não é JSON): {msg.payload}")
    except Exception as e:
        print(f"MOSQUITTO: Erro inesperado no processamento da mensagem: {e}")

