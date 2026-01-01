import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
    """
    Configura o sistema de logging da aplicação.

    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Se True, salva logs em arquivo
    """
    # Cria diretório de logs se não existir
    if log_to_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

    # Formato dos logs
    log_format = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Remove handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Handler para console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    # Handler para arquivo (com rotação)
    if log_to_file:
        file_handler = RotatingFileHandler(
            filename=log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_format)
        root_logger.addHandler(file_handler)

        # Handler separado para erros críticos
        error_handler = RotatingFileHandler(
            filename=log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(log_format)
        root_logger.addHandler(error_handler)

    # Reduz verbosidade de bibliotecas externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info("Sistema de logging configurado com sucesso.")


class LoggerAdapter(logging.LoggerAdapter):
    """
    Adapter para adicionar contexto automático aos logs.
    """

    def process(self, msg, kwargs):
        """Adiciona informações extras ao log."""
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra'].update(self.extra)
        return msg, kwargs


def get_logger(name: str, **extra_context) -> LoggerAdapter:
    """
    Retorna um logger configurado com contexto adicional.

    Args:
        name: Nome do logger (geralmente __name__)
        **extra_context: Contexto adicional a ser incluído em todos os logs

    Returns:
        Logger adaptado com contexto
    """
    logger = logging.getLogger(name)
    return LoggerAdapter(logger, extra_context)