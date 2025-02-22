#!/usr/bin/python3

debug=True
debug=False

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


bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
TOKEN = bot_token

myid = int(get_my_key("TELEGRAM_MY_ID"))
cid_tw = int(get_my_key("TELEGRAM_GROUP_TW"))
cid_ipfs = int(get_my_key("TELEGRAM_GROUP_IPFS"))
cid_wtfipfs = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

import sys
#for i in sys.argv:
#  print(i)



from telegram.ext import Updater
from telegram import InputMediaPhoto
from telegram import InputMediaVideo
from telegram import InputMediaDocument


#import telegram.error.RetryAfter
import telegram.error



updater = Updater(token=bot_token, use_context=True)
bot = updater.bot

#dispatcher = updater.dispatcher
#def start(update, context):
#  context.bot.send_message(chat_id=update.effective_chat.id, text="@liqsliu")
#from telegram.ext import CommandHandler
#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(start_handler)






from time import time
from time import sleep



import os
import traceback




def myprint(info,id=myid):
  print("print: "+ info)
  bot.send_message(chat_id=id, text=info)


def twtg():
  try:
    if len(sys.argv) > 1:
    #  my_list=sys.argv.copy()
      my_tw_text=sys.argv[1]
    my_tw_files=[]
    if len(sys.argv) > 2:
      my_tw_files=sys.argv[2].split(' ')

    my_chat_id=cid_tw

    if not debug:
      if time() % 600 < 25:
        sleep(30 - time() % 600)
      else:
        sleep(630 - time() % 600)
    else:
      bot.send_message(chat_id=myid, text="twtgbot.py argv: "+str(sys.argv))

    if len(sys.argv) > 2:
      media=[]
      for i in my_tw_files:
        if os.path.exists(i):
          file=open(i,"rb")
        else:
          file=i
        if i[-4:] == '.mp4':
          media.append(InputMediaVideo(file, caption=my_tw_text, parse_mode="MarkdownV2"))
        elif i[-4:] == '.jpg':
          media.append(InputMediaPhoto(file, caption=my_tw_text, parse_mode="MarkdownV2"))
        elif i[-4:] == '.png':
          media.append(InputMediaPhoto(file, caption=my_tw_text, parse_mode="MarkdownV2"))
        elif i[-5:] == '.webp':
          media.append(InputMediaPhoto(file, caption=my_tw_text, parse_mode="MarkdownV2"))
        else:
          media.append(InputMediaDocument(file, caption=my_tw_text, parse_mode="MarkdownV2"))
        my_tw_text=None
      i=0
      while True:
        try:
          msg=bot.send_media_group(chat_id=my_chat_id, media=media)
          break
        except telegram.error.RetryAfter as e:
          sleep(e.retry_after)
          sleep(18)
          i+=1
          if i==5:
            info="E: "+str(e)+"\n==\n"+traceback.format_exc()+"\n\nargv: "+str(sys.argv)
            myprint(info)
            sleep(5)
            break
        except:
          info="E: "+str(e)+"\n==\n"+traceback.format_exc()+"\n\nargv: "+str(sys.argv)
          myprint(info)


    elif len(sys.argv) == 2:
#      msg=bot.send_message(chat_id=my_chat_id, text=my_tw_text, parse_mode="MarkdownV2", disable_web_page_preview=True)
      i=0
      while True:
        try:
          msg=bot.send_message(chat_id=my_chat_id, text=my_tw_text, parse_mode="MarkdownV2", disable_web_page_preview=True)
          break
#        except telegram.error.RetryAfter:
        except telegram.error.RetryAfter as e:
          sleep(e.retry_after)
          sleep(18)
          i+=1
          if i==5:
            info="E: "+str(e)+"\n==\n"+traceback.format_exc()+"\n\nargv: "+str(sys.argv)
            myprint(info)
            sleep(5)
            break
        except:
          info="E: "+str(e)+"\n==\n"+traceback.format_exc()+"\n\nargv: "+str(sys.argv)
          myprint(info)
    if len(sys.argv) > 1:
      #print(msg.stringify())
      print(msg)
      if type(msg) == list:
        msg=msg[0]
  #    if not hasattr(msg, 'id'):
      if not hasattr(msg, 'message_id'):
  #      me = await client.get_me()
  #      msg=await client.send_message(me.id, "E: twtg.py:\n" + msg.__repr__())
        msg=bot.send_message(chat_id=myid, text=msg.to_json())
        print(msg)
  except Exception as e:
    bot.send_message(chat_id=myid, text="E: "+str(e)+"\n==\n"+traceback.format_exc()+"\n\nargv: "+str(sys.argv))

twtg()

updater.stop()
