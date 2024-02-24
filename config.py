bot_token="ENTER YOU BOT TOKEN HERE..."
#BOT TOKEN

api_id=000000 #--> ENter your API ID
#API ID

api_hash= "  " # --> Enter Your API HASh
#API HASh 

user_combos_count = {} # LEave Black

admin_ids = [666666666, 111111111] #--> ADMIN ID
#Owner ID

channel_username = "forcesub channel"
#FORCE SUB CHANNEL USERNAME 

account_name = "Nord Vpn"
#Name of Account.

MongoDB_Atalas_COnnection_String = "enter your connection string..."

from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from pyrogram.enums import ChatMemberStatus
from pyrogram import filters
def check_joined():
    async def func(flt, bot, message):
        join_msg = f"**To use this bot, Please join our channel.\nJoin From The Link Below 👇**"
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            member_info = await bot.get_chat_member(channel_username, user_id)
            if member_info.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                return True
            else:
                await bot.send_message(chat_id, join_msg , reply_markup=ikm([[ikb("✅ Join Channel", url= channel_username)]]))
                return False
        except Exception as e:
            await bot.send_message(chat_id, join_msg , reply_markup=ikm([[ikb("✅ Join Channel", url= channel_username)]]))
            return False

    return filters.create(func)
