import logging

# Создать экземпляр логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Установить уровень логирования на DEBUG

# Создать обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Установить уровень для вывода в консоль
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)  # Добавить обработчик в логгер

# Создать обработчик для сохранения в файл
file_handler = logging.FileHandler('my_logs.log')
file_handler.setLevel(logging.DEBUG)  # Установить уровень для сохранения в файл
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)  # Добавить обработчик в логгер

# Вывести сообщения
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")