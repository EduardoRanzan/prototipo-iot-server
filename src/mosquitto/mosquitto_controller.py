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
        sensor_type = msg.topic.split("/")[-1]

        value = float(msg.payload.decode().strip())

        post_records(sensor_type, value)

        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} MOSQUITTO: [{sensor_type}] Valor recebido: {value}")
    except ValueError as e:
        print(f"MOSQUITTO: Erro ao converter payload de {msg.topic}: {e}")
    except Exception as e:
        print(f"MOSQUITTO: Erro inesperado no processamento da mensagem: {e}")
