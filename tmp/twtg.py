#!/usr/bin/python3


import sys

#for i in sys.argv:
#  print(i)


if len(sys.argv) > 0:
#  my_list=sys.argv.copy()
  my_tw_text=sys.argv[1]
  my_tw_files=sys.argv[2].split(' ')



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



from telethon import TelegramClient, events, sync
#from telethon.tl.types.input_peer_chat import InputPeerChat
from telethon.tl.types import InputPeerChat, PeerUser, PeerChannel





# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = get_my_key("TELEGRAM_API_ID")
api_hash = get_my_key("TELEGRAM_API_ID")
#TOKEN = get_env('TG_TOKEN', 'Enter the bot token: ')
#NAME = TOKEN.split(':')[0]
#bot_token = 'xxxx:xxxxxxxxxx'
#bot_id = bot_token.split(':')[0]
#bot_hash = bot_token.split(':')[1]

#client = TelegramClient('session_name', api_id, api_hash)
client = TelegramClient('/home/liqsliu/.ssh/session_name.session', api_id, api_hash)
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
#async def handler(event):
#  print (event.stringify())
#  chat = await event.get_chat()
#  sender = await event.get_sender()
#  chat_id = event.chat_id
#  sender_id = event.sender_id
#  await event.respond(event.text)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
  if event.chat_id == my_id:
    if event.sender_id != my_id:
      await event.respond('{}'.format(event.stringify))

@client.on(events.NewMessage(incoming=True, pattern=r'ping'))
async def handler(event):
  if event.chat_id == my_id:
    await event.respond('pong')

@client.on(events.NewMessage(incoming=True, pattern=r'myid'))
async def handler(event):
  if event.is_reply:
    replied = await event.get_reply_message()
    sender = replied.sender
    if sender.id == my_id:
      await event.respond('your id: {}\nchat_id: {}'.format(event.sender_id, event.chat_id))
  elif event.chat_id == my_id:
      await event.respond('your id: {}\nchat_id: {}'.format(event.sender_id, event.chat_id))

@client.on(events.NewMessage(outgoing=True, pattern=r'id'))
async def handler(event):
  if event.is_reply:
    replied = await event.get_reply_message()
    sender = replied.sender
    await event.respond('id: {}\nchat_id: {}'.format(sender.id, event.chat_id))
    #stringify()
  else:
    await event.respond('chat_id: {}'.format(event.chat_id))

#@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
#async def handler(event):
#  if event.is_reply:
#    replied = await event.get_reply_message()
#    sender = replied.sender
#	await client.download_profile_photo(sender)
#    await event.respond('Saved your photo {}'.format(sender.username))

async def getmsgid():
#  chat = InputPeerChat(my_chat_id)
  chat = await client.get_entity(my_chat_id)
#  total_count, messages, senders = client.get_message_history(chat, limit=10)
  messages = await client.get_messages(chat, limit=64)

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
#    print (msg.stringify())
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
      continue
    content = msg.message
    for msg_text in content.splitlines():
      if msg_text[0:2] == "> ":
        continue
      if msg_text == "":
        continue
      content_line=msg_text
      break
    if content_line == "":
      continue
#    if content.splitlines()[0] == my_msg_text.splitlines()[0]:
#    if my_msg_text.splitlines()[0] in content:
#    if my_msg_text == content :
    if content_line == my_msg_text.splitlines()[0]:
      if type(msg.from_id) == PeerChannel:
#        if my_msg_sender == "T Telegram: ":
        if my_msg_sender == "Telegram":
          print(msg.id)
          break
      elif msg.sender_id == 1494863126:
        if my_msg_sender == "bot":
          print(msg.id)
          break
      elif type(msg.from_id) == PeerUser:
        sender= await msg.get_sender()
        if my_msg_sender == sender.first_name:
          print(msg.id)
          break


my_id=0
async def mytest():
  me = await client.get_me()
  my_id=me.id
  print(me.stringify())
#  await client.send_message('me', 'Hello, myself!')
#  await client.send_message(username, 'test')
#  await client.send_message(-1001193563578, 'test')
  cid_ipfsrss=-1001292248509
  cid_tw=-1001439521181
  my_chat_id=cid_ipfsrss
  my_chat_id=my_id
  my_chat_id=cid_tw
#  await client.send_message(my_chat_id, 'hi*test*')
#  await client.send_message(my_chat_id, 'hi**test**')
#  await client.send_message(my_chat_id, 'hi', file='twtg.py')
#  await client.send_file(my_chat_id, file='twtg.py', caption='send file')
#  await client.send_file(my_chat_id, file='/home/liqsliu/tmp/gs1T8DpGR5u4oPCjMp8zKw.jpg', caption='send file')
  await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md')
  exit()
  chat = await client.get_entity(my_chat_id)
#  total_count, messages, senders = client.get_message_history(chat, limit=10)
  messages = await client.get_messages(chat, limit=4)
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
    print(content)
    print(msg.stringify())
    if not hasattr(msg, 'message'):
      continue
    content = msg.message

async def main():
#    bot.run_until_disconnected()
#  await myinit()
#  await getmsgid()
  await mytest()
#  await client.run_until_disconnected()


#client.start()
#if __name__ == '__main__':
#  main()

with client:
  client.loop.run_until_complete(main())
