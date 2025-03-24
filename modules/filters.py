from aiogram import types
from aiogram.filters import BaseFilter


class TextEqualsFilter(BaseFilter):
    def __init__(self, text):
        self.text = text

    async def __call__(self, message: types.Message):
        return message.text == self.text
