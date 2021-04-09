
import http

import yarl
from aiohttp import web

from go_away.store.hits import HitsTable
from go_away.core.get_ip import get_referrer_ip_address

YEAR_IN_SECS = 31556952


def get_redirect_view(table: HitsTable, default_redirect_location: str):
    async def redirect(request: web.Request) -> None:
        response = web.StreamResponse(
            status=int(http.HTTPStatus.TEMPORARY_REDIRECT),
            reason="Temporary Redirect",
        )

        try:
            original_query = dict(request.query)
            query_mut = original_query.copy()

            if user_id := request.cookies.get("GoAwayUserId", None):
                query_mut["user_id"] = user_id

            query_mut["ip"] = get_referrer_ip_address(request)
            query_mut["user_agent"] = request.headers['user-agent']

            pk, data = table.split_pk_and_data(query_mut)
            response.set_cookie("GoAwayUserId", str(pk), max_age=YEAR_IN_SECS)

            await table.create_entry(data)
            response.headers["Location"] = str(
                yarl
                .URL(data.redirect_to)
                .update_query(data.other_params_to_python())
            )

        except (ValueError, KeyError):
            response.headers["Location"] = default_redirect_location

        response.content_type = "text/plain"
        response.content_length = 0

        await response.prepare(request)
        await response.write(b"\r\n")

    return redirect
