class ServiceError(Exception):
    def __init__(self, message):
        self.message = message


class ValueExistError(ServiceError): ...
