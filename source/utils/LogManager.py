import os
import logging
from datetime import datetime


class LogManager:
    _instance = None
    _logger = None
    _log_file = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._configure_logging()

        return cls._logger

    @classmethod
    def get_log_file(cls):
        if cls._log_file is None:
            cls._configure_logging()

        return cls._log_file

    @classmethod
    def ensure_unicode(cls, message):
        if isinstance(message, bytes):
            return message.decode('utf-8', errors='replace')

        return str(message)

    @classmethod
    def _configure_logging(cls):
        try:
            log_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'CompressionManager', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            cls._log_file = os.path.join(log_dir, f'file_compression_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(cls._log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            cls._logger = logging.getLogger('FileCompression')

        except Exception as e:
            user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'CompressionManager', 'logs')
            os.makedirs(user_data_dir, exist_ok=True)
            cls._log_file = os.path.join(user_data_dir, f'file_compression_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(cls._log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            cls._logger = logging.getLogger('FileCompression')
            cls._logger.error(f"Erro ao configurar logging no diretório padrão: {e}")

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(cls.ensure_unicode(message))

    @classmethod
    def info(cls, message):
        cls.get_logger().info(cls.ensure_unicode(message))

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(cls.ensure_unicode(message))

    @classmethod
    def error(cls, message, exc_info=False):
        cls.get_logger().error(cls.ensure_unicode(message), exc_info=exc_info)

    @classmethod
    def critical(cls, message, exc_info=True):
        cls.get_logger().critical(cls.ensure_unicode(message), exc_info=exc_info)
