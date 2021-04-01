
import http

from aiohttp import web

from go_away.store.base import BaseDataTable
from go_away.core.get_ip import get_referrer_ip_address

YEAR_IN_SECS = 31556952


def get_redirect_view(table: BaseDataTable, default_redirect_location: str):
    async def redirect(request: web.Request) -> None:
        response = web.StreamResponse(
            status=int(http.HTTPStatus.TEMPORARY_REDIRECT),
            reason="Temporary Redirect",
        )

        try:
            raw_data = dict(request.query)

            if user_id := request.cookies.get("GoAwayUserId", None):
                raw_data["user_id"] = user_id

            raw_data["ip"] = get_referrer_ip_address(request)
            raw_data["user_agent"] = request.headers['user-agent']

            pk, data = table.split_pk_and_data(raw_data)
            response.set_cookie("GoAwayUserId", str(pk), max_age=YEAR_IN_SECS)

            await table.create_entry(data)
            response.headers["Location"] = data.redirect_to

        except (ValueError, KeyError):
            response.headers["Location"] = default_redirect_location

        response.content_type = "text/plain"
        response.content_length = 0

        await response.prepare(request)
        await response.write(b"\r\n")

    return redirect
