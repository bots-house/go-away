
import http

from aiohttp import web

from go_away.store.base import BaseDataTable


def get_redirect_view(table: BaseDataTable, default_redirect_location: str):
    async def redirect(request: web.Request) -> None:
        response = web.StreamResponse(
            status=int(http.HTTPStatus.TEMPORARY_REDIRECT),
            reason="Temporary Redirect",
        )

        try:
            raw_data = dict(request.query)

            if user_id := request.cookies.get("User-Id", None):
                raw_data["user_id"] = user_id

            pk, data = table.split_pk_and_data(raw_data)
            response.set_cookie("User-Id", str(pk), max_age=31556952)

            await table.create_entry(data)
            response.headers["Location"] = data.redirect_to

        except (ValueError, KeyError):
            response.headers["Location"] = default_redirect_location

        response.content_type = "text/plain"
        response.content_length = 0

        await response.prepare(request)
        await response.write(b"\r\n")

    return redirect
