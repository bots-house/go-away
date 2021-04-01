
from typing import Generic, TypeVar, Tuple

from asyncpg import Pool

Pk = TypeVar("Pk")
DataT = TypeVar("DataT")


class BaseDataTable(Generic[Pk, DataT]):
    data: DataT
    pk: Pk
    table_name: str

    async def get_entry(self, pk: Pk) -> DataT:
        pass

    async def create_entry(self, data: DataT) -> None:
        pass

    async def update_entry(self, pk: Pk, data: DataT) -> None:
        pass

    async def migrate(self) -> None:
        pass

    def split_pk_and_data(self, raw_data: dict) -> Tuple[Pk, DataT]:
        pass

    def __init__(self, pool: 'Pool'):
        self.pool = pool
