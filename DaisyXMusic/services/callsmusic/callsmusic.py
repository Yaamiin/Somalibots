# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Dict

from pytgcalls import GroupCallFactory

from DaisyXMusic.services.callsmusic import client
from DaisyXMusic.services.queues import queues

from DaisyXMusic.config import que

instances: Dict[int, GroupCallFactory] = {}
active_chats: Dict[int, Dict[str, bool]] = {}




def init_instance(chat_id: int):
    global que, instances, active_chats
    if chat_id not in instances:
        instances[chat_id] = GroupCall(client, input_filename='', play_on_repeat=False, enable_logs_to_console=False)
    instance = instances[chat_id]
    
    @instance.on_playout_ended
    async def when_the_music_fucking_stops(group_call, filename):
        a_chat_id = int('-100'+ f'{group_call.full_chat.id}')
        queue = que.get(a_chat_id)
        if not len(queue) == 0:
            queue.pop(0)
            if not len(queue) == 0:
                await client.send_message(a_chat_id, f'- Now Playing : **{queue[0][0]}**\n- Requested by : **{queue[0][1].mention(style="md")}**')
                group_call.input_filename = queue[0][2]
            else:
                await client.send_message(a_chat_id, 'Done Playing.')
                if a_chat_id in active_chats:
                    del active_chats[a_chat_id]
                await group_call.stop()
        else:
            await client.send_message(a_chat_id, 'Done Playing..')
            if a_chat_id in active_chats:
                del active_chats[a_chat_id]
            await group_call.stop()

def remove(chat_id: int):
    if chat_id in instances:
        del instances[chat_id]

    if not queues.is_empty(chat_id):
        queues.clear(chat_id)

    if chat_id in active_chats:
        del active_chats[chat_id]


def get_instance(chat_id: int) -> GroupCallFactory:
    init_instance(chat_id)
    return instances[chat_id]


async def start(chat_id: int):
    await get_instance(chat_id).start(chat_id)
    active_chats[chat_id] = {"playing": True, "muted": False}


async def stop(chat_id: int):
    await get_instance(chat_id).stop()

    if chat_id in active_chats:
        del active_chats[chat_id]


async def set_stream(chat_id: int, file: str):
    if chat_id not in active_chats:
        await start(chat_id)
    get_instance(chat_id).input_filename = file


def pause(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif not active_chats[chat_id]["playing"]:
        return False

    get_instance(chat_id).pause_playout()
    active_chats[chat_id]["playing"] = False
    return True


def resume(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif active_chats[chat_id]["playing"]:
        return False

    get_instance(chat_id).resume_playout()
    active_chats[chat_id]["playing"] = True
    return True


async def mute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif active_chats[chat_id]["muted"]:
        return 1

    await get_instance(chat_id).set_is_mute(True)
    active_chats[chat_id]["muted"] = True
    return 0


async def unmute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif not active_chats[chat_id]["muted"]:
        return 1

    await get_instance(chat_id).set_is_mute(False)
    active_chats[chat_id]["muted"] = False
    return 0
