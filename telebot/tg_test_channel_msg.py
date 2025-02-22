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

#bot_token = get_my_key("TELEGRAM_BOT_TOKEN_AUTO_DELE_MSG")
bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
TOKEN = bot_token

import sys
#for i in sys.argv:
#  print(i)



from telegram.ext import Updater
from telegram import InputMediaPhoto
from telegram import InputMediaVideo
from telegram import InputMediaDocument

updater = Updater(token=bot_token, use_context=True)
bot = updater.bot

dispatcher = updater.dispatcher



#def start(update, context):
#  context.bot.send_message(chat_id=update.effective_chat.id, text="admin: @liqsliu")
#from telegram.ext import CommandHandler
#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(start_handler)



from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="只有格式为“@liqsliu text”的消息会被转发给 @liqsliu")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



my_id=113130580

from telegram.ext import MessageHandler, Filters

import json

def dump_msg(update: Update, context: CallbackContext):
  print("get a msg")
#  context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

  msg=update.effective_message
  if msg:
    if update.effective_chat.type == "private":
        pass
    else:
#        context.bot.send_message(chat_id=update.effective_chat.id, text='```\n'+json.dumps(msg.to_dict(),indent=2)+'\n```', parse_mode="Markdown")
      print(json.dumps(msg.to_dict(),indent=2))

handler = MessageHandler(Filters.text & (~Filters.command), dump_msg)
dispatcher.add_handler(handler)



print("run...")

#updater.stop()
updater.start_polling()

