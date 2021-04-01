
import asyncio
import logging

from go_away.core.config import Config
from go_away.core.init_db import make_tables
from go_away.store.hits import HitsTable
from go_away.web.app import get_service_fn


logging.basicConfig(
    level=logging.DEBUG if __debug__ else logging.INFO,
    format="%(levelname)-5s %(asctime)s %(name)s: %(message)s",
)


async def main():
    config = Config()

    hits_table, = await make_tables(config, (HitsTable,))

    fn = get_service_fn(hits_table, config)
    await fn()


if __name__ == '__main__':
    asyncio.run(main())
