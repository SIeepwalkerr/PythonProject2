from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton,WebAppInfo)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отменить запрос")]
],
    resize_keyboard=True)
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Чат')],
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню')