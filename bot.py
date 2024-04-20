from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,InlineKeyboardButton
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from filters.check_sub_channel import IsCheckSubChannels
from keyboard_buttons import admin_keyboard
from aiogram.fsm.context import FSMContext #new
from states.reklama import Adverts
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time 
from keyboard_buttons.id_button import get_id
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()




@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    text = f"""Welcome <a href='tg://user?id={telegram_id}'>Friend</a> 🎉

🤖In this bot you can get the id of any group, channel, user or bot

📤 To use the bot, click on the buttons below and share the chat whose ID you want to know. - In response, the bot will return the ID of the chat you shared

📝 For the list of available commands send the command /help"""
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        
        await message.answer(text=text)
    except:
        text = text.replace("Friend","Dear Friend")
        await message.answer(text=text,parse_mode="HTML",reply_markup=get_id)







@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message:Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-channel",url=ChatInviteLink.invite_link))
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} subscribe to the channels",reply_markup=button)




    
@dp.message(F.user_shared)
async def get_user_id(message: Message):
    print(message)
    id = message.user_shared.user_id
    print(id)
    text = "🏷 ID: <code>{id}</code>".format(id=id)
    await message.answer(text,reply_markup=get_id)

@dp.message(F.chat_shared)
async def get_chat_id(message: Message):
    id = message.chat_shared.chat_id
    text = "🏷 ID: <code>{id}</code>".format(id=id)
    await message.answer(text,reply_markup=get_id)




#help commands
@dp.message(Command("help"))
async def help_commands(message:Message):
    await message.answer("Familiarize yourself with bot commands:\n/start run the bot\n/help bot commands\n/about About the bot")



#about commands
@dp.message(Command("about"))
async def about_commands(message:Message):
    await message.answer("""🤩 In this bot you can get the id of any group, channel, user or bot

👨🏻‍💻 Admin: @MuslimMuslih""")


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="👥 Number of users",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Our bot has {counts[0]} users "
    await message.answer(text=text)

@dp.message(F.text=="🛫 Submit an ad",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="🛫 you can send an ad")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Advertisement was sent to  {count} users")
    await state.clear()


@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="The bot has started")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="The bot has stopped working!")
        except Exception as err:
            logging.exception(err)


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Spamdan himoya qilish uchun klassik ichki o'rta dastur. So'rovlar orasidagi asosiy vaqtlar 0,5 soniya
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))



async def main() -> None:
    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    await dp.start_polling(bot)
    setup_middlewares(dispatcher=dp, bot=bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())