import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from modules import functions
from modules.keyboards import Buttons, InlineButtons
from modules.filters import TextEqualsFilter
from modules.states import RegistrationState

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    response = await functions.add_user(
        str(message.from_user.id),
        message.from_user.full_name,
        message.from_user.username,
    )
    json_response = await response.json()
    status = await functions.check_is_subscribed(bot, message.from_user.id)

    if not status:
        await message.reply(
            f"Assalomu alaykum {message.from_user.full_name}, botdan foydalanishdan oldin birinchi navbatda siz mening kanal(lar)imga a'zo bo'lishingiz kerak",
            reply_markup=InlineButtons.get_subscribe_inline_buttons(
                has_registered=True if json_response.get("data", {}).get("phone_number") else False,
            )
        )
        return


    if response.status not in (200, 201) and json_response.get("error") == "User already exists":
        await message.answer(f"Assalomu alaykum, {json_response.get('data', {}).get('name')}")
        return


    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}\n"
        f"Azizbek Zaylobiddinov ning rasmiy botiga xush kelibsiz, birinchi navbata ro'yxatdan o'ting\n"
        f"Buning uchun quyidagi tugmani bosing!",
        reply_markup=Buttons.REGISTER_BUTTON,
    )


@dp.message(TextEqualsFilter("✍️ Ro'yxatdan o'tish"))
async def start_registration(message: Message, state: FSMContext) -> None:
    await message.reply("Ism va familiyangizni yozing", reply_markup=Buttons.REMOVE_BUTTON)
    await state.set_state(RegistrationState.name)


@dp.message(RegistrationState.name)
async def run_name_state(message: Message, state: FSMContext) -> None:
    await message.reply(
        "Engi telefon raqamingizni yuboring, buning uchun quyidagi tugmani bosing!",
        reply_markup=Buttons.PHONE_NUMBER_BUTTON
    )
    await state.update_data({"id": str(message.from_user.id), "name": message.text})
    await state.set_state(RegistrationState.phone_number)


@dp.message(RegistrationState.phone_number)
async def run_phone_number_state(message: Message, state: FSMContext) -> None:
    if message.contact:
        await state.update_data({"phone_number": message.contact.phone_number})
        state_data = await state.get_data()
        response = await functions.update_or_add_user(**state_data)
        if response.status not in (200, 201):
            await message.reply(
                "Qandaydir muammo bo'ldi tezda to'girlaymiz kamchiliklar uchun uzr, birozdan so'ng qaytadan urinib ko'ring",
                reply_markup=Buttons.REGISTER_BUTTON,
            )
            return

        await message.reply("Tabriklayman, siz muvaffaqqiyatli ro'yxatdan o'tdingiz!", reply_markup=Buttons.REMOVE_BUTTON)
    else:
        await message.reply("Telefon raqamni yuborish uchun ushbu tugmani bosing!")
        await state.set_state(RegistrationState.phone_number)


@dp.callback_query()
async def query_handlers(query: CallbackQuery, state: FSMContext) -> None:
    key, query_text = query.data.split(":")
    if key == "check-subscribe":
        await query.message.delete()
        status = await functions.check_is_subscribed(bot, query.message.chat.id)
        if not status:
            await query.answer("Siz barcha kanallarga a'zo bo'lishingiz kerak", show_alert=True)
            await query.message.answer(
                f"Botdan foydalanishdan oldin birinchi navbatda siz mening kanal(lar)imga a'zo bo'lishingiz kerak",
                reply_markup=InlineButtons.get_subscribe_inline_buttons(
                    has_registered=True if query_text == "registered" else False
                )
            )

        else:
            if query_text == "registered":
                await query.answer("Botdan foydalanishingiz mumkin")
            else:
                await query.message.answer("Ism va familiyangizni yozing", reply_markup=Buttons.REMOVE_BUTTON)
                await state.set_state(RegistrationState.name)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
