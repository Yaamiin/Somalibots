from pyrogram import Client
from pyrogram import idle

from DaisyXMusic import config

client1 = Client(config.SESSION_NAME1, config.API_ID1, config.API_HASH1)
client2 = Client(config.SESSION_NAME2, config.API_ID2, config.API_HASH2)

run1 = client1.run1
run2 = client2.run2
idle
