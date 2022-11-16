# Импорты
from peewee import *
import datetime

# Импорты с файлов проекта
from config import db



class BaseModel(Model):
	user_id = PrimaryKeyField(column_name='ID', unique=True)
	telegram_id = CharField(column_name='Telegram ID', unique=True)
	user_name = CharField(column_name='Nickname', null=True)
	first_name = CharField(column_name='First Name', null=True)


	class Meta:
		database = db
		order_by = 'user_id'

class User(BaseModel):
	last_name = CharField(column_name='Last name', null=True)
	date_time_join = DateTimeField(column_name='Date time join',
	                               default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	class Meta:
		db_table = 'users'

class Message(BaseModel):
	message_text = CharField(column_name='Text', null=False)
	date_time_add = DateTimeField(column_name='Date time add',
	                              default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	class Meta:
		db_table = 'messages'

# Создание таблиц
db.create_tables([User, Message ])


