class GeneratedCodeError(Exception):
    def __init__(self, message: str, **kwargs):
        super().__init__(message)
        self.name = 'GeneratedCodeError'
        self.message = message
        self.extra = kwargs
