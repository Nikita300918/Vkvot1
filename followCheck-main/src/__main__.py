import asyncio
import re

from vkbottle.bot import Bot, Message
from vkbottle import API

import configparser

from src.config import config
from src.utils import loop, loop_wrapper

bot = Bot(
    token=config.bot.token,
    loop=loop,
    loop_wrapper=loop_wrapper,
)
api = API(
    token=config.user.token,
)
config = configparser.ConfigParser()

groups = []
admins = [407654013]

@bot.on.message(text="!!")
async def delete_msg(message: Message):
    global admins

    if message.from_id in admins:
        print(message.reply_message)
        await message.ctx_api.messages.delete(
            peer_id=message.reply_message.from_id,
            cmids=message.reply_message.conversation_message_id,
            delete_for_all=1
        )


@bot.on.message(text="- <group_mention>")
async def add_group(message: Message, group_mention):
    global groups
    global admins

    match = re.search(r'vk\.com/(.+)', group_mention)

    if message.from_id in admins:
        group_info = (await api.groups.get_by_id(group_id=match.group(1)))[0]
        groups.remove(int(group_info.id))

        await message.answer(
            f"✅ Группа @{group_info.screen_name} ({group_info.name}) успешно убрана из списка."
        )


@bot.on.message(text="+ <group_mention>")
async def add_group(message: Message, group_mention):
    global groups
    global admins

    match = re.search(r'vk\.com/(.+)', group_mention)

    if message.from_id in admins:
        if group_mention not in groups:
            group_info = (await api.groups.get_by_id(group_id=match.group(1)))[0]
            groups.append(int(group_info.id))

            await message.answer(
                f"✅ Группа: @{group_info.screen_name} ({group_info.name}) успешно добавлена в список ✨vip✨."
            )


@bot.on.message(text="/")
async def add_group(message: Message):
    global groups
    global admins

    if message.from_id in admins:

        result = ''
        for index, group in enumerate(groups, 1):
            await asyncio.sleep(0.5)
            group_info = await api.groups.get_by_id(group_id=str(group))
            result += f'{index}. @{group_info[0].screen_name} ({group_info[0].name})\n'

        await message.answer(
            f"📚 Список сообществ, которые бот проверяет:\n\n{result if result else '@shoopblack'}"
        )


@bot.on.message(text="/groupsids")
async def add_group(message: Message):
    global groups
    global admins

    if message.from_id in admins:
        await message.answer(
            f"{groups}"
        )


@bot.on.chat_message()
async def check_user(message: Message):
    global groups
    groups_list = []

    if message.from_id <= 0:
        return None

    for group in groups:
        groups_list.append(await message.ctx_api.groups.is_member(group_id=group, user_id=message.from_id))

    if 0 in groups_list:
        result = ''
        for index, group in enumerate(groups, 1):
            await asyncio.sleep(0.1)
            group_info = await api.groups.get_by_id(group_id=str(group))
            result += f'{index}. @{group_info[0].screen_name} ({group_info[0].name})\n'

        await message.ctx_api.messages.delete(
            peer_id=message.peer_id,
            cmids=message.conversation_message_id,
            delete_for_all=1
        )

        user_info = (await message.ctx_api.users.get(message.from_id))[0]

        await message.answer(
            f"@id{user_info.id} ({user_info.first_name} {user_info.last_name}), чтобы писать в беседу, вступи в группы:\n\n"
            "➖➖➖➖➖\n"
            f"{result}"
            "➖➖➖➖➖\n\n"
            "📝 Хочешь добавить свою группу тоже?\n🖌 Пиши Администратору: @shoopblack"
        )


def __main__():
    loop_wrapper.add_task(bot.run_polling())
    loop_wrapper.run_forever(loop=loop)


if __name__ == "__main__":
    __main__()
