from dataclasses import dataclass


@dataclass
class ExceptionResponse:
    message: str = "Произошла ошибка на сервере!"
