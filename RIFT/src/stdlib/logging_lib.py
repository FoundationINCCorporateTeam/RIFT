"""
RIFT Standard Library - Logging Module

Structured logging utilities.
"""

import sys
import json
import time
import traceback
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable, IO
from enum import IntEnum


def create_logging_module(interpreter) -> Dict[str, Any]:
    """Create the logging module for RIFT."""
    
    # ========================================================================
    # Log Levels
    # ========================================================================
    
    class LogLevel(IntEnum):
        TRACE = 0
        DEBUG = 10
        INFO = 20
        WARN = 30
        ERROR = 40
        FATAL = 50
    
    LEVEL_NAMES = {
        LogLevel.TRACE: 'TRACE',
        LogLevel.DEBUG: 'DEBUG',
        LogLevel.INFO: 'INFO',
        LogLevel.WARN: 'WARN',
        LogLevel.ERROR: 'ERROR',
        LogLevel.FATAL: 'FATAL',
    }
    
    LEVEL_COLORS = {
        LogLevel.TRACE: '\033[90m',      # Gray
        LogLevel.DEBUG: '\033[36m',      # Cyan
        LogLevel.INFO: '\033[32m',       # Green
        LogLevel.WARN: '\033[33m',       # Yellow
        LogLevel.ERROR: '\033[31m',      # Red
        LogLevel.FATAL: '\033[35m',      # Magenta
    }
    
    RESET_COLOR = '\033[0m'
    
    # ========================================================================
    # Formatters
    # ========================================================================
    
    class LogFormatter:
        """Base log formatter."""
        
        def format(self, record: Dict[str, Any]) -> str:
            raise NotImplementedError
    
    class TextFormatter(LogFormatter):
        """Plain text formatter."""
        
        def __init__(self, pattern: str = None, colorize: bool = True):
            self.pattern = pattern or '{timestamp} [{level}] {message}'
            self.colorize = colorize
        
        def format(self, record: Dict[str, Any]) -> str:
            level = record.get('level', LogLevel.INFO)
            level_name = LEVEL_NAMES.get(level, 'INFO')
            
            timestamp = record.get('timestamp', datetime.now())
            if isinstance(timestamp, datetime):
                timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            
            message = record.get('message', '')
            
            # Add context
            context = record.get('context', {})
            if context:
                context_str = ' '.join(f'{k}={v}' for k, v in context.items())
                message = f'{message} {context_str}'
            
            output = self.pattern.format(
                timestamp=timestamp,
                level=level_name,
                message=message,
                name=record.get('name', 'root'),
            )
            
            # Add error details
            if 'error' in record:
                error = record['error']
                if isinstance(error, Exception):
                    output += f'\n  Error: {type(error).__name__}: {error}'
                    if 'traceback' in record:
                        output += f'\n{record["traceback"]}'
            
            if self.colorize and sys.stdout.isatty():
                color = LEVEL_COLORS.get(level, '')
                output = f'{color}{output}{RESET_COLOR}'
            
            return output
    
    class JsonFormatter(LogFormatter):
        """JSON formatter for structured logging."""
        
        def __init__(self, pretty: bool = False):
            self.pretty = pretty
        
        def format(self, record: Dict[str, Any]) -> str:
            output = {
                'timestamp': record.get('timestamp', datetime.now().isoformat()),
                'level': LEVEL_NAMES.get(record.get('level', LogLevel.INFO), 'INFO'),
                'message': record.get('message', ''),
            }
            
            if 'name' in record:
                output['logger'] = record['name']
            
            if 'context' in record:
                output['context'] = record['context']
            
            if 'error' in record:
                error = record['error']
                if isinstance(error, Exception):
                    output['error'] = {
                        'type': type(error).__name__,
                        'message': str(error),
                    }
                    if 'traceback' in record:
                        output['error']['traceback'] = record['traceback']
            
            if isinstance(output.get('timestamp'), datetime):
                output['timestamp'] = output['timestamp'].isoformat()
            
            if self.pretty:
                return json.dumps(output, indent=2, default=str)
            return json.dumps(output, default=str)
    
    # ========================================================================
    # Handlers
    # ========================================================================
    
    class LogHandler:
        """Base log handler."""
        
        def __init__(self, formatter: LogFormatter = None, level: LogLevel = LogLevel.DEBUG):
            self.formatter = formatter or TextFormatter()
            self.level = level
            self._lock = threading.Lock()
        
        def handle(self, record: Dict[str, Any]) -> None:
            if record.get('level', LogLevel.INFO) >= self.level:
                self._write(self.formatter.format(record))
        
        def _write(self, message: str) -> None:
            raise NotImplementedError
    
    class ConsoleHandler(LogHandler):
        """Log to console."""
        
        def __init__(self, stream: IO = None, **kwargs):
            super().__init__(**kwargs)
            self.stream = stream or sys.stdout
        
        def _write(self, message: str) -> None:
            with self._lock:
                print(message, file=self.stream)
    
    class FileHandler(LogHandler):
        """Log to file."""
        
        def __init__(self, filename: str, mode: str = 'a', **kwargs):
            super().__init__(**kwargs)
            self.filename = filename
            self.mode = mode
            self._file = None
        
        def _write(self, message: str) -> None:
            with self._lock:
                if self._file is None:
                    self._file = open(self.filename, self.mode)
                self._file.write(message + '\n')
                self._file.flush()
        
        def close(self) -> None:
            if self._file:
                self._file.close()
                self._file = None
    
    class RotatingFileHandler(LogHandler):
        """Log to rotating files."""
        
        def __init__(self, filename: str, max_size: int = 10 * 1024 * 1024,
                     backup_count: int = 5, **kwargs):
            super().__init__(**kwargs)
            self.filename = filename
            self.max_size = max_size
            self.backup_count = backup_count
            self._file = None
            self._size = 0
        
        def _rotate(self) -> None:
            import os
            
            if self._file:
                self._file.close()
                self._file = None
            
            # Rotate existing files
            for i in range(self.backup_count - 1, 0, -1):
                src = f'{self.filename}.{i}'
                dst = f'{self.filename}.{i + 1}'
                if os.path.exists(src):
                    os.rename(src, dst)
            
            if os.path.exists(self.filename):
                os.rename(self.filename, f'{self.filename}.1')
            
            self._size = 0
        
        def _write(self, message: str) -> None:
            import os
            
            with self._lock:
                if self._file is None:
                    self._file = open(self.filename, 'a')
                    if os.path.exists(self.filename):
                        self._size = os.path.getsize(self.filename)
                
                msg_bytes = (message + '\n').encode('utf-8')
                
                if self._size + len(msg_bytes) > self.max_size:
                    self._rotate()
                    self._file = open(self.filename, 'a')
                
                self._file.write(message + '\n')
                self._file.flush()
                self._size += len(msg_bytes)
    
    class MemoryHandler(LogHandler):
        """Log to memory buffer."""
        
        def __init__(self, max_records: int = 1000, **kwargs):
            super().__init__(**kwargs)
            self.max_records = max_records
            self.records: List[str] = []
        
        def _write(self, message: str) -> None:
            with self._lock:
                self.records.append(message)
                if len(self.records) > self.max_records:
                    self.records = self.records[-self.max_records:]
        
        def get_records(self) -> List[str]:
            return list(self.records)
        
        def clear(self) -> None:
            with self._lock:
                self.records = []
    
    # ========================================================================
    # Logger
    # ========================================================================
    
    class Logger:
        """Main logger class."""
        
        def __init__(self, name: str = 'root', level: LogLevel = LogLevel.DEBUG):
            self.name = name
            self.level = level
            self.handlers: List[LogHandler] = []
            self.context: Dict[str, Any] = {}
            self.parent: Optional['Logger'] = None
        
        def addHandler(self, handler: LogHandler) -> 'Logger':
            """Add a log handler."""
            self.handlers.append(handler)
            return self
        
        def removeHandler(self, handler: LogHandler) -> 'Logger':
            """Remove a log handler."""
            if handler in self.handlers:
                self.handlers.remove(handler)
            return self
        
        def setLevel(self, level: LogLevel) -> 'Logger':
            """Set minimum log level."""
            self.level = level
            return self
        
        def setContext(self, context: Dict[str, Any]) -> 'Logger':
            """Set persistent context."""
            self.context = context
            return self
        
        def addContext(self, **kwargs) -> 'Logger':
            """Add to context."""
            self.context.update(kwargs)
            return self
        
        def child(self, name: str = None, **context) -> 'Logger':
            """Create child logger with additional context."""
            child_name = f'{self.name}.{name}' if name else self.name
            child = Logger(child_name, self.level)
            child.parent = self
            child.context = {**self.context, **context}
            child.handlers = self.handlers  # Share handlers with parent
            return child
        
        def _log(self, level: LogLevel, message: str, *args, **kwargs) -> None:
            """Internal log method."""
            if level < self.level:
                return
            
            # Format message with args
            if args:
                try:
                    message = message % args
                except (TypeError, ValueError):
                    message = f'{message} {args}'
            
            record = {
                'timestamp': datetime.now(),
                'level': level,
                'message': message,
                'name': self.name,
                'context': {**self.context, **kwargs.get('context', {})},
            }
            
            # Handle error/exception
            error = kwargs.get('error') or kwargs.get('exc')
            if error:
                record['error'] = error
                if isinstance(error, Exception):
                    record['traceback'] = ''.join(traceback.format_exception(
                        type(error), error, error.__traceback__
                    ))
            
            for handler in self.handlers:
                try:
                    handler.handle(record)
                except Exception as e:
                    print(f"Error in log handler: {e}", file=sys.stderr)
        
        def trace(self, message: str, *args, **kwargs) -> None:
            """Log trace message."""
            self._log(LogLevel.TRACE, message, *args, **kwargs)
        
        def debug(self, message: str, *args, **kwargs) -> None:
            """Log debug message."""
            self._log(LogLevel.DEBUG, message, *args, **kwargs)
        
        def info(self, message: str, *args, **kwargs) -> None:
            """Log info message."""
            self._log(LogLevel.INFO, message, *args, **kwargs)
        
        def warn(self, message: str, *args, **kwargs) -> None:
            """Log warning message."""
            self._log(LogLevel.WARN, message, *args, **kwargs)
        
        def error(self, message: str, *args, **kwargs) -> None:
            """Log error message."""
            self._log(LogLevel.ERROR, message, *args, **kwargs)
        
        def fatal(self, message: str, *args, **kwargs) -> None:
            """Log fatal message."""
            self._log(LogLevel.FATAL, message, *args, **kwargs)
        
        def exception(self, message: str, error: Exception = None, **kwargs) -> None:
            """Log exception with traceback."""
            if error is None:
                # Get current exception
                error = sys.exc_info()[1]
            self.error(message, error=error, **kwargs)
        
        def time(self, label: str) -> 'LogTimer':
            """Start a timer for measuring operations."""
            return LogTimer(self, label)
        
        def __repr__(self):
            return f"Logger(name={self.name}, level={LEVEL_NAMES[self.level]})"
    
    class LogTimer:
        """Timer for measuring operation duration."""
        
        def __init__(self, logger: Logger, label: str):
            self.logger = logger
            self.label = label
            self.start_time = None
        
        def __enter__(self):
            self.start_time = time.time()
            return self
        
        def __exit__(self, *args):
            elapsed = (time.time() - self.start_time) * 1000
            self.logger.debug(f'{self.label}: {elapsed:.2f}ms')
    
    # ========================================================================
    # Global Logger
    # ========================================================================
    
    _loggers: Dict[str, Logger] = {}
    _root_logger = Logger('root')
    _root_logger.addHandler(ConsoleHandler())
    _loggers['root'] = _root_logger
    
    def get_logger(name: str = 'root') -> Logger:
        """Get or create a logger."""
        if name in _loggers:
            return _loggers[name]
        
        logger = Logger(name)
        logger.addHandler(ConsoleHandler())
        _loggers[name] = logger
        return logger
    
    def configure(config: Dict[str, Any]) -> None:
        """Configure logging from config dict."""
        level = config.get('level', 'DEBUG')
        if isinstance(level, str):
            level_map = {
                'TRACE': LogLevel.TRACE,
                'DEBUG': LogLevel.DEBUG,
                'INFO': LogLevel.INFO,
                'WARN': LogLevel.WARN,
                'ERROR': LogLevel.ERROR,
                'FATAL': LogLevel.FATAL,
            }
            level = level_map.get(level.upper(), LogLevel.DEBUG)
        
        _root_logger.setLevel(level)
        _root_logger.handlers = []
        
        handlers = config.get('handlers', ['console'])
        for handler_config in handlers:
            if isinstance(handler_config, str):
                handler_config = {'type': handler_config}
            
            handler_type = handler_config.get('type', 'console')
            
            if handler_type == 'console':
                formatter_config = handler_config.get('formatter', {})
                if formatter_config.get('json'):
                    formatter = JsonFormatter(pretty=formatter_config.get('pretty', False))
                else:
                    formatter = TextFormatter(
                        pattern=formatter_config.get('pattern'),
                        colorize=formatter_config.get('colorize', True)
                    )
                _root_logger.addHandler(ConsoleHandler(formatter=formatter, level=level))
            
            elif handler_type == 'file':
                filename = handler_config.get('filename', 'app.log')
                formatter = JsonFormatter() if handler_config.get('json') else TextFormatter(colorize=False)
                _root_logger.addHandler(FileHandler(filename, formatter=formatter, level=level))
            
            elif handler_type == 'rotating':
                filename = handler_config.get('filename', 'app.log')
                max_size = handler_config.get('maxSize', 10 * 1024 * 1024)
                backup_count = handler_config.get('backupCount', 5)
                formatter = JsonFormatter() if handler_config.get('json') else TextFormatter(colorize=False)
                _root_logger.addHandler(RotatingFileHandler(
                    filename, max_size, backup_count, formatter=formatter, level=level
                ))
    
    # ========================================================================
    # Convenience Functions
    # ========================================================================
    
    def log_trace(message: str, *args, **kwargs) -> None:
        _root_logger.trace(message, *args, **kwargs)
    
    def log_debug(message: str, *args, **kwargs) -> None:
        _root_logger.debug(message, *args, **kwargs)
    
    def log_info(message: str, *args, **kwargs) -> None:
        _root_logger.info(message, *args, **kwargs)
    
    def log_warn(message: str, *args, **kwargs) -> None:
        _root_logger.warn(message, *args, **kwargs)
    
    def log_error(message: str, *args, **kwargs) -> None:
        _root_logger.error(message, *args, **kwargs)
    
    def log_fatal(message: str, *args, **kwargs) -> None:
        _root_logger.fatal(message, *args, **kwargs)
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    def create_logger(name: str = 'app') -> Logger:
        return get_logger(name)
    
    def create_console_handler(**kwargs) -> ConsoleHandler:
        return ConsoleHandler(**kwargs)
    
    def create_file_handler(filename: str, **kwargs) -> FileHandler:
        return FileHandler(filename, **kwargs)
    
    def create_rotating_handler(filename: str, **kwargs) -> RotatingFileHandler:
        return RotatingFileHandler(filename, **kwargs)
    
    def create_memory_handler(**kwargs) -> MemoryHandler:
        return MemoryHandler(**kwargs)
    
    def create_text_formatter(**kwargs) -> TextFormatter:
        return TextFormatter(**kwargs)
    
    def create_json_formatter(**kwargs) -> JsonFormatter:
        return JsonFormatter(**kwargs)
    
    return {
        # Logger
        'Logger': create_logger,
        'getLogger': get_logger,
        'configure': configure,
        
        # Handlers
        'ConsoleHandler': create_console_handler,
        'FileHandler': create_file_handler,
        'RotatingHandler': create_rotating_handler,
        'MemoryHandler': create_memory_handler,
        
        # Formatters
        'TextFormatter': create_text_formatter,
        'JsonFormatter': create_json_formatter,
        
        # Convenience
        'trace': log_trace,
        'debug': log_debug,
        'info': log_info,
        'warn': log_warn,
        'error': log_error,
        'fatal': log_fatal,
        
        # Levels
        'TRACE': int(LogLevel.TRACE),
        'DEBUG': int(LogLevel.DEBUG),
        'INFO': int(LogLevel.INFO),
        'WARN': int(LogLevel.WARN),
        'ERROR': int(LogLevel.ERROR),
        'FATAL': int(LogLevel.FATAL),
    }
