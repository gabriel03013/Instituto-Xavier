from db.helpers.logger import logger

# caso precise debuggar mais a fundo
def debug(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Executando: {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"Função {func.__name__} executada com sucesso!")
        return result
    return wrapper