#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
#from ..bot import *

from . import *

logger = logging.getLogger(__name__)
mp = logger.info

import base64
from ..utils.tools import encode_base64, decode_base64

#pattern=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( [.\n]*)?$')
#pattern_bot=re.compile(r'^(/|\.)?'+ __name__.split('.')[-1] + r'(@'+BOT_NAME+r')?( |$)')


async def _(event):
    "base64"
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    client = event.client
    #  await send_msg_to_mt(event)
    #  await run_cmd_for_bots(event)
    #    mp("get msg: "+event.raw_text)
    #    await run_task_for_event(event)
    #    await event.reply("pong")
    #  await UB.send_message(MY_ID, "ok")

    #  await my_popen(event.raw_text.lstrip("./"), msg=event)
    cmd = await get_cmd(event)
    #  asyncio.create_task(my_exec(" ".join(cmd[1:]), msg=event), name="py")
    #  await my_exec(" ".join(cmd[1:]), msg=event.message)
    #  await client.send_message(event.chat_id, "end")

#    if cmd[0] == "bs":
    if len(cmd) == 1:
        info = "data:;charset=utf8;base64,SGVsbG8gV29ybGQg8J+Qtg=="
    elif cmd[1] == "fp":
        info = """
def f(msg):
#  import base64
#  info=base64.b64decode(msg.encode()).decode()
import base64
import re
altchars=b'+/'
data=msg.encode()
data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
missing_padding = len(data) % 4
if missing_padding:
data += b'='* (4 - missing_padding)
info=base64.b64decode(data, altchars).decode()
print(info)

f('''  ''')

"""
    elif cmd[1] == "fu":
        info = """
def f(msg):
#  import base64
#  info=base64.b64decode(msg.encode()).decode()
import base64
import re
altchars=b'+/'
data=msg.encode()
data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
missing_padding = len(data) % 4
if missing_padding:
data += b'='* (4 - missing_padding)
info=base64.b64decode(data, altchars).decode()
print(info.encode("ascii","backslashreplace").decode())

f('''  ''')

"""
    elif cmd[1] == "e":
        #          info=base64.b64encode(event.raw_text.split(' ',2)[2].encode()).decode()
        info = encode_base64(" ".join(cmd[2:]))
    elif cmd[1] == "d":
        #          info=decode_base64(event.raw_text.split(' ',2)[2]).decode()
        #          info=base64.b64decode(event.raw_text.split(' ',2)[2].encode()).decode()
        info = base64.b64decode(
            (" ".join(cmd[2:])).encode() + b'=' *
            (-len(event.raw_text.split(' ', 2)[2].encode()) % 4)).decode()
    else:
        #          import base64
        #          info=base64.b64decode(event.raw_text.split(' ',1)[1].encode()).decode()
        #          info=base64.b64decode(event.raw_text.split(' ',1)[1].encode() + b'=' * (-len(event.raw_text.split(' ',1)[1].encode()) % 4)).decode()
#        info = decode_base64(event.raw_text.split(' ', 1)[1]).decode()
        info = decode_base64(" ".join(cmd[1:])).decode()

    await cmd_answer(info, event.message)







need = need & ~CMD.is_admin
cmd = __name__.split(".")[-1]

CMD.add(_, cmd=cmd, need=need, forbid=forbid)
