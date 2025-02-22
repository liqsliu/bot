from . import *

from .telegram import cmd_answer

logger = logging.getLogger(__name__)
mp = logger.info


async def _(client, message):
    "pong"
    text = message.text
    mp("cmd {}: {}".format(
        __name__.split(".")[-1], text))
    await message.reply("pong")
    return
    await cmd_answer("pong", client, message)
    await cmd_answer(dir(message), client, message)
    print(message.__dict__)
    return
    print(dict(message))
    await cmd_answer(str(dict(message)), client, message)


need = CMD.is_new
need += CMD.is_text
need += CMD.is_me

forbid = CMD.is_bot
forbid += CMD.is_out
forbid += CMD.is_not_mentioned_in_group




cmd = __name__.split(".")[-1]

need = need & ~CMD.is_me

CMD.add(_, cmd=cmd, need=need, forbid=forbid)




from .telegram import put
put("put ok")

async def _(client, message):
    "pong"
    text = message.text
    mp("cmd {}: {}".format(
        __name__.split(".")[-1], text))

    if text[0] == "@":
        text = text[1:]
        m = await client.get_chat(text)
    else:
        m = await client.get_chat(int(text))
    # m = await client.get_users(int(text))
    print(m)
    await message.reply(str(m))
    put("put ok")
    

need = CMD.is_new
need += CMD.is_text
need += CMD.is_me
need += CMD.is_private

forbid = CMD.is_bot
forbid += CMD.is_out
forbid += CMD.is_not_mentioned_in_group

cmd = None

CMD.add(_, cmd=cmd, need=need, forbid=forbid)



