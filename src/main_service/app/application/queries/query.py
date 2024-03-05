import sys
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class QueryResult(Protocol):
    """Базовый класс запросов"""

    payload: Any = None
    errors: list[Any] = field(default_factory=list)

    @classmethod
    def failure(cls, message="Failure", exception=None) -> "QueryResult":
        """Creates a failed result"""
        exception_info = sys.exc_info()
        errors = [(message, exception, exception_info)]
        result = cls(errors=errors)
        return result

    @classmethod
    def success(cls, payload=None) -> "QueryResult":
        """Creates a successful result"""
        return cls(payload=payload)
