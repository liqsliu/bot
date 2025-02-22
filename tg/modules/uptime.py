#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)


from ..config import SH_PATH
from ..telegram import my_popen



async def _(client, message):

    chat_id = get_chat_id(message)
    cmd = await get_cmd(client, message)
    if len(cmd) > 1:
        for j in asyncio.all_tasks():
            if cmd[1] == j.get_name():
                #  message = await client.send_message(chat_id, str(j))
                return await cmd_answer(str(j), client, message)
    tasks = []
    for j in asyncio.all_tasks():
        tasks.append(j.get_name())
    info = "queue: {}\nall tasks: {}\n{}".format(MSG_QUEUE.qsize(), len(tasks), "\n".join(tasks))
    #  message = await client.send_message(chat_id, info)
    message = await cmd_answer(info, client, message)
    message = await my_popen(cmd[0], client=client, msg=message, return_msg=True)
    #  info += await my_popen(cmd[0])
    #  message = await cmd_answer(info, client, message)
    await my_popen("{}/ns.sh {}".format(SH_PATH, 5), shell=True, msg=message, client=client)

