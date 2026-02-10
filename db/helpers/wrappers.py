from db.helpers.logger import logger

# caso precise debuggar mais a fundo
def logging_wrapper(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Executando a função: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Função {func.__name__} executada com sucesso!")
        return result
    return wrapper