from pyrogram import Client, filters
import os
from config import bot_token, api_hash, api_id, check_joined, user_combos_count, admin_ids, account_name, channel_username
from database import collection

bot = Client(
    "TesTBoTt",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash
)


@bot.on_message(filters.command('start') & filters.private & check_joined())
async def start(bot, message):
    await bot.send_message(message.chat.id,
                           f"""<b> Hi {message.from_user.first_name} </b>,
                           \n<b>I am an Account Generator Bot</b>
                           \n<b>I can provide premium accounts of different services</b>
                           \n<b>Do /gen to generate an account</b>
                           \n\n❤️<b>Brought to You By @PandaZnetwork || Made by </b>@MrXed_bot❤️

                           \n Do /help if you want to contact me.. 
                           """)


@bot.on_message(filters.command('addhits') & filters.private)
async def add_hits(bot, message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.chat.id, "Only admin can add hits.")
        await bot.send_message(message.chat.id , "🤷‍♂️")
        return

    # Get the replied message containing hits
    replied_message = message.reply_to_message
    if not replied_message or not replied_message.text:
        await bot.send_message(message.chat.id, "Please reply to a message containing email:password combinations.")
        return
    lion = await bot.send_message(message.chat.id , "🦁")
    AddingAccountsMsg = await bot.send_message(message.chat.id, "<code>Adding Accounts in DB.. </code>")
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

@bot.on_message(filters.command('removehits') & filters.private)
async def remove_hits(bot, message):
    if message.from_user.id not in admin_ids:
        await bot.send_message(message.chat.id, "Only admin can remove hits.")
        return

    collection.delete_many({})
    await bot.send_message(message.chat.id, "All hits have been removed.")

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
        limit = 3

    # Check if user has reached the limit
    if user_combos_count[user_id] >= limit:
        if limit == float('inf'):
            await bot.send_message(message.chat.id, "Admins have no limit for account generation.")
        else:
            await bot.send_message(message.chat.id, "You have reached your limit of 3 generated accounts.")
        return

    # Retrieve and delete the first combo from the database
    combo = collection.find_one_and_delete({})
    if combo:
        user_combos_count[user_id] += 1
        await bot.send_message(message.chat.id, f" 𝙃𝙚𝙧𝙚 𝙄𝙨 𝙔𝙤𝙪𝙧 {account_name} 𝘼𝙘𝙘𝙤𝙪𝙣𝙩\n\n𝙀𝙢𝙖𝙞𝙡: `{combo['email']}`\n𝙋𝙖𝙨𝙨: `{combo['password']}` \n𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙 𝘽𝙮: {message.from_user.first_name} \n\n𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙢𝙚!\n ❤️𝙎𝙝𝙖𝙧𝙚 & 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 {channel_username}❤️")
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

bot.run()
