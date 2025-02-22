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
#    print(line)
    if line.split(' ',1)[0] == key:
      break
    line = f.readline()
  f.close()
  return line.split(' ',1)[1].rstrip('\n')



from telethon import TelegramClient, events, sync
#from telethon.tl.types.input_peer_chat import InputPeerChat
from telethon.tl.types import InputPeerChat, PeerUser, PeerChannel

from datetime import timedelta
from time import time




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



async def mytest():
#  await client.send_message('me', 'Hello, myself!')
#  await client.send_message(username, 'test')
#  await client.send_message(-1001193563578, 'test')
  cid_ipfsrss=-1001292248509
  cid_tw=-1001439521181
  my_chat_id=cid_ipfsrss
  my_chat_id=cid_tw
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
