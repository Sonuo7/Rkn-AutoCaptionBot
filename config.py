# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr

import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Rkn_Bots(object):
    
    # Rkn client config  ( required.. 😥)
    API_ID = os.environ.get("API_ID", "24139145")
    API_HASH = os.environ.get("API_HASH", "726096d9244efd78707cd468ef89d431")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # start_pic
    RKN_PIC = os.environ.get("RKN_PIC", "https://telegra.ph/file/21a8e96b45cd6ac4d3da6.jpg")

    # wes response configuration
    BOT_UPTIME = time.time()
    PORT = int(os.environ.get("PORT", "8080"))

    # force subs channel ( required.. 😥)
    FORCE_SUB = os.environ.get("FORCE_SUB", "Alsamovies") 
    
    # database config ( required.. 😥)
    DB_NAME = os.environ.get("DB_NAME", "AutoCaption")     
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://sonuoj:sonuhij@cluster0.a9dkw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # default caption 
    DEF_CAP = os.environ.get("DEF_CAP", "<b><a href='https//:t.me/Alsamovies'>{file_name} Main Telegram Channel: @Alsamovies</a></b>",
    )

    # sticker Id
    STICKER_ID = os.environ.get("STICKER_ID", "CAACAgIAAxkBAAELFqBllhB70i13m-woXeIWDXU6BD2j7wAC9gcAAkb7rAR7xdjVOS5ziTQE")

    # admin id  ( required.. 😥)
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '897584437').split()]
    

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
