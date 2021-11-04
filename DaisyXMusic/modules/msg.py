from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import sudo_users_only, authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("days", 60 * 60 * 24),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 𝙃𝙀𝙇𝙇𝙊 𝙏𝙃𝙀𝙍𝙀 {message.from_user.mention}</b> ❗ 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙈𝙔 𝘽𝙊𝙏💞

𝙏𝙃𝙄𝙎 𝙄𝙎 𝘼 𝘽𝙊𝙏 𝘿𝙀𝙎𝙄𝙂𝙉𝙀𝘿 𝙏𝙊 𝙋𝙇𝘼𝙔 𝙈𝙐𝙎𝙄𝘾 𝙄𝙉 𝙔𝙊𝙐𝙍 𝙂𝙍𝙊𝙐𝙋𝙎!

𝙏𝙃𝙄𝙎 𝙄𝙎 𝘼 𝙋𝙍𝙄𝙑𝘼𝙏𝙀 𝙋𝙍𝙊𝙅𝙀𝘾𝙏 𝙊𝙁 [Wʜɪᴛᴇʜᴀᴛ](https://t.me/Somaliprogrammer)....𝙈𝘼𝘿𝙀 𝙒𝙄𝙏𝙃 ❤️

𝙃𝙀𝙍𝙀 𝘼𝙍𝙀 𝙎𝙊𝙈𝙀 𝘾𝙈𝘿𝙎 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏, 𝘾𝙇𝙄𝘾𝙆 » **/help**""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ ᴋᴜ ᴅᴀʀsᴏ ɢʀᴏᴜᴘᴋᴀᴅᴀ 📛 ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "​​Oᴡɴᴇʀ 🥀", url="https://t.me/@Somaliprogrammer"
                    ),
                    InlineKeyboardButton(
                        "Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ 👥", url=f"https://t.me/{GROUP_SUPPORT}")
                ],[
                    InlineKeyboardButton(
                        "❓Hᴏᴡ Tᴏ Usᴇ Mᴇ​ ❓​", callback_data="cbguide"
                    )
                ]
            ]
        ),
     disable_web_page_preview=False
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    delta_ping = time() - start
    await message.reply_text(
        f"""<b>☺️ **𝙃𝙀𝙇𝙇𝙊 {message.from_user.mention()}** ❗</b>

✅ **𝙔𝙊,𝙄𝘼𝙈 𝘼𝙇𝙄𝙑𝙀 𝙓𝘿!
• Start time: `{START_TIME_ISO}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 𝙎𝙐𝙋𝙋𝙊𝙍𝙏", url=f"https://t.me/{GROUP_SUPPORT}"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>☺️ 𝙃𝙚𝙮 𝙔𝙤𝙤.. {message.from_user.mention()}</b>
**Please press the button below to read the explanation and see the list of available commands !**

🥀 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" Hᴏᴡ Tᴏ Usᴇ Mᴇ", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>😇 **Hᴇʟʟᴏ {message.from_user.mention} welcome to the help menu !**</b>

**__In this menu you can open several available command menus, in each command menu there is also a brief explanation of each command__**

🦄 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝙃𝙀𝙇𝙋", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("`Pinging...`")
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    delta_ping = time() - start
    await m_reply.edit_text(
        "**Pong !!**\n" 
        f"**Time taken:** `{delta_ping * 1000:.3f} ms`\n"
        f"**Service uptime:** `{uptime}`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
