class DomainError(Exception):
    """Base class for domain errors"""
    
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)