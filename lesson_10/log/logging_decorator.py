import inspect
import logging
import sys
import log.server_log_config
import log.client_log_config
from functools import wraps

"""
lesson_6: 
1. Продолжая задачу логирования, реализовать декоратор @log, фиксирующий обращение к
декорируемой функции. Он сохраняет её имя и аргументы.
2.В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная.
"""


def log(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if "server.py" in sys.argv[0]:
            logger = logging.getLogger("server")
        else:
            logger = logging.getLogger("client")
        logger.debug(
            f"Function {func.__module__}.{func.__name__} was called from {inspect.stack()[1][3]}"
        )
        return func(*args, **kwargs)

    return decorated
