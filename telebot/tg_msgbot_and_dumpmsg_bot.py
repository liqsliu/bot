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
#  context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
  msg=update.effective_message
  if msg:
#    context.bot.send_message(chat_id=my_id, text=msg.to_json())
#    context.bot.send_message(chat_id=my_id, text=json.dumps(msg.to_dict(),indent=2))
#    context.bot.send_message(chat_id=my_id, text='```\n'+json.dumps(msg.to_dict(),indent=2)+'```', parse_mode="MarkdownV2")
    if update.effective_chat.type == "private":
      if msg.text[0:8] == "@liqsliu":
        info="tg://openmessage?user_id="+str(msg.from_user.id)
        info=info+"\n==\n"
        if msg.text[8] == ' ':
          info=info+msg.text[9:]
        else:
          info=info+msg.text[8:]
        context.bot.send_message(chat_id=my_id, text=info)
#        context.bot.send_message(chat_id=my_id, text='```\n'+json.dumps(msg.to_dict(),indent=2)+'\n```', parse_mode="MarkdownV2")
        context.bot.send_message(chat_id=my_id, text='```\n'+json.dumps(msg.to_dict(),indent=2)+'\n```', parse_mode="Markdown")
        context.bot.send_message(chat_id=update.effective_chat.id, text="已发送")
      else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='```\n'+json.dumps(msg.to_dict(),indent=2)+'\n```', parse_mode="Markdown")

handler = MessageHandler(Filters.text & (~Filters.command), dump_msg)
dispatcher.add_handler(handler)


#updater.stop()
updater.start_polling()

