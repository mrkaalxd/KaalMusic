from pyrogram import filters, Client
from pyrogram.types import Message

from modules import bot as app
from modules.helpers.decorators import errors, sudo_users_only
from modules.helpers.command import commandpro
from modules.database.dbchat import (get_served_chats, is_served_chat, add_served_chat, remove_served_chat)  


@app.on_message(commandpro(["add"]))
@errors
@sudo_users_only
async def auth_chat_func(_, message: Message):
    if len(message.commandpro) != 2:
        return await message.reply_text(
            "**usage:**\n\n/add [chat_id]"
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
        await message.reply_text("✅ Chat added to database.")
    else:
        await message.reply_text("✅ This Chat already added.")


@app.on_message(commandpro(["del"]))
@errors
@sudo_users_only
async def unauth_chat_func(_, message: Message):
    if len(message.commandpro) != 2:
        return await message.reply_text(
            "**usage:**\n\n/del [chat_id]"
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await message.reply_text("❌ This Chat not in database.")
        return
    try:
        await remove_served_chat(chat_id)
        await message.reply_text("❌ Chat removed from database.")
        return
    except Exception as e:
      await message.reply_text(f"error: `{e}`")


@app.on_message(filters.commandpro("allowedchat"))
@errors
@sudo_users_only
async def blacklisted_chats_func(_, message: Message):
    served_chats = []
    text = "💡 **allowed chats:**\n\n"
    try:
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"error: `{e}`")
        return
    count = 0
    for served_chat in served_chats:
        
        try:
            title = (await app.get_chat(served_chat)).title
        except Exception:
            title = "Private"
        count += 1
        text += f"**{count}. {title}** [`{served_chat}`]\n"
    if not text:
        await message.reply_text("❌ **no allowed chats**")  
    else:
        await message.reply_text(text) 
