from typing import Protocol

from structlog import get_logger

from main_service.app.domain.bond import Bond

logger = get_logger()


class BondRepoInterface(Protocol):
    def get(self, name: str):
        ...

    def add(self, entity: Bond):
        ...


class BondRepoDatabase:
    def get(self, name: str):
        logger.info(f"get bond with name {name}")

    def add(self, entity: Bond):
        logger.info(f"add bond with name {entity.name}")
