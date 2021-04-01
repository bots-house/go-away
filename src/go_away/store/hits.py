
from typing import Optional, Tuple

import uuid
import ipaddress
import datetime
from dataclasses import dataclass
from functools import cached_property

from asyncpg import Connection

from go_away.store.base import BaseDataTable


@dataclass(frozen=True)
class HitData:
    """
    id: unique identifier of a hit

    user_id: generated UUID hit for cookies
    """

    at: datetime.datetime

    redirect_to: str
    redirect_from: str

    user_id: uuid.UUID
    ip: ipaddress.IPv4Address
    user_agent: Optional[str]

    other_params: Optional[str]


class HitsTable(BaseDataTable[uuid.UUID, HitData]):
    table_name = "hits"

    async def create_entry(self, data: HitData) -> None:
        async with self.pool.acquire() as conn:  # type: Connection
            await conn.execute(
                self.create_statement,
                data.at,
                data.redirect_to,
                data.redirect_from,
                data.user_id,
                data.ip,
                data.user_agent,
                data.other_params,
            )

    @cached_property
    def create_statement(self) -> str:
        return f"""
        insert into "{self.table_name}" (
            at, redirect_to, redirect_from, user_id, ip, user_agent, other_params
        ) values ($1, $2, $3, $4, $5, $6, $7);
        """

    def split_pk_and_data(self, raw_data: dict) -> Tuple[uuid.UUID, HitData]:
        try:
            _data = {
                "redirect_to": raw_data["to"],
                "redirect_from": raw_data["from"],
                "ip": raw_data["ip"],
                "user_agent": raw_data["user_agent"],
                "at": datetime.datetime.utcnow(),
            }
        except KeyError:
            raise ValueError

        try:
            user_id = uuid.UUID(raw_data["user_id"])
        except (ValueError, KeyError):
            user_id = uuid.uuid4()

        other_params = {
            key: raw_data[key]
            for key in raw_data
            if key not in _data
        }

        _data["other_params"] = other_params
        _data["user_id"] = user_id

        return user_id, HitData(**_data)