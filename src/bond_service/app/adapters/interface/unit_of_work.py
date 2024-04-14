from typing import Protocol

import structlog

logger = structlog.get_logger(__name__)


class UOWInterface(Protocol):
    async def __aenter__(self) -> "UOWInterface": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
