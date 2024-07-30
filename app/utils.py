import base64
from typing import Union, Any, TypedDict

from cryptography.fernet import Fernet


from django.conf import settings
import logging
from logging import Logger
from elasticsearch import Elasticsearch
from django.utils import timezone


class SecurityLogger:
    logger: Logger

    def __init__(self, name="SecurityLogger", filename="./logoutput.log", log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.setup_logger(self.logger, filename=filename, name=name, log_level=log_level)
        self.logger.info(f"Initialize {name}...")

    @staticmethod
    def setup_logger(logger: Logger, filename: str, name: str, log_level: int):
        # Clear existing handlers to avoid duplicate messages
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(log_level)  # For the logger
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # FileHandler logs to a file if filename is provided
        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.name = name


class LogRecord(TypedDict):
    message: str
    ip_addr: str
    status: int


class LogHandler:
    """
    Singleton class linking to Elasticsearch
    """
    _instance = None
    _index_name = 'HELLO_DOCKER_DJANGO'
    es: Elasticsearch

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def _log(self, level: int, record: LogRecord, backup_security_logger: Union[SecurityLogger, None]):
        try:
            log_entry: dict[str, Any] = {
                'timestamp': timezone.now().isoformat(),
                'name': backup_security_logger.logger.name if backup_security_logger else self._index_name,
                'level': logging.INFO,
                'message': record.get("message", ""),
                'ip_addr': record.get("ip_addr", "Unrecorded"),
                'status': record.get("status", -1)
            }
            self.es.index(index=self._index_name, body=log_entry)
        except Exception as e:
            if backup_security_logger:
                backup_security_logger.logger.error(record.get("message", "") + " Also, " + str(e))

    def info(self, record: LogRecord, backup_security_logger: Union[SecurityLogger, None]) -> None:
        self._log(logging.INFO, record, backup_security_logger)

    def warning(self, record: LogRecord, backup_security_logger: Union[SecurityLogger, None]) -> None:
        self._log(logging.WARNING, record, backup_security_logger)

    def error(self, record: LogRecord, backup_security_logger: Union[SecurityLogger, None]) -> None:
        self._log(logging.ERROR, record, backup_security_logger)




class ObfuscatedSecret:
    def __init__(self, secret):
        key = Fernet.generate_key()
        self.key = key
        f = Fernet(key)
        self.encrypted = f.encrypt(secret.encode())

    def __str__(self):
        return "ObfuscatedSecret"

    def get(self):
        f = Fernet(self.key)
        return f.decrypt(self.encrypted).decode()
