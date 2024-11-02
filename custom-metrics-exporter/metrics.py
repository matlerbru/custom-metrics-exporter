import typing

from configuration import config
from prometheus_client import Gauge
from ssh import SSH


class Metrics:
    _metrics: list[typing.Callable] = []

    @staticmethod
    def add_metric(function: typing.Callable) -> None:
        Metrics._metrics.append(function)

    @staticmethod
    async def run_all() -> None:
        for metric in Metrics._metrics:
            await metric()


directory_usage_gauge = Gauge(
    "directory_usage_bytes", "Directory usage in bytes", ["host", "path", "directory"]
)


@Metrics.add_metric
async def directory_usage():
    for path in config.directory_usage:
        client = SSH(path.host, path.username, path.password)
        result = client.execute_command(f"du -sb {path.path}/*")

        for line in result.stdout.strip().split("\n"):
            columns = line.split("\t/")
            value = columns[0]
            labels = {}
            labels.update(
                {
                    "host": path.host,
                    "path": "/".join(columns[1].split("/")[0:-1]),
                    "directory": columns[1].split("/")[-1],
                }
            )
            directory_usage_gauge.labels(
                host=labels["host"], path=labels["path"], directory=labels["directory"]
            ).set(int(value))
