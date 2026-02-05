# RIFT Standard Library
"""
Standard library modules for the RIFT language.

Modules:
    - http: HTTP server and client
    - db: Database connections (SQL, NoSQL)
    - crypto: Cryptography and hashing
    - fs: File system operations
    - json: JSON parsing and serialization
    - math_lib: Comprehensive mathematical functions
    - string_lib: Advanced string manipulation
    - array_lib: Array utilities and transformations
    - datetime_lib: Date and time handling
    - regex_lib: Regular expressions
    - validation_lib: Input validation and sanitization
    - collections_lib: Advanced data structures
    - events_lib: Event emitter and pub/sub
    - logging_lib: Structured logging utilities
    - async_lib: Promise-like async utilities
    - functional_lib: Functional programming utilities
"""

from .math_lib import create_math_module
from .string_lib import create_string_module
from .array_lib import create_array_module
from .datetime_lib import create_datetime_module
from .regex_lib import create_regex_module
from .validation_lib import create_validation_module
from .collections_lib import create_collections_module
from .events_lib import create_events_module
from .logging_lib import create_logging_module
from .async_lib import create_async_module
from .functional_lib import create_functional_module

__all__ = [
    'create_math_module',
    'create_string_module',
    'create_array_module',
    'create_datetime_module',
    'create_regex_module',
    'create_validation_module',
    'create_collections_module',
    'create_events_module',
    'create_logging_module',
    'create_async_module',
    'create_functional_module',
]
