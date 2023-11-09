import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import TOKEN, mainUserId
from user import User
from users import UsersList

bot = Bot(token=TOKEN)
dp = Dispatcher()

usersList = UsersList()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await bot.send_message(message.from_user.id, "Привет.\n\nЯ — тестовый бот.\n\nУ меня не так много вычислительных мощностей, поэтому иногда я отвечаю не сразу.")


@dp.message()
async def get_text_message(msg: types.Message):
    if msg.from_user.id == mainUserId:
        text = msg.text
        id = text.split(":\n")[0]
        if usersList.getUserById(int(id)) is not None:
            await bot.send_message(id, text.split(":\n")[1])
        else:
            print(usersList)
            await bot.send_message(mainUserId, f"Нет пользователя с ID: {id}")
    else:
        if usersList.getUserById(msg.from_user.id) is None:
            usersList.addUser(User(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name))
        link = f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name} {msg.from_user.last_name}</a>'
        await bot.send_message(mainUserId, f"<code>{msg.from_user.id}</code>\n{link}:\n\n{msg.text}", parse_mode=ParseMode.HTML)

    #     <a href="tg://user?id=' + str(user.user_id) + '">' + user.name + ''
    return


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
