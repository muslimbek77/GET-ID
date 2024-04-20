
from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           KeyboardButtonRequestChat,KeyboardButtonRequestUser)
get_id = ReplyKeyboardMarkup(
    keyboard=[
[KeyboardButton(text="👤 User",request_user=KeyboardButtonRequestUser(request_id=123,user_is_bot=False)),KeyboardButton(text="🤖 Bot",request_user=KeyboardButtonRequestUser(request_id=124,user_is_bot=True))],
[KeyboardButton(text="👥 Group",request_chat=KeyboardButtonRequestChat(request_id=125,chat_is_channel=False)),KeyboardButton(text="📢 Channel",request_chat=KeyboardButtonRequestChat(request_id=126,chat_is_channel=True))],


    ],resize_keyboard=True,
)
