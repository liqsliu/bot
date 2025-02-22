#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

@tg_exceptions_handler
async def _(event):
    "str to hex"
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
    #  await client.send_message(event.chat_id, "end")

    if cmd[0] == "hex":
        if len(cmd) == 1:
            #          code='''.encode().hex()'''
            #          code='"""'+code+'"""'
            info = '''py
c="1"
print(c.encode("unicode_escape","backslashreplace").decode()+" "+c.encode().hex())

# https://docs.python.org/zh-cn/3/library/codecs.html#text-encodings
'''
        elif cmd[1] == "help":
            info = '''r
4
u(default)'''
        elif cmd[1] == "raw":
            code = event.raw_text.split(' ', 2)[2]
            #          code='"""'+code+'"""'+'.encode().hex("\n",-4)'
            info = code.encode().hex()
        elif cmd[1] == "4":
            code = event.raw_text.split(' ', 2)[2]
            #          code='"""'+code+'"""'+'.encode().hex("\n",-4)'
            info = code.encode().hex("\n", -4)
        elif cmd[1] == "f":
            code = event.raw_text.split(' ', 2)[2]
            #          code='"""'+code+'"""'+'.encode().hex("\n",-4)'
            info = code.encode().hex("\n", -4)
        else:
            code = event.raw_text.split(' ', 1)[1]
            #          info=code.encode().hex("\n",-4)
            info = ""
            i = 0
            for c in code:
                i += 1
                if i != 1:
                    info += "\n"
#            info=info+str(i)+" "+c+" "+ c.encode("ascii","backslashreplace").decode()+" "+c.encode().hex()

#https://docs.python.org/zh-cn/3/library/codecs.html#text-encodings
#            if len(c.strip()) == 0:
                if c.isspace() and c != " ":
                    #http://tw.piliapp.com/symbol/square/
                    #              info=info+str(i)+" "+"⊠ "
                    #              info=info+str(i)+" "+"◼ "
                    info = info + str(i) + " " + "∎ "  # half
                else:
                    info = info + str(i) + " " + c + " "
#            info=info+c.encode("unicode_escape","backslashreplace").decode()+" "+c.encode().hex()
                info = info + ascii(c)[1:-1] + " " + c.encode().hex()


#    if info:
#          await myprint(str(info))
#      await client.send_message(event.chat_id, str(info))
        await cmd_answer(info, event.message)




need = need & ~CMD.is_admin
cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)
