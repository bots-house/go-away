
import os
from typing import Callable, TypeVar
from dataclasses import dataclass, field

T = TypeVar("T")


def _lazy_getenv(var: str, cast: Callable[[str], T], /) -> Callable[[], T]:
    def _func():
        try:
            return cast(os.environ[var])
        except (KeyError, ValueError):
            raise RuntimeError(f"Misconfiguration found for {var}")

    return _func


@dataclass(frozen=True)
class Config:
    redirect_to_default: str = field(
        default_factory=_lazy_getenv("REDIRECT_TO_DEFAULT", str),
    )

    db_dsn: str = field(
        default_factory=_lazy_getenv("DB_DSN", str),
    )

    host: str = field(
        default_factory=_lazy_getenv("HOST", str),
    )

    port: int = field(
        default_factory=_lazy_getenv("PORT", int),
    )
