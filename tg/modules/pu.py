from . import *

logger = logging.getLogger(__name__)

from ..telegram import my_eval

async def _(client, message):
    cmd = await get_cmd(client, message)
    #  asyncio.create_task(my_exec(" ".join(cmd[1:]), msg=event), name="py")
    #  await client.send_message(event.chat_id, "end")
    if cmd[0] == "pu":
        if len(cmd) == 1:
            info = '''
#.encode("ascii","backslashreplace").decode()
#.encode("unicode_escape","backslashreplace").decode()
#.encode().hex()
ascii( "" )
'''
            #          code='"""'+code+'"""'
            await cmd_answer(info, client, message)
        elif cmd[1] == "o":
            code = " ".join(cmd[2:])
            code = '"""' + code + '"""' + '''.encode("unicode_escape","backslashreplace").decode()'''
            #      asyncio.create_task(my_eval(code, msg=msg), name="my_eval")
            await my_eval(code, client=client, msg=message)
        else:
            info = ascii(" ".join(cmd[1:]))
            info = info[1:-1]
            #      await client.send_message(event.chat_id, code)
            await cmd_answer(info, client, message)
