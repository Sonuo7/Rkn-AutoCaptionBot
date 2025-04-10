# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Bots
# Developer @RknDeveloperr

import motor.motor_asyncio
from config import Rkn_Bots

client = motor.motor_asyncio.AsyncIOMotorClient(Rkn_Bots.DB_URL)
db = client[Rkn_Bots.DB_NAME]
chnl_ids = db.chnl_ids
users = db.users

# Insert user data
async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
# Total User
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users

async def delete(id):
    await users.delete_one(id)

# Caption functions
async def addCap(chnl_id, caption):
    dets = {"chnl_id": chnl_id, "caption": caption}
    await chnl_ids.insert_one(dets)

async def updateCap(chnl_id, caption):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$set": {"caption": caption}})

# Remove Words functions
async def update_remove_words(chnl_id, words):
    await chnl_ids.update_one(
        {"chnl_id": chnl_id},
        {"$set": {"remove_words": words}},
        upsert=True
    )

async def get_remove_words(chnl_id):
    doc = await chnl_ids.find_one({"chnl_id": chnl_id})
    return doc.get("remove_words", []) if doc else []

async def clear_remove_words(chnl_id):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$unset": {"remove_words": ""}})
