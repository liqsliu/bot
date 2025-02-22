# connect to matterbridge api

import socket

from .tools import SH_PATH, http_exceptions_handler, http, my_exceptions_handler

from .config import cid_wtfipfs, cid_ipfsrss, cid_tw, cid_ipfsrss, cid_btrss, cid_fw
from .config import MT_GATEWAY_LIST, MT_GATEWAY_LIST_for_tg

from .telegram import tg_exceptions_handler
from .telegram import MSG_QUEUE, put
from .telegram import MAX_MSG_LEN
from .telegram import MAX_MSG_LINE

from .telegram import get_peer
from .telegram import put

#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG

#from .. import *
from ..bot import *
#from .config import cid_wtfipfs, cid_ipfsrss, cid_tw

#import logging
logger = logging.getLogger(__name__)
mp = logger.warning

#from .config import MT_GATEWAY_LIST
#from .config import MT_GATEWAY_LIST_for_tg

#from .telegram import get_peer, my_popen

import asyncio

import json
import traceback

#from telethon.errors import FloodWaitError

#from urllib.parse import urlencode
#import urllib.request.Request

import urllib
import urllib.request
import urllib.error


class MTReadProtocol(asyncio.Protocol):
    # https://docs.python.org/zh-cn/3.8/library/asyncio-protocol.html#tcp-echo-client
    #  def __init__(self, message, on_con_lost, msgq, loop):
    def __init__(self, message, on_con_lost, loop, queue):
        self.message = message
        self.on_con_lost = on_con_lost
        #    self.msgq = msgq
        self.loop = loop
        self.queue = queue

    def connection_made(self, transport):
        logger.warning("connected")
        transport.write(self.message.encode())
        #    print('Data sent: {!r}'.format(self.message))
        logger.info('Data sent: {!r}'.format(self.message))

    def data_received(self, data):

        #    await self.msgq.put(data)

        logger.info('Data received: {!r}'.format(data))
        #    self.loop.create_task(self.msgq.put(data), name="send_msg_queue")
        #    self.loop.call_soon_threadsafe(self.msgq.put, data)
        #    future = asyncio.run_coroutine_threadsafe(self.msgq.put(data), self.loop)
        #    result = future.result()
        #    self.loop.create_task(MSG_QUEUE.put(["mt_msg", data]), name="send_mt_msg_to_queue")

        #      data=await mt_msg_to_tg_msg(data)
        #    self.loop.create_task(self.queue.put(["mt_msg", data]), name="send_mt_msg_to_queue")
        self.loop.create_task(send_mt_msg_to_queue(data, self.queue),
                              name="send_mt_msg_to_queue")

        #    mp("result: {}".format(result))
        logger.info("exit")

    def connection_lost(self, exc):
        msg = 'The server closed the connection'
        logger.warning(msg)
        self.on_con_lost.set_result(True)


@my_exceptions_handler
async def mt_read(queue):
    # out for tg
    MT_API_TG = "127.0.0.1:4245"

    url = "http://" + MT_API_TG + "/api/stream"
    host = MT_API_TG.split(":")[0]
    port = int(MT_API_TG.split(":")[1])

    path = "/" + url.split("/", 3)[3]
    query = (f"GET {path} HTTP/1.1\r\n"
             f"Host: {host}\r\n"
             f"\r\n")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    #  MAX_SIZE_OF_QUEUE=64
    #  msgq=asyncio.Queue(MAX_SIZE_OF_QUEUE)

    #  asyncio.create_task(send_mt_msg_to_tg(), name="send_mt_msg_to_tg")
    #  asyncio.create_task(send_mt_msg_to_tg(msgq), name="mt_msg_to_tg")

    #  message = 'Hello World!'
    message = query
    while True:
        try:
            on_con_lost = loop.create_future()

            transport, protocol = await loop.create_connection(
                lambda: MTReadProtocol(message, on_con_lost, loop, queue),
                host, port)
        except asyncio.exceptions.InvalidStateError:
            print("connect fail, invalid")
            await asyncio.sleep(5)
            continue
        except ConnectionRefusedError:
            mp("wait for api...")
            await asyncio.sleep(5)
            continue
        except:
            print("connect fail, unknown error")
            await asyncio.sleep(5)
            continue

    #  asyncio.create_task(send_mt_msg(msg))

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
        try:
            await on_con_lost
        except:
            pass
            print("connection error")
        finally:
            transport.close()
            print("connection closed")
        await asyncio.sleep(5)


async def mt_read_bu():
    url = "http://" + MT_API + "/api/stream"

    host = MT_API.split(":")[0]
    port = int(MT_API.split(":")[1])
    path = "/" + url.split("/", 3)[3]
    reader, writer = await asyncio.open_connection(host, port)
    query = (f"GET {path} HTTP/1.1\r\n"
             f"Host: {host}\r\n"
             f"\r\n")
    #  writer.write(query.encode('latin-1'))
    writer.write(query.encode("utf-8"))
    while True:
        try:
            line = await reader.readline()
#    except CancelledError:
#      print('CancelledError')
        except:
            print('unknown Error')
            await asyncio.sleep(3)
        if not line:
            break


#    line = line.decode('latin1').rstrip()
        line = line.decode('utf-8').rstrip()
        print(line)
    print('Close the connection')
    writer.close()
    await writer.wait_closed()



@my_exceptions_handler
async def mt_read(queue):
    # msg from mt to tg

    MT_API_TG = "127.0.0.1:4245"
    url = "http://" + MT_API_TG + "/api/stream"
    from .tools import init_aiohttp_session
    session = await init_aiohttp_session()
    from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError
    while True:
        try:
            async with session.get(url, timeout=0) as resp:
                await NB.send_message(MY_ID, "mt connected")
        #        resp.content.read()
                async for line in resp.content:
                    await send_mt_msg_to_queue(line, queue)
        except ClientPayloadError:
            logger.warning("mt closed")
#                from .telegram import put
#                put("mt closed")
            await NB.send_message(MY_ID, "mt closed")
        except ClientConnectorError:
            logger.warning("wait for mt...")
        await asyncio.sleep(5)



#@http_exceptions_handler
@my_exceptions_handler
async def mt_send(text="null", username="C bot", gateway="gateway1", qt=None):

    # in for all
    MT_API = "127.0.0.1:4240"
    # send msg to matterbridge
    url = "http://" + MT_API + "/api/message"

    #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
    #  url="http://127.0.0.1:5555/api/message"

#    if not username.startswith("C "):
#        username = "T " + username


    if qt:
        username = "{}\n\n{}".format("> " + "\n> ".join(qt.splitlines()), username)


#  gateway="gateway0"
    data = {
        "text": "{}".format(text),
        "username": "{}".format(username),
        "gateway": "{}".format(gateway)
    }
    data = json.dumps(data).encode()
    logger.debug(data)
    req = urllib.request.Request(url, data)
    req.add_header("Content-Type", "application/json")
    req.add_header('User-agent', 'Chrome Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) Apple    WebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')
    with urllib.request.urlopen(req, timeout=8) as res:
        res = res.read().decode()
        logger.info("D: send msg to mt, res: " + res)




@my_exceptions_handler
async def mt_send(text="null", username="C bot", gateway="gateway1", qt=None):

    # in for all
    MT_API = "127.0.0.1:4240"
    # send msg to matterbridge
    url = "http://" + MT_API + "/api/message"

    #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
    #  url="http://127.0.0.1:5555/api/message"

#    if not username.startswith("C "):
#        username = "T " + username


    if qt:
        username = "{}\n\n{}".format("> " + "\n> ".join(qt.splitlines()), username)


#  gateway="gateway0"
    data = {
        "text": "{}".format(text),
        "username": "{}".format(username),
        "gateway": "{}".format(gateway)
    }
    res = await http(url, method="POST", json=data)
    logger.info("sent msg to mt, res: " + res)
    return



@my_exceptions_handler
async def send_mt_msg_to_queue(msg, queue):
    try:
        try:
            msg = msg.decode()
#       Data sent: 'GET /api/stream HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
#      Data received: 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nDate: Wed, 19 Jan 2022 02:03:29 GMT\r\nTransfer-Encoding: chunked\r\n\r\nd5\r\n{"text":"","channel":"","username":"","userid":"","avatar":"","account":"","event":"api_connected","protocol":"","gateway":"","parent_id":"","timestamp":"2022-01-19T10:03:29.666861315+08:00","id":"","Extra":null}\n\r\n'
#            if not msg or msg.startswith("HTTP/1.1"):
#                logger.info("ignore init msg")
#                return

#        msg.replace(',"Extra":null}','}',1)
#        msgd=ast.literal_eval(msg.splitlines()[1])
#            msgd = json.loads(msg.splitlines()[1])
#            print(msg)
            msgd = json.loads(msg)
        except json.decoder.JSONDecodeError:
            logger.error("fail to decode msg from mt")
            print("################")
            print(msg)
            print("################")
            info = "E: {}\n==\n{}\n==\n{}".format(sys.exc_info()[1], traceback.format_exc(), sys.exc_info())
            logger.error(info)
            return

        text = msgd["text"]
        name = msgd["username"]

        if name == "C twitter: ":
            return

        # need fix
        if "gateway11" in MT_GATEWAY_LIST:
            if msgd["gateway"] == "gateway1":
                msgd["gateway"] = "gateway11"

        if msgd["gateway"] in MT_GATEWAY_LIST:
            chat_id = MT_GATEWAY_LIST[msgd["gateway"]][0]
        else:
            # first msg is empty
            logger.warning("unkonwon gateway: {}".format(msgd["gateway"]))
            logger.warning("received data: {}".format(msg))
            return

        if msgd["Extra"]:
            # file
            #,"id":"","Extra":{"file":[{"Name":"proxy-image.jpg","Data":"/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAA ... 6P9ZgOT6tI33Ff5p/MAOfNnzPzQAN4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAGQAAYAkAAGTGAAAAAAAAwsAAHLAAAK//9k=","Comment":"","URL":"https://liuu.tk/ddb833ad/proxy_image.jpg","Size":0,"Avatar":false,"SHA":"ddb833ad"}]}}\n\r\n'
            for file in msgd["Extra"]["file"]:
                if text:
                    if text == file["Name"]:
                        text = ""
                    else:
                        text += "\n\n"
                text += "[{}]({})".format(file["Name"], file["URL"])
        else:
            msgd.pop("Extra")
            logger.warning("removed file info from mt api")

        logger.info("mt msg: {}".format(msgd))
        #      if name == "C Telegram: ":

        msgd.update({"chat_id": chat_id})
        msgd.update({"text": text})

        #7    msg = [0, chat_id, text, {"reply_to":reply_to}]
        #    await queue.put(msg)
        #    await queue.put(msgd)
        await queue.put([1, msgd])
        return

        text = name + text
        #    await NB.send_message(chat_id, text, reply_to=reply_to)
        #    return [0, chat_id, text, {"reply_to":reply_to}]
        msg = [0, chat_id, text, {"reply_to": reply_to}]
#    await queue.put(msg)

    except:
        info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
        logger.error(info)
        await NB.send_message(MY_ID, info)
        await asyncio.sleep(5)


#    finally:
#      mt_send_need_wait=False
