
import asyncio
import logging
from typing import Callable, Awaitable

from aiohttp import web

from go_away.store.base import BaseDataTable
from go_away.core.config import Config
from go_away.web.views import (health, redirector)


def get_service_fn(hits_table: BaseDataTable, config: Config) -> Callable[[], Awaitable[None]]:
    app = web.Application()

    app.router.add_get(
        path="/",
        handler=redirector.get_redirect_view(hits_table, config.redirect_to_default),
        allow_head=False,
    )

    app.router.add_get(
        path="/health",
        handler=health.get_healthcheck_view(config.db_dsn),
        allow_head=False,
    )

    async def _idle():
        runner = web.AppRunner(app)

        await runner.setup()
        site = web.TCPSite(runner, config.host, config.port)
        await site.start()
        logging.info(
            f"Started background service on http://{config.host}:{config.port}",
        )

        while True:
            await asyncio.sleep(3600)  # sleep forever

    return _idle
