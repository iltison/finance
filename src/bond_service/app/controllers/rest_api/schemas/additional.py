from dataclasses import dataclass


@dataclass
class ExceptionResponse:
    message: str = "Произошла ошибка на сервере!"


@dataclass
class NotFoundResponse:
    message: str = "Запрашиваемый ресурс не найден"
