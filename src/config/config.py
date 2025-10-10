import os

class Config:
    INFLUX_URL = os.environ.get("INFLUX_URL")
    INFLUX_TOKEN = os.environ.get("INFLUX_TOKEN")
    INFLUX_ORG = os.environ.get("INFLUX_ORG")
    INFLUX_BUCKET = os.environ.get("INFLUX_BUCKET")

    MQTT_BROKER = os.environ.get("MOQ_BROKER")
    MQTT_PORT = int(os.environ.get("MOQ_PORT"))
