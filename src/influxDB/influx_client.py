from influxdb_client import InfluxDBClient
from config.config import Config


url = Config.INFLUX_URL
token = Config.INFLUX_TOKEN
org = Config.INFLUX_ORG
bucket = Config.INFLUX_BUCKET

client = InfluxDBClient(url=url, token=token, org=org)

def client_write_api():
    return client.write_api()

def client_query_api():
    return client.query_api()

def client_delete_api():
    return client.delete_api()

def get_bucket():
    return bucket

def get_org():
    return org