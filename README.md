My first big personal project "Telegram bot"

What i use in this project: aiogram, SQLite > Peewee ORM

When sending any command or message, the bot records the sending user in the Database.
Logs as user and simultaneously logs the sent message to another database table.
If the user has already been in the database,
then the bot checks the relevance of the data: username, first name, last name and updates them in the database if necessary.

What bot can do? He had small pool functions:

/start - welcome message and description of the bot: 
    /admin - If you Admin, this command show you some different text in /menu:
        /mailing - If you are an administrator and you have a password, you can mail out to users specified in the config.
        
    /menu - show all command:
      /joke - sending a random little joke.
      /stats - Show for user 3 parametrs: Count users in DataBase; Count message in DataBase; Count message from this user in DataBase.
      /id - resend for user him Telegram ID.
      
      /twitch - My twitch.
      /discord - Invite to Discord server.
      /telegram - My telegram.
      
      /start - back to start.

