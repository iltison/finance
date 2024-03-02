import sys
from dataclasses import dataclass, field
from typing import Any, Protocol


class Command(Protocol):
    """Абстрактный класс для всех команд"""


@dataclass
class CommandResult:
    """Абстрактный класс результатов"""

    result: Any = None
    errors: list[Any] = field(default_factory=list)

    @classmethod
    def ok(cls, result=None) -> "CommandResult":
        """Успешный результат"""
        return cls(result=result)

    @classmethod
    def failed(cls, message="Failure", exception=None) -> "CommandResult":
        """Неуспешный результат"""
        exception_info = sys.exc_info()
        errors = [(message, exception, exception_info)]
        return cls(errors=errors)
