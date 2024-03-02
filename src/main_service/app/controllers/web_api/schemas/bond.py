from dataclasses import dataclass


@dataclass
class BondCreateRequest:
    name: str


@dataclass
class BondCreateResponse:
    name: str
