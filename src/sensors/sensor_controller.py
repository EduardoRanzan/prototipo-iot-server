from influxdb_client import Point, WritePrecision
from influxDB.influx_client import client_write_api, client_query_api, client_delete_api, get_bucket, get_org

bucket = get_bucket()
org = get_org()

def post_records(sensor, valor, timestamp):
    write_api = client_write_api()

    point = (
        Point("records")
        .tag("sensor", sensor)
        .field("valor", float(valor))
        .time(timestamp, WritePrecision.MS)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    print(f"INFLUXDB: Registros inseridos valor: {valor} timestamp {timestamp}")
    write_api.close()

def get_records(sensor, range):
    query_api = client_query_api()

    query = f'''
        from(bucket: "{bucket}")
        |> range(start: -{range})
        |> filter(fn: (r) => r._measurement == "records")
        |> filter(fn: (r) => r.sensor == "{sensor}")
    '''
    tables = query_api.query(query, org=org)
    
    result = []
    for table in tables:
        for record in table.records:
            result.append(record.get_value())
    return result

def delete_records(start, stop, sensor, valor=None):
    delete_api = client_delete_api()

    predicate = f'_measurement="records" AND sensor="{sensor}"'
    if valor is not None:
        predicate += f' AND valor={float(valor)}'

    delete_api.delete(start=start, stop=stop, predicate=predicate, bucket=bucket, org=org)
