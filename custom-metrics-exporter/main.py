import asyncio
import logging
import sys

import metrics
from configuration import config
from prometheus_client import start_http_server


def setup_logging(level: int) -> None:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )


async def main() -> None:

    async def scrape(scrape_interval) -> None:
        asyncio.create_task(metrics.Metrics.run_all())
        await asyncio.sleep(scrape_interval)

    asyncio.create_task(scrape(config.scrape_interval))

    start_http_server(8000)

    while True:
        await asyncio.sleep(1000)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
