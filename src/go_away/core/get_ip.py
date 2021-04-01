
from typing import Optional

from aiohttp.web import Request


def get_referrer_ip_address(request: Request) -> Optional[str]:
    if forwarded_for := request.headers.get('X-Forwarded-For'):
        return forwarded_for

    if forwarded_for := request.headers.get('Forwarded'):
        return forwarded_for

    peer_name = request.transport.get_extra_info('peername')
    if peer_name is not None:
        host, _ = peer_name
        return host

    return request.remote
