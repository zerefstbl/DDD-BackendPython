class InvalidUuidException(Exception):
    def __init__(self, error: str = 'ID must be a valid UUID') -> None:
        super().__init__(error)


class DomainException(Exception):
    def __init__(self, error: str = 'Name os description must be provided') -> None:
        super().__init__(error)


class ValidationException(Exception):
    pass
