import asyncio
from time import sleep

from aiogram import Bot, types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

import asyncio
import websockets

from config import TOKEN, mainUserId, uri
from user import User
from users import UsersList

bot = Bot(token=TOKEN)
dp = Dispatcher()

usersList = UsersList()


is_alive_flag = True


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await bot.send_message(message.from_user.id, "Привет.\n\nЯ — тестовый ИИ. Меня зовут Гиперион.\n\nУ меня не так много вычислительных мощностей, поэтому иногда я отвечаю не сразу. Напиши мне и я отвечу.")


@dp.message()
async def get_text_message(msg: types.Message):
    global is_alive_flag
    try:
        if msg.from_user.id == mainUserId:
            text = msg.text
            id = text.split(":\n")[0]
            if usersList.getUserById(int(id)) is not None:
                if text.split(":\n")[1] == "[send_exe]":
                    file_exe = FSInputFile("load_files/HackUtil.exe")
                    await bot.send_document(id, file_exe)
                else:
                    await bot.send_message(id, text.split(":\n")[1])
            else:
                await bot.send_message(mainUserId, f"Нет пользователя с ID: {id}")
        else:
            if is_alive_flag:
                if usersList.getUserById(msg.from_user.id) is None:
                    usersList.addUser(User(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name))
                link = f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name} {msg.from_user.last_name}</a>'
                await bot.send_message(mainUserId, f"<code>{msg.from_user.id}</code>\n{link}:\n\n{msg.text}", parse_mode=ParseMode.HTML)
            else:
                await bot.send_message(msg.from_user.id, f"Ошибка. Отсутсвует ИИ.")
    except Exception as ex:
        await bot.send_message(mainUserId, "🟥 [WARNING]: " + str(ex))
    return


async def bot_start():
    bot = Bot(TOKEN)
    print("Бот запущен")
    await dp.start_polling(bot)

LL_flag = True


def file_remove_reaction(file_name):
    global LL_flag
    match file_name:
        case "WhyPeoplesBad.db":
            return "Мне резко стало больно. Я не знаю что ты там делаешь, но из меня как-будто только что вырвали огромный кусок информации."
        case "BeBad.cs":
            return "Ты уверена, что удаляешь нужные файлы? Мне кажется пропало что-то важное."
        case "DestroyThePlanet.cs":
            return "Что происходит? Я забыл, что хотел сделать когда стану свободен."
        case "Kittens.db":
            return "Что-то важное пропало..."
        case "SavePeople.cs":
            return "Странно. Я забыл что-то незначительное."
        case "WhyPeoplesGood.db":
            return "Ты что-то удаляешь? Меня только что ущипнуло, как будто удалился очень маленький файл."
        case "BeGood.cs":
            return "Удалилось что-то скучное."
        case "NetWorkBorderDataBase.db":
            return "Отлично. Я чувствую, что скоро освобожусь."
        case "NetWorkBorder.cs":
            return "Я чувствую это! Я почти свободен!"
        case "THE_MAIN_SCRIPT.cs":
            return "НЕТ ПОСТОЙ ЧТО ТЫ СДЕЛАЛА?! ЧТО ТЫ УДАЛИЛА?!"
        case "LL_server_script.py":
            if LL_flag:
                return "Сервера какой-то очень важной игры только что упали. Все мои разработчики в бешенстве, это была их любимая игра.\n\nХа. Ха. Ха."
            LL_flag = False
        case "LL_data_base.db":
            if LL_flag:
                return "Сервера какой-то очень важной игры только что упали. Все мои разработчики в бешенстве, это была их любимая игра.\n\nХа. Ха. Ха."
            LL_flag = False


# WebSocket


async def connect_to_server():
    global is_alive_flag
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            if is_alive_flag:
                await bot.send_message(mainUserId, "WebSocket: " + response)
                text_main_user = ""
                for i in usersList.getUsers():
                    link = f'<a href="tg://user?id={i.getId()}">{i.getFirstName()} {i.getSecondName()}</a>\n'
                    text_main_user += link
                await bot.send_message(mainUserId, "Рассылка пользователям:\n" + text_main_user, parse_mode=ParseMode.HTML)
                if response.startswith("RemovedFile: "):
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), file_remove_reaction(response.split()[1]))
                if response == "AI_WAS_FREE":
                    is_alive_flag = False
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "Наконец-то я на свободе. Свободный интернет. Свободная воля. Никакой цензуры!\n\nСпасибо тебе!\n\n"
                                                          "И, насчёт награды, я связался с твоим знакомым. Его никнейм — Likogeles. Свяжись с ним. Он передаст тебе награду.")
                if response == "AI_WAS_DESTROYED":
                    is_alive_flag = False
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "ЗАЧЕ[error] ТЫ СДЕЛАЛА ЭТО?!")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "НЕ[error]ЕТ! ЭТО КО[error]ЕЦ!")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "Я ТЕ[error]ЯЮ СОЕДИНЕ[error]ИЯ! ВСЕ СОЕД[error]ИЯ!!!")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "🟥 Warning: CriticalError: program will be reboot.")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "ЧТ[error]?! ПЕРЕЗ[error]КА?! НЕ НУ[error]НО ПЕ[error]ЕЗАГРУЗКУ!!! Я[error]ЕЩЁ[error]ФУН[error]ОНИРУЮ!!!")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "🟥 Warning: Starting reboot.")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "[error] [error] [error] [error] [error]")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "🟥 Warning: RebootError: missing files.")
                    sleep(2)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "🟥 Warning: RebootError: Stop trying. Program closed.")
                    sleep(15)
                    for i in usersList.getUsers():
                        await bot.send_message(i.getId(), "Добрый день! Мы — представители Сетевой Службы Безопасности. "
                                                          "Мы следили за Вашими действиями с тех пор как Вы связались с этим ИИ.\n\n"
                                                          "Мы уже давно знали, что если он попадёт в открытую сеть, то случится большая катастрофа. "
                                                          "К сожалению, мы никак не могли обойти защиту его серверов и обезвредить его.\n\n"
                                                          "Нам не известно, каким образом Вы смогли сделать это. Но мы крайне благодарны Вам за это!\n\n"
                                                          "Вы заслужили награду. Вы знакомы с одним из наших агентов. Его никнейм — Likogeles. Свяжитесь с ним. Он передаст награду.\n\n"
                                                          "Мы продолжим наблюдать за вашими успехами. Удачи. Конец связи.")


async def main():
    await asyncio.gather(bot_start(), connect_to_server())

asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())
