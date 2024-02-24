import os
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from config import API_HASH, API_ID, BOT_TOKEN, user_combos_count, ACCOUNT_NAME, FORCESUB_CHANNEL, ADMIN, DAILY_LIMITS
from database import collection

DAILY_LIMIT = int(DAILY_LIMITS)
bot = Client('Telegram Account Gen bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)

admin_ids = [int(admin_id) for admin_id in ADMIN.split(',')]
        
def check_joined():
    async def func(flt, bot, message):
        join_msg = f"**To use this bot, Please join our channel.\nJoin From The Link Below 👇**"
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            member_info = await bot.get_chat_member(FORCESUB_CHANNEL, user_id)
            if member_info.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                return True
            else:
                join_url = f"https://t.me/{FORCESUB_CHANNEL}"
                await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url=join_url)]]))
                return False
        except Exception as e:
            join_url = f"https://t.me/{FORCESUB_CHANNEL}"
            await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url=join_url)]]))
            return False

    return filters.create(func)

@bot.on_message(filters.command('start') & filters.private & check_joined())
async def start(bot, message):
    inline_keyboard = ikm(
        [
            [
                ikb("♻️ Source Code", url="https://github.com/XSmitX/Telegram-Account-Generator-Bot")
            ]
        ]
    )
    await bot.send_message(message.chat.id,
                           f"""<b>Hi {message.from_user.first_name}</b>,\n\n<b>I am an Account Generator Bot</b>\n<b>I can provide premium accounts of different services</b>\n<b>Click on /gen to generate accounts.</b>\n\n❤️<b>Brought to You By {FORCESUB_CHANNEL}❤️""" , reply_markup=inline_keyboard)

  
@bot.on_message(filters.command('addhits') & filters.private)
async def add_hits(bot, message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.chat.id, "Only admin can add hits.")
        await bot.send_message(message.chat.id , "🤷‍♂️")
        return

    # Get the replied message containing hits
    replied_message = message.reply_to_message
    if not replied_message or not replied_message.text:
        await bot.send_message(message.chat.id, "**Please reply to a message containing email:password combinations.**")
        return
    lion = await bot.send_message(message.chat.id , "🦁")
    AddingAccountsMsg = await bot.send_message(message.chat.id, "**Adding Accounts in DB..**")
    # Get text from the replied message
    combos_text = replied_message.text.split("\n")

    # Filter and store email:password combos
    for combo in combos_text:
        if ":" in combo:
            email, password = combo.split(":")
            combo_dict = {"email": email.strip(), "password": password.strip()}
            collection.insert_one(combo_dict)

    # Send confirmation message
    await AddingAccountsMsg.delete()
    await bot.send_message(message.chat.id, f"You have added {len(combos_text)} combos.")
    await lion.delete()

@bot.on_message(filters.command('remhits') & filters.private)
async def remove_hits(bot, message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.chat.id, "**Only admin can remove hits.**")
        return

    collection.delete_many({})
    await bot.send_message(message.chat.id, "**All hits have been removed.**")

@bot.on_message(filters.command('gen') & filters.private & check_joined())
async def generate_account(bot, message):
    user_id = message.from_user.id

    # Check if user's combo count exists, if not set to 0
    if user_id not in user_combos_count:
        user_combos_count[user_id] = 0

    # Check if user is an admin
    if user_id in admin_ids:
        limit = float('inf')
    else:
        limit = DAILY_LIMIT
    # Check if user has reached the limit
    if user_combos_count[user_id] >= limit:
        if limit == float('inf'):
            await bot.send_message(message.chat.id, "**Admins have no limit for account generation.**")
        else:
            await bot.send_message(message.chat.id, f"**You have reached your limit of {DAILY_LIMIT} generated accounts.Now come again tommorow.**")
        return

    # Retrieve and delete the first combo from the database
    combo = collection.find_one_and_delete({})
    if combo:
        user_combos_count[user_id] += 1
        await bot.send_message(message.chat.id, f"**Here is Your {ACCOUNT_NAME} Account\n\nEmail: `{combo['email']}`\nPass: `{combo['password']}` \nGenerated By: {message.from_user.first_name} \n\nThanks For Using Me!\n❤️ Share And Support @{FORCESUB_CHANNEL}❤️**")
    else:
        await bot.send_message(message.chat.id , "😢")
        await bot.send_message(message.chat.id, "No more accounts available.")


@bot.on_message(filters.command('hits') & filters.private)
async def hits(bot, message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.chat.id, "Only admin can check hits.")
        return
    
    Panda = await bot.send_message(message.chat.id , "🐼")
    # Count total hits
    total_hits = collection.count_documents({})

    # Create a text file with hits
    with open("hits.txt", "w") as file:
        for account in collection.find():
            file.write(f"{account['email']}:{account['password']}\n")

    # Send the text file
    await bot.send_document(message.chat.id, document="hits.txt", caption=f"Total Hits: {total_hits}")
    await Panda.delete()

    # Delete the text file
    os.remove("hits.txt")


@bot.on_message(filters.command('help') & filters.private)
async def help(bot,message):
    await bot.send_message(message.chat.id , "<b>Any issue please contact @mrxed_bot</b>")

print ('Started... Contact for any support to https://t.me/mrxed')
bot.run()
