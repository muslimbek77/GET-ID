from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👥 Number of users"),
            KeyboardButton(text="🛫 Submit an ad"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Choose one from the menu"
)