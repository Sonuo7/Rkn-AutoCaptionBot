# (c) @RknDeveloperr
# Telegram Channel @RknDeveloper & @Rkn_Bots

from pyrogram import Client, filters, errors, types
from config import Rkn_Bots
import asyncio, re, time, sys, os
from .database import total_user, getid, delete, addCap, updateCap, insert, chnl_ids, get_remove_words, update_remove_words, clear_remove_words
from pyrogram.errors import FloodWait

# -- ADMIN COMMANDS --

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["rknusers"]))
async def all_db_users_here(client, message):
    start_t = time.time()
    rkn = await message.reply_text("Processing...")
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
    total_users = await total_user()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rkn.edit(
        f"**--Bot Processed--** \n\n**Bot Started UpTime:** {uptime} \n"
        f"**Bot Current Ping:** `{time_taken_s:.3f} ᴍꜱ` \n**All Bot Users:** `{total_users}`"
    )

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if message.reply_to_message:
        rkn = await message.reply_text("Bot Processing.\nI am checking all bot users.")
        all_users = await getid()
        tot = await total_user()
        success = failed = deactivated = blocked = 0
        await rkn.edit("Broadcasting started...")
        async for user in all_users:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated += 1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked += 1
                await delete({"_id": user['_id']})
            except:
                failed += 1
                await delete({"_id": user['_id']})
                pass
            try:
                await rkn.edit(
                    f"<u>Broadcasting</u>\n\n• Total: {tot}\n• Success: {success}"
                    f"\n• Blocked: {blocked}\n• Deleted: {deactivated}\n• Failed: {failed}"
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
        await rkn.edit(
            f"<u>Broadcast Completed</u>\n\n• Total: {tot}\n• Success: {success}"
            f"\n• Blocked: {blocked}\n• Deleted: {deactivated}\n• Failed: {failed}"
        )

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    msg = await b.send_message("**Restarting...**", chat_id=m.chat.id)
    await asyncio.sleep(3)
    await msg.edit("**✅ Restarted**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# -- START --

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, message):
    user_id = int(message.from_user.id)
    await insert(user_id)
    await message.reply_photo(
        photo=Rkn_Bots.RKN_PIC,
        caption=(
            f"<b>Hey, {message.from_user.mention}\n\nI'm an auto-caption bot. "
            f"I edit captions for videos, audio files, and documents posted on channels.\n\n"
            f"Use <code>/set_caption</code> to set a caption\nUse <code>/delcaption</code> to delete.\n\n"
            f"Note: Commands work in channels only.</b>"
        ),
        reply_markup=types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton('Main Channel', url='https://t.me/Alsamovies'),
            types.InlineKeyboardButton('Help Group', url='https://t.me/Alsamovies')
        ], [
            types.InlineKeyboardButton('🔥 Source Code 🔥', url='https://t.me/+gnEoVsO3kmc4MzVl')
        ]])
    )

# -- CAPTION COMMANDS --

@Client.on_message(filters.command("set_caption") & filters.channel)
async def setCaption(bot, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /set_caption Your caption here (you can use {file_name}, etc)")
    chnl_id = message.chat.id
    caption = message.text.split(" ", 1)[1]
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
    if chkData:
        await updateCap(chnl_id, caption)
    else:
        await addCap(chnl_id, caption)
    await message.reply(f"Caption updated:\n\n`{caption}`")

@Client.on_message(filters.command(["delcaption", "del_caption", "delete_caption"]) & filters.channel)
async def delCaption(_, msg):
    chnl_id = msg.chat.id
    try:
        await chnl_ids.delete_one({"chnl_id": chnl_id})
        return await msg.reply("Caption deleted. Default will be used.")
    except Exception as e:
        rkn = await msg.reply(f"Error: {e}")
        await asyncio.sleep(5)
        await rkn.delete()

# -- REMOVE WORDS --

@Client.on_message(filters.command("remove_word") & filters.channel)
async def set_remove_words(bot, message):
    if len(message.command) < 2:
        return await message.reply("Send words like: `/remove_word 720p, x264, Hindi`")
    chnl_id = message.chat.id
    word_list = [w.strip().lower() for w in message.text.split(" ", 1)[1].split(",") if w.strip()]
    await update_remove_words(chnl_id, word_list)
    await message.reply(f"These words will now be removed: {', '.join(word_list)}")

@Client.on_message(filters.command("rmw_off") & filters.channel)
async def remove_words_off(bot, message):
    chnl_id = message.chat.id
    await clear_remove_words(chnl_id)
    await message.reply("Word removal disabled.")

# -- UTILS --

def extract_language(file_name):
    pattern = r'\b(Hindi|English|Tamil|Bhojpuri|Nepali|Punjabi|Telugu|Malayalam|Kannada|Korean|Chinese|Japanese|Jap|Hin|Eng|Kor)\b'
    return ", ".join(sorted(set(re.findall(pattern, file_name, re.IGNORECASE)), key=str.lower)) or "Unknown"

def extract_year(file_name):
    match = re.search(r'\b(19\d{2}|20\d{2})\b', file_name)
    return match.group(1) if match else None

def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    size = float(size)
    i = 0
    while size >= 1024 and i < len(units) - 1:
        i += 1
        size /= 1024
    return "%.2f %s" % (size, units[i])

def extract_quality(file_name):
    match = re.search(r"(\d{3,4}p)", file_name)
    return match.group(1) if match else "Unknown"

def extract_resolution(file_name):
    options = ["WEBRip", "WEB-Rip", "WEB DL", "WEB-DL", "BluRay", "HDRip", "HDTV", "DVDRip", "CAMRip", "TS", "SDTV"]
    for res in options:
        if res.lower() in file_name.lower():
            return res
    return "Unknown"

def remove_words(text, word_list):
    for word in word_list:
        text = re.sub(rf'\b{re.escape(word)}\b', '', text, flags=re.IGNORECASE)
    return ' '.join(text.split())

# -- AUTO EDIT CAPTION --

@Client.on_message(filters.channel)
async def auto_edit_caption(bot, message):
    chnl_id = message.chat.id
    if message.media:
        for ftype in ("video", "audio", "document", "voice"):
            obj = getattr(message, ftype, None)
            if obj and hasattr(obj, "file_name"):
                file_name = obj.file_name.replace("_", " ").replace(".", " ")
                file_size = get_size(obj.file_size) if hasattr(obj, "file_size") else "Unknown"
                quality = extract_quality(file_name)
                resolution = extract_resolution(file_name)
                language = extract_language(file_name)
                year = extract_year(file_name)

                cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                caption = message.caption if message.caption else file_name

                # Word removal
                remove_list = await get_remove_words(chnl_id)
                file_name = remove_words(file_name, remove_list)
                caption = remove_words(caption, remove_list)

                try:
                    if cap_dets and "caption" in cap_dets:
                        cap = cap_dets["caption"]
                        replaced_caption = cap.format(
                            file_name=file_name,
                            caption=caption,
                            language=language,
                            year=year,
                            file_size=file_size,
                            quality=quality,
                            resolution=resolution
                        )
                    else:
                        replaced_caption = Rkn_Bots.DEF_CAP.format(
                            file_name=file_name,
                            caption=caption,
                            language=language,
                            year=year,
                            file_size=file_size,
                            quality=quality,
                            resolution=resolution
                        )
                    await message.edit(replaced_caption)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                continue
    return
