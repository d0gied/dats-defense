from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
from ..config import Config

class MetricsClient:
    def __init__(
        self, host: str, port: int
    ):
        self.metrics_server = InfluxDBClient(
            url=f"http://{host}:{port}", token=Config.Metrics.INFLUXDB_TOKEN, org="zombiedef"
        )
        self.bucket = "zombiedef"

    async def push_rate(self, measurement: str, fields: dict[str, str], tags: dict[str, str]):
        point = Point(measurement)
        for key, value in tags.items():
            point = point.tag(key, value)
        for key, value in fields.items():
            point = point.field(key, value)
        self.metrics_server.write_api(write_options=ASYNCHRONOUS).write(bucket=self.bucket, record=point)
