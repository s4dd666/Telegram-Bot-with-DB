# Импорты
from aiogram.utils import executor

# Импорты с файлов проекта
from create_bot import dp


try:
	async def on_startup(_):
		print('\nBot status: Online\n')

	import admin
	import client

	client.register_handlers_client(dp)
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup, fast=True)

except:
    print("Bot module: Error")
finally:
    print("Bot module: Close\n")