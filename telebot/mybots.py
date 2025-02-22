#!/usr/bin/python3

#info: run two bots
#   my userbot:get uid,auto forward msg, run cmd...
#   normal bot:others can send msg to me with it. dump msg and replace userbot




import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

import sys

def get_my_key(key):
  f = open("/home/liqsliu/.ssh/private_keys.txt")
  line = f.readline()
  while line:
    if len(line.split(' ',1)) == 2 and line.split(' ',1)[0] == key:
      f.close()
      return line.split(' ',1)[1].rstrip('\n')
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





# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = int(get_my_key("TELEGRAM_API_ID"))
api_hash = get_my_key("TELEGRAM_API_HASH")
#TOKEN = get_env('TG_TOKEN', 'Enter the bot token: ')
#NAME = TOKEN.split(':')[0]
#bot_token = 'xxxx:xxxxxxxxxx'
bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
bot_id = int(bot_token.split(':', 1)[0])
bot_hash = bot_token.split(':', 1)[1]
#print(bot_token)

myid = int(get_my_key("TELEGRAM_MY_ID"))

cid_ipfsrss = int(get_my_key("TELEGRAM_GROUP_IPFSRSS"))
cid_tw = int(get_my_key("TELEGRAM_GROUP_TW"))
cid_wtfipfs = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

cid_btrss = int(get_my_key("TELEGRAM_GROUP_BTRSS"))
cid_fw = int(get_my_key("TELEGRAM_GROUP_FW"))

my_chat_id=cid_tw

#client = TelegramClient('session_name', api_id, api_hash)
userbot = TelegramClient('/home/liqsliu/.ssh/telethon_session_name.session', api_id, api_hash)


bot = TelegramClient('/home/liqsliu/.ssh/telethon_bot.session', api_id, api_hash).start(bot_token=bot_token)
#client.start(bot_token=bot_token)
# bot.start()
# bot.sign_in(bot_token=bot_token)


#with bot:
#  me = bot.get_me()
#  print (me.id)

last_grouped_id=None
#@events.register(events.NewMessage(pattern='ping',incoming=True))
#@events.register(events.NewMessage(pattern='ping'))


#@userbot.on(events.NewMessage(pattern='ping',incoming=True))
#async def handler(event):
#  await ping(event)

@userbot.on(events.MessageEdited)
async def handler(event):
  await send_msg_to_mt(event, edited=True)
  await run_cmd_for_bots(event)

#@userbot.on(events.NewMessage(incoming=True))
@userbot.on(events.NewMessage)
async def handler(event):
  await send_msg_to_mt(event)
  await run_cmd_for_bots(event)






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
      client=event.client
      cid=event.chat_id
      peer=await client.get_entity(cid)
      msgs=await client.get_messages(peer,ids=event.deleted_ids)
      for msg in msgs:
        if msg:
          await bot.send_message(myid, "msg was deleted: "+ msg.stringify() + "\n" + get_msg_link(msg) )
        else:
          await bot.send_message(myid, "msg was deleted: "+ str(msg) )
        await asyncio.sleep(5)


# [cid,msg_id]
check_list=[]

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
      info=""
      if msg.chat.username:
        info=info+"I: msg been read: msg link: https://t.me/"+msg.chat.username+"/"+str(msg.id)
      else:
        info=info+"I: msg been read: msg link: https://t.me/c/"+str(utils.resolve_id(msg.chat_id)[0])+"/"+str(msg.id)
      await event.client.send_message(myid, info)
      await asyncio.sleep(3)
#    if mag.chat_id in check_list:
    global check_list
    for i in check_list.copy():
      if msg.chat_id == i[0] and msg.id == i[1]:
        check_list.remove(i)
        await event.client.send_message(myid, "msg been read: "+ msg.message)
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

@bot.on(events.NewMessage(incoming=True))
async def handler(event):
  client = event.client
  try:
    sender_id = event.sender_id
#    if type(event.peer_id) == PeerUser and ( event.raw_text and event.raw_text[0] != "/" or not event.raw_text ):
    if sender_id == me.id:
      if event.is_reply:
        replied = await event.get_reply_message()
        if replied:
#          if replied.raw_text.split("\n",1)[0] == "new msg":
          lines=replied.raw_text.split("\n")
          if lines[0] == "new msg":
            target_id=int(lines[-1].split(" ")[1])
            target=await client.get_entity(target_id)
            if target:
              if target.status:
#                msg_id=int(lines[-2].split(" ")[1])
#                orig_msg=await client.get_messages(target,ids=msg_id)
                msg_t=await event.forward_to(target)
                await client.send_message(myid, "I: ok")
                global check_list
                # not work
#                check_list.append([msg_t.chat_id, msg_t.id])

                if debug:
                  await client.send_message(myid, "check_list: "+str(check_list))

              else:
                await bot.send_message(myid, "E: can not send, stopped or deleted chat")
            else:
              await bot.send_message(myid, "E: wtf: no entity")

            return

      await run_cmd_for_bots(event)
    else:
      if event.raw_text and event.raw_text[0] == "/":
        await run_cmd_for_bots(event)
      chat_id = event.chat_id
      msg=event.message
#      msg_info="new msg: "+msg.raw_text+"\n"
      msg_info="new msg\n"
      from_info="\nmsg_id "+str(msg.id)+"\nfrom " + str(sender_id)+" tg://openmessage?user_id="+str(sender_id)
      if type(event.peer_id) == PeerUser:
#        await bot.send_message(me.id, "new message: " + msg.raw_text + "\n\nfrom " + str(sender_id))
#        chat=await bot.get_input_entity(me.id)
        chat=await bot.get_entity(me.id)
        if chat.status:
          try:
            msg=await event.forward_to(chat)
            await msg.reply(msg_info+from_info)
          except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await asyncio.sleep(5)
            await bot.send_message(chat_id, "error: forwarding failed, please chat with him directly")
            await bot.send_message(myid, "E: msg bot is down: "+traceback.format_exc())
            return
          except:
            await bot.send_message(chat_id, "error: forwarding failed, please chat with him directly")
            await bot.send_message(myid, "E: msg bot is down: "+traceback.format_exc())
            return

          if event.raw_text and event.raw_text[0] == "/":
            pass
          else:
            await bot.send_message(chat_id, "msg has been sent")
        else:
          if event.raw_text and event.raw_text[0] == "/":
            pass
          else:
            if me.username:
              await bot.send_message(chat_id, "error: forwarding failed, @"+me.username+" has stopped forwarding, please chat with him directly")
            else:
              await bot.send_message(chat_id, "error: forwarding failed, please chat with him directly")
      else:
        if msg.mentioned:
          chat=await bot.get_input_entity(me.id)
          msg=await event.forward_to(chat)
          chat_info="\nchat_id "+str(chat_id)+" tg://openmessage?chat_id="+str(utils.resolve_id(msg.chat_id)[0])
          await msg.reply(msg_info+chat_info+from_info)

  except Exception as e:
#    await client.send_message(log_cid, "E: bot: "+str(e)+"\n==\n"+traceback.format_exc())
    await bot.send_message(myid, "E: bot: "+str(e)+"\n==\n"+traceback.format_exc())









#@events.register(events.NewMessage)
async def run_cmd_for_bots(event):
  client = event.client
#  sender=await client.get_input_entity(sender_id)
  try:


  #  if msg.via_bot:
  #    return
  #  if type(event.peer_id) == PeerUser and chat.bot:
  #    return
  #  if sender and sender.bot:
  #    return



    MAX_MSG_LEN=4096

    def mdraw(msg,type="text"):
    #  msg=msg.replace("\\","\\\\")
      chars={
          "text": "\\_*[]()~`>#+-=|{}.!",
          "code": "\\`",
          "link": "\\)",
          "md": "\\_*[`"
          }
      if type in chars:
        type=chars[type]
      if msg:
        for i in type:
          msg=msg.replace(i,"\\"+i)
      return msg


    async def myprint(msg, parse_mode="text", *args, **kwagrs):
      if args:
        msg+=" ".join(str(v) for v in args)
      if len(msg.strip()) == 0:
        msg="null"
      if debug:
        print("\nI: myprint:"+str(msg))
      if len(msg) > MAX_MSG_LEN:
        msg=subprocess.run(["bash", "change_long_text.sh", msg ], stdout=subprocess.PIPE, text=True ).stdout
      if event.chat_id:
        id=event.chat_id
      else:
        id=log_cid
      if parse_mode == "md":
    #    return await client.send_message(log_cid, msg, parse_mode=parse_mode)
#        return await client.send_message(log_cid, msg, parse_mode=parse_mode)

        return await client.send_message(id, msg, parse_mode=parse_mode)
      else:
        return await client.send_message(id, msg)




    async def myprintmd(msg, *args, **kwagrs):
      return await myprint(msg, parse_mode="md")

    async def myprintraw(msg, *args, **kwagrs):
    #  return await myprintmd("`"+msg.replace("`","\\`")+"`")
      if len(msg) > MAX_MSG_LEN:
        return await myprint(msg)
      else:
        return await myprintmd("```\n"+msg+"\n```")
        msg=mdraw(msg,"code")



    async def get_id(url):
      id=0
      if type(url) == int:
        return url
      elif type(url) == str:
        if url[0] =="@":
        #          peer=await client.get_input_entity(cmd[1][1:])
        #          await client.send_message(me.id, str(peer.id))
  #        id=url[1:]
          try:
            peer=await client.get_entity(url[1:])
  #        except ValueError:
          except (ValueError, PeerIdInvalidError) as e:
            peer=await client2.get_entity(url[1:])
          id=peer.id
        elif len(url.split('/')) >=4 and url.split('/')[2] == "t.me":
          if url.split('/')[3] == "c":
            id=int(url.split('/')[4])
          else:
  #          id=url.split('/')[3]
            peer=await client.get_entity(url.split('/')[3])
            id=peer.id
        else:
          id=int(url)
        if "?comment=" in url:
          id=await get_linked_cid(id)
        if id:
          return id
        else:
          return None
      else:
        return url

    async def get_msg_id(url):
      id=0
      if type(url) == int:
        return url
      elif "?comment=" in url:
        id=int(url.split('=')[1])
      else:
#        id=int(url.split('/')[-1].split('?')[0])
        id=int(url.split('/')[-1])
      if id:
        return id
      else:
        return None

    async def get_peer(msg):
      try:
        peer=await client.get_entity(await get_id(msg))
#        peer=await client.get_entity(utils.get_peer_id(peer))
      except (ValueError, PeerIdInvalidError) as e:
        peer=await client2.get_entity(await get_id(msg))
        if debug:
          info="E: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
          await client.send_message(myid, info)
      return peer

    async def get_msg(cid,ids):
      try:
#        msg=await client.get_messages(await client.get_entity(chat.id),ids=id)
        peer=await client.get_entity(cid)
        msg=await client.get_messages(peer,ids=ids)
        if not msg:
          if debug:
            await client.send_message(myid, "E: default client: no such msg")
          raise ValueError
#      except ValueError:
      except (ValueError, PeerIdInvalidError) as e:
#        msg=await client2.get_messages(chat,ids=id)
        peer=await client2.get_entity(cid)
        msg=await client2.get_messages(peer,ids=ids)
        if debug:
          info="E: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
          await client.send_message(myid, info)
      return msg

    async def my_get_msg(url):
    #  elif cmd[0] == "link":
    #    url=cmd[1]
      msg=None
      if len(url.split('/')) >=5 and url.split('/')[2] == "t.me":
        cid=await get_id(url)
        id=await get_msg_id(url)
        msg=await get_msg(cid,ids=id)
        if not msg:
          if debug:
            await client.send_message(myid, "E: all clients: can't find the msg")
          return None
      return msg

    #group
    async def get_admins(chat):
      if type(chat) == str or type(chat) == int:
#        chat=await client.get_entity(await get_id(chat))
        chat=await get_peer(chat)
      info="admin: "
      if chat.username:
        info=info+"@"+chat.username
      try:
        # Filter by admins
        from telethon.tl.types import ChannelParticipantsAdmins
#        async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        try:
          users=await client.get_participants(chat, filter=ChannelParticipantsAdmins)
        except ChannelInvalidError:
          users=await client2.get_participants(chat, filter=ChannelParticipantsAdmins)
        for user in users:
  #      for user in await client.iter_participants(chat, filter=ChannelParticipantsAdmins):
  #        print(user.first_name)
          info=info+"\n"
          if user.bot:
            info=info+"bot"
          else:
            info=info+str(user.id)
          if user.username:
            info=info+" @"+user.username
          if user.first_name:
            info=info+" "+user.first_name
      except ChatAdminRequiredError:
        info = "E: need admin"
        if event.chat_id == myid and chat.broadcast:
          info = info+", but:\n"
          info = info + (await get_admin_of_channel(chat.id))
      return info

    #small group: Chat
    async def get_admin_of_group(msg):
      peer=await get_peer(msg)
      if type(peer) == Chat:
        info="id: `"+str(utils.get_peer_id(peer))
        if peer.username:
          info=info+"` @"+peer.username
        else:
          info=info+"` no name, tg://openmessage?chat_id="+str(peer.id)
    #    full = await client(functions.messages.GetFullChatRequest(peer.id))
        full = await client(functions.channels.GetFullChannelRequest(peer))
        full_chat = full.full_chat
        if full_chat.exported_invite:
          id=str(full_chat.exported_invite.admin_id)
          info=info+"\nadmin id: `"+id+"` tg://openmessage?user_id="+id
        else:
          info=info+"can't find admin id in group"
        return info


    #channel or big group: Channel
    async def get_admin_of_channel(msg):
    #  id=await get_id(msg)
#      peer=await client.get_entity(await get_id(msg))
      peer=await get_peer(msg)
    #  if type(peer) == User:
    #  if type(peer) == Channel:
#      if peer.broadcast or peer.megagroup or peer.gigagroup:
      if peer.broadcast:
        info="id: `"+str(utils.get_peer_id(peer))
        if peer.username:
          info=info+"` @"+peer.username
        else:
          info=info+"` no username, tg://openmessage?chat_id="+str(peer.id)
        try:
          full = await client(functions.channels.GetFullChannelRequest(peer))
        except:
          full = await client2(functions.channels.GetFullChannelRequest(peer))
        full_chat = full.full_chat
        if full_chat.exported_invite:
          id=str(full_chat.exported_invite.admin_id)
          info=info+"\nadmin id: `"+id+"` tg://openmessage?user_id="+id
        elif full_chat.linked_chat_id:
          info=info+"\nlinked id: `"+str(utils.get_peer_id(types.PeerChannel(full_chat.linked_chat_id)))
          if len(full.chats) == 2:
            if full.chats[1].username:
              info=info+"` @"+full.chats[1].username
            else:
              info=info+"` no username, tg://openmessage?chat_id="+str(full_chat.linked_chat_id)
          else:
            info=info+"` unknown group, tg://openmessage?chat_id="+str(full_chat.linked_chat_id)
#          if peer.broadcast:
    #        info=info+"\n==\n"+await get_admin_of_channel(peer.id)
          info=info+"\n"+(await get_admins(full_chat.linked_chat_id))
        else:
          info=info+"\nno linked group or channel"
#      elif type(peer) == Chat:
#        info=await get_admin_of_group(peer.id)
      elif type(peer) == Chat or type(peer) == Channel:
        info=await get_admins(peer)
      else:
    #    await myprint(peer.stringify())
        info="wtf: "+str(type(peer))+" "+str(utils.get_peer_id(peer))
      return info










    async def update_stdouterr(msg):
    #          info = info+p.stdout.read()
    #          errs = errs+p.stderr.read()
      while msg[2].poll() == None:
    #    msg[0] = msg[0]+msg[2].stderr.read()
    #    print(1)
        await asyncio.sleep(0.1)

    #    tmp=msg[2].stdout.read(64)
    #    tmp=await msg[2].stdout.read()
    #https://stackoverflow.com/questions/33886406/how-to-avoid-the-deadlock-in-a-subprocess-without-using-communicate
    #https://stackoverflow.com/a/33886970
    #    tmp=await msg[2].stdout.readline()
    #    tmp=msg[2].stdout.readline()
    #deadlock
    #    tmp=msg[2].stdout.read()
    #    async for tmp in msg[2].stdout:
    #      print(1.1)
    #      msg[0]=msg[0]+tmp.decode("utf-8")
    #    break

    #    tmp=p.stdout.read(64)
        try:
    #      out,errs = msg[2].communicate(timeout=0.3)
          msg[0],msg[1] = msg[2].communicate(timeout=0.3)
        except subprocess.TimeoutExpired as e:
    #      msg[0]=str(type(e.stdout))
    #      msg[1]=e.stderr
          if e.stdout:
            msg[0]=e.stdout.decode("utf-8")
          if e.stderr:
            msg[1]=e.stderr.decode("utf-8")
    #  print(11)


    async def update_stdout(msg):
    #          info = info+p.stdout.read()
    #          errs = errs+p.stderr.read()
      while True:
    #    msg[0] = msg[0]+msg[2].stderr.read()
        print(1)
        await asyncio.sleep(0.2)
    #    tmp=msg[2].stdout.read(64)
    #    tmp=await msg[2].stdout.read()
    #https://stackoverflow.com/questions/33886406/how-to-avoid-the-deadlock-in-a-subprocess-without-using-communicate
    #https://stackoverflow.com/a/33886970
        tmp=await msg[2].stdout.readline()
    #    tmp=msg[2].stdout.readline()
    #deadlock
    #    tmp=msg[2].stdout.read()
    #    async for tmp in msg[2].stdout:
    #      print(1.1)
    #      msg[0]=msg[0]+tmp.decode("utf-8")
    #    break

    #    tmp=p.stdout.read(64)
        if tmp:
          msg[0]=msg[0]+tmp.decode("utf-8")
        else:
          break
      print(11)





    async def update_stderr(msg):
      while True:
        print(2)
        await asyncio.sleep(0.2)
        tmp=await msg[2].stderr.readline()
    #    tmp=msg[2].stderr.readline()
    #    tmp=msg[2].stderr.read()
    #    tmp=p.stderr.read(64)
        if tmp:
          msg[1]=msg[1]+tmp.decode("utf-8")
        else:
          break
      print(22)



    async def get_linked_cid(id):
      peer=await client.get_input_entity(id)
    #  if type(peer) == User:
      if type(peer) == InputPeerUser:
        return None
        full = await client(functions.users.GetFullUserRequest(id=peer))
    #  elif type(peer) == Chat:
      elif type(peer) == InputPeerChat:
        full = await client(functions.messages.GetFullChatRequest(peer.chat_id))
      #https://docs.telethon.dev/en/latest/concepts/chats-vs-channels.html
      #megagroups are channels
    #  elif peer.broadcast or peer.megagroup or peer.gigagroup:
      elif type(peer) == InputPeerChannel:
        full = await client(functions.channels.GetFullChannelRequest(peer))
      else:
        await myprint("unknown type,not full:"+str(type(peer)))
      full_chat = full.full_chat
      if full_chat.linked_chat_id:
    #      info=info+"\nlinked id: `"+str(utils.get_peer_id(types.PeerChannel(full_chat.linked_chat_id)))
        return full_chat.linked_chat_id
      else:
        return None




    async def my_popen(cmd,shell=True,max_time=64,cmd_msg=None):
    #        args=shlex.split(event.raw_text.split(' ',1)[1])

    #        p=subprocess.Popen(event.raw_text.split(' '))
    #        p=subprocess.Popen(event.raw_text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #        p=subprocess.Popen(shlex.split(event.raw_text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)

    #        p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #        p=Popen(args,text=True,universal_newlines=True,bufsize=1,stdout=PIPE, stderr=PIPE)
    #        p=Popen(args,text=True,stdout=PIPE, stderr=PIPE)
    #        p=await asyncio.create_subprocess_shell(event.raw_text.split(' ',1)[1],stdout=PIPE, stderr=PIPE)#limit=None
    #        p=Popen(args,stdout=PIPE, stderr=PIPE,bufsize=8000000)
    #        p=Popen(args,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
      p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")

      start_time=time.time()
      info=""
      errs=""
#      if client == userbot and event.chat_id < 0:
#      if client == userbot and event.is_group:
#      msg=await cmd_answer("...",cmd_msg)
      msg=None
      msg=cmd_msg

      msgs=["","",p]
      await asyncio.sleep(0.5)
    #        await myprintraw(str(args))
      if debug:
        await myprintraw(str(p.args))
      if p.poll() == None and p.returncode == None:
        asyncio.create_task(update_stdouterr(msgs))
        while p.poll() == None and p.returncode == None:
          if time.time()-start_time > max_time:
            p.kill()
            break
          await asyncio.sleep(0.5)
          info=msgs[0]
          errs=msgs[1]

          tmp=info+"\n==\nE: \n"+errs
    #            tmp=tmp.lstrip('\n').rstrip('\n').lstrip(' ').rstrip(' ')
          if not msg or tmp != msg.raw_text:
            try:
#              msg=await msg.edit(tmp)
              msg=await cmd_answer(tmp, msg)
  #                await msg.delete()
  #                msg=await myprint(tmp)
  #                await myprintraw(msg.raw_text.encode().hex())
  #                await myprintraw(tmp.encode().hex())
            except MessageNotModifiedError:
              await myprint("E: wtf? MessageNotModifiedError")
              await asyncio.sleep(5)
            except:
              await client.send_message(myid, "E: can't edit msg(in)")
              msg=await client.send_message(event.chat_id, tmp)
          await asyncio.sleep(1)
              

    #        await asyncio.sleep(0.5)
      #info=msgs[0]
      #errs=msgs[1]
      try:
        info, errs = p.communicate(timeout=5)
      except subprocess.TimeoutExpired as e:
        info=e.stdout
        errs=e.stderr

    #        if info:
    #          info=info.decode("utf-8")
    #        else:
    #          info=""
    #        if errs:
    #          errs=errs.decode("utf-8")
    #        else:
    #          errs=""

      if not info:
        info="null"
      info=str(info)
      if p.returncode:
        info=info+"\n==\nE: "+str(p.returncode)
        if errs:
          info=info+"\n"+errs
        #await msg.delete()
      msg=await cmd_answer(info, msg)


    async def my_exec(cmd):
    #  exec(cmd) #return always is None
    #  p=Popen("my_exec.py "+event.raw_text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
      await my_popen(["python3", "my_exec.py",cmd],shell=False)

    async def cmd_answer(text,msg=None):
      text=text.strip()
      if msg:
        if text == msg.raw_text:
          return msg
        if msg.out:
          return await msg.edit(text)
        else:
          return await client.send_message(myid, "E: can't edit msg(in)")
          return await client.send_message(event.chat_id, text)
      else:
        if event.is_group:
          if client == userbot and event.out:
            msg=event.message
            return await msg.edit(text)
          else:
            return await event.message.reply(text)
        else:
          return await client.send_message(event.chat_id, text)

    async def my_eval(cmd):
      try:
        res=eval(cmd)
        if debug:
          await myprint(str(res)+"\n"+str(type(res)))
        else:
#          await myprint(str(res))
#          await client.send_message(event.chat_id, str(res))
          await cmd_answer(str(res))
      except MessageEmptyError:
        await myprint("E: null msg")
      except:
        info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
        if client == userbot:
          await client.send_message(myid, "E: > tg://openmessage?user_id="+str(bot_id))
        await bot.send_message(myid, info)



    DOWNLOAD_PATH="/var/www/dav/tmp"
    MY_DOMAIN="liuu.tk"
    #https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.downloads.DownloadMethods.download_media
    # Printing download progress
    async def download_media_callback(current, total):
      nonlocal msg_before_return
#      print('Downloaded', current, 'out of', total,'bytes: {:.2%}'.format(current / total))
#      await myprint('Downloaded', current, 'out of', total,'bytes: {:.2%}'.format(current / total))
      msg_before_return=('Downloaded '+str(current)+' out of '+str(total)+' bytes: {:.2%}'.format(current / total)).strip()


#    async def download_media_task(msg,path):

    #https://docs.python.org/3/library/asyncio-task.html#asyncio.run
    async def download_media(msg):
      nonlocal msg_before_return
      task=asyncio.create_task(msg.download_media(file=DOWNLOAD_PATH+"/",progress_callback=download_media_callback))
      last_msg=""
      msg=""
      while True:
        await asyncio.sleep(1)
        if task.done():
          break
        elif not msg_before_return:
          if last_msg != msg_before_return:
            last_msg = msg_before_return
#            await myprint(msg_before_return)
            if msg:
              await msg.edit(msg_before_return)
            else:
             msg=await client.send_message(event.chat_id, msg_before_return)
#      msg.delete()
      return task.result()

    async def my_method(custom_method):
      result = await client(functions.bots.SendCustomRequestRequest(
        custom_method=custom_method,
        params=types.DataJSON(
            data='some string here'
        )
      ))
      await myprint(result.stringify())

    async def update_profile(msg):
      result = await client(functions.account.UpdateProfileRequest(
        first_name='some string here',
        last_name='some string here',
        about='some string here'
      ))
      await myprint(result.stringify())
    async def update_name(msg):
#      result = await client(functions.account.UpdateProfileRequest(
      result = await userbot(functions.account.UpdateProfileRequest(
        first_name=msg
      ))
      await myprint(result.stringify())

#    async def ban_chat(chat_id,sender_chat_id):
    async def ban_chat(chat, target):
      chat=await client.get_input_entity(chat)
      target=await client.get_input_entity(target)
      result=await client(functions.channels.EditBannedRequest(
          channel=chat,
          participant=target,
          banned_rights=types.ChatBannedRights(
			view_messages=True,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            send_polls=False,
            change_info=False,
            invite_users=False,
            pin_messages=False,
            until_date=0
            )
          ))

#      await myprint(result.stringify())

    async def ban_chat_test(sender_chat_id):
      #https://core.telegram.org/bots/api#banchatsenderchat
      #telethon.errors.rpcerrorlist.UserBotInvalidError: This method can only be called by a bot (caused by SendCustomRequestRequest)
#      result = await client(functions.bots.SendCustomRequestRequest(

#      data='{"chat_id":'+str(event.chat_id)+',"text":"test custom req: ok"}'
      data='{\"chat_id\":'+str(event.chat_id)+',\"text\":\"test custom req: ok\"}'
      await myprint(data)
      result = await bot(functions.bots.SendCustomRequestRequest(
        custom_method="sendMessage",
        params=types.DataJSON(data=data)
      ))
      await myprint(result.stringify())

    async def ban_chatbu(sender_chat_id):
      #https://core.telegram.org/bots/api#banchatsenderchat
      #telethon.errors.rpcerrorlist.UserBotInvalidError: This method can only be called by a bot (caused by SendCustomRequestRequest)
#      result = await client(functions.bots.SendCustomRequestRequest(
      data='{"chat_id":'+str(event.chat_id)+',"sender_chat_id":'+str(sender_chat_id)+'}'
      await myprint(data)
      result = await bot(functions.bots.SendCustomRequestRequest(
        custom_method="banChatSenderChat",
        params=types.DataJSON(data=data)
      ))
      await myprint(result.stringify())

    async def ban_chatbu(sender_chat_id):
      #https://core.telegram.org/bots/api#banchatsenderchat
      #telethon.errors.rpcerrorlist.UserBotInvalidError: This method can only be called by a bot (caused by SendCustomRequestRequest)
      data={
          "chat_id": event.chat_id,
          "sender_chat_id": sender_chat_id
          }
#      result = await client(functions.bots.SendCustomRequestRequest(
      result = await bot(functions.bots.SendCustomRequestRequest(
        custom_method="banChatSenderChat",
        params=types.DataJSON(
            data=str(data)
        )
      ))
      await myprint(result.stringify())

    async def check_status_before_cmd(target=None):
      if debug:
        await myprint("D: check cmd target: "+ str(target))
      if event.via_bot_id:
        return False
      if event.out:
        if type(event.chat) == User and event.chat.bot:
          return False
        if event.chat_id == cid_wtfipfs:
          return False

      if target & 0b100 == 0: # only admin
        if event.sender_id != myid:
          return False

      if target & 0b010 == 0: # no private
#            if event.chat_id > 0:
        if event.is_private:
          return False
      else:
        if event.out:
          if type(event.chat) == User:
            if event.chat_id != myid:
              if event.raw_text[0] != ".":
                return False

      if target & 0b001 == 0: # no group
#            if event.chat_id < 0:
        if event.is_group:
          return False
      else:
        if event.is_group:
          if not event.mentioned:

            if client == bot:
#              if event.raw_text.endswith("@"+bot_name) or "@{} ".format(bot_name) in event.raw_text:
              if event.raw_text =="/{}@{}".format(cmd[0], bot_name):
                return True
              elif event.raw_text.startswith("/{}@{} ".format(cmd[0], bot_name)):
                return True
              else:
                if event.is_reply:
                  replied = await event.get_reply_message()
                  if replied:
                    if replied.sender_id == client_id:
                      return True
                return False



            if not event.out:
              return False

            if event.raw_text[0] != ".":
              return False

            sender=event.sender
            if not sender:
              sender = await event.get_sender()
            if type(sender) == User and sender.bot:
              return False

#              if event.sender_id == myid and event.out:
            if event.is_reply:
              replied = await event.get_reply_message()
              if replied.sender_id == bot_id:
                return False

      if debug:
        await myprint("D: target is ok: "+ str(target))

      return True

      #############


      if event.chat_id == myid:
        #admin
        if target:
          if target & 0b100 > 0:
            return True
          else:
            return False
        else:
          return 0b100
      elif event.chat_id > 0:
        #private chat
        if target:
          if target & 0b010 > 0:
            if event.via_bot_id:
              return False
            sender=event.sender
            if not sender:
              sender = await event.get_sender()
      #      if type(sender) == Channel and sender.broadcast:
            if type(sender) == User and sender.bot:
              return False
            return True
          else:
            return False
        else:
          return 0b010
#      elif event.from_id == None or type(event.from_id) == PeerChannel:
#      elif event.from_id == None:
#      elif event.peer_id.broadcast:
      elif event.is_channel:
        #channel
        if target != None:
          return False
        else:
          return 0b000
      else:
        #group
        if target:
          if target & 0b001 > 0 and event.mentioned:
            if event.via_bot_id:
              return False
            sender=event.sender
            if not sender:
              sender = await event.get_sender()
      #      if type(sender) == Channel and sender.broadcast:
            if type(sender) == User and sender.bot:
              return False
            return True
          #elif target & 0b001 > 0 and event.sender_id == myid:
          elif target & 0b001 > 0 and event.out:
            return True
          else:
            return False
        else:
          return 0b001
        
    async def set_bot_cmd():

      tg_cmd="help ping myid dc uptime free"



      commands=[]
      for i in tg_cmd.split(" "):
        if event.is_private:
          if 0b010 & cmd_dict[i][0] == 0:
            continue
        if event.is_group:
          if 0b001 & cmd_dict[i][0] == 0:
            continue
        if event.chat_id != myid:
          if 0b100 & cmd_dict[i][0] == 0:
            continue

        if len(cmd_dict[i]) >1:
          commands.append(types.BotCommand(command=i,description=cmd_dict[i][1]))
        else:
          commands.append(types.BotCommand(command=i,description=i))

      scope=types.BotCommandScopeDefault()
      if event.chat_id != myid:
        if event.is_private:
#          scope=types.BotCommandScopeDefault()
#          scope=types.BotCommandScopePeer(await get_peer(event.sender_id))
          scope=types.BotCommandScopeUsers()
        elif event.is_group:
          scope=types.BotCommandScopeChats()
#          scope=types.BotCommandScopePeer(await get_peer(event.chat_id))
#          scope=types.BotCommandScopeChatAdmins() #for admin of group https://core.telegram.org/constructor/botCommandScopeChatAdmins
      else:
        if event.is_private:
#          scope=types.BotCommandScopeDefault()
#          scope=types.BotCommandScopePeerAdmins(peer=event.chat_id)
#          peer=await bot.get_input_entity(event.chat_id)
#          peer=await bot.get_entity(event.chat_id)
#          scope=types.BotCommandScopePeerAdmins(peer)
          peer=await bot.get_input_entity(event.chat_id)
          scope=types.BotCommandScopePeer(peer)
        elif event.is_group:
#          scope=types.BotCommandScopeChatAdmins()
#          scope=types.BotCommandScopeDefault()
          peer=await bot.get_input_entity(event.chat_id)
          scope=types.BotCommandScopePeerUser(peer, myid)
#      result = await client(functions.bots.SetBotCommandsRequest(
      await bot(functions.bots.SetBotCommandsRequest(
        scope=scope,
#        lang_code='en',
#        lang_code='zh-hans',
        lang_code='',
        commands=commands
   	  ))

#    async def admin_cmd(cmd=[]):
    async def run_cmd(cmd=[]):
      global auto_forward_list, debug, auto_msg_list, feed_list
      chat_id = event.chat_id
      sender_id = event.sender_id
      chat = event.chat
      sender = event.sender
      msg = event.message

      if cmd[0] == "ping":
        if len(cmd) == 1:
#          await client.send_message(event.chat_id, "pong")
          await event.reply("pong")
      elif cmd[0] == "dc":
        info=""
        if ( len(cmd) > 1 and cmd[1] == "f" ) or not sender:
          sender = await event.get_sender()
        if not sender:
          if sender_id:
            sender = await get_peer(sender_id)

        if not sender or not sender.photo:
          if sender_id:
            sender = await client2.get_entity(sender_id)
            info+="(via bot2): "

        if sender:
          if sender.photo:
            info+="dc"+str(sender.photo.dc_id)
          else:
            info+="no photo"
        else:
          info+="error"

        await event.reply(info)
      elif cmd[0] == "help":
        if client == bot:
          await set_bot_cmd()
        await client.send_message(event.chat_id, "use cmd")
      elif cmd[0] == "start":
        if client == bot:
          await set_bot_cmd()
        await client.send_message(event.chat_id, "ok")
      elif cmd[0] == "dg":
        if len(cmd) == 1:
          debug=not debug
        await myprint(str(debug))
      elif cmd[0] == "an":
#        if url:
#          cmd += cmd + [url]

        if len(cmd) == 1 and not event.is_reply:
#          info="https://pypi.org/project/archivenow/"
          info="https://github.com/oduwsdl/archivenow"
          info=info+"\n"
          info=info+"\nia Use The Internet Archive"
          info=info+"\nis Use The Archive.is"
          info=info+"\n"
          info=info+"\nall"
          info=info+"\nhelp"
          await client.send_message(event.chat_id, info)
#            await my_popen(event.raw_text)
#            await my_popen(" ".join(cmd[1:]))
        else:
          shell_cmd=None

          an_cmd="cd ~/tmp/; archivenow"
          ex_cmd=" "
          if len(cmd) > 1:
            if cmd[1] == "ia" or cmd[1] == "is" or cmd[1] == "all":
              ex_cmd=" --"
            if cmd[1] == "help":
              shell_cmd=an_cmd+" --help"

          url_re=re.compile(r"https?://\S+")
          url=url_re.search(event.raw_text)
          if url:
            shell_cmd=an_cmd+ex_cmd+event.raw_text.split(" ",1)[1]
          else:
            if event.is_reply:
              replied = await event.get_reply_message()
              if replied:
#                  url=re.search(r"https?://\S+", replied.raw_text).group()
                url=url_re.search(replied.raw_text)
                if url:
                  url=url.group()
                  if len(cmd) == 1:
                    shell_cmd=an_cmd
                  else:
                    shell_cmd=an_cmd+ex_cmd+event.raw_text.split(" ",1)[1]
                  shell_cmd+=" "+url
            
          if shell_cmd:
            if client == userbot and chat_id < 0:
              await my_popen(shell_cmd, cmd_msg=msg)
            else:
              await my_popen(shell_cmd, max_time=900)
          else:
            await myprint("W: no url")
            if chat_id == myid:
              shell_cmd=an_cmd+ex_cmd+event.raw_text.split(" ",1)[1]
              await my_popen(shell_cmd)

      elif cmd[0] == "myid" and len(cmd) == 1:
        if event.is_private:
          await event.reply(str(sender_id))
        else:
          if event.is_reply:
            replied = await event.get_reply_message()
            if replied:
              await event.reply(str(replied.sender_id))
          else:
            await event.reply(str(sender_id))


      elif cmd[0] == "save":
        await save_config()
        await client.send_message(event.chat_id, str([auto_forward_list,auto_msg_list,feed_list]).replace(" ", "").strip())
      elif cmd[0] == "md":
        result=await client.send_message(event.chat_id, event.raw_text,parse_mode="md")
        
        await client.send_message(event.chat_id, result.stringify())
      elif cmd[0] == "hm":
        result=await client.send_message(event.chat_id, event.raw_text,parse_mode="htm")
        
        await client.send_message(event.chat_id, result.stringify())
      elif cmd[0] == "unpin":
        peer=await client.get_input_entity(await get_id(cmd[1]))
        if not peer:
          peer=await client.get_entity(await get_id(cmd[1]))
        result=await client(functions.messages.UnpinAllMessagesRequest(peer))
        await client.send_message(event.chat_id, result.stringify())
      elif cmd[0] == "me":
        if len(cmd) == 1:
          await client.send_message(event.chat_id, "me name|all text")
        elif cmd[1] == "name":
          await update_name(event.raw_text.split(" ",2)[2])
      elif cmd[0] == "rss":
        if len(cmd) == 1:
#          await client.send_message(event.chat_id, "hi")
          await client.send_message(event.chat_id, str(feed_list))
        elif cmd[1] == "cid":
          global cid_btrss
          cid_btrss=int(cmd[2])
          await client.send_message(event.chat_id, "rss to: "+str(cid_btrss))
        elif cmd[1] == "stop" or cmd[1] == "disable":
          if len(cmd) > 2:
            if cmd[2] in feed_list:
              feed_list[cmd[2]][0]="disable"
              if len(cmd) > 3:
                feed_list[cmd[2]][1]=cmd[3]
              else:
                feed_list[cmd[2]][1]=0
              await client.send_message(event.chat_id, str(feed_list[cmd[2]]))
            else:
              await client.send_message(event.chat_id, "need a rss url")
        elif cmd[1] == "add":
          if len(cmd) == 2:
            await client.send_message(event.chat_id, "rss add url [cid]")

          else:
            if not cmd[2] in feed_list:
              url=cmd[2]
              request_headers={'Cache-control': 'max-age=600'}
#              d=feedparser.parse(url,extra_headers={'Cache-control': 'max-age=600'})
#              d=feedparser.parse(url,request_headers={'Cache-control': 'max-age=600'})
              d=feedparser.parse(url,request_headers=request_headers)
              if debug:
                await client.send_message(event.chat_id, str(d.etag)+str(d.modified_parsed))

  #              feed_list.update({cmd[2]: [int(cmd[3])]})
#              feed_list.update({cmd[2]: [d.etag,d.modified]})
              feed_list.update({cmd[2]: []})
              if hasattr(d, 'etag'):
                feed_list[cmd[2]].append(d.etag)
              else:
                feed_list[cmd[2]].append(0)
              if hasattr(d, 'modified'):
                feed_list[cmd[2]].append(d.modified)
              else:
                feed_list[cmd[2]].append(0)
#			  feed_list[cmd[2]][1]=d.get('modified',d.get('updated',d.entries[-1].get('published',0)))

                #https://www.codenong.com/13297077/
#                feed_list[cmd[2]].append(d["headers"]["Date"])
#                await client.send_message(event.chat_id,"header date: "+d["headers"]["Date"])
#                await client.send_message(event.chat_id,"headers: "+str(d["headers"]))
#              if await check_feed(url):
              if d.entries:
                if feed_list[cmd[2]][0] and feed_list[cmd[2]][1]:
                  d=feedparser.parse(url,etag=feed_list[cmd[2]][0],modified=feed_list[cmd[2]][1],request_headers=request_headers)
                  if d.status != 304:
                    d=feedparser.parse(url,etag=d.etag,modified=d.modified,request_headers=request_headers)
                elif feed_list[cmd[2]][0]:
                  d=feedparser.parse(url,etag=feed_list[cmd[2]][0],request_headers=request_headers)
                  if d.status != 304:
                    d=feedparser.parse(url,etag=d.etag,request_headers=request_headers)
                elif feed_list[cmd[2]][1]:
                  d=feedparser.parse(url,modified=feed_list[cmd[2]][1],request_headers=request_headers)
                  if d.status != 304:
                    d=feedparser.parse(url,modified=d.modified,request_headers=request_headers)
                if d.status != 304:
                  await client.send_message(event.chat_id, "W: etag or ctime is not efficient, deleted!")
                  feed_list[cmd[2]][0]=0
                  feed_list[cmd[2]][1]=0
                max_date=await max_entry_date(d)
                feed_list[cmd[2]].append((datetime.datetime(*(max_date[0:6]))+datetime.timedelta(hours=8)).strftime(time_format))
#                  await client.send_message(event.chat_id, "W: bad server, entry's keys:"+str(d.entries[0].keys()))

              else:
                feed_list.pop(cmd[2])
                await client.send_message(event.chat_id, "no entry,deleted")
            if len(cmd) == 4:
              feed_list[cmd[2]].append(int(cmd[3]))
#            await client.send_message(event.chat_id, str(feed_list))
            await client.send_message(event.chat_id, str(feed_list[cmd[2]]))
        elif cmd[1] == "update" or cmd[1] == "up":
          if len(cmd) == 2:
            await client.send_message(event.chat_id, "rss up|update url")
          else:
            if not cmd[2] in feed_list:
              await client.send_message(event.chat_id, "no url")
            else:
              url=cmd[2]
              request_headers={'Cache-control': 'max-age=600'}
              d=feedparser.parse(url,request_headers=request_headers)
#              feed_list.update({cmd[2]: []})
              feed_list[cmd[2]][0]=d.get("etag",0)
              feed_list[cmd[2]][1]=d.get("modified",0)

              info="feed url : "+d.feed.get("link",None)
              info=info+"\nentry num: "+str(len(d.entries))
              if d.entries:
                max_date=await max_entry_date(d)
                feed_list[cmd[2]][2]=(datetime.datetime(*(max_date[0:6]))+datetime.timedelta(hours=8)).strftime(time_format)


                info=info+"\nstatus: "+str(d.get("status",None))
                if feed_list[cmd[2]][0] and feed_list[cmd[2]][1]:
                  d=feedparser.parse(url,etag=feed_list[cmd[2]][0],modified=feed_list[cmd[2]][1],request_headers=request_headers)
                  if d.status != 304:
                    d=feedparser.parse(url,etag=d.etag,modified=d.modified,request_headers=request_headers)
                elif feed_list[cmd[2]][0]:
                  d=feedparser.parse(url,etag=feed_list[cmd[2]][0],request_headers=request_headers)
                  if d.status != 304:
                    d=feedparser.parse(url,etag=d.etag,request_headers=request_headers)
                elif feed_list[cmd[2]][1]:
                  d=feedparser.parse(url,modified=feed_list[cmd[2]][1],request_headers=request_headers)
                  if d.status != 304:
                    d=feedparser.parse(url,modified=d.modified,request_headers=request_headers)
                info=info+"\nstatus new: "+str(d.get("status",None))
                info=info+"\nentry num new: "+str(len(d.entries))
                if d.status != 304:
                  info=info+"\nW: etag or ctime is not efficient, deleted?"
                  info=info+"\nkeys:"+str(d.keys())
                await client.send_message(event.chat_id, info)
              else:
                await client.send_message(event.chat_id, "no entry,delete?")
            await client.send_message(event.chat_id, str(feed_list[cmd[2]]))
        elif cmd[1] == "load":
          import ast
          feed_list=ast.literal_eval(event.raw_text.split(' ',2)[2])
          await client.send_message(event.chat_id, str(feed_list))
        elif cmd[1] == "del":
#          feed_list.pop(int(cmd[1]))
          if len(cmd) == 3:
            feed_list.pop(cmd[2])
          else:
            feed_list[cmd[2]].pop(feed_list[cmd[2]].index(int(cmd[3])))
            if not feed_list[cmd[2]]:
              feed_list.pop(cmd[2])
          if cmd[2] in feed_list:
            await client.send_message(event.chat_id, "E: fail")
          else:
            await client.send_message(event.chat_id, "deleted")

#          await client.send_message(event.chat_id, str(feed_list[cmd[2]]))
#          await client.send_message(event.chat_id, str(feed_list))
        elif cmd[1] == "clear":
          feed_list={}
          await client.send_message(event.chat_id, str(feed_list))
        elif cmd[1] == "se" or cmd[1] == "search":
          found=0
          info=""
          for url in feed_list:
            if cmd[2] in url:
              found+=1
              if found > 5:
#                await client.send_message(event.chat_id, url+" : "+str(feed_list[url])+"\n\n...")
                info=info+"\n\n..."
                break
              else:
                info=info+"\n"+url+" : "+str(feed_list[url])

          if not found:
#          if not info:
            await client.send_message(event.chat_id, "None")
          else:
            await client.send_message(event.chat_id, info)
        else:
          await client.send_message(event.chat_id, "wtf cmd")


      elif cmd[0] == "down":
        if len(cmd) == 1:
          if event.is_reply:
#                msg=event.message
            replied = await event.get_reply_message()
            if replied.media:
#                  path=await replied.download_media(file=DOWNLOAD_PATH+"/",progress_callback=download_media_callback)
#                  path=await asyncio.run(replied.download_media(file=DOWNLOAD_PATH+"/"))
#                  task=asyncio.create_task(download_media(msg,path), name="download_media")
              path=await download_media(replied)
              if path:
                await client.send_message(event.chat_id, "downloaded: " + path +"\nurl: https://"+ MY_DOMAIN +"/"+ urllib.parse.quote(path.split("/")[-1]))
              else:
                await myprint("error")
            else:
              await myprint("no media")
          else:
            await myprint("reply the msg to download")
      elif cmd[0] == "fid":
        msg=await my_get_msg(cmd[1])
        if msg:
          if msg.file:
            await myprint(str(msg.file.id))
          elif msg.media:
            if hasattr(msg.media, 'document'):
              await myprint(str(msg.media.id))
            elif hasattr(msg.media, 'photo'):
              await myprint(str(msg.photo.id))
  #            await myprint(str(type(utils.pack_bot_file_id(msg.photo))))
  #            await myprint(str(utils.pack_bot_file_id(msg.photo)))
            else:
              await myprint(msg.stringify())
          else:
            await myprint(msg.stringify())
        else:
          await myprint("E: can't find msg")
      elif cmd[0] == "file":
  #        msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md', schedule=timedelta(seconds=delay))
  #https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.uploads.UploadMethods.send_file
  #          telethon.utils.pack_bot_file_id(file)
        if len(cmd[1].split('/')) >=5 and cmd[1].split('/')[2] == "t.me":
          msg=await my_get_msg(cmd[1])
          file=msg.file
          if msg and msg.media:
            if hasattr(msg.media, 'document'):
              file=msg.media
            elif hasattr(msg.media, 'photo'):
              file=msg.photo
          if file:
            msg=await client.send_file(event.chat_id, file=file)
          else:
            await myprint("no file")
        else:
  #          await myprint(msg.stringify())
  #          await myprint("file_id can't work")
  #          file=cmd[1]

          file=utils.resolve_bot_file_id(cmd[1])
          #https://github.com/LonamiWebs/Telethon/issues/1613 #file_id in userbot if different from file_id in bot
          await bot.send_file(log_cid, file=file)
      elif cmd[0] == "p" or cmd[0] == "cal":
        if len(cmd) == 1:
          code='''https://docs.python.org/zh-cn/3/howto/unicode.html'''
          code='"""'+code+'"""'
          asyncio.create_task(my_eval(code), name="my_eval")
        else:
          try:
            asyncio.create_task(my_eval(event.raw_text.split(' ',1)[1]), name="my_eval")
          except MessageEmptyError:
            await myprint("E: null msg")
      elif cmd[0] == "pu":
        if len(cmd) == 1:
          code='''
#.encode("ascii","backslashreplace").decode()
#.encode("unicode_escape","backslashreplace").decode()
#.encode().hex()
ascii( "" )
'''
#          code='"""'+code+'"""'
          await myprint(code)
        elif cmd[1] == "o":
          code=event.raw_text.split(' ',2)[2]
          code='"""'+code+'"""'+'''.encode("unicode_escape","backslashreplace").decode()'''
          asyncio.create_task(my_eval(code), name="my_eval")
        else:
          code=ascii(event.raw_text.split(' ',1)[1])
          code=code[1:-1]
          await client.send_message(event.chat_id, code)
          
      elif cmd[0] == "hex":
        if len(cmd) == 1:
#          code='''.encode().hex()'''
#          code='"""'+code+'"""'
          info='''py
c="1"
print(c.encode("unicode_escape","backslashreplace").decode()+" "+c.encode().hex())

# https://docs.python.org/zh-cn/3/library/codecs.html#text-encodings
'''
        elif cmd[1] == "help":
          info='''r
4
u(default)'''
        elif cmd[1] == "raw":
          code=event.raw_text.split(' ',2)[2]
#          code='"""'+code+'"""'+'.encode().hex("\n",-4)'
          info=code.encode().hex()
        elif cmd[1] == "4":
          code=event.raw_text.split(' ',2)[2]
#          code='"""'+code+'"""'+'.encode().hex("\n",-4)'
          info=code.encode().hex("\n",-4)
        elif cmd[1] == "f":
          code=event.raw_text.split(' ',2)[2]
#          code='"""'+code+'"""'+'.encode().hex("\n",-4)'
          info=code.encode().hex("\n",-4)
        else:
          code=event.raw_text.split(' ',1)[1]
#          info=code.encode().hex("\n",-4)
          info=""
          i=0
          for c in code:
            i+=1
            if i != 1:
              info+="\n"
#            info=info+str(i)+" "+c+" "+ c.encode("ascii","backslashreplace").decode()+" "+c.encode().hex()

            #https://docs.python.org/zh-cn/3/library/codecs.html#text-encodings
#            if len(c.strip()) == 0:
            if c.isspace() and c != " ":
              #http://tw.piliapp.com/symbol/square/
#              info=info+str(i)+" "+"⊠ "
#              info=info+str(i)+" "+"◼ "
              info=info+str(i)+" "+"∎ " # half
            else:
              info=info+str(i)+" "+c+" "
#            info=info+c.encode("unicode_escape","backslashreplace").decode()+" "+c.encode().hex()
            info=info+ascii(c)[1:-1]+" "+c.encode().hex()

#        asyncio.create_task(my_eval(code), name="my_eval")
        if info:
#          await myprint(str(info))
          await client.send_message(event.chat_id, str(info))
      elif cmd[0] == "py":
#        if event.raw_text.split("\n",1)[0] == "py":
#          asyncio.create_task(my_exec(event.raw_text.split("\n",1)[1]), name="my_exec")
#        else:
#          asyncio.create_task(my_exec(event.raw_text.split(' ',1)[1]), name="my_exec")
        asyncio.create_task(my_exec(" ".join(cmd[1:])), name="my_exec")
      elif cmd[0] == "echo":
#        asyncio.create_task(my_popen(event.raw_text), name="my_echo")
#        await my_popen("echo "+event.raw_text.split(' ',1)[1])
#        await my_popen(event.raw_text)
        if len(cmd) == 1:
          await cmd_answer("/{}@{} helloworld".format(cmd[0], bot_name))
        else:
#          await my_popen( "echo " + " ".join(cmd[1:]) )
          await my_popen( "echo {}".format(ascii(cmd[1:])) )
      elif cmd[0] == "uptime":
        await my_popen(cmd[0])
      elif cmd[0] == "free":
        await my_popen("free -h; echo; df -h")
      elif cmd[0] == "sh":
        if len(cmd) == 1:
          info="""run shell
sh c: cpu top 10
sh m: mem top 10
"""
#          await myprint(info)
          await cmd_answer(info)
        elif len(cmd) == 2:
          if cmd[1] == "c":
            shell_cmd="ps -eo user,pid,pcpu,pmem,args --sort=-pcpu  |head -n 10"
          elif cmd[1] == "cc":
            shell_cmd="ps -eo user,pcpu,pmem,args --sort=-pcpu  |head -n 10"
          elif cmd[1] == "ccc":
            shell_cmd="ps -eo pcpu,args --sort=-pcpu  |head -n 10"
          elif cmd[1] == "m":
            shell_cmd="ps -eo user,pid,pcpu,pmem,args --sort=-pmem  |head -n 10"
          elif cmd[1] == "mm":
            shell_cmd="ps -eo user,pcpu,pmem,args --sort=-pmem  |head -n 10"
          elif cmd[1] == "mmm":
            shell_cmd="ps -eo pmem,args --sort=-pmem  |head -n 10"
          else:
            shell_cmd=cmd[1]
          await my_popen(shell_cmd)
#        asyncio.create_task(my_popen(event.raw_text.split(' ',1)[1]), name="my_sh")
#        await my_popen(event.raw_text.split(' ',1)[1])
#        await my_popen(" ".join(cmd[1:]))
        else:
          await my_popen(" ".join(cmd[1:]))
      elif cmd[0] == "b64":





        if len(cmd) == 1:
          info="data:;charset=utf8;base64,SGVsbG8gV29ybGQg8J+Qtg=="
        elif cmd[1] == "fp":
          info="""
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
          info="""
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
          info=encode_base64(event.raw_text.split(' ',2)[2])
        elif cmd[1] == "d":
#          info=decode_base64(event.raw_text.split(' ',2)[2]).decode()
#          info=base64.b64decode(event.raw_text.split(' ',2)[2].encode()).decode()
          info=base64.b64decode(event.raw_text.split(' ',2)[2].encode() + b'=' * (-len(event.raw_text.split(' ',2)[2].encode()) % 4)).decode()
        else:
#          import base64
#          info=base64.b64decode(event.raw_text.split(' ',1)[1].encode()).decode()
#          info=base64.b64decode(event.raw_text.split(' ',1)[1].encode() + b'=' * (-len(event.raw_text.split(' ',1)[1].encode()) % 4)).decode()
          info=decode_base64(event.raw_text.split(' ',1)[1]).decode()
        await myprint(info)
      elif cmd[0] == "mkchat":
        result = await client.functions.messages.CreateChatRequest(users=['liqsliu_bot'],title=me.username)
        await myprint(result.stringify())
      elif cmd[0] == "ad":
#        info=await get_admin_of_channel(cmd[1])
        info=await get_admins(cmd[1])
        await myprint(info)
      elif cmd[0] == "id":
        if len(cmd) == 1:
          info="tg://openmessage?user_id="
          await myprintmd(info)
          info="tg://openmessage?chat_id="
          await myprintmd(info)
        else:
  #          await client.send_message(me.id, str(type(peer)))
  #          if type(peer) == PeerUser:
  #        peer=await client.get_entity(id)
          peer=await get_peer(cmd[1])
          if type(peer) == User:
            if peer.username:
              name="@"+peer.username
            else:
              name=peer.first_name
    #          await client.send_message(me.id, "["+str(peer.id)+"](tg://user?id="+str(peer.id)+")", parse_mode="md")
            if name:
              info="["+name+"](tg://openmessage?user_id="+str(peer.id)+")"
              info=info+" tg://openmessage?user_id="+str(peer.id)
            else:
              info="deleted user: tg://openmessage?user_id="+str(peer.id)
          else:
    #          "\ntg://openmessage?chat_id="+str(cid))+"\ntg://openmessage?user_id="+str(msg.sender_id))+"\n\nby draft\ncid: `"+str(cid)+"`\nuid: `"+str(msg.sender_id)+"`"
            info="tg://openmessage?chat_id="+str(peer.id)
    #        info = "```\n"+ mdraw(peer.stringify(),"code") +"\n```\n\n"+ info+"\n"+str(type(peer))+ ": `" +str(utils.get_peer_id(peer))+"`"
          info = info+"\n"+str(type(peer))+ ": `" +str(utils.get_peer_id(peer))+"`"
          if len(peer.stringify()+"\n\n"+info) > MAX_MSG_LEN:
            await myprintmd(info)
            await myprint(peer.stringify())
          else:
    #          await myprintmd(peer.stringify() +"\n\n"+ info)
            await myprintmd("```\n"+mdraw(peer.stringify(),"`") +"\n```\n\n"+ info)
      elif cmd[0] == "link":
        url=cmd[1]
  #          chat=utils.resolve_id(cid)[1]
        msg=await my_get_msg(cmd[1])
        if msg:
  #          info=mdraw(msg.stringify(),"code")
          info=mdraw(msg.stringify(),"`")
          info="```\n"+info+"\n```"
          info=info+"\n\ntg://openmessage?chat_id="+str(utils.resolve_id(msg.chat_id)[0])+"\ncid: `"+str(msg.chat_id)+"`"
          if msg.sender_id and msg.chat_id != msg.sender_id:
            if msg.sender_id > 0:
              info=info+"\n\ntg://openmessage?user_id="+str(msg.sender_id)+"\nuid: `"+str(msg.sender_id)+"`"
            else:
              info=info+"\n\ntg://openmessage?chat_id="+str(utils.resolve_id(msg.sender_id)[0])+"\ncid: `"+str(msg.sender_id)+"`"
          if "?comment=" in url:
  #chat=await client.get_entity(chat_id)
            chat=msg.chat
            if chat.username:
              info=info+"\nmsg link: https://t.me/"+chat.username+"/"+str(msg.id)
            else:
              info=info+"\n\nmsg link: https://t.me/c/"+str(cid)+"/"+str(msg.id)
        else:
  #          info=mdraw(msg.stringify(),"code")
          info="no msg"
  #        await client.send_message(me.id, "msg:" + msg)
  #        await myprint("msg: " + msg)
        await myprintmd(info)
      elif cmd[0] == "idf":
        peer=await client.get_input_entity(await get_id(cmd[1]))
#        peer=await client.get_entity(await get_id(cmd[1]))
#        if not peer:
#          peer=await client.get_entity(utils.get_peer_id(peer))
#          peer=await client.get_entity(await get_id(cmd[1]))
#        if type(peer) == User:
        if type(peer) == InputPeerUser:
#          peer = await client.functions.users.GetFullUserRequest(id=peer)
          peer = await client(functions.users.GetFullUserRequest(id=peer))
  #            await client.send_message(me.id, peer.stringify())
  #          await myprint(peer.stringify())
          info=str(type(peer))+ ": `"+str(utils.get_peer_id(peer.user))+"`"
#        elif type(peer) == Chat:
        elif type(peer) == InputPeerChat:
#          peer = await client.functions.messages.GetFullChatRequest(peer.id)
          peer = await client(functions.messages.GetFullChatRequest(peer.chat_id))
          info=str(type(peer))+ ": `"+str(utils.get_peer_id(peer.full_chat))+"`"
  #        elif type(peer) == Channel:
        elif type(peer) == InputPeerChannel:
        #https://docs.telethon.dev/en/latest/concepts/chats-vs-channels.html
        #megagroups are channels
#        elif peer.broadcast or peer.megagroup or peer.gigagroup:
#          peer = await client.functions.channels.GetFullChannelRequest(peer)
          peer = await client(functions.channels.GetFullChannelRequest(peer))
          info=str(type(peer))+ ": `"+str(utils.get_peer_id(peer.full_chat))+"`"
        else:
          peer=await client.get_entity(await get_id(cmd[1]))
          info="unknown type,not full:"+str(type(peer))
        if len("```\n"+ mdraw(peer.stringify(),"code") +"\n```\n\n"+ info) > MAX_MSG_LEN:
          if len(peer.stringify()) > MAX_MSG_LEN:
            await myprintmd(info)
            await myprint(peer.stringify())
          else:
            await myprint(peer.stringify())
            await myprintmd(info)
        else:
          info = "```\n"+ mdraw(peer.stringify(),"code") +"\n```\n\n"+ info
          await myprintmd(info)
      elif cmd[0] == "am":
        if event.raw_text == "am":
          await myprint(str(auto_msg_list))
        elif len(cmd) != 4:
  #          await myprint("id [ctime interval target text]")
          await myprint("am interval target text")
          
        else:
          ctime=time.time()
          interval=int(cmd[1])
          target=int(cmd[2])
          text=event.raw_text.split(' ', 3)[3]
          item=[ctime,interval,target,text]
          if len(auto_msg_list) == 0:
            max_id=0
          else:
            max_id=auto_msg_list.keys()[-1]
          auto_msg_list.update({max_id+1:item})
          await myprint(str(auto_msg_list[max_id+1]))
      elif cmd[0] == "amadd":
#        await myprint("id [ctime interval target text]")
  #        await myprint("am interval target text")
        await myprint("am interval target text")
      elif cmd[0] == "amload":
        import ast
        auto_msg_list=ast.literal_eval(event.raw_text.split(' ',1)[1])
        await myprint(str(auto_msg_list))
      elif cmd[0] == "amdel":
        auto_msg_list.pop(int(cmd[1]))
        await myprint(str(auto_msg_list))
      elif cmd[0] == "amclear":
        auto_msg_list={}
        await myprint(str(auto_msg_list))
      elif cmd[0] == "af":
        if event.raw_text == "af":
          await myprint(str(auto_forward_list))
        else:
          if len(cmd) == 3:
            auto_forward_list.update({int(cmd[1]):int(cmd[2])})
            await myprint(str(auto_forward_list))
          else:
            await client.send_message(myid, "格式有误: am cid cid")
      elif cmd[0] == "afad":
        await client.send_message(myid, "格式: am cid cid")
      elif cmd[0] == "afload":
  #        import json
  #        auto_forward_list=json.loads(event.raw_text.split(' ',1)[1])
  #        auto_forward_list=eval(event.raw_text.split(' ',1)[1])
        import ast
        auto_forward_list=ast.literal_eval(event.raw_text.split(' ',1)[1])
        await client.send_message(me.id, str(auto_forward_list))
      elif cmd[0] == "aflist":
        await client.send_message(me.id, str(auto_forward_list))
      elif cmd[0] == "afdel":
        auto_forward_list.pop(int(cmd[1]))
        await client.send_message(me.id, str(auto_forward_list))
      elif cmd[0] == "afclear":
        auto_forward_list={}
        await client.send_message(me.id, str(auto_forward_list))

      elif cmd[0] == "msgclear":
        if client == bot:
          await client.send_message(me.id, "W: please use userbot")
          return
        if len(cmd) == 1:
          await client.send_message(me.id, "msgclear http://t.me/... [max_msg_id]")
          return

        url=cmd[1]
        if cmd[1][0] =="@":
          peer=await client.get_entity(cmd[1][1:])
        elif url.split('/')[2] == "t.me":
          if url.split('/')[3] == "c":
            cid=int(url.split('/')[4])
            max_msg_id=int(url.split('/')[5])
          else:
            cid=url.split('/')[3]
            max_msg_id=int(url.split('/')[4])
          peer=await client.get_entity(cid)
        else:
          peer=await client.get_entity(int(cmd[1]))
        if len(cmd) == 3:
          max_msg_id=int(cmd[2])
        if max_msg_id:
          await client.delete_messages(peer, message_ids=list(range(1,max_msg_id+1)))
          await client.send_message(me.id, "clear ok")
        else:
          await client.send_message(me.id, "格式有误")

    async def forward_msg():
      chat_id = event.chat_id
      #https://www.runoob.com/python/att-dictionary-has_key.html
  #    elif chat_id in auto_forward_list and not await is_debug("auto_forward"):
      if chat_id in auto_forward_list:
  #      schat=utils.resolve_id(chat_id)[1]
  #      schat=await client.get_entity(chat_id)
        cid=auto_forward_list[chat_id]
        #chat=await client.get_entity(cid)
  #      chat=PeerChannel(cid)
  #      chat=utils.resolve_id(cid)[1]
        chat=await client.get_input_entity(cid)
        if chat:
  #        await event.forward_to(chat)
          msg=event.message
          if msg.grouped_id != None:
            grouped_id = msg.grouped_id
            msg_id=msg.id
            schat=await client.get_input_entity(chat_id)
            msg=await client.get_messages(schat, ids=msg_id-1)
            if not msg or grouped_id != msg.grouped_id:
    #          msg0 = await client.get_messages(schat, ids=msg_id)
    #          msg = event.message
    #          msgs=[await client.get_messages(schat, ids=msg_id)]
              msgs = [event.message]
  #            await asyncio.sleep(30)
              #for id in range(msg_id+1,end_id+1):
              for id in range(msg_id+1,msg_id+16):
                msg=await client.get_messages(schat, ids=msg_id)
                msgs.append(msg)
                if msg:
                  if msg.grouped_id == grouped_id:
                    await asyncio.sleep(0.5)
                  else:
                    break
                else:
                  break
              await client.forward_messages(chat, messages=msgs)
          else:
            await msg.forward_to(chat)
      return




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

    msg_before_return=""
    if client==bot:
      client_id=bot_id
      client2=userbot
    else:
      client_id=me.id
      client2=bot

    if event.chat_id == cid_wtfipfs:
      if type(event.from_id) == PeerChannel:
        if client==userbot:
#        if client == bot:
          if event.sender_id == cid_tw:
            while True:
              try:
                await event.unpin()
              except FloodWaitError as e:
                await asyncio.sleep(e.seconds+5)
                continue
              break
            return
          else:
            await event.delete()
            while True:
              try:
                await myprint("I: get a channel msg in wtf from: "+str(event.sender_id))
                await ban_chat(event.chat_id, event.sender_id)
              except FloodWaitError as e:
                await asyncio.sleep(e.seconds+5)
                continue
              break
            return
    elif event.chat_id == cid_fw:
      if type(event.from_id) == PeerChannel:

#        if event.sender_id == cid_tw:
        if client == bot:
          await event.delete()
          while True:
            try:
              await myprint("I: get a channel msg in fw from: "+str(event.sender_id))
              await ban_chat(event.chat_id, event.sender_id)
            except FloodWaitError as e:
              await asyncio.sleep(e.seconds+5)
              continue
            break
#          await myprint(event.stringify())
#          target=await client.get_input_entity(target)
#      chat=await client.get_input_entity(chat.id)
#          await ban_chat(await client.get_input_entity(event.chat_id), await client.get_input_entity(event.sender_id))
          return
    cmd=[]
    if event.raw_text:
      cmd=event.raw_text.split(' ')
  #    if len(event.raw_text.split(' ',1)[0].split("\n",1)) == 2:
  #    if len(cmd[0].split("\n",1)) == 2:
      if "\n" in cmd[0]:
        cmd=cmd[0].split('\n',1)+cmd
  #      del cmd[2]
        cmd.pop(2)
      if event.raw_text[0] == "/":
        if client == bot:
#          if event.mentioned:
          cmd[0] = cmd[0].lstrip("/")
          if cmd[0].endswith("@{}".format(bot_name)):
            cmd[0] = cmd[0].rstrip("@{}".format(bot_name))
      elif event.raw_text[0] == ".":
        if client == userbot:
#          if event.out:
          cmd[0] = cmd[0].lstrip(".")

    #https://stackoverflow.com/a/53519143
#    if event.peer_id.broadcast:
#    if event.from_id == None:
#    if await check_status_before_cmd() == 0b000:
# https://docs.telethon.dev/en/latest/modules/custom.html#telethon.tl.custom.chatgetter.ChatGetter
    if event.is_channel and event.chat.broadcast:
      if client==userbot:
        await forward_msg()
      else:
        await myprint("E: wtf: bot get a msg from channel")
    elif event.raw_text and cmd and cmd[0] and cmd[0] in cmd_dict and await check_status_before_cmd(cmd_dict[cmd[0]][0]):
      if debug:
        await myprint("D: run cmd: "+str(cmd))
      await run_cmd(cmd)
    elif event.chat_id == myid:
      #for admin: dump msg
      msg=event.message
      if debug:
#          await myprint(event.stringify())
        if client == bot:
          await myprint(msg.stringify())
        else:
          await myprint(msg.stringify())
        await myprint("sender: "+msg.sender.stringify())
        if type(event.peer_id) != PeerUser:
          await myprint("chat: "+msg.chat.stringify())
      else:
        if client == bot:
#          await myprint(event.original_update) #UpdateNewMessage
          await myprint(event.original_update.stringify())

      msg=event.forward
      if msg:
#        await myprint(msg.stringify())
#        chat=msg.chat
#          chat = await msg.get_chat()
#        elif type(msg.from_id) == PeerChannel:



        chat_id=None
        sender_id_id=None
        info=""


        peer=msg.from_id
        if peer:
          sender_id=utils.get_peer_id(peer)
          if sender_id:
            info=info+"from: "+str(type(peer))
            if sender_id < 0:
              info=info+"\ncid: `"+str(sender_id)+"`"
            else:
              info=info+"\nuid: `"+str(sender_id)+"`"
#          sender_id = msg.sender_id

        peer=msg.saved_from_peer
        msg_id=msg.saved_from_msg_id
        if peer:
          chat_id=utils.get_peer_id(peer)
          if sender_id and chat_id and sender_id != chat_id:
            info=info+"\n\nchat: "+str(type(peer))
            info=info+"\ncid: `"+str(chat_id)+"`"
#          chat_id = msg.chat_id

#          chat=await client.get_entity(chat_id)

#          info=info+"\nmsg link: https://t.me/c/"+chat_id+"/"+str(msg.id)
#          if msg_id:
#            info=info+"\nmsg link: https://t.me/c/"+utils.resolve_id(cid)[0]+"/"+str(msg_id)
#          await myprint(info, parse_mode="md")

#          drafts=await client.get_drafts()
#          if type(drafts) == list and len(drafts) >= 1:
#            draft=drafts[0]
#          chat=None

        if True:
#        if client == userbot or client == bot:

#          async for draft in client.iter_drafts():
          async for draft in userbot.iter_drafts():
            if draft.text == "":
  #            print(draft.text)
  #              await client.send_message(me.id, "fwd:" + event.message.stringify())
  #            await client.send_message(me.id, str(draft))
  #              await client.send_message(me.id, draft.stringify())
              msg_id=draft.reply_to_msg_id
              if msg_id != None:
  #                cid=draft.entity.id
  #                chat=await client.get_input_entity(cid)
  #                msg=await client.get_messages(chat,ids=msg_id)
#                msg=await client.get_messages(draft.entity,ids=msg_id)
                msg=await userbot.get_messages(draft.entity,ids=msg_id)

                chat=msg.chat
                if msg:
                  chat_id=msg.chat_id
                  msg_id=msg.id
                  await draft.set_message(text="["+str(msg.sender_id)+"](tg://user?id="+str(msg.sender_id)+")", parse_mode="md")
                  info="```\n"+mdraw(msg.stringify(),"code")+"\n```\n\ntg://openmessage?chat_id="+str(utils.resolve_id(chat_id)[0])+"\ntg://openmessage?user_id="+str(msg.sender_id)+"\n\nby draft\ncid: `"+str(chat_id)+"`\nuid: `"+str(msg.sender_id)+"`"
  #                  await client.send_message(me.id, info, parse_mode="md")
  #                  info="uid: "+str(msg.sender_id)
  #                  await draft.set_message(text="["+str(msg.sender_id)+"](tg://user?id="+str(msg.sender_id)+") "+info, parse_mode="md")
  #                  await client.send_message(me.id, "["+str(msg.sender_id)+"](tg://user?id="+str(msg.sender_id)+")", parse_mode="md")
        if chat_id and msg_id:
          info=info+"\nmsg link: https://t.me/c/"+str(utils.resolve_id(chat_id)[0])+"/"+str(msg_id)
        if len(info) > MAX_MSG_LEN:
          info="tg://openmessage?chat_id="+str(utils.resolve_id(chat_id)[0])+"\ntg://openmessage?user_id="+str(msg.sender_id)+"\n\nby draft\ncid: `"+str(chat_id)+"`\nuid: `"+str(msg.sender_id)+"`"
          if chat_id and msg_id:
            if not chat.username:
              if chat.is_private:
                chat=msg.get_sender()
              else:
                chat=msg.get_chat()
              if not chat.username:
                chat=await client.get_entity(chat.id)
            if chat.username:
              info=info+"\nmsg link: https://t.me/"+chat.username+"/"+str(msg_id)
            else:
              info=info+"\nmsg link: https://t.me/c/"+str(utils.resolve_id(chat_id)[0])+"/"+str(msg_id)
            info=info+"\nmsg link2: tg://openmessage?chat_id="+str(utils.resolve_id(chat_id)[0])+"&message_id="+str(msg_id)
          if len(msg.stringify()) > MAX_MSG_LEN:
            await myprintmd(info)
            await myprin(msg.stringify())
          else:
            await myprin(msg.stringify())
            await myprintmd(info)
        else:
          await myprintmd(info)
      return True
    else:
      pass




#  except Exception as e:
  except:
#    await client.send_message(me.id, "E: "+str(e)+"\n==\n"+traceback.format_exc())
#    await myprint("==\n"+traceback.format_exc())
#    await bot.send_message(me.id, "E: "+str(e)+"\n==\n"+traceback.format_exc())
#    await client.send_message(me.id, "E: "+sys.exc_info()[0]+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info()))
    info="E: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
    await bot.send_message(myid, info)
    if client == userbot:
      await client.send_message(myid, "E: > tg://openmessage?user_id="+str(bot_id))


#https://www.codenong.com/13297077/
async def max_entry_date(feed):
#  if 'published', 'updated' ]:
#  entry_pub_dates = (e.get('published_parsed') for e in feed.entries)
#  entry_pub_dates = (e.get('updated_parsed', e.get('published_parsed',time.localtime())) for e in feed.entries)
  entry_pub_dates = (e.get('updated_parsed', e.get('published_parsed',time.gmtime())) for e in feed.entries)
#  entry_pub_dates = tuple(e for e in entry_pub_dates if e is not None)
  entry_pub_dates = tuple(e for e in entry_pub_dates if e != None)
  if len(entry_pub_dates) > 0:
    return max(entry_pub_dates)    
#  return None
#  return time.localtime()
  return time.gmtime()



#time_format="%Y%m%d_%H%M%S%z" #strptime() can not identify %z , zoneinfo will be -1(unknown)
#time_format="%Y%m%d_%H%M%S%Z" #zoneinfo is not correct, always is HKT
time_format="%Y%m%d_%H%M%S"


#async def send_entry_task(cid=0):
#  t=threading.Thread(target=send_entry_task_1, kwargs={"cid":cid})
#  t.start()
#  t.join()
#  while t.is_alive():
#    await asyncio.sleep(5)

#def send_entry_task_1(cid=0):
#  asyncio.run(send_entry_task_2(cid))





#need_wait=False
need_wait=0

async def send_entry_task(cid=cid_btrss):
  global entry_task
  global need_wait

#  while True:
#    for msg in entry_task.copy():
#  for i in range(0,MAX_AUTO_MSG_TASK_TIME,3):
  i=0
  await asyncio.sleep(1)
  while i < MAX_AUTO_MSG_TASK_TIME:
    if len(entry_task) > 512:
      entry_task=[]
      await bot.send_message(myid, "E: waiting entry num > 512, cleared!")

    msg=None
    for msg in entry_task:
      if msg[0] == myid:
        entry_task.remove(msg)
#        elif msg[0] == cid_btrss and cid == cid_btrss:
      elif msg[0] != cid:
        msg=None
        continue
      else:
        entry_task.remove(msg)
      break

    if msg:
      if debug:
        print("I: task got a msg")
      try:
        i=0
        while need_wait:
          await asyncio.sleep(5)
          i+=1
          if i > 512:
            await bot.send_message(myid, "E: send_entry_task wait too long, wtf?")
            break

        if len(msg) == 2:
          #          await bot.send_message(msg[0], msg[1],parse_mode="htm")
          await bot.send_message(msg[0], msg[1],parse_mode="htm")
        elif len(msg) == 3:
          await bot.send_message(msg[0], msg[1],parse_mode="htm",link_preview=msg[2])
        elif len(msg) == 4:
          await bot.send_message(msg[0], msg[1],parse_mode=msg[3],link_preview=msg[2])
        elif len(msg) == 5:
          # tw_fav with files
#      msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md')
          if len(msg[4]) == 1:
            await bot.send_file(msg[0], file=msg[4][0], caption=msg[1], parse_mode=msg[3], link_preview=msg[2])
          else:
            await bot.send_file(msg[0], file=msg[4], caption=msg[1], parse_mode=msg[3], link_preview=msg[2])
        else:
          await bot.send_message(myid, "E: wtf entry_task msg:"+str(msg))
#        except telethon.errors.rpcerrorlist.FloodWaitError as e:
      except FloodWaitError as e:
#        need_wait=True
        need_wait+=1

#          entry_task.append(msg)
        entry_task.insert(0,msg)

        info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
        print(info)

        await asyncio.sleep(e.seconds)
        await asyncio.sleep(5)

#        need_wait=False
        need_wait-=1
        if need_wait < 0:
          need_wait=0
      except:
        info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
        await bot.send_message(myid, "E: entry_task: msg: "+str(msg)+ "\n==\n" +info)
      i=0 # for loop
    else:
      i+=3
    await asyncio.sleep(3)

entry_task=[]
#[cid,info,False,"htm",files]

async def send_entry(entry, url):
#      threading.Thread(target=send_entry_task).start()
  global entry_task
  tasks=[]
  for j in asyncio.all_tasks():
    tasks.append(j.get_name())
  if len(feed_list[url]) == 3:
    task_name="send_entry_task"
    if task_name not in tasks:
      asyncio.create_task(send_entry_task(),name=task_name)
  elif len(feed_list[url]) > 3:
    for cid in feed_list[url][3:]:
      task_name="send_entry_task_"+str(cid)
      if task_name not in tasks:
        asyncio.create_task(send_entry_task(cid),name=task_name)
  else:
    await bot.send_message(myid, "E: rss url data error: "+url)
    return
  #        await myprint("new rss: "+str(entry))
  #        await bot.send_message(myid, "new rss: "+str(entry))
#          await bot.send_message(myid, "new rss: "+entry.link+"\n"+entry.title+"\n"+entry.updated)
  info=entry.link+"\n<b>"+entry.title+"</b>\n"+entry.get("updated",entry.get("published","E: wtf!"))
  info2=entry.get("description", entry.get("content", entry.get("summary","")))
  info=info+"\n"+info2
  if len(info) > 4096:
    info=info[0:4090]+"..."
#    await bot.send_message(myid, info,parse_mode="htm")
  if len(feed_list[url]) == 3:
#      await bot.send_message(cid_btrss, info,parse_mode="htm")
    entry_task.append([cid_btrss,info])
  elif len(feed_list[url]) < 3:
    return
  else:
    for cid in feed_list[url][3:]:
      if info2:
#          await bot.send_message(cid, info,parse_mode="htm",link_preview=False)
        entry_task.append([cid,info,False])
      else:
#          await bot.send_message(cid, info,parse_mode="htm")
        entry_task.append([cid,info])




async def get_one_feed(url,**kwargs):
  global feeds
#    d=feedparser.parse(url,etag=status[0],modified=status[1],request_headers=request_headers)
  d=0
  try:
    if "etag" in kwargs and "modified" in kwargs:
      d=feedparser.parse(url,etag=kwargs["etag"],modified=kwargs["modified"],request_headers=kwargs["request_headers"])
    elif "etag" in kwargs:
      d=feedparser.parse(url,etag=kwargs["etag"],request_headers=kwargs["request_headers"])
    elif "modified" in kwargs:
      d=feedparser.parse(url,modified=kwargs["modified"],request_headers=kwargs["request_headers"])
    else:
      d=feedparser.parse(url,request_headers=kwargs["request_headers"])
  except:
    return False
  if d:
    if hasattr(d, 'status'):
      if d.status != 304:
#        feeds.append(dict(d).copy())
        if hasattr(d.feed, 'link'):
          feeds.append(d)
          if debug:
            print("I: got "+url)
          return True
  return False




feeds=[]
t_1_tasks=[]


async def get_feed():
  if debug:
    print("I: new update_feed lood")
#  for url in feed_list:
  for url in feed_list.copy():
    global t_1_tasks
    t_1_tasks=[]
    for j in asyncio.all_tasks():
      if t_1.is_alive():
        t_1_tasks.append(j.get_name())
    if url not in feed_list:
      continue
    status=feed_list[url]
    d={}
    for j in asyncio.all_tasks():
#        tasks.append(j.get_name())
      if j.get_name() == url:
        print("E: rss timeout: "+url)
        j.cancel()
        await asyncio.sleep(5)
        if j.done():
          print("E: rss stoped: "+url)
          break
        else:
          print("E: can't stop rss:  "+url)
          j.cancel()
          break
    if status[0] == "disable" or status[0] == 1 :
      continue
    if debug:
      print("I: get "+url)
#    if status[0] == "updated" or status[0] == "published":
#      if status[0] == 0 or status[1] == 0:
#      continue
    request_headers={'Cache-control': 'max-age=600'}
    if status[0] and status[1]:
  #  t.start()
  #  t.join()
  #  while t.is_alive():
#        d=feedparser.parse(url,etag=status[0],modified=status[1],request_headers=request_headers)
      asyncio.create_task(get_one_feed(url,etag=status[0],modified=status[1],request_headers=request_headers), name=url)
    elif status[0]:
#        d=feedparser.parse(url,etag=status[0],request_headers=request_headers)
      asyncio.create_task(get_one_feed(url,etag=status[0],request_headers=request_headers), name=url)
    elif status[1]:
#        d=feedparser.parse(url,modified=status[1],request_headers=request_headers)
      asyncio.create_task(get_one_feed(url,modified=status[1],request_headers=request_headers), name=url)
    else:
#        d=feedparser.parse(url)
      asyncio.create_task(get_one_feed(url,request_headers=request_headers), name=url)
#      await asyncio.sleep(1)
#      await asyncio.sleep(len(asyncio.all_tasks())/5+len(entry_task)/2+1)
#        time.sleep(3)
#  await save_config()
    await asyncio.sleep(len(asyncio.all_tasks())/2)

def get_feed_t1():
  if debug:
    print("I: new update_feed lood")
  for url in feed_list.copy():
    global t_1_tasks
    if url not in feed_list:
      continue
    status=feed_list[url]
    d={}
    if status[0] == "disable" or status[0] == 1 :
      continue
    if debug:
      print("I: get "+url)
    request_headers={'Cache-control': 'max-age=600'}
    try:
      if status[0] and status[1]:
        d=feedparser.parse(url,etag=status[0],modified=status[1],request_headers=request_headers)
      elif status[0]:
        d=feedparser.parse(url,etag=status[0],request_headers=request_headers)
      elif status[1]:
        d=feedparser.parse(url,modified=status[1],request_headers=request_headers)
      else:
        d=feedparser.parse(url,request_headers=request_headers)
    except:
      info="E: get_feed_t1 raise an Exception, url: "+url
      print(info)
      info="E: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
      print(info)
#      asuncio.run(bot.send_message(myid, info))
      global entry_task
      entry_task.append([myid,info,False,None])
      info="E: get_feed_t1 raise an Exception, url: "+url
      entry_task.append([myid,info,False,None])
      continue
    if d:
      if hasattr(d, 'status'):
        if d.status != 304:
  #        feeds.append(dict(d).copy())
          if hasattr(d.feed, 'link'):
            global feeds
            feeds.append(d)
            if debug:
              print("I: got "+url)


async def get_feed_loop_bu():
  while True:
    if debug:
      print("I: new loop: get_feed")
    await get_feed()
    await save_config()
    if debug:
      print("I: loop end: get_feed")
#    await asyncio.sleep(60)
#    await asyncio.sleep(30/len(feed_list)+len(feeds)+len(entry_task)+1)


#def get_feed(status,url):
def get_feed_loop():
  global entry_task
  entry_task.append([myid,"get_feed_loop start",False,None])
#  await start_send_entry_task(cid=myid)

  #https://stackoverflow.com/questions/9772691/feedparser-with-timeout
  import socket
  socket.setdefaulttimeout(300)

  while True:
    if debug:
      print("I: new loop: get_feed")
    try:
      get_feed_t1()
    except:
      print("E: get_feed_t1 raise an Exception")
      info="E: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
      print(info)
#      asuncio.run(bot.send_message(myid, info))
      entry_task.append([myid,info,False,None])
#    if not t_1.is_alive():
#      print("I: thraed 1 is dead")
#      await save_config()
#      await asyncio.sleep(5)
      #https://stackoverflow.com/questions/46992496/runtimeerror-threads-can-only-be-started-once
#      t_1=threading.Thread(target=thread_1,daemon=True)
#      t_1.start()

    if debug:
      print("I: loop end: get_feed")
#    time.sleep(60)
    time.sleep(60/len(feed_list)+len(feeds)+len(entry_task)+30)

def thread_2():
  try:
    asyncio.run(mt_read())
#    mt_read()
  except:
    info="E: thraed 2 raise an Exception: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
    print(info)
#    await bot.send_message(myid, info)
    global entry_task
    entry_task.append([myid, info, False])


def thread_1():
  try:
#  asyncio.run(parse_feed())
#    asyncio.run(get_feed_loop())
#    get_feed_t1()
    get_feed_loop()
  except:
    info="E: thraed 1 raise an Exception: "+str(sys.exc_info()[0])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
#    await bot.send_message(myid, info)
    print(info)
  print("thraed 1 is over")
  global entry_task
  entry_task.append([myid,"thread 1 is over",False])

t_1=threading.Thread(target=thread_1,daemon=True)
t_2=threading.Thread(target=thread_2,daemon=True)

async def get_feed_main():
  t_1.start()
#  await get_feed_loop()
  task_name="parse_feed"
  asyncio.create_task(parse_feed(),name=task_name)
  asyncio.create_task(tw_fav_loop(),name="tw_fav_loop")

#  t_2.start()


async def parse_feed():
  global feed_list
  global feeds
#  t=threading.Thread(target=get_feed, kwargs={"status":status,"url":url})
#  task_name="get_feed"
#  asyncio.create_task(get_feed(),name=task_name)
  while True:
#    if debug:
#      t_1_tasks=[]
#      for j in asyncio.all_tasks():
#        t_1_tasks.append(j.get_name())
#    await asyncio.sleep(MAX_AUTO_MSG_TASK_TIME / (40+len(feed_list)) + 50 )
#    await asyncio.sleep(8)
    await asyncio.sleep(len(entry_task)/5+8)
    await save_config()
    while True:
      await asyncio.sleep(1)
#      if threading.active_count() == 1:
#        if len(feeds) == 0:
#          break
      if len(feeds) == 0:
        break
      d=feeds[0]
      feeds.pop(0)
#      feeds.remove(d)
    #    elif status[0] == "published" or status[0] == "updated":
         
#      url=d.feed.link
      url=d.feed.title_detail.base
      if url not in feed_list:
#        url=d.feed.link
        for link in d.feed.links:
          if link.rel == "self":
            url=link.href
            break
        if url not in feed_list:
          continue
      status=feed_list[url]
      if d.get('etag',0) or d.get('modified',0):
        status[0] = d.get('etag',0)
        status[1] = d.get('modified',0)

      url_count=0
      url_max=int(720/(20+len(d.entries))+2)
      if type(status[2]) != str:
        await bot.send_message(myid, "E: rss url data error: "+url)
        continue
      old_max_date=(datetime.datetime.strptime(status[2], time_format)-datetime.timedelta(hours=8)).utctimetuple()
      new_max_date=()
      for entry in d.entries:
        if entry.get("updated_parsed",entry.get("published_parsed",old_max_date)) > old_max_date:
          await send_entry(entry,url)
          if new_max_date:
            new_max_date=max(( new_max_date,entry.get("updated_parsed",entry.get("published_parsed",old_max_date)) ))
          else:
            new_max_date=entry.get("updated_parsed",entry.get("published_parsed",old_max_date))
          url_count+=1
          if url_count > url_max:
            await bot.send_message(cid_btrss, "W: too many rss : "+url+"\n"+str(len(d.entries))+" > "+str(url_max))
            break
        else:
          continue
      if new_max_date and new_max_date != old_max_date:
        if url not in feed_list:
          continue
        feed_list[url][2] = (datetime.datetime(*(new_max_date[0:6]))+datetime.timedelta(hours=8)).strftime(time_format)
    #      await save_config() # no need save too early, or will be telethon.errors.rpcerrorlist.FloodWaitError:
    #  if config_save_buffer != [auto_forward_list,auto_msg_list,feed_list]:
#    await save_config()


# https://stackoverflow.com/a/9807138
def decode_base64(data, altchars=b'+/'):
  """Decode base64, padding being optional.

  :param data: Base64 data as an ASCII byte string
  :returns: The decoded byte string.

  """
  if type(data) == str:
    data=data.encode()
  data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
  missing_padding = len(data) % 4
  if missing_padding:
    data += b'='* (4 - missing_padding)
  return base64.b64decode(data, altchars)

def encode_base64(data):
  if type(data) == str:
    data=data.encode()
  return base64.b64encode(data).decode().rstrip("=")


def compress(data):
  if type(data) == str:
    data=data.encode()
  return zstandard.compress(data,level=22)
#  return zlib.compress(data,level=9)

def decompress(data):
  if type(data) == str:
    data=data.encode()
  return zstandard.decompress(data)



async def save_config():
  global config_save_buffer
  if config_save_buffer != str([auto_forward_list,auto_msg_list,feed_list]).replace(" ", "").strip():
    chat=await userbot.get_input_entity(myid)
    msg=await userbot.get_messages(chat, ids=config_saved_msgid)
    if chat and msg:
#      config_save_buffer=[auto_forward_list,auto_msg_list,feed_list]
      config_save_buffer = str([auto_forward_list,auto_msg_list,feed_list]).replace(" ", "").strip()
      if msg.raw_text != config_save_buffer:
#        await msg.edit(config_save_buffer)
#        await msg.edit( encode_base64(zlib.compress(config_save_buffer.encode())) )
        tmp=encode_base64(compress(config_save_buffer.encode()))
        if len(tmp) < 4096:
          await msg.edit( tmp )
        else:
          await bot.send_message(myid, "E: fail to save config, too long")
    else:
      await userbot.send_message(myid, str([auto_forward_list,auto_msg_list,feed_list]).replace(" ", "").strip())
      await userbot.send_message(myid, "E: fail to save config, can't find the msg or chat")
  else:
    pass
#    await userbot.send_message(myid, "not change")

async def load_config():
  global auto_forward_list,auto_msg_list, feed_list, config_save_buffer
  config_save_buffer=[]
  auto_forward_list={}
  auto_msg_list={}
  feed_list={}
#  rss_status={}

  chat=await userbot.get_input_entity(myid)
  if chat:
    msg=await userbot.get_messages(chat, ids=config_saved_msgid)
  if chat and msg and msg.raw_text:

    if msg.raw_text[0:2] == "[{":
      config_save_buffer=msg.raw_text
    else:
      try:
        config_save_buffer=decompress(decode_base64(msg.raw_text)).decode()
      except:
        import zlib
        config_save_buffer=zlib.decompress(decode_base64(msg.raw_text)).decode()

    tmp=ast.literal_eval( config_save_buffer )
    auto_forward_list=tmp[0]
    auto_msg_list=tmp[1]
    feed_list=tmp[2]

    await msg.reply("loaded, size: "+str(len(msg.raw_text))+ " < "+str(len(config_save_buffer)))
    if len(config_save_buffer) > 4096:
      await bot.send_message(myid, "config too long")
    else:
      await bot.send_message(myid, str(config_save_buffer))

  else:
    await userbot.send_message(myid, "start, but no list: forward and feed")

async def is_debug(text="auto_msg"):
  msg=0
  while debug:
    tasks=""
    for j in asyncio.all_tasks():
      tasks=tasks+"\n"+j.get_name()
#    msg=await myprint(text+" is running,but will not work in debug mode.\nrunning tasks: "+tasks)
#    msg=await myprint(text+"is running, now tasks: \n"+str(tasks))
#    msg=await myprint(text+"is running, now tasks: \n"+str(asyncio.all_tasks()))
    info=text+" is stopped, now tasks: \n"+str(tasks)
    info=info+"\nwaiting feed num: "+str(len(feeds))
    info=info+"\nwaiting entry num: "+str(len(entry_task))

    if t_1_tasks:
      info=info+"\n\nthread 1 tasks: "+"\n".join(t_1_tasks)
    info=info+"\n\nthread count: "+str(threading.active_count())
    info=info+"\nthread t_1 alive: "+str(t_1.is_alive())
#    info=info+"\nthread current: "+str(threading.current_thread())
#    info=info+"\nthread all: "+str(threading.enumerate())
    if msg:
      if msg.raw_text != info.strip():
        msg=await msg.edit(info)
    else:
      msg=await userbot.send_message(myid, info)
    await asyncio.sleep(5)
  if msg:
    await msg.delete()
  return True
  return False



def get_sh_path():
  f = open(os.getcwd() + "/SH_PATH")
  line = f.readline()
  line=line.rstrip('\n')
  f.close()
  if line:
    return line
  else:
    print("E: can't set SH_PATH")
    return None

SH_PATH=get_sh_path()

async def start_send_entry_task(cid=cid_btrss):
  tasks=[]
  for j in asyncio.all_tasks():
    tasks.append(j.get_name())
  if cid == cid_btrss:
    task_name="send_entry_task"
  else:
    task_name="send_entry_task_"+str(cid)
  if task_name not in tasks:
    asyncio.create_task(send_entry_task(cid),name=task_name)


async def tw_fav_task(tw_text, file=None):
#from datetime import timedelta
#from time import time
#  delay=600 - time.time() % 600
  if time.time() % 600 < 30:
    await asyncio.sleep(30 - time.time() % 600)
  else:
    await asyncio.sleep(630 - time.time() % 600)
#  msg=await userbot.send_message(cid_tw, tw_text, parse_mode='md', link_preview=False, schedule=datetime.timedelta(seconds=delay))
#  await bot.send_message(cid_tw, tw_text, parse_mode='md', link_preview=False)

  #[cid,info,False,"htm",file]
  global entry_task
  if file:
#    if type(file) == list:
#      msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md')
    entry_task.append([cid_tw,tw_text,False,"md",file])
  else:
    entry_task.append([cid_tw,tw_text,False,"md"])
  await start_send_entry_task(cid=cid_tw)


async def tw_fav_loop():
#  global auto_msg_list # id [ctime interval target text]
  tw_fav_path=SH_PATH + "/tw_fav"
  while True:
    await asyncio.sleep(25)
#    tw_path=os.environ.get("tmp")
    try:
      tw_list=os.listdir(tw_fav_path)
    except FileNotFoundError:
      continue
    for tw_file in tw_list:
      f = open(tw_fav_path + "/" + tw_file)
#      lines = f.readlines()
      tw_text = f.read()
      f.close()
      tw_url="https://twitter.com/"

      if debug:
        print("D: tw_text: "+tw_text)
        await bot.send_message(myid, "tw_text: "+tw_text)

#      lines = tw_text.split("\n")
#      if lines[0][0:len(tw_url)] == tw_url:
      if tw_text[0:len(tw_url)] == tw_url:
        # no file
        asyncio.create_task(tw_fav_task(tw_text),name="tw_fav "+tw_file)
      else:
        # with file
        file=tw_text.split("\n\n",1)[0].split(" ")
        tw_text=tw_text.split("\n\n",1)[1]
        asyncio.create_task(tw_fav_task(tw_text,file),name="tw_fav "+tw_file)
      os.remove(tw_fav_path + "/" + tw_file)



async def auto_msg_send(item):
  await userbot.send_message("start auto_msg: "+str(item)+" to: "+item[2], item[3])

  if item[1] > 0:
    wait=MAX_AUTO_MSG_TASK_TIME - ( ( time.time() - item[0] ) % item[1] )
    if wait > 0:
      await asyncio.sleep(wait)

MAX_AUTO_MSG_TASK_TIME=300

async def auto_msg_task():
#  global uf
#  uf=threading.Thread(target=go)
#  uf.start()
  global auto_msg_list # id [ctime interval target text]
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
    tasks=[]
#    await update_feed()
    for j in asyncio.all_tasks():
      tasks.append(j.get_name())
    if len(auto_msg_list) > 0:
      for i in auto_msg_list.copy():
        item=auto_msg_list[i]
        task_name = str(item[0:3])
        if item[1] > 0:
          gogo=( time.time() - item[0] ) % item[1]
          if gogo > 0 and gogo < MAX_AUTO_MSG_TASK_TIME:
            if task_name not in tasks:
              asyncio.create_task(auto_msg_send(item),name=task_name)
  #          msg=await client.send_message(auto_msg[i][2], auto_msg[i][2])
        elif item[1] < 0:
          gogo=( time.time() - item[0] ) + item[1]
          if gogo > 0:
            asyncio.create_task(auto_msg_send(item),name=task_name)
            auto_msg_list.pop(i)




async def myinit():
  global config_saved_msgid
  config_saved_msgid=2817682
  await load_config()
  task_name="auto_msg"
  asyncio.create_task(auto_msg_task(),name=task_name)
#  task_name="parse_feed"
#  asyncio.create_task(parse_feed(),name=task_name)
#  t_1.start()
  task_name="get_feed_main"
  asyncio.create_task(get_feed_main(),name=task_name)

#  await mt_read()
  asyncio.create_task(mt_read(), name="mt_read")


async def main():
#  await mytest()
#  await client.loop.run_until_complete()
#  await client.run_until_disconnected()

#print(client.get_me().stringify())
#me = client.get_me()

#client.send_file('username', '/home/myself/Pictures/holidays.jpg')

#client.download_profile_photo('me')
#messages = client.get_messages('username')
#messages[0].download_media()

#@client.on(events.NewMessage(pattern='(?i)hi|hello'))
#@client.on(events.NewMessage(pattern='liqsliu'))
#async def handler(event):
#  await event.respond('hi')
  
  global me,log_cid,debug,bot_id,bot_name,user_id,myid

#  me = client.get_me()
  me = await userbot.get_me()
  user_id=me.id
  log_cid=me.id
  print(me.id)
  print("\tconnected: "+str(userbot.is_connected))

  tmp=await bot.get_me()
  bot_id=tmp.id
  bot_name=tmp.username
  print(bot_id)
  print("\tconnected: "+str(bot.is_connected))
  #print (me.stringify())
  debug=False

  if myid:
    if me.id == myid:
      await myinit()
  else:
    myid=me.id
  await bot(functions.bots.SetBotCommandsRequest(
    scope=types.BotCommandScopeDefault(),
#        lang_code='en',
#        lang_code='zh-hans',
    lang_code='',
    commands=[]
  ))
  await userbot.run_until_disconnected()





#client.start()



#https://docs.python.org/3/library/asyncio-task.html#asyncio.run
#loop = asyncio.get_running_loop()
#loop = asyncio.get_event_loop()
#loop.create_task(auto_msg_task(msgs))
#asyncio.create_task(auto_msg_task())
#asyncio.run(auto_msg_task())





#    # mentioned:8

# anyone is ok:4
# private is ok:2
# group is ok:1
cmd_dict={
    "help":       [0b111, "cmds"],
    "ping":       [0b111, "pong"],
    "dc":         [0b111, "dc1?"],
    "start":      [0b110, "start"],
    "dg":         [0b010, "debug"],
    "an":         [0b011, "archivenow"],
    "down":       [0b011, "download"],
    "id":         [0b011, "info of"],
    "idf":        [0b011, "full info of"],
    "fid":        [0b010, "file id"],
    "file":       [0b011, "get file of the fid"],
    "md":         [0b011, "print markdown str"],
    "hm":         [0b011, "print html str"],
    "p":          [0b011, "eval str"],
    "pu":         [0b011, "unicode"],
    "hex":        [0b011, "unicode and hex"],
    "b64":        [0b011, "base64 decode"],
    "py":         [0b011, "run py code"],
    "sh":         [0b011, "run shell code"],
    "uptime":     [0b010, "admin only"],
    "free":       [0b010, "admin only"],
    "echo":       [0b011, "echo helloworld"],
    "rss":        [0b010, "rss add|del|se"],
    "mkchat":     [0b010, "creat group"],
    "ad":         [0b010, "get admin"],
    "link":       [0b010, "get msg"],
    "msgclear":   [0b010, "clear msg(userbot)"], #userbot only
    "me":         [0b010, "me name"],
    "af":         [0b010],
    "afad":       [0b010],
    "afload":     [0b010],
    "afdel":      [0b010],
    "afclear":    [0b010],
    "aflist":     [0b010],
    "unpin":      [0b010],
    "save":       [0b010],
    "amoad":      [0b010],
    "amdel":      [0b010],
    "amclear":    [0b010],
    "am":         [0b010],
    "myid":       [0b111, "get my id"]}





async def bash_for_cmd(cmd,shell=True,max_time=64,cmd_msg=None):
  p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")

  start_time=time.time()
  info=""
  errs=""
  msg=None

  await asyncio.sleep(0.5)
  if p.poll() == None and p.returncode == None:
    while p.poll() == None and p.returncode == None:
      if time.time()-start_time > max_time:
        p.kill()
        break
      await asyncio.sleep(1)
          
  try:
    info, errs = p.communicate(timeout=3)
  except subprocess.TimeoutExpired as e:
    info=e.stdout
    errs=e.stderr

  if not info:
    info="null"
  info=str(info)
  if p.returncode:
    info=info+"\n==\nE: "+str(p.returncode)
    if errs:
      info=info+"\n"+errs
    #await msg.delete()
  return info




tw_re=re.compile(r"^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./?=&%-]+$")
my_host_re=re.compile(r"^https://liuu\.tk/[a-zA-Z0-9_./?=%-]+$")
pic_re=re.compile(r"^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(jpe?g|png|mp4|gif)$")
#url_re=re.compile(r"^(http(s)?|ftp|file)://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*$")
#url_re=re.compile(r"^(?=^.{3,255}$)http(s)?://(([0-9a-zA-Z][0-9a-zA-Z-]{0,62}\.)+\.[a-zA-Z]+|([0-9]+\.){4})(:[0-9]+)?/?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|$")

#URL_RE_TEXT=r"(?=^.{3,255}$)(http(s)?|ftp|file)://([0-9a-zA-Z][0-9a-zA-Z-]{0,62}(\.[0-9a-zA-Z][0-9a-zA-Z-]{0,62})+|([0-9]+\.){3}[0-9]+)(:[0-9]+)?(/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])?"
URL_RE_TEXT=r"(?P<url>(?=.{3,255})(http(s)?|ftp|file)://([0-9a-zA-Z][0-9a-zA-Z-]{0,62}(\.[0-9a-zA-Z][0-9a-zA-Z-]{0,62})+|([0-9]+\.){3}[0-9]+)(:[0-9]+)?(/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])?)"

url_re=re.compile(URL_RE_TEXT)
url_only_re=re.compile(r"^"+URL_RE_TEXT+r"$")

url_md_re=re.compile(r"\[[^\n\]]+\]\(\s*"+URL_RE_TEXT+r"(\s.+)?\)")
url1_md_re=re.compile(r"\[[^\n\]]+\] ?\[(?P<mark>[^\n\]]+)\]")
url2_md_re=re.compile(r"^\[(?P<mark>[^\n\]]+)\]: "+URL_RE_TEXT+r"(\s['\”(].+['\”)])?", re.M)
pic_md_re=re.compile(r"^\!\[[^\n\]]+\]\(\s*"+URL_RE_TEXT+r"(\s.+)?\)$", re.M)


def text_has_md(text, url=None):
  i=0
  while True:
    s=url_md_re.search(text,i)
    if s:
      if not url or url == s["url"]:
        return True
      i=s.span()[1]
    else:
      s=url1_md_re.search(text,i)
      if s:
        ss=url2_md_re.search(text)
        if ss and s["mark"] == ss["mark"]:
          if not url or url == ss["url"]:
            return True
        i=s.span()[1]
      else:
        s=pic_md_re.search(text,i)
        if s:
          if not url or url == s["url"]:
            return True
          i=s.span()[1]
        else:
          break
  return False


async def run_bash_for_cmd(msg):
#  shell_cmd="{} {} {} {}"
  shell_cmd=[SH_PATH+"/bcmd.sh"]
  shell_cmd.append(msg["gateway"])
  shell_cmd.append(msg["username"])
  shell_cmd.append(msg["text"])
  shell_cmd.append(repr(msg))


  if shell_cmd[1] == "gateway1":
    if my_host_re.match(shell_cmd[3]):
      print("my url")
      shell_cmd[3]=".ipfs {} only".format(shell_cmd[3])
      shell_cmd[1]="gateway4"
    elif tw_re.match(shell_cmd[3]):
      print("a twitter")
      shell_cmd[3]=".tw {}".format(shell_cmd[3])
      shell_cmd[1]="gateway4"
    elif pic_re.match(shell_cmd[3]):
      print("a pic")
      shell_cmd[3]=".ipfs {} only".format(shell_cmd[3])
      shell_cmd[1]="gateway4"
    elif url_only_re.match(shell_cmd[3]):
      print("a url")
      shell_cmd[3]=".ipfs {} autocheck".format(shell_cmd[3])
      shell_cmd[1]="gateway4"
  print("bash cmd: {}".format(shell_cmd))
  await bash_for_cmd(shell_cmd, shell=False)



def get_msg_link(msg):
  return "msg link: https://t.me/c/"+ str(utils.resolve_id(msg.chat_id)[0]) +"/"+ str(msg.id)


async def media2url(msg):
  if msg.media != None:
    #media=MessageMediaPhoto(
    #path = await msg.download_media('/home/liqsliu/test.jpg')
    path = await msg.download_media('/home/liqsliu/tmp/')
    if path != None:
      path = path.split('/')[-1]
      #print('https://liuu.tk/'+path.replace(' ','%20'))
      return('https://liuu.tk/'+path.replace(' ','%20'))


async def msg2md(msg):
#  client=bot
  event=msg
  client=event.client
  if debug:
    event=msg
    print("#### msg ####")
    print(msg.message.stringify())
    print("#### event ####")
    print(msg.stringify())
    print("#### orig ####")
    print(event.original_update) #UpdateNewMessage
    print(msg.raw_text)

  text=msg.raw_text
  # just for spoiler
  if msg.media and type(msg.media) == MessageMediaUnsupported:
#    client=userbot #will get ""
#    chat = await client.get_entity(msg.chat_id)
#    msgn = await client.get_messages(chat, ids=msg.id)
#    msgn = await client.get_messages(msg.chat_id, ids=msg.id)
    msgn = await bot.get_messages(msg.chat_id, ids=msg.id)

    if msgn:
      if msgn.raw_text:
        text=msgn.raw_text
      else:
        text=msgn.message
    if debug:
      print("spoiler msg:")
      print(msgn.stringify())
      print("text: {}".format(text))



  if text and msg.entities and not pic_md_re.search(text):
    text_fix={}
    url_index=0
    urls=[]
    for t in msg.entities:
      if type(t) == MessageEntityTextUrl:
#      if type(t) == MessageEntityUrl:

        url=text[t.offset:t.offset+t.length]
        if url == t.url:
          s=url_re.match(text,t.offset)
          if s:
            if s.group("url") == url:
              continue
            else:
              pass
          else:
            await bot.send_message(myid, "E: can't find a url, text: "+text[t.offset:])
            await bot.send_message(myid, "E: can't find a url, msg: "+msg.stringify())
        else:
          s=url_re.match(text,t.offset)
          if s:
            if s.span()[0] < t.offset+t.length:
              if s.group("url") == url:
                # no need to fix
                # no fix is better
                continue
              else:
                # may be malicious
                pass
            else:
              pass
          else:
            pass

        if text_has_md(text, t.url):
          continue

#        if text[t.offset-1] == "(" and len(text) >= t.offset+t.length and text[t.offset+t.length] == "(":
#          continue
        url_index+=1
        tmp="["
        if t.offset in text_fix:
          tmp=text_fix[t.offset]+tmp
        text_fix.update({t.offset:tmp} )

        tmp="][%s]" % url_index
        if t.offset+t.length in text_fix:
          tmp=text_fix[t.offset+t.length]+tmp
        text_fix.update({t.offset+t.length:tmp} )

        urls.append(t.url)
    if url_index:
      new_text=""
      o=0
#      for i in sorted(text_fix):
      for i in text_fix:
        new_text+=text[o:i]
        new_text+=text_fix[i]
        o=i
      if len(text) != i:
        new_text+=text[i:]

      new_text+="\n"
      url_index=0
      for url in urls:
        url_index+=1
        new_text+="\n[%s]: %s" % (url_index, url)
        text=new_text


  text_from_group=None
  if msg.media and type(msg.media) != MessageMediaWebPage and type(msg.media) != MessageMediaUnsupported:
    text+="\n"
#    print(await get_media(msg))
#    text+="\n![](%s)" % await media2url(msg)
    grouped_id = msg.grouped_id
    msg_id=msg.id
#      chat=await msg.get_chat()
      #for id in range(msg_id+1,end_id+1):
#      for id in range(msg_id,msg_id+4):
    for id in range(msg_id,msg_id+8):
#        msgn = await client.get_messages(chat, ids=id)
      if id == msg_id:
        msgn=msg
      else:
#        msgn = await client.get_messages(msg.chat_id, ids=id)
        msgn = await msg.client.get_messages(msg.chat_id, ids=id)
      if msgn and msgn.grouped_id == grouped_id:
        url=await media2url(msgn)
#          if msgn.message:
        if hasattr(msgn, 'message') and msgn.message:
          if id == msg_id:
            text+='\n![{}]({})'.format(url, url)
          else:
            if msg.raw_text:
#                text+='\n![{}]({})'.format(msgn.message, url)
              text+='\n![{}]({})'.format(msgn.raw_text.replace("\n", ""), url)
            else:
              text_from_group+=msgn.raw_text
              text+='\n![{}]({})'.format(url, url)
        else:
          text+='\n![{}]({})'.format(url, url)
      else:
        break
      if grouped_id:
        continue
      else:
        break

#  if msg.reply_to:
#    replied = await event.get_reply_message()
#    if replied:
#      pass



  if text_from_group:
    if not msg.raw_text:
      text=text_from_group+text
  if text:
    if msg.fwd_from:
#      fwd_info="Forwarded from "
      fwd_info="转自 "

      # username? firstname?
      if msg.fwd_from.from_name:
        fwd_info+=msg.fwd_from.from_name
      else:
        if msg.fwd_from.from_id:
          try:
            peer=await userbot.get_entity(msg.fwd_from.from_id)
          except ValueError:
            try:
              peer=await bot.get_entity(msg.fwd_from.from_id)
            except ValueError:
              pass
          if peer:
            if type(peer) == User:
              if peer.username:
                fwd_info+=peer.username
              else:
                fwd_info+=peer.first_name
            else:
              # ignore username
              if hasattr(peer, 'title'):
                fwd_info+=peer.title
              elif hasattr(peer, 'username'):
                fwd_info+=peer.username
              elif hasattr(peer, 'first_name'):
                fwd_info+=peer.first_name
              else:
                fwd_info+=str(peer.id)
          else:
            if type(msg.fwd_from.from_id) == PeerChannel:
              fwd_info+="channel(%s)" % str(msg.fwd_from.from_id.channel_id)
            elif type(msg.fwd_from.from_id) == PeerUser:
              fwd_info+="user(%s)" % str(msg.fwd_from.from_id.user_id)
            elif type(msg.fwd_from.from_id) == PeerChat:
              fwd_info+="chat(%s)" % str(msg.fwd_from.from_id.chat_id)
            else:
              fwd_info+="wtf"
        else:
          fwd_info+="unknown"

      fwd_info+=": "
      text=fwd_info+text




    return text
  else:
    return "null"



async def get_name_from_msg(msg):
  if msg.sender_id == cid_tw:
    return "twitter"
  sender=msg.sender
  if not sender:
    sender=await msg.get_sender()
  if sender:
    if sender.username:
      username=sender.username
    else:
      username=sender.first_name
  elif msg.sender_id:
    username="%s" % event.sender_id
  else:
    username="null"
  return username


MT_GATEWAY_LIST={
#    "gateway4":[cid_ipfsrss],
    "gateway2":[-1001137152439],
    "gateway1":[cid_wtfipfs]
    }                              
MT_GATEWAY_LIST_for_tg={}
for i in MT_GATEWAY_LIST:
  MT_GATEWAY_LIST_for_tg.update({MT_GATEWAY_LIST[i][0]: i})



async def send_msg_to_mt(event, edited=False):
  if debug:
    print("prepare send msg to mt: {}".format(event.raw_text))
  if event.chat_id in MT_GATEWAY_LIST_for_tg:
    gateway=MT_GATEWAY_LIST_for_tg[event.chat_id]
  else:
    return
  if event.sender_id == bot_id:
    return
  if event.sender_id == 1494863126:
    return
#  msg=event.message
  msg=event
  if msg.grouped_id:
    global last_grouped_id
    if msg.grouped_id == last_grouped_id:
      return
    else:
     last_grouped_id = msg.grouped_id

  if event.fwd_from:
    if event.sender_id == cid_tw:
      print("I: ignore a msg from tw")
      return
    elif type(event.from_id) == PeerChannel:
      if event.from_id.channel_id == cid_tw:
        print("I: ignore a msg from tw: event.from_id.channel_id")
        return
      elif event.fwd_from.from_id.channel_id == cid_tw:
        print("I: ignore a msg from tw: event.fwd_from.from_id.channel_id")
        return

#    if event.sender_id == myid:


  username=await get_name_from_msg(event)
  qt=None

  if msg.reply_to:
    replied = await event.get_reply_message()
    if replied:
      if event.sender_id == bot_id:
        qt="""{}""".format(replied.raw_text)
      else:
        qt="""T {}: {}""".format(await get_name_from_msg(replied), await msg2md(replied))
#          mt_send(event.message,gateway="gateway1")
#        mt_send(event, gateway)
  mt_send(await msg2md(event),username, gateway, qt)



def mt_send(text="null", username="C bot", gateway="gateway1", qt=None):

  # in for all
  MT_API="127.0.0.1:4240"
  # send msg to matterbridge
  url="http://"+MT_API+"/api/message"

  #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
#  url="http://127.0.0.1:5555/api/message"

  if not username.startswith("C "):
    username="T "+username
  if qt:
    username="{}\n\n{}: ".format("> "+"\n> ".join(qt.splitlines()), username)
#  gateway="gateway0"
  data={"text":"{}".format(text),
      "username":"{}".format(username),
      "gateway":"{}".format(gateway)
      }
#  data={"text":"test","username":"null", "gateway":"gateway0" }

#  data=str(data)
#  data=urlencode(data)#将字典类型的请求数据转变为url编码
#  data=urllib.parse.quote(json.dumps(data), safe="{}:\\\"',+ ")
#  data=urllib.parse.quote_plus(json.dumps(data))
#  data=data.encode('ascii')#将url编码类型的请求数据转变为bytes类型
  data=json.dumps(data).encode()
  if debug:
    print(data)
  req_data=urllib.request.Request(url,data)#将url和请求数据处理为一个Request对象，供urlopen调用
  req_data.add_header("Content-Type", "application/json")
  with urllib.request.urlopen(req_data) as res:
#  with urllib.request.urlopen(url, data) as res:
    if debug:
      print(str(res.headers))
    res=res.read().decode()#read()方法是读取返回数据内容，decode是转换返回数据的bytes格式为str
  if debug:
    print("D: send msg to mt, res: "+res)


def mylog(msg):
#  await bot.send_message(myid, "I: msg from mt_read: "+ str(data.decode()) )
  if not need_wait:
    asyncio.create_task(bot.send_message(myid, msg))
  else:
    print("E: mylog need wait:"+msg)


async def get_peer(name, chat=None):
  if type(name) == str:
    if chat:
      users=[]
      async for user in client.iter_participants(chat, search=name):
        if user.username:
          if name != user.username:
            continue
        elif user.first_name != name:
          continue
        users.append(user)
      if users:
        return users
      elif len(name) < 5:
        return None
  if type(name) == str and name.isnumeric():
      id=int(name)
  else:
      id=name
  try:
    user=await userbot.get_input_entity(id)
  except ValueError:
    try:
      user=await userbot.get_entity(id)
    except ValueError:
      try:
        user=await bot.get_entity(id)
      except ValueError:
        user=None
  return user

async def get_msg_id_from_text(text,chat_id=None,name=None, client=userbot):
  if chat_id:
    chat = await client.get_entity(chat_id)
  else:
    return
  my_msg_text=text
  if not my_msg_text:
    return None

  my_msg_sender=name
  limit=10*int(64/len(my_msg_text)+1)
  if my_msg_sender == "bot":
    limit=limit*10

  if name:
    user=await get_peer(name)
  else:
    name=None

  if user:
    if type(user) == list:
      for u in user:
        async for msg in client.iter_messages(chat, limit=limit, search=my_msg_text, from_user=u):
          return msg.id
    else:
      async for msg in client.iter_messages(chat, limit=limit, search=my_msg_text, from_user=user):
        return msg.id


  async for msg in client.iter_messages(chat, limit=int(limit/10), search=my_msg_text):
    return msg.id

  if "\n\n" in my_msg_text:
    for line in my_msg_text.splitlines():
      if line:
        async for msg in client.iter_messages(chat, limit=int(limit/10), search=line):
          return msg.id
        async for msg in client.iter_messages(chat, limit=int(limit/100+8)):
          if msg.raw_text.splitlines()[0] == text.splitlines()[0]:
            return msg.id
          for line2 in msg.raw_text.splitlines():
            if line == line2:
              return msg.id
        break

  return None



mt_msg_need_wait=False

async def send_mt_msg():
  try:
    global mt_msg_need_wait
    mt_send_need_wait=True
    global mt_msgs
    while True:
      if not mt_msgs:
        break
      else:
        msg=mt_msgs[0]
#      text=msg
#      await bot.send_message(myid, text)
      try:
#        msg.replace(',"Extra":null}','}',1)
#        msgd=ast.literal_eval(msg.splitlines()[1])
        msgd=json.loads(msg.splitlines()[1])
      except:
        print("E: can't convert msg to dict")
        print("################")
        print(ascii(msg.splitlines()[1]))
        print("################")
        print(msg.splitlines()[1])
        print("################")
        mt_msgs.remove(msg)
        info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
        
    #    await bot.send_message(myid, "E: send_mt_msg: "+str(msg))
        print(info)
        try:
          await bot.send_message(myid, msg.splitlines()[1][0:len(4096-info-3-5)]+"\n==\n" +info)
        except:
          info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
          print(info)
        continue
#        raise
#       Data sent: 'GET /api/stream HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
#      Data received: 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nDate: Wed, 19 Jan 2022 02:03:29 GMT\r\nTransfer-Encoding: chunked\r\n\r\nd5\r\n{"text":"","channel":"","username":"","userid":"","avatar":"","account":"","event":"api_connected","protocol":"","gateway":"","parent_id":"","timestamp":"2022-01-19T10:03:29.666861315+08:00","id":"","Extra":null}\n\r\n'




      if msgd["gateway"] in MT_GATEWAY_LIST:
        chat_id=MT_GATEWAY_LIST[msgd["gateway"]][0]
      else:
        continue


      text=msgd["text"]
      name=msgd["username"]

      if msgd["Extra"]:
        # has file
        #,"id":"","Extra":{"file":[{"Name":"proxy-image.jpg","Data":"/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAA ... 6P9ZgOT6tI33Ff5p/MAOfNnzPzQAN4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAGQAAYAkAAGTGAAAAAAAAwsAAHLAAAK//9k=","Comment":"","URL":"https://liuu.tk/ddb833ad/proxy_image.jpg","Size":0,"Avatar":false,"SHA":"ddb833ad"}]}}\n\r\n'
        pass
        for file in msgd["Extra"]["file"]:
          if text:
            if text != file["name"]:
              text+="\n\n"
            else:
              text=""
          text+="[{}]({})".format(file["Name"], file["URL"])

      else:
        msgd.pop("Extra")

      print("\nget msg from mt: ")
      print(msgd)

      if len(name.splitlines()) > 1:
        qt_text=name
        name=name.splitlines()[-1]
      else:
        qt_text=name


#      if name == "C Telegram: ":
      if name == "C twitter: ":
        mt_msgs.remove(msg)
        continue


#      if text and username != "C Bot: ":
      if text and not name.startswith("C "):
        if text[0] == ".":
          asyncio.create_task(run_bash_for_cmd(msgd))
        elif text == "ping":
          mt_send("pong", gateway=msgd["gateway"])
        else:
          asyncio.create_task(run_bash_for_cmd(msgd))




      if name.startswith("T "):
        mt_msgs.remove(msg)
        continue





      reply_to=None
#      if text.startswith("> "):
      if qt_text.startswith("> "):
        print("reply?: "+qt_text+text)
#        name=msgd["username"]
#        if text.startswith("> T "):

        qt=None
        tg_nick=None
        for line in qt_text.splitlines():
          if not qt and line.startswith("> > "):
            continue
          elif line != "----" and line != "> " and line.startswith("> "):
            if tg_nick:
              qt+="\n"+line[2:]
            else:
              if ": " in line:
                if qt_text.startswith("> C Twitter: "):
                  tg_nick=cid_tw
                  qt=line.split(": ",1)[1]
                elif qt_text.startswith("> T "):
                  tg_nick=line[4:].split(": ",1)[0]
                  if line.split(": ",1)[1].startswith("转自") and ": " in line.split(": ",1)[1]:
                    qt=line.split(": ",2)[2]
                  elif line.split(": ",1)[1].startswith("Forwarded from") and ": " in line.split(": ",1)[1]:
                    qt=line.split(": ",2)[2]
                  else:
                    qt=line.split(": ",1)[1]
                else:
                  tg_nick=bot_name
                  qt="\n"+line[2:]
              else:
                qt=None
                break

          else:
            break

        print("chat_id: {}".format(chat_id))
        print("tg_nick: {}".format(tg_nick))
        print("qt: "+qt)
        if qt:
          reply_to=await get_msg_id_from_text(qt,chat_id,tg_nick)
          print("reoly to id: %s" % reply_to)
          if not reply_to:
            name=qt_text

      text=name+text
      await bot.send_message(chat_id, text, reply_to=reply_to)
#        await bot.send_message(myid, msgd["gateway"]+msgd["username"]+msgd["text"])

      mt_msgs.remove(msg)
  except FloodWaitError as e:
    await asyncio.sleep(e.seconds+5)
    await bot.send_message(myid, "E: send_mt_msg: floodwaiterror")
    await asyncio.sleep(5)
  except:
    info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
#    await bot.send_message(myid, "E: send_mt_msg: "+str(msg))
    await bot.send_message(myid, "\n==\n" +info)
    await asyncio.sleep(5)
  finally:
    mt_send_need_wait=False


mt_msgs=[]







class MTReadProtocol(asyncio.Protocol):
  # https://docs.python.org/zh-cn/3.8/library/asyncio-protocol.html#tcp-echo-client
  def __init__(self, message, on_con_lost):
    self.message = message
    self.on_con_lost = on_con_lost

  def connection_made(self, transport):
    transport.write(self.message.encode())
    print('Data sent: {!r}'.format(self.message))

  def data_received(self, data):
#    print(json.loads(data.decode()))
#    print(data.decode())
    try:
      msg=data.decode()
    except UnicodeDecodeError:
      pass
      info="E: "+str(sys.exc_info()[1])+"\n==\n"+traceback.format_exc()+"\n==\n"+str(sys.exc_info())
      print(info)
      return
    print('Data received: {!r}'.format(msg))

#    if msg.startswith("HTTP/1.1 200 OK"):
    if msg and not msg.startswith("HTTP/1.1"):
      global mt_msgs
      mt_msgs.append(msg)
      if not mt_msg_need_wait:
        asyncio.create_task(send_mt_msg())
      if debug:
        print('Data received: {!r}'.format(msg))
  #      mylog("I: msg from mt_read: "+ msg )

  def connection_lost(self, exc):
    msg='The server closed the connection'
    print(msg)
    mylog("W: msg from mt_read: "+ msg )
    self.on_con_lost.set_result(True)


async def mt_read():
  # out for tg
  MT_API_TG="127.0.0.1:4245"

  url="http://"+MT_API_TG+"/api/stream"
  host=MT_API_TG.split(":")[0]
  port=int(MT_API_TG.split(":")[1])

  path="/"+url.split("/",3)[3]
  query = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    f"\r\n"
  )

  # Get a reference to the event loop as we plan to use
  # low-level APIs.
  loop = asyncio.get_running_loop()

  on_con_lost = loop.create_future()
#  message = 'Hello World!'
  message=query

  while True:
    try:
      transport, protocol = await loop.create_connection(
      lambda: MTReadProtocol(message, on_con_lost),
      host, port)
    except asyncio.exceptions.InvalidStateError:
      print("connect fail")
      pass

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
  url="http://"+MT_API+"/api/stream"

  host=MT_API.split(":")[0]
  port=int(MT_API.split(":")[1])
  path="/"+url.split("/",3)[3]
  reader, writer = await asyncio.open_connection(host, port)
  query = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    f"\r\n"
  )
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





#client.run_until_disconnected()


client=userbot

with userbot:
  userbot.loop.run_until_complete(main())
