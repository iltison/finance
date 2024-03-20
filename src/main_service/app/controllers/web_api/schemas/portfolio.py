import uuid
from dataclasses import dataclass


@dataclass
class PortfolioGetRequest:
    id: uuid.UUID


@dataclass
class PortfolioGetResponse:
    id: uuid.UUID
    name: str
