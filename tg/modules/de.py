from . import *

from ..utils.tools import ennum, denum, denum_auto, chr_list, enstr, destr, http, pastebin, ipfs_add

logger = logging.getLogger(__name__)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

async def _(client, message):
    "str to space or num to sapce, or reverse"
    cmd = await get_cmd(client, message)
    if len(cmd) == 1:
        info = "de [d] $spaces"
        info += "\nde e $str"
        info += "\nde nd $spaces"
        info += "\nde ne $num"
        sender_id = get_sender_id(message)
        if sender_id == MY_ID:
            s = "\n"
            for i in range(len(chr_list)):
                s += "\n{}{}".format(i, ascii(chr_list[i])[1:-1])
            info += s
            info += "\n\nall: "+str(len(chr_list))

    elif cmd[1] == "ne":
        if cmd[2].isnumeric():
            info = ennum(int(cmd[2]))
        else:
            info += "need a number"
    elif cmd[1] == "nd":
        #  info = denum(cmd[2])
        info = denum_auto(" ".join(cmd[2:]))
        if info is not None:
            info = '"{}"'.format(info)
    elif cmd[1] == "e":
        info = enstr(" ".join(cmd[2:]))
        message = await cmd_answer(info, client, message)
        if info is not None:
            info = '"{}"'.format(info)
    elif cmd[1] == "d":
        info = destr(" ".join(cmd[2:]))
    elif cmd[1].startswith("aesgcm://"):
        url = cmd[1]
        keys = url.split("#")[1]
        url = url.split("#")[0]

        file_url = "https://" + url[9:]

        nonce = keys[:24]
        key = keys[24:]
        key = bytes.fromhex(key)
        aesgcm = AESGCM(key)
        nonce = bytes.fromhex(nonce)

        logger.info(key, nonce, file_url)

        ct = await http(file_url)
        logger.info(type(ct))
        from ..utils.tools import aes_decrypt_file as df
        res = df(key, nonce, ct)
        res_url = await pastebin(res, filename=file_url.split("/")[-1])

    elif cmd[1].startswith("iiiiaesgcm://"):
        # https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM
        url = cmd[1]
        keys = url.split("#")[1]
        url = url.split("#")[0]

        file_url = "https://" + url[9:]

        nonce = keys[:24]
        key = keys[24:]
        key = bytes.fromhex(key)
        aesgcm = AESGCM(key)
        nonce = bytes.fromhex(nonce)
        aad = None

        logger.info(file_url)
        ct = await http(file_url)
        logger.info(type(ct))
        add = ct[-16:]
        ct = ct[:-16]

        res = aesgcm.decrypt(nonce, ct, aad)
        res_url = await pastebin(res, filename=file_url.split("/")[-1])

    else:
        info = destr(" ".join(cmd[1:]))
    message = await cmd_answer(info, client, message)

need = need & ~CMD.is_me
