"""Custom exceptions for the Language Test application."""


class LanguageTestException(Exception):
    """Base exception for the application."""
    pass


class EvaluationException(LanguageTestException):
    """Exception raised during evaluation processes."""
    pass


class InvalidLevelException(EvaluationException):
    """Exception raised for invalid CEFR levels."""
    pass


class EvaluationNotFoundException(EvaluationException):
    """Exception raised when evaluation data is not found."""
    pass


class LLMException(LanguageTestException):
    """Exception raised during LLM operations."""
    pass


class InvalidResponseException(LLMException):
    """Exception raised when LLM returns invalid response."""
    pass


class RepositoryException(LanguageTestException):
    """Exception raised during repository operations."""
    pass


class CacheException(LanguageTestException):
    """Exception raised during cache operations."""
    pass