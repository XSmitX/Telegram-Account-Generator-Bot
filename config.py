from os import environ

API_ID = int(environ.get('API_ID', '1455678'))
API_HASH = environ.get('API_HASH', 'a6b02f54dab5607e542eb216f28a1e6d')
BOT_TOKEN = environ.get('BOT_TOKEN', '1643063196:AAElqqVI2O8oEqGWyXK35SLaFc5K0rrokig')
ADMIN = environ.get('ADMIN', '1111214141') #seperate by id
ACCOUNT_NAME = environ.get('ACCOUNT_NAME', 'NordVPN') 
FORCESUB_CHANNEL = environ.get("FORCESUB_CHANNEL", "nordvpn_1") #username without @ 
DB_URL = environ.get('DB_URL', 'mongodb+srv://whatsappbot:WbFWxnSrzNvXMzAA@whatsappbot.n058qik.mongodb.net/?retryWrites=true&w=majority')
user_combos_count = {} #Leave Black
DAILY_LIMITS = environ.get("DAILY_LIMIT", "5")

#https://github.com/XSmitX/Telegram-Account-Generator-Bot