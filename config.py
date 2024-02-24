from os import environ

API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')
ADMIN = environ.get('ADMIN', '') #seperate by id
ACCOUNT_NAME = environ.get('ACCOUNT_NAME', '') #for example: NordVPN
FORCESUB_CHANNEL = environ.get("FORCESUB_CHANNEL", "") #username without @ 
DB_URL = environ.get('DB_URL', '')
user_combos_count = {} #Leave Black
DAILY_LIMITS = environ.get("DAILY_LIMIT", "5") #default is 3

#https://github.com/XSmitX/Telegram-Account-Generator-Bot
