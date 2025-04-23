import logging
import threading
from functools import wraps
from logging.handlers import RotatingFileHandler
from typing import Optional, Union, Callable

StringFormatter = Union[str, logging.Formatter]


class LogDecorator:
    """
    一个灵活且线程安全的日志装饰器类，支持动态配置和结构化日志，避免全局配置冲突。
    """

    def __init__(
            self,
            name: str = __name__,
            level: int = logging.DEBUG,
            formatter: StringFormatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            logfile: Optional[str] = None,
            console: bool = True,
            max_bytes: int = 10 * 1024 * 1024,  # 10MB 文件轮转
            backup_count: int = 5,
    ):
        self.name = name
        self.base_level = level
        self.base_formatter = self._ensure_formatter(formatter)
        self.base_logfile = logfile
        self.base_console = console
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.logger = logging.getLogger(name)
        self._configure_base_logger()
        self._lock = threading.Lock()

    def _configure_base_logger(self) -> None:
        """配置基础日志处理器，避免影响动态添加的处理器"""
        self.logger.setLevel(self.base_level)
        self.logger.propagate = False

        # 仅当初始化参数指定时添加基础处理器
        if self.base_console:
            self._add_handler(logging.StreamHandler(), self.base_level, self.base_formatter)
        if self.base_logfile:
            self._add_handler(
                RotatingFileHandler(
                    filename=self.base_logfile,
                    maxBytes=self.max_bytes,
                    backupCount=self.backup_count,
                    encoding="utf-8",
                ),
                self.base_level,
                self.base_formatter
            )

    def _add_handler(self, handler: logging.Handler, level: int, formatter: logging.Formatter) -> None:
        """通用方法添加处理器"""
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _ensure_formatter(self, formatter: StringFormatter) -> logging.Formatter:
        """确保格式器正确"""
        if isinstance(formatter, str):
            return logging.Formatter(formatter)
        return formatter

    def __call__(self, func: Callable) -> Callable:
        """装饰器实现，使用上下文管理器管理临时配置"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 提取临时配置参数（使用'_log_'前缀防止冲突）
            temp_config = {
                'level': kwargs.pop('_log_level', None),
                'formatter': kwargs.pop('_log_formatter', None),
                'logfile': kwargs.pop('_log_file', None),
                'console': kwargs.pop('_log_console', None),
            }

            # 使用线程锁确保临时配置的线程安全
            with self._lock:
                # 创建临时处理器
                temp_handlers = []
                try:
                    # 动态添加处理器
                    formatter = self._ensure_formatter(temp_config['formatter']) if temp_config[
                        'formatter'] else self.base_formatter
                    level = temp_config['level'] or self.base_level

                    if temp_config.get('console', self.base_console):
                        console_handler = logging.StreamHandler()
                        console_handler.setLevel(level)
                        console_handler.setFormatter(formatter)
                        self.logger.addHandler(console_handler)
                        temp_handlers.append(console_handler)

                    if temp_config.get('logfile'):
                        file_handler = RotatingFileHandler(
                            filename=temp_config['logfile'],
                            maxBytes=self.max_bytes,
                            backupCount=self.backup_count,
                            encoding="utf-8",
                        )
                        file_handler.setLevel(level)
                        file_handler.setFormatter(formatter)
                        self.logger.addHandler(file_handler)
                        temp_handlers.append(file_handler)

                    # 执行函数
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    self.logger.exception(f"Error in {func.__name__}: {str(e)}")
                    raise
                finally:
                    # 清理临时处理器
                    for handler in temp_handlers:
                        self.logger.removeHandler(handler)
                        handler.close()

        return wrapper

    # 快捷日志方法
    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        self.logger.exception(msg, *args, **kwargs)


if __name__ == '__main__':
    logger = LogDecorator("test")

    logger.debug("This is a debug message.")
