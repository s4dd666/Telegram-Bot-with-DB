# Импорты
import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Импорты с файлов проекта
import config


try:
	bot_token = config.TOKEN
	if not bot_token:
		exit('Error: no token provided')

	# Проверка токена
	bot = Bot(token=bot_token)

	# Включение диспечера для бота
	dp = Dispatcher(bot, storage=MemoryStorage())

	# Включаем логирование
	logging.basicConfig(level=logging.INFO)

	print("Create module: Start")
except:
    print("Create module: Error")
finally:
    print("Create module: Close\n")