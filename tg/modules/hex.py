from . import *

logger = logging.getLogger(__name__)

async def _(client, message):
    "str to hex"
    cmd = await get_cmd(client, message)
    #  asyncio.create_task(my_exec(" ".join(cmd[1:]), msg=message), name="py")
    #  await client.send_message(message.chat_id, "end")

    if cmd[0] == "hex":
        if len(cmd) == 1:
            info = '''str to hex
--
id char unicode utf-8'''
        elif cmd[1] == "help":
            info = '''
py
c="1"
print(c.encode("unicode_escape","backslashreplace").decode()+" "+c.encode().hex())

# https://docs.python.org/zh-cn/3/library/codecs.html#text-encodings
'''
        elif cmd[1] == "raw":
            code = " ".join(cmd[2:])
            info = code.encode().hex()
        elif cmd[1] == "4":
            code = " ".join(cmd[2:])
            info = code.encode().hex("\n", -4)
        elif cmd[1] == "f":
            code = " ".join(cmd[2:])
            info = code.encode().hex("\n", -4)
        else:
            code = " ".join(cmd[1:])
            info = ""
            i = 0
            for c in code:
                i += 1
                if i != 1:
                    info += "\n"
#            info=info+str(i)+" "+c+" "+ c.encode("ascii","backslashreplace").decode()+" "+c.encode().hex()
#https://docs.python.org/zh-cn/3/library/codecs.html#text-encodings
                if c.isspace() and c != " ":
                    #              info=info+str(i)+" "+"⊠ "
                    #              info=info+str(i)+" "+"◼ "
                    info = info + str(i) + " " + "∎ "  # half
                else:
                    info = info + str(i) + " " + c + " "
                info = info + ascii(c)[1:-1] + " " + c.encode().hex()


        await cmd_answer(info, client, msg=message)


need = need & ~CMD.is_me
