class ValidationError(ValueError):
    """Raised when business data violates validation rules."""


class TransitionError(ValueError):
    """Raised when a status change violates workflow rules."""


class NotFoundError(KeyError, ValueError):
    """Raised when a requested ticket or record cannot be found."""


class StorageError(Exception):
    """Raised when JSON read/write or persistence fails."""
