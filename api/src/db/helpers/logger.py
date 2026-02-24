import logging

def get_logger(name: str = __name__):
    
    COLORS = {
        "DEBUG": "\033[36m",    # ciano
        "INFO": "\033[32m",     # verde
        "WARNING": "\033[33m",  # amarelo
        "ERROR": "\033[31m",    # vermelho
        "CRITICAL": "\033[41m", # fundo vermelho
    }
    RESET = "\033[0m"

    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                color = COLORS.get(record.levelname, "")
                return f"{color}{super().format(record)}{RESET}"

        formatter = ColoredFormatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = get_logger()