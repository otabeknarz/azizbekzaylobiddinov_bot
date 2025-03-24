from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
)
from .settings import CHANNELS


class Buttons:
    REGISTER_BUTTON = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✍️ Ro'yxatdan o'tish")]]
    )
    REMOVE_BUTTON = ReplyKeyboardRemove()
    PHONE_NUMBER_BUTTON = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Telefon raqamimni yuborish", request_contact=True)]]
    )


class InlineButtons:
    @staticmethod
    def get_subscribe_inline_buttons(has_registered: bool = False) -> InlineKeyboardMarkup:
        inline_buttons = [
            [InlineKeyboardButton(text=channel_name, url=channel_link)]
            for channel_id, (channel_name, channel_link) in CHANNELS.items()
        ]
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="I've joined ✅",
                    callback_data="check-subscribe:registered"
                    if has_registered else "check-subscribe:not-registered",
                )
            ]
        )
        return InlineKeyboardMarkup(
            inline_keyboard=inline_buttons,
        )
