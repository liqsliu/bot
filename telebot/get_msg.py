#!/usr/bin/python3



def get_my_key(key):
  f = open("/home/liqsliu/.ssh/private_keys.txt")
  line = f.readline()
  while line:
#    print(line)
    if line.split(' ',1)[0] == key:
      break
    line = f.readline()
  f.close()
  return line.split(' ',1)[1].rstrip('\n')

import sys

#for i in sys.argv:
#  print(i)


# id reply_msg fwd_msg
my_cmd=sys.argv[1]

my_msg_text=str(sys.argv[2])
my_msg_sender=str(sys.argv[3])
my_chat_id=int(sys.argv[4])

if my_cmd == "debug":
  info=str(sys.argv)
  info+="my_msg_text: "+my_msg_text
  print(info)
  exit()

debug=False
if my_cmd == "iddebug":
  my_cmd="id"
  debug=True

forward_flag="Forwarded from "
if my_msg_text.startswith(forward_flag):
  if ": " in my_msg_text.split('\n', 1)[0]:
#        if not ":" in my_msg_line.split(': ', 1)[0]
    my_msg_text=my_msg_text.split(': ', 1)[1]


if my_msg_text == "":
  exit()




from telethon import TelegramClient, events, sync
#from telethon.tl.types.input_peer_chat import InputPeerChat
from telethon.tl.types import InputPeerChat, PeerUser, PeerChannel


# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = int(get_my_key("TELEGRAM_API_ID"))
api_hash = get_my_key("TELEGRAM_API_HASH")
#TOKEN = get_env('TG_TOKEN', 'Enter the bot token: ')
#NAME = TOKEN.split(':')[0]
#bot_token = 'xxxx:xxxxxxxxxx'
#bot_id = bot_token.split(':')[0]
#bot_hash = bot_token.split(':')[1]


#client = TelegramClient('session_name', api_id, api_hash)
#client = TelegramClient('/home/liqsliu/.ssh/telethon_session_name.session', api_id, api_hash)
client = TelegramClient('/home/liqsliu/.ssh/telethon_for_get_msg.session', api_id, api_hash)
#client = TelegramClient('bot', bot_id, bot_hash).start(bot_token=bot_token)


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

#@client.on(events.NewMessage)
#async def echo(event):
#  print (event.stringify())
#  chat = await event.get_chat()
#  sender = await event.get_sender()
#  chat_id = event.chat_id
#  sender_id = event.sender_id
#  await event.respond(event.text)

#@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
#async def wiki(event):
#  if event.is_reply:
#    replied = await event.get_reply_message()
#    sender = replied.sender
#	await client.download_profile_photo(sender)
#    await event.respond('Saved your photo {}'.format(sender.username))

async def bugetmsgid():
  for msg in reversed(messages):
    # Format the message content
    if getattr(msg, 'media', None):
      content = '<{}> {}'.format(  # The media may or may not have a caption
      msg.media.__class__.__name__,
      getattr(msg.media, 'caption', ''))
    elif hasattr(msg, 'message'):
      content = msg.message
    elif hasattr(msg, 'action'):
      content = str(msg.action)
    else:
      # Unknown message, simply print its class name
      content = msg.__class__.__name__




def check_msg(msg):
#    print (msg.stringify())
#    print (content)
#    print (type(msg.sender))
#    print (type(msg.from_id))
#    print (msg.from_id.stringify())
#    if type(msg.from_id) == PeerChannel:
#    if hasattr(msg.from_id, 'channel_id'):
#      continue
#    if type(msg.from_id) == PeerUser:
#      sender= await msg.get_sender()
#      text = '[{}:{}] (ID={})({}) {}({}): {}'.format(msg.date.hour, msg.date.minute, msg.id, msg.chat_id, sender.first_name, msg.chat_id, content)
#      print (text)
#      print(content.splitlines()[0])
#      print(my_msg_text.splitlines()[0])
    #print('{}: {}'.format(msg.sender_id, msg.message))
#    print('{}=={}: {}'.format(my_msg_text, content, msg.message))
  if not hasattr(msg, 'message'):
    return False

  if my_cmd == 'reply_msg':
#        print(msg.stringify())
    if not hasattr(msg, 'reply_to'):
      return False
    if msg.reply_to == None:
      return False

  elif my_cmd == 'fwd_msg':
    if not hasattr(msg, 'fwd_from'):
      return False
    if msg.fwd_from == None:
      return False

  content = msg.message
  if not content:
    return False
  for msg_text in content.splitlines():
    if msg_text[0:2] == "> ":
      continue
    if msg_text == "":
      continue
    content_line=msg_text
    break
  if not "content_line" in locals().keys():
    return False
  if content_line == "":
    return False

  for msg_text in my_msg_text.splitlines():
    if msg_text[0:2] == "> ":
      continue
    if msg_text == "":
      continue
    my_msg_line=msg_text
    break
  if not "my_msg_line" in locals().keys():
    return False
  if my_msg_line == "":
    return False

#    forward_flag="Forwarded from unknown: "
#    forward_flag="Forwarded from "
#    if my_msg_line.startswith(forward_flag):
#      if ": " in my_msg_line:
#        if not ":" in my_msg_line.split(': ', 1)[0]
#        my_msg_line=my_msg_line.split(': ', 1)[1]
#        my_msg_text=my_msg_text.split(': ', 1)[1]


#    if content.splitlines()[0] == my_msg_text.splitlines()[0]:
#    if my_msg_text.splitlines()[0] in content:
#    if my_msg_text == content :
#    if content == my_msg_text or content_line == my_msg_text.splitlines()[0] or (my_msg_text[0:5] == 'X ?: '  and len(my_msg_text.split(' ', 2)) == 3 and content_line[0:2] == my_msg_text[0:2] and content_line.endswith(': '+my_msg_text.split(' ', 2)[2])):
  if content == my_msg_text or content_line == my_msg_line or (my_msg_line[0:5] == 'X ?: '  and len(my_msg_line.split(' ', 2)) == 3 and content_line[0:2] == my_msg_text[0:2] and content_line.endswith(': '+my_msg_line.split(': ', 1)[1])):
    return True
  else:
    return False


async def getmsgid____():
#  total_count, messages, senders = client.get_message_history(chat, limit=10)
#  messages = await client.get_messages(chat, limit=64)
  messages = await client.get_messages(chat, limit=4, search=my_msg_text, from_user=my_msg_sender)
  if debug:
    info="I: get msg 1:"+str(messages)
  if not messages:
    messages = await client.get_messages(chat, limit=8, search=my_msg_text)
    if debug:
      info+="I: msg 2: "+str(messages)
    if not messages:
      if my_msg_sender == "bot":
        messages = await client.get_messages(chat, limit=64, from_user=my_msg_sender)
      elif my_msg_sender == "Telegram":
        messages = await client.get_messages(chat, limit=32, from_user=my_msg_sender)
      else:
        messages = await client.get_messages(chat, limit=16, from_user=my_msg_sender)
      if debug:
        info+="I: msg 3: "+str(messages)
      if not messages:
        messages = await client.get_messages(chat, limit=64)
        if debug:
          info+="I: msg max: "+str(len(messages))
  if debug:
    print(info+"\ntype: "+str(type(messages)))





async def get_msg():
  global chat
  chat = await client.get_entity(my_chat_id)

  if not my_msg_text:
    return False

#  chat = InputPeerChat(my_chat_id)
#  if debug:
#    msgsit = await client.iter_messages(chat, limit=4, search=my_msg_text, from_user=my_msg_sender)


  limit=10*int(64/len(my_msg_text)+1)
  if my_msg_sender == "bot":
    limit=limit*10

  async for msg in client.iter_messages(chat, limit=limit, search=my_msg_text, from_user=my_msg_sender):
    await run_cmd(msg)
    return True


  async for msg in client.iter_messages(chat, limit=int(limit/10), search=my_msg_text):
    if check_msg(msg):
      await run_cmd(msg)
      return True

  if "\n" in my_msg_text:
    async for msg in client.iter_messages(chat, limit=int(limit/10), search=my_msg_text.split("\n")[0]):
      if check_msg(msg):
        await run_cmd(msg)
        return True

  async for msg in client.iter_messages(chat, limit=int(limit/10), from_user=my_msg_sender):
    if check_msg(msg):
      await run_cmd(msg)
      return True

  async for msg in client.iter_messages(chat, limit=int(limit/100+5)):
    if check_msg(msg):
      await run_cmd(msg)
      return True


  return False



async def run_cmd(msg):
#  for msg in messages:
 # for msg in reversed(messages):
#    if check_msg(msg):
  if msg:
    if my_cmd == 'id':
      if type(msg.from_id) == PeerChannel:
        if msg.from_id.channel_id == 1439521181:
  #        if my_msg_sender == "T Telegram: ":
          if my_msg_sender == "twitter":
            print(msg.id)
          elif my_msg_sender == "Telegram":
            print(msg.id)
        else:
          channel = await client.get_entity(msg.from_id.channel_id)
          if my_msg_sender == channel.title:
            print(msg.id)
      elif msg.sender_id == 1494863126:
        if my_msg_sender == "bot":
          print(msg.id)
      elif type(msg.from_id) == PeerUser:
        sender= await msg.get_sender()
        if my_msg_sender == sender.first_name:
          print(msg.id)
    elif my_cmd == 'reply_msg':
#        print(msg.stringify())
      #if msg.reply_to.reply_to_top_id == None:
#        print(msg.stringify())
      msg_id=msg.reply_to.reply_to_msg_id
      msg = await client.get_messages(chat, ids=msg_id)
#        print(msg.stringify())
#        channel = await client.get_entity(msg.from_id.channel_id)
#        print(channel.stringify())
#        msg = await msg.get_reply_message()
#        print(msg.stringify())
      if type(msg.from_id) == PeerChannel:
        if msg.from_id.channel_id == 1439521181:
#          first_name = "Telegram"
          first_name = "twitter"
        else:
          channel = await client.get_entity(msg.from_id.channel_id)
          first_name = channel.title
      elif msg.sender_id == 1494863126:
        first_name = "bot"
      else:
        sender= await msg.get_sender()
#        if sender.id == myid:
        if sender.bot:
          first_name=sender.first_name
        else:
          if sender.username:
            first_name=sender.username
          else:
            first_name=sender.first_name


      msg_id=await get_gmsgid(chat, msg)
      msg = await client.get_messages(chat, ids=msg_id)
      #print('T {}: '.format(first_name))
     # if hasattr(msg, 'message'):
      if hasattr(msg, 'message') and msg.message != '':
        print('T {}: {}'.format(first_name, msg.message))
      else:
        print('T {}: '.format(first_name))
      if msg.media == None:
        return
      else:
        print('')
      print(await get_media(msg))
      if msg.grouped_id != None:
        grouped_id = msg.grouped_id
        #for id in range(msg_id+1,end_id+1):
        for id in range(msg_id+1,msg_id+4):
          msg = await client.get_messages(chat, ids=id)
          if msg.grouped_id == grouped_id:
            if hasattr(msg, 'message') and msg.message != '':
              print('{}: {}'.format(msg.message, await get_media(msg)))
            else:
              print('{}'.format(await get_media(msg)))
          else:
            break

    elif my_cmd == 'fwd_msg':
      pass

async def get_gmsgid(chat, msg):
  if msg.grouped_id != None:
    grouped_id = msg.grouped_id
    for id in range(1, 32):
      #if grouped_id != await client.get_messages(chat, ids=msg.id-id).grouped_id:
      mmsg=await client.get_messages(chat, ids=msg.id-id)
      if grouped_id != mmsg.grouped_id:
        return(msg.id-id+1)
  else:
    return(msg.id)


async def get_media(msg):
  if msg.media != None:
    #media=MessageMediaPhoto(
    #path = await msg.download_media('/home/liqsliu/test.jpg')
    path = await msg.download_media('/home/liqsliu/tmp/')
    if path != None:
      path = path.split('/')[-1]
      #print('https://liuu.tk/'+path.replace(' ','%20'))
      return('https://liuu.tk/'+path.replace(' ','%20'))

async def myinit():
  print(me.stringify())
#  await client.send_message('me', 'Hello, myself!')
#  await client.send_message(username, 'test')
#  await client.send_message(113130580, 'test')
#  await client.send_message(-1001193563578, 'test')




async def main():
  global myid, me, my_msg_sender
  me = await client.get_me()
  myid=me.id
  if my_msg_sender == me.username:
    my_msg_sender = me.first_name

#  await client.send_message(myid, "D: get_msg.py: argv"+str(sys.argv))

#    bot.run_until_disconnected()
#  await myinit()
  await get_msg()
#  await client.run_until_disconnected()


#client.start()
#if __name__ == '__main__':
#  main()



with client:
  client.loop.run_until_complete(main())

exit(0)
