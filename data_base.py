# Импорты
from peewee import *
import datetime

# Импорты с файлов проекта
from config import db



class BaseModel(Model):
	telegram_id = PrimaryKeyField(column_name='Telegram ID', unique=True)
	user_name = CharField(column_name='Nickname', null=True)
	first_name = CharField(column_name='First Name', null=True)

	class Meta:
		database = db

class User(BaseModel):
	user_id = PrimaryKeyField(column_name='ID', unique=True)
	telegram_id = ForeignKeyField(BaseModel, column_name='Telegram ID', unique=True)
	last_name = CharField(column_name='Last Name', null=True)
	date_time_join = DateTimeField(column_name='Date time join', default=now)

	class Meta:
		db_table = 'users'

class Message(BaseModel):
	message_id = PrimaryKeyField(column_name='Message ID', unique=True)
	telegram_id = ForeignKeyField(BaseModel, column_name='Telegram ID', unique=False)
	message_text = CharField(column_name='Text', null=False)
	date_time_add = DateTimeField(column_name='Date time add', default=now)

	class Meta:
		db_table = 'messages'

# Создание таблиц
db.create_tables([User, Message ])


