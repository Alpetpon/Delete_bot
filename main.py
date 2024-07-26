import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from config import API_TOKEN, CHANNEL_ID


router = Router()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        "Привет! Используй команды для управления подписчиками:\n"
        "/remove_by_username <username> - удалить по нику\n"
        "/remove_first <n> - удалить первых N подписчиков\n"
        "/remove_last <n> - удалить последних N подписчиков\n"
        "/remove_deleted - удалить неактивных пользователей."
    )

@router.message(Command(commands=['remove_by_username']))
async def remove_by_username(message: types.Message, state: FSMContext):
    username = message.get_args().strip()
    if not username:
        await message.answer("Пожалуйста, укажите имя пользователя (ник).")
        return

    try:
        async for member in bot.get_chat_administrators(chat_id=CHANNEL_ID):
            if member.user.username == username:
                await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=member.user.id)
                await message.reply(f"Пользователь @{username} удален.")
                return
        await message.answer("Пользователь с таким ником не найден.")
    except Exception as e:
        await message.answer(f"Ошибка при удалении пользователя: {e}")


    await state.set_state()


@router.message(Command(commands=['remove_first']))
async def remove_first(message: types.Message):
    try:
        n = int(message.get_args().strip())
        async for member in bot.get_chat_members(chat_id=CHANNEL_ID):
            if n <= 0:
                break
            await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=member.user.id)
            n -= 1
        await message.reply(f"Первые {n} пользователей были удалены.")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное количество пользователей.")
    except Exception as e:
        await message.reply(f"Ошибка при удалении пользователей: {e}")

@router.message(Command(commands=['remove_last']))
async def remove_last(message: types.Message):
    try:
        n = int(message.get_args().strip())
        async for member in bot.get_chat_members(chat_id=CHANNEL_ID):
            if n <= 0:
                break
            await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=member.user.id)
            n -= 1
        await message.reply(f"Последние {n} пользователей были удалены.")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное количество пользователей.")
    except Exception as e:
        await message.reply(f"Ошибка при удалении пользователей: {e}")

@router.message(Command(commands=['remove_deleted']))
async def remove_deleted(message: types.Message):
    try:
        async for member in bot.get_chat_administrators(chat_id=CHANNEL_ID):
            if member.user.is_bot or member.user.status == ChatMemberStatus.KICKED:
                await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=member.user.id)
        await message.reply("Все удаленные пользователи были удалены.")
    except Exception as e:
        await message.reply(f"Ошибка при удалении пользователей: {e}")

if __name__ == '__main__':
    dp.run_polling(bot)