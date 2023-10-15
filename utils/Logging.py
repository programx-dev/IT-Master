import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.ERROR)
c_formatter = logging.Formatter("(%(filename)s) - [%(levelname)s] - %(message)s")
c_handler.setFormatter(c_formatter)
logger.addHandler(c_handler)

f_handler = logging.FileHandler(r"logs\log.log", mode = "w", encoding = "utf-8")
f_formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - (%(filename)s) - %(message)s")
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(f_formatter)
logger.addHandler(f_handler)