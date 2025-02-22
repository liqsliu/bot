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

#bot_token = get_my_key("TELEGRAM_BOT_TOKEN_LIQSLIU")
bot_token = get_my_key("TELEGRAM_BOT_TOKEN_AUTO_DELE_MSG")
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)




from telegram.ext import MessageHandler, Filters

def delete_msg(update: Update, context: CallbackContext):
#  context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#      msg=bot.send_message(chat_id=113130580, text=msg.to_json())
  msg=update.effective_message
  if msg != None:
    context.bot.send_message(chat_id=113130580, text=msg.to_json())
    info="delete: "
    if msg.from_user != None:
      info=info+str(msg.from_user.id)
    info=info+":"
#    if update.effective_user != None:
    if msg.sender_chat != None:
      info=info+str(msg.sender_chat.id)
    info=info+":"
    info=info+str(update.effective_chat.id)
    info=info+"+"
    info=info+str(msg.message_id)
#    context.bot.send_message(chat_id=113130580, text=info)
    if msg.from_user != None:
      if msg.from_user.id == 777000:
        if msg.sender_chat.id != update.effective_chat.id:
#          if update.effective_chat.ban_member(msg.sender_chat.id) == True:
#            info=info+"++baned"
          import subprocess
          context.bot.send_message(chat_id=113130580, text="ban:"+subprocess.run(["bash", "ban_chat.sh", bot_token, str(update.effective_chat.id), str(msg.sender_chat.id) ], stdout=subprocess.PIPE, text=True ).stdout )
          if msg.delete() == True:
            info=info+"++deleted"
            context.bot.send_message(chat_id=update.effective_chat.id, text="禁止此类匿名消息，已删除。")
          context.bot.send_message(chat_id=113130580, text=info)

#          info=str(context.bot.get_chat_administrators(chat_id=msg.sender_chat.id))
#          info=str(context.bot.get_chat_administrators(chat_id="@"+msg.sender_chat.username))
#          context.bot.send_message(chat_id=113130580, text=info)


delete_handler = MessageHandler(Filters.text & (~Filters.command), delete_msg)
dispatcher.add_handler(delete_handler)





#updater.stop()
updater.start_polling()

