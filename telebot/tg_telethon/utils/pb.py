# import logging

# logger = logging.getLogger(__name__)
# mp = logger.warning

# from .. import *

# from .tools import SH_PATH, tw_re, pic_re, url_only_re, my_host_re

import Test_pb2
import pb_pb2 as P
from google.protobuf import json_format

import zlib


async def encode(text, to="RAW"):
    pass
    pb = P.Button()
    # T = P.Button.TYPE
    # Name = P.Button.TYPE.Name
    Value = P.Button.TYPE.Value
    pb.type = Value(to)
    t = pb.type
    # if to == "RAW":
    if t == 0:
        data = zlib.compress(text.encode())
        pb.msg.data = data
    return pb


async def decode(pb):
    # if pb.type == 0:
    Value = P.Button.TYPE.Value
    if pb.type == Value("RAW"):
        data = zlib.decompress(pb.msg.data)
        msg = data.decode()
        print(msg)

    # print(dir(pb))
    # print(json_format.MessageToJson(pb))
    # print(pb.SerializeToString())
    print(len(pb.SerializeToString()))
    print(pb.ByteSize())
    # print(pb)
    # print(pb.type)
    # print(pb.RAW)
    # print(pb.BS)


async def test():
    text="1234567890"*100
    text="""1234567890i#求购 #pod #AirPods_PRO #air
    联系 @ 200-300收一个AirPods PRO的单右耳
    自用的右耳出了官网描述的爆裂声，因为是两年前二手买的，没有发票，没办法返厂。同时如果大家有办法返厂也期待一个解决方案"""
    print(len(text.encode()))
    pb = await encode(text)
    await decode(pb)


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    msg = Test_pb2.Msg()
    # msg.n = 6
    ss = msg.ss
    s = ss.add()
    ss.pop()
    s.n = 1
    msg.ss.append(s)
    s.n = 2
    s = msg.ss.add()
    s.n = 3

    print(dir(P))
    # msg = P.Button(type="RAW", msg={"text": "test"})
    msg = P.Button()
    # print(json_format.MessageToJson(msg))
    # print(dir(P))
    # print(dir(P.Button))
    # print(dir(P.Button.TYPE))
    # print(type(P.Button.TYPE))
    # print(type(P.Button.TYPE.values))
    # tmp ="1234567890"*1000
    # tmp = tmp.encode()
    # tmp = zlib.compress(tmp)
    # msg.msg.text="1234567890"*100
    # msg.msg.data=b"jddjdi"
    # msg.msg.data=tmp
    # print(msg.type)
    # msg.type = 1
    # print(msg)
    # print(msg.SerializeToString)
    # print(dir(msg))
    # print(dir(msg.ss))
    # print(json_format.MessageToJson(msg))
    # print(type(msg))
    # print(type(msg.ss))
    # print(dir(msg.ss))
    # print(dir(s))
    # print(msg.ByteSize())
    import asyncio
    asyncio.run(test())

else:
    print('{} 运行'.format(__file__))
