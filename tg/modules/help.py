from . import *


from ..telegram import set_bot_cmd, get_chat_id


async def _(client, message):
    "print help info and all cmd"
    if client.bot_token is not None:
        await set_bot_cmd(client, message)
    chat_id = get_chat_id(message)
    if chat_id == MY_ID:
        info = await CMD.print_cmd()
    else:
        info = await CMD.list_cmd(client, message)
    await cmd_answer(info, client, message)



need = need ^ CMD.is_me


CMD.add(_, "start", need, forbid)

CMD.add(_, "cmd", need, forbid)
