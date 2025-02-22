#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
#from ..bot import *

from . import *

logger = logging.getLogger(__name__)

import base64
from ..utils.tools import encode_base64, decode_base64



async def _(client, message):
    "base64"
    cmd = await get_cmd(client, message)
    if len(cmd) == 1:
        info = "ba d str\nbs e str\nbs fp\nbs fu\nbs b\naltchars: +/"
    elif cmd[1] == "b":
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
        info = encode_base64(" ".join(cmd[2:]))
    elif cmd[1] == "d":
        if len(cmd) > 2 and len(cmd[1]) == 2:
            altchars = cmd[1].encode()
        else:
            altchars = None
        # info = base64.b64decode( (" ".join(cmd[2:])).encode() + b'=' * (-len(event.text.split(' ', 2)[2].encode()) % 4)).decode()
        try:
          info = base64.b64decode((" ".join(cmd[2:])).encode() + b'=' * (-len(" ".join(cmd[2:]).encode()) % 4)).decode()
        except UnicodeDecodeError as e:
          info = base64.b64decode((" ".join(cmd[2:])).encode() + b'=' * (-len(" ".join(cmd[2:]).encode()) % 4))
          info = str(info)
    else:
        data = decode_base64(" ".join(cmd[1:]))
        try:
            info = data.decode()
        except UnicodeDecodeError as e:
            pass
        try:
            info = data.decode(errors="replace")
            info += f"\n====\nE: {e=}"
        except UnicodeDecodeError as e:
          info = str(data)

    await cmd_answer(info, client, msg=message)




need = need & ~CMD.is_me
