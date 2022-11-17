# Импорты
from aiogram import types, Dispatcher
import asyncio

# Импорты с файлов проекта
from data_base import User, Message, db

from create_bot import dp, bot

from config import *

from admin import FSMContext, State, UserState


# *****************************************************************************************************
# Основные функции:

# Хендлер стартового меню
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
	await log(message)  # Вызов функции логгирования
	id = message.from_user.id
	if id == Admin:
		await message.answer(f"Привет, {message.from_user.username}.\n"
		                     f"Ты был определён как Администратор\n"
		                     f"\nСписок админ команд, нажми:\n/admin\n"
		                     f"\nСписок всех команд, нажми:\n/menu\n\n"
		                     )
	else:
		await message.answer(f"Привет, {message.from_user.full_name}.\n"
		                     f"\nЯ, бот-клоун 🤡 \n"
		                     f"Я как ты, только бот 🤡 \n"
		                     f"\nГлавное меню, нажми:\n/menu\n\n"
		                     )

# @dp.message_handler(commands=['admin'], user_id=Admin)
@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
	await log(message)  # Вызов функции логгирования
	id = message.from_user.id
	if id == Admin:
		await message.answer(f"Вы вошли в админское меню!\n\n"
		                     f"Сделать рассылку пользователям в БД:\n/mailing"
		                     f"\n\nНазад в /menu")
	else:
		await message.answer(f"У вас нет доступа к данной команде"
		                     f"\n\nНазад в /menu")


# Хендлер вызова основного меню
@dp.message_handler(commands=['menu'])
async def cmd_menu(message: types.Message):
	await log(message)  # Вызов функции логгирования
	id = message.from_user.id
	if id == Admin:
		await message.answer('\nПанель управления:\n'
		                     '/admin\n'

		                     '\nРазвлечения:'
		                     '\n/joke\n'

		                     '\nCтатистика:\n'
		                     '/stats\n'

		                     '\nTelegram ID:'
		                     '\n/id\n'

		                     '\nКонтакты:'
		                     '\n/twitch'
		                     '\n/discord'
		                     '\n/telegram\n'

		                     '\nВ начало:\n'
		                     '/start\n'
		                     )

	else:
		await message.answer('\nРазвлечения:'
		                     '\n/joke\n'

		                     '\nCтатистика:\n'
		                     '/stats\n'

		                     '\nTelegram ID:'
		                     '\n/id\n'

		                     '\nКонтакты:'
		                     '\n/twitch'
		                     '\n/discord'
		                     '\n/telegram\n'

		                     '\nВ начало:\n'
		                     '/start\n'
		                     )


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
	await log(message)  # Вызов функции логгирования
	await message.answer(f"Твой Telegram ID: {message.from_user.id}\n\nНазад в /menu")

# *****************************************************************************************************
# Социальные сети:
@dp.message_handler(commands=['telegram'])
async def cmd_telegram(message: types.Message):
	await log(message)  # Вызов функции логгирования
	await message.answer('[Директор цирка:](https://t.me/s4dd666)', parse_mode='Markdown')
	await message.answer('\n\nНазад в /menu')

@dp.message_handler(commands=['twitch'])
async def cmd_twitch(message: types.Message):
	await log(message)  # Вызов функции логгирования
	await message.answer('[Смотреть на клоуна:](https://www.twitch.tv/s4dd666)', parse_mode='Markdown')
	await message.answer('\n\nНазад в /menu')

@dp.message_handler(commands=['discord'])
async def cmd_discord(message: types.Message):
	await log(message)  # Вызов функции логгирования
	await message.answer('[Цирк "Шапито":](https://discord.gg/VS8SvUC)', parse_mode='Markdown')
	await message.answer('\n\nНазад в /menu')

# *****************************************************************************************************
# Фан
@dp.message_handler(commands=['joke'])
async def cmd_joke(message: types.Message):
	await log(message)  # Вызов функции логгирования

	import random
	from joke_list import jokes

	await asyncio.sleep(0.5)
	await message.answer('Держи разрывную:')
	await asyncio.sleep(1)
	await message.answer(random.choice(jokes))
	photo = open('pic/capibara.jpg', 'rb')
	await asyncio.sleep(0.1)
	await bot.send_photo(message.from_user.id, photo)
	await asyncio.sleep(1.5)
	await message.answer("Ну как, поел шуточек?\nКлоун!🤡\n\nИли ещё насыпать?\n/joke\n\nНазад в /menu")


# Хендлер статистики
@dp.message_handler(commands=['stats'])
async def cmd_stats(message: types.Message):
	await log(message)  # Вызов функции логгирования

	with db: # Подсчёт количества пользователей в БД
		users = User.select().where(User.user_id != 0)
		await message.answer(f'Пользователей в базе данных: {len(users)}')

	with db: # Подсчёт количества всех сообщений в БД
		messages = Message.select().where(Message.user_id != 0)
		await message.answer(f'Всего сообщений боту: {len(messages)}')

	with db: # Подсчёт сообщений в БД от конкретного юзера
		self_messages = Message.select(Message.telegram_id).where(message.from_user.id == Message.telegram_id)
	await message.answer(f'Сообщений от вас: {len(self_messages)}')
	await message.answer('\n\nНазад в /menu')

# *****************************************************************************************************
# FSM Модуль рассылки
@dp.message_handler(commands=['mailing'])
async def mailing(message: types.Message):
	id = message.from_user.id
	if id == Admin:
		await log(message)  # Вызов функции логгирования
		await message.answer("Введите текст рассылки")
		await UserState.text.set()
	else:
		await message.answer(f"У вас нет доступа к данной команде"
		                     f"\n\nНазад в /menu")


@dp.message_handler(state=UserState.text)
async def get_username(message: types.Message, state: FSMContext):
	await log(message)  # Вызов функции логгирования
	await state.update_data(username=message.text)
	await message.answer(f"Введите ключ подтверждения\n\n"
	                     f"Чтобы прервать процесс, напишите: Cansel")
	await UserState.next()  # либо же UserState.adress.set()


@dp.message_handler(state=UserState.confirm)
async def get_address(message: types.Message, state: FSMContext):
	await state.update_data(address=message.text)
	data = await state.get_data()
	if message.text == 'Cansel':
		await message.answer(f'Рассылка отменена\n'
		                     f'Чтобы начать новую рассылку, нажмите:\n'
		                     f'/mailing')
		await state.finish()
		elif message.text == Password:
		with db:
			query = (User.select())
			count = 0
			for all_users in query:
				count += 1
				All = (all_users.telegram_id)
				await bot.send_message(All, f"Рассылка от Админа {message.from_user.username}:\n"
				                            f"\n{data['username']}\n")

		await message.answer(f"Уведомление:\nРассылка успешно выполнена\n"
		                     f"\nПользователей вcего: {count}\n"
		                     f"\nНазад в /menu")
		await state.finish()
	else:
		await message.answer('Произошла ошибка: Неверный ключ\n\n'
		                     'Назад в панель /admin'
		                     '\nНазад в /menu'
		                     )
		await state.finish()

# *****************************************************************************************************
# Ответ если заданной команды нет или она была отключена
@dp.message_handler()
async def empty(message: types.Message):
	await log(message)  # Вызов функции логгирования
	await asyncio.sleep(1.5)
	await message.answer('Данной команды не существует\n'
	                     'Либо она была отключена\n'
	                     )
	await asyncio.sleep(0.5)
	await message.answer('\n\nНазад в /menu')

# *****************************************************************************************************
# Актуализация данных пользователя и логгинг его сообщений
async def log(message: types.Message):
	# Функция добавления или обновление информации о пользователе в БД
	create_or_update = (User
	                    .insert(telegram_id=message.from_user.id, user_name=message.from_user.username,
	                            first_name=message.from_user.first_name, last_name=message.from_user.last_name,
	                            date_time_join=message.date)
	                    .on_conflict(
		conflict_target=[User.telegram_id],
		preserve=[User.telegram_id],
		update={
			'user_name': message.from_user.username,
			'first_name': message.from_user.first_name,
			'last_name': message.from_user.last_name})
	                    .execute())

	# Функция добавления отправленного пользователем сообщения в БД
	create_message = Message.insert([
		{'telegram_id': message.from_user.id,
		 'user_name': message.from_user.username,
		 'first_name': message.from_user.first_name,
		 'message_text': message.text,
		 'date_time_add': message.date}
	]).execute()

# *****************************************************************************************************
# Регистрация хендлеров в Диспечере
def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(cmd_start, commands=['start'])
	dp.register_message_handler(cmd_menu, commands=['menu'])

	dp.register_message_handler(cmd_telegram, commands=['telegram'])
	dp.register_message_handler(cmd_twitch, commands=['twitch'])
	dp.register_message_handler(cmd_discord, commands=['discord'])
	dp.register_message_handler(cmd_stats, commands=['stats'])
	dp.register_message_handler(cmd_id, commands=['id'])

	dp.register_message_handler(cmd_joke, commands=['joke'])

	dp.register_message_handler(empty)

	dp.register_message_handler(mailing, commands=['mailing'])
	dp.register_message_handler(get_username)
	dp.register_message_handler(get_address)
