
import http

from aiohttp import web
from asyncpg import connect, Connection, exceptions


def get_healthcheck_view(db_dsn: str):
    async def healthcheck(_: web.Request) -> web.Response:
        status = int(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        once_failed = False

        try:
            conn = await connect(db_dsn)  # type: Connection
            await conn.execute("select 1;")
            response = "db:ok;"
        except exceptions.PostgresError as err:
            once_failed = True
            response = f"db:{err!s};"

        if not once_failed:
            status = int(http.HTTPStatus.OK)

        return web.Response(status=status, body=response)

    return healthcheck
