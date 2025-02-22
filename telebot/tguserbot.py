#!/usr/bin/python3


import sys

#for i in sys.argv:
#  print(i)

if len(sys.argv) > 1:
#  my_list=sys.argv.copy()
  my_tw_text=sys.argv[1]
my_tw_files=[]
if len(sys.argv) > 2:
  my_tw_files=sys.argv[2].split(' ')

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
#from telethon.tl.types.input_peer_chat import InputPeerChat
#from telethon.tl.types import InputPeerChat, PeerUser, PeerChannel
from telethon.tl.types import PeerChat, PeerUser, PeerChannel, Chat, User, Channel, ChatFull, UserFull, ChannelFull, InputPeerUser, InputPeerChat, InputPeerChannel


#telethon.errors.rpcerrorlist.MessageNotModifiedError
from telethon.errors.rpcerrorlist import MessageNotModifiedError
#from telethon.errors import ValueError

from datetime import timedelta
from time import time


import subprocess
from subprocess import Popen, PIPE

#import shlex

import asyncio
#from asyncio import sleep

import traceback



# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = int(get_my_key("TELEGRAM_API_ID"))
api_hash = get_my_key("TELEGRAM_API_HASH")
#TOKEN = get_env('TG_TOKEN', 'Enter the bot token: ')
#NAME = TOKEN.split(':')[0]
#bot_token = 'xxxx:xxxxxxxxxx'
#bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
#bot_id = int(bot_token.split(':', 1)[0])
#bot_hash = bot_token.split(':', 1)[1]
#print(bot_token)

myid = int(get_my_key("TELEGRAM_MY_ID"))
cid_tw = int(get_my_key("TELEGRAM_GROUP_TW"))
cid_ipfs = int(get_my_key("TELEGRAM_GROUP_IPFS"))
cid_wtfipfs = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

my_chat_id=cid_tw

#client = TelegramClient('session_name', api_id, api_hash)
client = TelegramClient('/home/liqsliu/.ssh/telethon_session_name.session', api_id, api_hash)


#client = TelegramClient('/home/liqsliu/.ssh/telethon_liqsliu_bot.session', bot_id, bot_hash).start(bot_token=bot_token)
#client.start(bot_token=bot_token)


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

async def myprint(msg, parse_mode="text"):
  if len(msg) > MAX_MSG_LEN:
    msg=subprocess.run(["bash", "change_long_text.sh", msg ], stdout=subprocess.PIPE, text=True ).stdout
  if parse_mode == "md":
    return await client.send_message(log_cid, msg, parse_mode=parse_mode)
  else:
    return await client.send_message(log_cid, msg)

async def myprintmd(msg):
  return await myprint(msg, parse_mode="md")

async def myprintraw(msg):
#  return await myprintmd("`"+msg.replace("`","\\`")+"`")
  if len(msg) > MAX_MSG_LEN:
    return await myprint(msg)
  else:
    msg=mdraw(msg,"code")
    return await myprintmd("```\n"+msg+"\n```")



def get_id(msg):
  if type(msg) == int:
    return msg
  elif msg[0] =="@":
  #          peer=await client.get_input_entity(cmd[1][1:])
  #          await client.send_message(me.id, str(peer.id))
    id=msg[1:]
  elif len(msg.split('/')) >=4 and msg.split('/')[2] == "t.me":
    if msg.split('/')[3] == "c":
      id=int(msg.split('/')[4])
    else:
      id=msg.split('/')[3]
  else:
    id=int(msg)
  return id

async def get_msg(url):
#  elif cmd[0] == "link":
#    url=cmd[1]
  if len(url.split('/')) >=5 and url.split('/')[2] == "t.me":
    if url.split('/')[3] == "c":
      cid=int(url.split('/')[4])
      id=int(url.split('/')[5].split('?')[0])
      chat=utils.resolve_id(cid)[1]
    else:
      cid=url.split('/')[3]
      id=int(url.split('/')[4].split('?')[0])
#      chat=await client.get_input_entity(cid)
      chat=await client.get_input_entity(cid)
    msg=await client.get_messages(chat,ids=id)
    return msg
  else:
    return False


#small group
async def get_admin_of_group(msg):
  peer=await client.get_entity(get_id(msg))
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


#channel or big group
async def get_admin_of_channel(msg):
#  id=get_id(msg)
  peer=await client.get_entity(get_id(msg))
#  if type(peer) == User:
#  if type(peer) == Channel:
  if peer.broadcast or peer.megagroup or peer.gigagroup:
    info="id: `"+str(utils.get_peer_id(peer))
    if peer.username:
      info=info+"` @"+peer.username
    else:
      info=info+"` no username, tg://openmessage?chat_id="+str(peer.id)
    full = await client(functions.channels.GetFullChannelRequest(peer))
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
      if peer.broadcast:
        a=1
#        info=info+"\n==\n"+await get_admin_of_channel(peer.id)
    else:
      info=info+"\nno linked group or channel"
  elif type(peer) == Chat:
    info=await get_admin_of_group(peer.id)
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
    full = await client(functions.messages.GetFullChatRequest(peer.id))
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




async def my_popen(cmd,shell=True):
  p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")

  start_time=time()
  info=""
  errs=""
  msg=""
  msgs=["","",p]
  await asyncio.sleep(0.5)
#        await myprintraw(str(args))
  if debug:
    await myprintraw(str(p.args))
  if p.poll() == None and p.returncode == None:
    asyncio.create_task(update_stdouterr(msgs))
    while p.poll() == None and p.returncode == None:
      if time()-start_time > 64:
        p.kill()
        break
      await asyncio.sleep(0.5)
      info=msgs[0]
      errs=msgs[1]

      tmp=info+"\n==\nE: \n"+errs
      tmp=tmp.strip()
#            tmp=tmp.lstrip('\n').rstrip('\n').lstrip(' ').rstrip(' ')
      if msg == "":
        msg=await myprint(tmp)
      else:
        if tmp != msg.raw_text:
          try:
            msg=await msg.edit(tmp)
#                await msg.delete()
#                msg=await myprint(tmp)
#                await myprintraw(msg.raw_text.encode().hex())
#                await myprintraw(tmp.encode().hex())
          except MessageNotModifiedError:
            await myprint("E: wtf? MessageNotModifiedError")
            await asyncio.sleep(5)
      await asyncio.sleep(1)
          

#        await asyncio.sleep(0.5)
  #info=msgs[0]
  #errs=msgs[1]
  try:
    info, errs = p.communicate(timeout=2)
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

  if p.returncode:
    info=info+"\n==\nE: "+str(p.returncode)
    if errs:
      info=info+"\n"+errs
  info=info.strip()
  if info == "":
    info="null"
  if msg == "":
    msg=await myprint(info)
  else:
    #await msg.delete()
    if info != msg.raw_text:
      await msg.edit(info)


async def my_exec(cmd):
#  exec(cmd) #return always is None
#  p=Popen("my_exec.py "+event.raw_text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
  await my_popen(["python3", "my_exec.py",cmd],shell=False)









async def my_eval(cmd):
  res=eval(cmd)
  if debug:
    await myprint(str(res)+"\n"+str(type(res)))
  else:
    await myprint(str(res))



@client.on(events.NewMessage)
async def handler(event):
#  print (event.stringify())
#  chat = await event.get_chat()
#  print(chat.stringify())
#  sender = await event.get_sender()
#  print(sender.stringify())

#  if not "auto_forward_list" in locals().keys():
#    auto_forward_list={cid_tw:cid_ipfsrss}
  try:
    chat_id = event.chat_id
    sender_id = event.sender_id
    global auto_forward_list, debug, auto_msg
#    if event.raw_text == "test":
#      await myprint(event.stringify())
#      await myprint(str(chat_id) + " " +str(type(chat_id)))
#      await myprint(str(sender_id) + " " +str(type(sender_id)))
#  await event.respond(event.text)
#  if chat_id == cid_ipfsrss:
#    msg=await client.send_message(me.id, "N:" + event.stringify())
    if chat_id == me.id:
#      await myprint(event.stringify())
#      cmd=event.raw_text.split(' ',1)
      cmd=event.raw_text.split(' ')
      if cmd[0] == "ping":
        await myprint("pong")
      elif cmd[0] == "dg":
        debug=not debug
        await myprint(str(debug))
      elif cmd[0] == "fid":
        msg=await get_msg(cmd[1])
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
              await myprint(msg.stringfy())
          else:
            await myprint(msg.stringfy())
        else:
          await myprint("E: no msg")
      elif cmd[0] == "file":
#        msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md', schedule=timedelta(seconds=delay))
#https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.uploads.UploadMethods.send_file
#          telethon.utils.pack_bot_file_id(file)
        if len(cmd[1].split('/')) >=5 and cmd[1].split('/')[2] == "t.me":
          msg=await get_msg(cmd[1])
          if msg and msg.media:
            if hasattr(msg.media, 'document'):
              file=msg.media
            elif hasattr(msg.media, 'photo'):
              file=msg.photo
            else:
              file=None
        else:
#          file=cmd[1]
#          file=utils.resolve_bot_file_id(cmd[1])
          await myprint("file_id can't work in userbot")
          file=None
        if file:
          msg=await client.send_file(log_cid, file=file)
        else:
          await myprint(msg.stringfy())
      elif cmd[0] == "p":
        asyncio.create_task(my_eval(event.raw_text.split(' ',1)[1]), name="my_eval")
      elif cmd[0] == "py":
        asyncio.create_task(my_exec(event.raw_text.split(' ',1)[1]), name="my_exec")
      elif cmd[0] == "sh":
        asyncio.create_task(my_popen(event.raw_text.split(' ',1)[1]), name="my_sh")
      elif cmd[0] == "shbu":
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
        p=Popen(event.raw_text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
#        p=Popen(args,stdout=PIPE, stderr=PIPE)

        start_time=time()

#        loop.create_task(update_stdout(msgs))
#        loop.create_task(update_stderr(msgs))

#        loop.create_task(update_msg(msgs))

        info=""
        errs=""
        msg=""
        msgs=["","",p]
        await asyncio.sleep(0.5)
#        await myprintraw(str(args))
        if debug:
          await myprintraw(str(p.args))
        if p.poll() == None and p.returncode == None:
#        if True:
#          loop.create_task(update_stdouterr(msgs))
          asyncio.create_task(update_stdouterr(msgs), name="my_sh")


          while p.poll() == None and p.returncode == None:
  #        while p.returncode == None:
            if time()-start_time > 64:
              p.kill()
              break
            await asyncio.sleep(0.5)
            info=msgs[0]
            errs=msgs[1]
  #          print("M: "+info+"\n==\nE: "+errs)

            tmp=info+"\n==\nE: \n"+errs
            tmp=tmp.strip()
#            tmp=tmp.lstrip('\n').rstrip('\n').lstrip(' ').rstrip(' ')
            if msg == "":
              msg=await myprint(tmp)
            else:
              if tmp != msg.raw_text:
                try:
                  msg=await msg.edit(tmp)
  #                await msg.delete()
  #                msg=await myprint(tmp)
  #                await myprintraw(msg.raw_text.encode().hex())
  #                await myprintraw(tmp.encode().hex())
                except MessageNotModifiedError:
                  await myprint("E: wtf? MessageNotModifiedError")
                  await asyncio.sleep(5)
            await asyncio.sleep(1)
                

#        await asyncio.sleep(0.5)
        #info=msgs[0]
        #errs=msgs[1]
        try:
          info, errs = p.communicate(timeout=2)
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

        if p.returncode:
          info=info+"\n==\nE: "+str(p.returncode)
          if errs:
            info=info+"\n"+errs
        info=info.strip()
        if info == "":
          info="null"
        if msg == "":
          msg=await myprint(info)
        else:
          #await msg.delete()
          if info != msg.raw_text:
            await msg.edit(info)
      elif cmd[0] == "shbu":
#        p=subprocess.Popen(event.raw_text.split(' '))
#        p=subprocess.Popen(event.raw_text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
#        p=subprocess.Popen(shlex.split(event.raw_text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)
        args=shlex.split(event.raw_text.split(' ',1)[1])
        await myprint(str(args))
        info=""
        errs=""
#        p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
        p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE)
        try:
#        p.wait(timeout=64)
#        info=p.stdout.read()
          info, errs = p.communicate(timeout=15)
        except subprocess.TimeoutExpired:
          p.kill()
          info, errs = p.communicate(timeout=8)
        else:
          info, errs = p.communicate(timeout=64)
        finally:
          if p.returncode:
            if errs:
              info=info+"\nE: "+str(p.returncode)+"\n"+errs
            else:
              info=info+"\nE: "+str(p.returncode)
          if info:
            await myprint(info)
          else:
            await myprint("null")
      elif cmd[0] == "sh2":
#        msg=subprocess.run(["bash", "-c", event.raw_text.split(' ', 1) ], stdout=subprocess.PIPE, text=True ).stdout
#        try:
        cp=subprocess.run(["bash", "-l", "-c", event.raw_text.split(' ', 1)[1] ], stdout=subprocess.PIPE, text=True, timeout=64, stderr=subprocess.PIPE )
#        finally:
        info=""
        if cp.stdout:
#          await myprint(cp.stdout)
          info=cp.stdout+"\n"
        if cp.returncode:
          if cp.stderr:
            info=info+"E: "+str(cp.returncode)+"\n"+cp.stderr
          else:
            info=info+"E: "+str(cp.returncode)
        if info:
          await myprint(info)
      elif cmd[0] == "mkchat":
        result = await client(functions.messages.CreateChatRequest(users=['liqsliu_bot'],title=me.username))
        await myprint(result.stringify())
      elif cmd[0] == "ad":
        info=await get_admin_of_channel(cmd[1])
        await myprint(info)
      elif cmd[0] == "id":
#          await client.send_message(me.id, str(type(peer)))
#          if type(peer) == PeerUser:
#        peer=await client.get_entity(id)
        peer=await client.get_entity(get_id(cmd[1]))
#        await myprint(peer.stringify())
        if type(peer) == User:
          if peer.username:
            name="@"+peer.username
          else:
            name=peer.first_name
#          await client.send_message(me.id, "["+str(peer.id)+"](tg://user?id="+str(peer.id)+")", parse_mode="md")
          info="["+name+"](tg://openmessage?user_id="+str(peer.id)+")"
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
        if url.split('/')[3] == "c":
          cid=int(url.split('/')[4])
          id=int(url.split('/')[5].split('?')[0])
#          chat=utils.resolve_id(cid)[1]
        else:
          cid=url.split('/')[3]
          id=int(url.split('/')[4].split('?')[0])
        if "?comment=" in url:
#          linked_cid=await get_linked_cid(cid)
          cid=await get_linked_cid(cid)
          id=int(url.split('=')[1])

        chat=await client.get_input_entity(cid)
        msg=await client.get_messages(chat,ids=id)
        if msg:
#          info=mdraw(msg.stringify(),"code")
          info=mdraw(msg.stringify(),"`")
          info="```\n"+info+"\n```"
          info=info+"\n\ntg://openmessage?chat_id="+str(utils.resolve_id(msg.chat_id)[0])+"\ncid: `"+str(msg.chat_id)+"`"
          if msg.chat_id != msg.sender_id:
            if msg.sender_id < 0:
              info=info+"\n\ntg://openmessage?chat_id="+str(utils.resolve_id(msg.sender_id)[0])+"\ncid: `"+str(msg.sender_id)+"`"
            else:
              info=info+"\n\ntg://openmessage?user_id="+str(msg.sender_id)+"\nuid: `"+str(msg.sender_id)+"`"
          if "?comment=" in url:
            info=info+"\n\nmsg link: https://t.me/c/"+str(cid)+"/"+str(msg.id)
        else:
#          info=mdraw(msg.stringify(),"code")
          info="no msg"
#        await client.send_message(me.id, "msg:" + msg)
#        await myprint("msg: " + msg)
        await myprintmd(info)
      elif cmd[0] == "idf":
        peer=await client.get_input_entity(get_id(cmd[1]))
        if type(peer) == User:
          peer = await client(functions.users.GetFullUserRequest(id=peer))
#            await client.send_message(me.id, peer.stringify())
#          await myprint(peer.stringify())
          info=str(type(peer))+ ": `"+str(utils.get_peer_id(peer.user))+"`"
        elif type(peer) == Chat:
          peer = await client(functions.messages.GetFullChatRequest(peer.id))
          info=str(type(peer))+ ": `"+str(utils.get_peer_id(peer.full_chat))+"`"
#        elif type(peer) == Channel:
        #https://docs.telethon.dev/en/latest/concepts/chats-vs-channels.html
        #megagroups are channels
        elif peer.broadcast or peer.megagroup or peer.gigagroup:
          peer = await client(functions.channels.GetFullChannelRequest(peer))
          info=str(type(peer))+ ": `"+str(utils.get_peer_id(peer.full_chat))+"`"
        else:
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
          await myprint(str(auto_msg))
        elif len(cmd) < 4:
#          await myprint("id [ctime interval target text]")
          await myprint("am interval target text")
          
        else:
          ctime=time()
          interval=int(cmd[1])
          target=int(cmd[2])
          text=event.raw_text.split(' ', 3)[3]
          item=[ctime,interval,target,text]
          if len(auto_msg) == 0:
            max_id=0
          else:
            max_id=auto_msg.keys()[-1]
          auto_msg.update({max_id+1:item})
          await myprint(str(auto_msg[max_id+1]))
      elif cmd[0] == "amad":
        await myprint("id [ctime interval target text]")
#        await myprint("am interval target text")
      elif cmd[0] == "amload":
        import ast
        auto_msg=ast.literal_eval(event.raw_text.split(' ',1)[1])
        await myprint(str(auto_msg))
      elif cmd[0] == "amdel":
        auto_msg.pop(int(cmd[1]))
        await myprint(str(auto_msg))
      elif cmd[0] == "amclear":
        auto_msg={}
        await myprint(str(auto_msg))
      elif cmd[0] == "af":
        if event.raw_text == "af":
          await client.send_message(me.id, str(auto_forward_list))
        else:
          if len(cmd) == 3:
            auto_forward_list.update({int(cmd[1]):int(cmd[2])})
            await client.send_message(me.id, str(auto_forward_list))
          else:
            await client.send_message(me.id, "格式有误: am cid cid")
      elif cmd[0] == "afad":
        await client.send_message(me.id, "格式: am cid cid")
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
        url=cmd[1]
        if cmd[1][0] =="@":
          peer=await client.get_entity(cmd[1][1:])
        elif url.split('/')[2] == "t.me":
          if url.split('/')[3] == "c":
            cid=int(url.split('/')[4])
            max_msg_id=int(url.split('/')[5])
          else:
            cid=int(url.split('/')[3])
            max_msg_id=int(url.split('/')[4])
          peer=await client.get_entity(cid)
        else:
          peer=await client.get_entity(int(cmd[1]))
        if len(msg) == 3:
          max_msg_id=int(cmd[2])
        else:
          max_msg_id=None
          await client.send_message(me.id, "格式有误")
        if max_msg_id:
          await client.delete_messages(peer, message_ids=list(range(1,max_msg_id+1)))
          await client.send_message(me.id, "clear ok")
        else:
          await client.send_message(me.id, "格式有误")
      else:
        if debug:
          await myprint(event.stringify())
        msg=event.forward
        if msg != None:
  #          chat = await msg.get_chat()
  #        elif type(msg.from_id) == PeerChannel:
          peer=msg.saved_from_peer
          if peer:
            chat_id=utils.get_peer_id(peer)
          else:
            chat_id = msg.chat_id

          info=str(type(peer))
          info=info+"\ncid: `"+str(chat_id)+"`"

          peer=msg.from_id
          if peer:
            sender_id=utils.get_peer_id(peer)
          else:
            sender_id = msg.sender_id

          if sender_id != chat_id:
            info=info+"\n"+str(type(peer))
            if sender_id < 0:
              info=info+"\ncid: `"+str(sender_id)+"`"
            else:
              info=info+"\nuid: `"+str(sender_id)+"`"
#          info=info+"\nmsg link: https://t.me/c/"+chat_id+"/"+str(msg.id)
#          if msg_id:
#            info=info+"\nmsg link: https://t.me/c/"+utils.resolve_id(cid)[0]+"/"+str(msg_id)
#          await myprint(info, parse_mode="md")

#          drafts=await client.get_drafts()
#          if type(drafts) == list and len(drafts) >= 1:
#            draft=drafts[0]
          msg_id=msg.saved_from_msg_id
          async for draft in client.iter_drafts():
            if draft.text == "" or draft.text == "v":
  #            print(draft.text)
#              await client.send_message(me.id, "fwd:" + event.message.stringify())
  #            await client.send_message(me.id, str(draft))
#              await client.send_message(me.id, draft.stringify())
              msg_id=draft.reply_to_msg_id
              if msg_id != None:
#                cid=draft.entity.id
#                chat=await client.get_input_entity(cid)
#                msg=await client.get_messages(chat,ids=msg_id)
                msg=await client.get_messages(draft.entity,ids=msg_id)
                if msg:
                  chat_id=msg.chat_id
#                  await draft.set_message(text="["+str(msg.sender_id)+"](tg://user?id="+str(msg.sender_id)+")", parse_mode="md")
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
              info=info+"\nmsg link: https://t.me/c/"+str(utils.resolve_id(chat_id)[0])+"/"+str(msg_id)
            if len(msg.stringify()) > MAX_MSG_LEN:
              await myprintmd(info)
              await myprin(msg.stringify())
            else:
              await myprin(msg.stringify())
              await myprintmd(info)
          else:
            await myprintmd(info)
    elif event.raw_text == "myid":
      if event.is_reply:
        replied = await event.get_reply_message()
        #sender = replied.sender
        if replied:
          if replied.sender_id == me.id:
            await event.reply(str(sender_id))
      elif type(event.peer_id) == PeerUser:
        await event.reply(str(sender_id))
    elif event.raw_text == "ping":
      if event.is_reply:
        replied = await event.get_reply_message()
        #sender = replied.sender
        if replied:
          if replied.sender_id == me.id and event.sender_id != me.id:
            await event.reply("pong")
      elif type(event.peer_id) == PeerUser and event.sender_id != me.id:
        await client.send_message(chat_id, "pong")
    #https://stackoverflow.com/a/53519143
    elif chat_id == cid_wtfipfs:
  #    await myprint("cid wtf ok")
      if type(event.from_id) == PeerChannel:
        if sender_id == cid_tw:
          await event.unpin()
        else:
          await event.delete()
    #https://www.runoob.com/python/att-dictionary-has_key.html
#    elif chat_id in auto_forward_list and not await is_debug("auto_forward"):
    elif chat_id in auto_forward_list:
#      schat=utils.resolve_id(chat_id)[1]
#      schat=await client.get_entity(chat_id)
      cid=auto_forward_list[chat_id]
      #chat=await client.get_entity(cid)
#      chat=PeerChannel(cid)
#      chat=utils.resolve_id(cid)[1]
      chat=await client.get_input_entity(cid)
      if chat:
#        await event.forward_to(chat)
        if event.grouped_id != None:
          msg_id=event.id
          schat=await client.get_input_entity(chat_id)
          msg=await client.get_messages(schat, ids=msg_id-1)
          if not msg or event.grouped_id != msg.grouped_id:
  #          msg0 = await client.get_messages(schat, ids=msg_id)
  #          msg = event.message
  #          msgs=[await client.get_messages(schat, ids=msg_id)]
            grouped_id = event.grouped_id
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
          await event.forward_to(chat)

  except Exception as e:
    await client.send_message(me.id, "E: "+str(e)+"\n==\n"+traceback.format_exc())
#    await client.send_message(me.id, "E: "+str(e))
#    await myprint("==\n"+traceback.format_exc())




async def wtf_my_get_entity(id):
  try:
    peer=await client.get_input_entity(id)
  except ValueError:
    peer=await client.get_entity(id)
  return peer


async def mytest():
#  await client.send_message('me', 'Hello, myself!')
#  await client.send_message(username, 'test')
#  await client.send_message(-1001193563578, 'test')
#  await client.send_message(my_chat_id, 'hi*test*')
#  await client.send_message(my_chat_id, 'hi**test**')
#  await client.send_message(my_chat_id, 'hi', file='twtg.py')
#  await client.send_file(my_chat_id, file='twtg.py', caption='send file')
#  await client.send_file(my_chat_id, file='/home/liqsliu/tmp/gs1T8DpGR5u4oPCjMp8zKw.jpg', caption='send file')
  delay=600 - time() % 600
  if len(sys.argv) > 2:
    msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md', schedule=timedelta(seconds=delay))
  elif len(sys.argv) == 2:
    msg=await client.send_message(my_chat_id, my_tw_text, parse_mode='md', link_preview=False, schedule=timedelta(seconds=delay))
  if len(sys.argv) > 1:
    #print(msg.stringify())
    print(msg)
    if type(msg) == list:
      msg=msg[0]
    if not hasattr(msg, 'id'):
      me = await client.get_me()
      msg=await client.send_message(me.id, "E: twtg.py:\n" + msg.__repr__())
      print(msg)


async def is_debug(text="auto_msg"):
  if debug:
    tasks=""
    for j in asyncio.all_tasks():
      tasks=tasks+"\n"+j.get_name()
#    msg=await myprint(text+" is running,but will not work in debug mode.\nrunning tasks: "+tasks)
    msg=await myprint(text+"is running, now tasks: \n"+str(tasks))
#    msg=await myprint(text+"is running, now tasks: \n"+str(asyncio.all_tasks()))
    await asyncio.sleep(5)
    await msg.delete()
    return True
  else:
    return False



async def auto_msg_send(item):
  await myprint("start auto_msg: "+str(item))
  await client.send_message(item[2], item[3])

  if item[1] > 0:
    wait=MAX_AUTO_MSG_TASK_TIME - ( ( time() - item[0] ) % item[1] )
    if wait > 0:
      await asyncio.sleep(wait)


MAX_AUTO_MSG_TASK_TIME=60

async def auto_msg_task():
  global auto_msg # id [ctime interval target text]
  while True:
    await asyncio.sleep(3)
    if await is_debug():
      continue
    if len(auto_msg) > 0:
      for i in auto_msg:
        item=auto_msg[i]
        if item[1] > 0:
          gogo=( time() - item[0] ) % item[1]
          if gogo > 0 and gogo < MAX_AUTO_MSG_TASK_TIME:
            j=0
            for j in asyncio.all_tasks():
              if j.get_name() == str(item[0:3]):
                break
            if j:
              if j.get_name() == str(item[0:3]):
                break
            asyncio.create_task(auto_msg_send(item),name=str(item[0:3]))
  #          msg=await client.send_message(auto_msg[i][2], auto_msg[i][2])
        elif item[1] < 0:
          gogo=( time() - item[0] ) + item[1]
          if gogo > 0:
            asyncio.create_task(auto_msg_send(item),name=str(item[0:3]))
            auto_msg.pop(i)

async def myinit():
  global me,log_cid,debug,auto_forward_list,auto_msg
  auto_msg={}
  asyncio.create_task(auto_msg_task())
  auto_forward_list={}
  chat=await client.get_input_entity(myid)
  if chat:
    msg=await client.get_messages(chat, ids=2817682)
  if chat and msg and msg.raw_text:
    import ast
    auto_forward_list=ast.literal_eval(msg.raw_text)
    await msg.reply("atlist")
  else:
    await client.send_message(myid, "start")




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
  
  global me,log_cid,debug
#  me = client.get_me()
  me = await client.get_me()
  print (me.id)
  #print (me.stringify())
  debug=False
  log_cid=me.id

  if me.id == myid:
    await myinit()
  await client.run_until_disconnected()





#client.start()



#https://docs.python.org/3/library/asyncio-task.html#asyncio.run
#loop = asyncio.get_running_loop()
#loop = asyncio.get_event_loop()
#loop.create_task(auto_msg_task(msgs))
#auto_msg={}
#asyncio.create_task(auto_msg_task())
#asyncio.run(auto_msg_task())



#client.run_until_disconnected()

with client:
  client.loop.run_until_complete(main())
