
from typing import Type, Tuple

from asyncpg.pool import create_pool

from go_away.store.base import BaseDataTable
from go_away.core.config import Config


async def make_tables(
    config: Config,
    table_clss: Tuple[Type[BaseDataTable], ...],
) -> Tuple[BaseDataTable, ...]:
    shared_pool = await create_pool(config.db_dsn, min_size=3, max_size=3)

    return tuple(table_cls(shared_pool) for table_cls in table_clss)
