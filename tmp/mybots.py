#!/usr/bin/python3

#info: run two bots
#   my userbot:get uid,auto forward msg, run cmd...
#   normal bot:others can send msg to me with it. dump msg and replace userbot

import logging

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)

import sys


def get_my_key(key):
    f = open("/home/liqsliu/.ssh/private_keys.txt")
    line = f.readline()
    while line:
        if len(line.split(' ', 1)) == 2 and line.split(' ', 1)[0] == key:
            f.close()
            return line.split(' ', 1)[1].rstrip('\n')
            break
        line = f.readline()
    f.close()
    return None


from telethon import TelegramClient, events, sync, utils, functions, types
from telethon.events import StopPropagation

#from telethon.tl.types.input_peer_chat import InputPeerChat
#from telethon.tl.types import InputPeerChat, PeerUser, PeerChannel

from telethon.tl.types import PeerChat, PeerUser, PeerChannel, Chat, User, Channel, ChatFull, UserFull, ChannelFull, InputPeerUser, InputPeerChat, InputPeerChannel, MessageEntityTextUrl, MessageMediaUnsupported, MessageMediaWebPage

#telethon.errors.rpcerrorlist.MessageNotModifiedError
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
from telethon.errors.rpcerrorlist import ChannelInvalidError
from telethon.errors.rpcerrorlist import PeerIdInvalidError, FloodWaitError, MessageEmptyError

#from telethon.errors import ValueError

from datetime import timedelta
import time
#from time import time
#from time import strftime
#from time import strptime

import datetime

import subprocess
from subprocess import Popen, PIPE

#import shlex

import asyncio
#from asyncio import sleep
import threading

import traceback
import os
import re
#import zlib
import zstandard
import base64
import ast

#urllib.parse.quote
#from urllib import parse

#import urllib
import urllib.request
import urllib.parse
from urllib.parse import urlencode
import json

import feedparser

my_chat_id = cid_tw

#client = TelegramClient('session_name', api_id, api_hash)
userbot = TelegramClient('/home/liqsliu/.ssh/telethon_session_name.session',
                         api_id, api_hash)

bot = TelegramClient('/home/liqsliu/.ssh/telethon_bot.session', api_id,
                     api_hash).start(bot_token=bot_token)
#client.start(bot_token=bot_token)
# bot.start()
# bot.sign_in(bot_token=bot_token)

#with bot:
#  me = bot.get_me()
#  print (me.id)

last_grouped_id = None


#@events.register(events.NewMessage(pattern='ping',incoming=True))
#@events.register(events.NewMessage(pattern='ping'))

#@userbot.on(events.NewMessage(pattern='ping',incoming=True))
#async def handler(event):
#  await ping(event)

#@userbot.on(events.MessageDeleted)
async def handler(event):
    #  msg=event.message
    #  if msg:
    #    if msg.mentioned:
    #      await myprint(event.original_update.stringify())
    if event.deleted_ids:
        #      await bot.send_message(myid, "msg was deleted: "+ event.original_update.stringify())
        #      await bot.send_message(myid, "msg was deleted: "+ event.stringify() + "\nids: "+ str(event.deleted_ids))
        #      await asyncio.sleep(5)
        if event.chat_id:
            client = event.client
            cid = event.chat_id
            peer = await client.get_entity(cid)
            msgs = await client.get_messages(peer, ids=event.deleted_ids)
            for msg in msgs:
                if msg:
                    await bot.send_message(
                        myid, "msg was deleted: " + msg.stringify() + "\n" +
                        get_msg_link(msg))
                else:
                    await bot.send_message(myid,
                                           "msg was deleted: " + str(msg))
                await asyncio.sleep(5)


# [cid,msg_id]
check_list = []


#@client.on(events.MessageRead(inbox=True))
# Log when you read message in a chat (from your "inbox")
#@bot.on(events.MessageRead)
async def handler(event):
    #  print('You have read messages until', event.max_id)
    for msg in event.get_messages():
        if debug:
            #      await event.client.send_message(myid, "I: msg been read: "+msg.stringify())
            if msg.chat_id == myid:
                continue
            info = ""
            if msg.chat.username:
                info = info + "I: msg been read: msg link: https://t.me/" + msg.chat.username + "/" + str(
                    msg.id)
            else:
                info = info + "I: msg been read: msg link: https://t.me/c/" + str(
                    utils.resolve_id(msg.chat_id)[0]) + "/" + str(msg.id)
            await event.client.send_message(myid, info)
            await asyncio.sleep(3)
#    if mag.chat_id in check_list:
        global check_list
        for i in check_list.copy():
            if msg.chat_id == i[0] and msg.id == i[1]:
                check_list.remove(i)
                await event.client.send_message(
                    myid, "msg been read: " + msg.message)
                await asyncio.sleep(3)


#@bot.on(events.NewMessage(pattern='/start',incoming=True))
#async def handler(event):
#  if type(event.peer_id) == PeerUser:
#    await event.client.send_message(event.chat_id, "fine")
#    raise StopPropagation

#@bot.on(events.Raw)
#async def handler(event):
#  sender_id = event.sender_id
#    if type(event.peer_id) == PeerUser and ( event.raw_text and event.raw_text[0] != "/" or not event.raw_text ):
#  if sender_id == me.id:
#  if not debug:
#    await msg.reply(event.stringify())
#    await bot.send_message(me.id, str(event))

#    myprint=lambda msg : mylog(msg,account=account)
#    myprintmd=lambda msg : mylogmd(msg,account=account)
#    myprintraw=lambda msg : mylograw(msg,account=account)

#  print (event.stringify())
#  chat = await event.get_chat()
#  print(chat.stringify())
#  sender = await event.get_sender()
#  print(sender.stringify())

#  if not "auto_forward_list" in locals().keys():
#    auto_forward_list={cid_tw:cid_ipfsrss}

#    if event.raw_text == "test":
#      await myprint(event.stringify())
#      await myprint(str(chat_id) + " " +str(type(chat_id)))
#      await myprint(str(sender_id) + " " +str(type(sender_id)))
#  await event.respond(event.text)
#  if chat_id == cid_ipfsrss:
#    msg=await client.send_message(me.id, "N:" + event.stringify())
#    if chat_id == me.id:
#      await myprint(event.stringify())
#      cmd=event.raw_text.split(' ',1)
#      cmd=event.raw_text.split(' ')

#    if event.out and event.chat_id != myid:
#    if event.out and event.chat_id == bot_id:
#    if event.out and type(event.chat) == User and event.chat.bot:
#      return


async def auto_msg_send(item):
    await userbot.send_message(
        "start auto_msg: " + str(item) + " to: " + item[2], item[3])

    if item[1] > 0:
        wait = MAX_AUTO_MSG_TASK_TIME - ((time.time() - item[0]) % item[1])
        if wait > 0:
            await asyncio.sleep(wait)


MAX_AUTO_MSG_TASK_TIME = 300


async def auto_msg_task():
    #  global uf
    #  uf=threading.Thread(target=go)
    #  uf.start()
    global auto_msg_list  # id [ctime interval target text]
    #  global config_save_buffer #save config tmp
    while True:
        #    await asyncio.sleep(MAX_AUTO_MSG_TASK_TIME/10)
        await asyncio.sleep(5)
        if await is_debug():
            #      print("uf ok: "+str(uf.is_alive()))
            continue
#    if not t_1.is_alive():
#      await bot.send_message(myid, "W: get_feed restart")
#      t_1.start()
        tasks = []
        #    await update_feed()
        for j in asyncio.all_tasks():
            tasks.append(j.get_name())
        if len(auto_msg_list) > 0:
            for i in auto_msg_list.copy():
                item = auto_msg_list[i]
                task_name = str(item[0:3])
                if item[1] > 0:
                    gogo = (time.time() - item[0]) % item[1]
                    if gogo > 0 and gogo < MAX_AUTO_MSG_TASK_TIME:
                        if task_name not in tasks:
                            asyncio.create_task(auto_msg_send(item),
                                                name=task_name)
    #          msg=await client.send_message(auto_msg[i][2], auto_msg[i][2])
                elif item[1] < 0:
                    gogo = (time.time() - item[0]) + item[1]
                    if gogo > 0:
                        asyncio.create_task(auto_msg_send(item),
                                            name=task_name)
                        auto_msg_list.pop(i)


#client.start()

#https://docs.python.org/3/library/asyncio-task.html#asyncio.run
#loop = asyncio.get_running_loop()
#loop = asyncio.get_event_loop()
#loop.create_task(auto_msg_task(msgs))
#asyncio.create_task(auto_msg_task())
#asyncio.run(auto_msg_task())

#client.run_until_disconnected()

client = userbot

with userbot:
    userbot.loop.run_until_complete(main())
