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
    await bot.send_message(message.from_user.id, "Привет.\n\nЯ — тестовый ИИ.\n\nУ меня не так много вычислительных мощностей, поэтому иногда я отвечаю не сразу.")


@dp.message()
async def get_text_message(msg: types.Message):
    try:
        if msg.from_user.id == mainUserId:
            text = msg.text
            id = text.split(":\n")[0]
            if usersList.getUserById(int(id)) is not None:
                await bot.send_message(id, text.split(":\n")[1])
            else:
                await bot.send_message(mainUserId, f"Нет пользователя с ID: {id}")
        else:
            if usersList.getUserById(msg.from_user.id) is None:
                usersList.addUser(User(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name))
            link = f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name} {msg.from_user.last_name}</a>'
            await bot.send_message(mainUserId, f"<code>{msg.from_user.id}</code>\n{link}:\n\n{msg.text}", parse_mode=ParseMode.HTML)
    except Exception as ex:
        await bot.send_message(mainUserId, "🟥 [WARNING]: " + str(ex))
    return


async def bot_start():
    bot = Bot(TOKEN)
    print("Бот запущен")
    await dp.start_polling(bot)


# WebSocket
import asyncio
import websockets

async def connect_to_server():
    uri = "wss://socketsbay.com/wss/v2/1/0aecfa6db87c0600e0bc7182c1a56c63/"  # Замените на ваш адрес WebSocket сервера

    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print(f"Получено от сервера: {response}")

async def main():
    await asyncio.gather(bot_start(), connect_to_server())

asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())
