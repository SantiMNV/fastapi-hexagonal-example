class BaseAppException(Exception):
    def __init__(self, message: str, *, code: str = "application_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)
