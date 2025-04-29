
#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
#  import signal
#  import sys
#
#  def handler(signum, frame):
#      print("Caught signal:", signum, frame)
#      sys.exit(0)
#
#  signal.signal(signal.SIGINT, handler)

#  from . import *  # noqa: F403
#  from enum import auto
from typing import Type
from . import debug, WORK_DIR, PARENT_DIR, LOG_FILE, get_my_key, HOME, LOGGER


from telethon import TelegramClient
#  from tg.telegram import DOWNLOAD_PATH
from telethon.tl.types import InputChannel, InputPeerChannel, InputPeerUser, InputPhoneContact, KeyboardButton, KeyboardButtonUrl, KeyboardButtonCallback, KeyboardButtonUrl, PeerUser, PeerChannel, PeerChat, User, Channel, Chat, MessageMediaDocument, InputPeerChat, InputPeerChannel, InputPeerUser
from telethon import events, utils
import telethon.errors
from telethon.errors import rpcerrorlist

import aioxmpp
from aioxmpp import stream, ibr, protocol, node, dispatcher, connector, JID, im, errors, MessageType, PresenceType, chatstates

import aiofiles
#  from aiofile import async_open
import aiofiles, aioxmpp, aiohttp

import zstandard

#  from  urltitle.urltitle import URLTitleError
#  from urltitle import URLTitleReader
#  from urltitle import config as urltitle_config

from aiohttp import FormData
from aiohttp.client_exceptions import ClientPayloadError
import io
from io import BufferedReader, TextIOWrapper, BytesIO

from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError




def jaccard_similarity(s1, s2):
    set1, set2 = set(s1), set(s2)
    return len(set1 & set2) / len(set1 | set2)

#  print(jaccard_similarity("hello", "helo"))  # 输出 Jaccard 相似度

#  from Levenshtein import ratio
#  ratio("test", "testt")

from difflib import SequenceMatcher

def similarity(s1, s2):
    #  return SequenceMatcher(None, s1, s2).ratio()
    return SequenceMatcher(lambda x: x in " \t\r\n`", s1, s2).ratio()

#  print(similarity("hello", "helo"))  # 输出相似度



from inspect import isawaitable, currentframe

from functools import wraps
from functools import partial
import pickle
from pathlib import Path
import shlex

import os
import sys

import json
import base64
import re
import ast
import mimetypes
import uuid

import socket
import urllib
import urllib.request
import urllib.error
#  from urllib import request
#  from urllib import parse
import urllib.parse
import html


import binascii
import traceback

import zlib
import gzip
import brotli


import threading
import subprocess
from subprocess import Popen, PIPE

import getpass, random, string
import unicodedata


# http://docs.python.org/zh-cn/3.13/library/collections.html#collections.deque
from collections import deque

from os.path import isdir


import time
#  from time import time, sleep
#  from time import time
from asyncio import sleep
import asyncio

#  HOME = os.environ.get("HOME")

import logging
logger = logging.getLogger(__name__)

#  class NoParsingFilter(logging.Filter):
#    def filter(self, record):
#      #  if record.name == 'tornado.access' and record.levelno == 20:
#      if record.levelno == 20:
#        if record.name == 'httpx':
#          #  pprint(record)
#          msg = record.getMessage()
#          if msg.startswith('HTTP Request: GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/') and msg.endswith(' "HTTP/1.1 404 Not Found"'):
#            return False
#          elif '404 Not Found' in msg and 'GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/' in msg:
#             #  info(f"根据关键词找到了文本: {msg=}")
#             return False
#          elif '404 Not Found' in msg:
#             info(f"根据关键词找到了文本: {msg=}")
#             return False
#          #  else:
#          #    info(f"文本不对: {msg=}")
#      return True


interval = 6
download_media_time_max = 60
upload_media_time_max = 900
run_shell_time_max = 60


msg_delay_default = 0

async def safe_send(jid):
  # msg_safe_delay
  if jid not in send_locks:
    send_locks[jid] = asyncio.Lock()
  #  async with send_locks[jid]:
  return send_locks[jid]




#  class MyMsgLock(asyncio.Lock):
#    def __init__(self) -> None:
#      self.lock = super().__init__()
#      self.last = 0
#      return self
#
#    async def __aenter__(self, jid) -> None:
#      #  return await super().__aenter__()
#      l =  await super().__aenter__()
#      now = time.time()
#      #  now = time.time()
#      # fixme：检测多条消息好一点
#      await sleep(0.02/(time.time()-self.last)-0.004)
#      self.last = now
#
#    #  async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None) -> None:
#    #    return await super().__aexit__(exc_type, exc, tb)

#  def get_send_lock(jid):
#    if jid not in send_locks:
#      send_locks[jid] = asyncio.Lock()
#    now = time.time()
#    #  now = time.time()
#    # fixme：检测多条消息好一点
#    await sleep(0.02/(time.time()-self.last)-0.004)



wtf_time = 5
wtf_time_max = 1800

wtf_line = 20
wtf_line_max = 300

wtf_limit = 512
wtf_ban_time = 300

async def wtf_loop():
  while True:
    await sleep(wtf_time)
    for muc in users:
      if muc not in public_groups:
        continue
      jids = users[muc]
      for jid in jids:
        j = jids[jid]
        w = j[4]
        if w[0] > 1:
          w[0] = w[0]/2
    info("wtf_loop is running...")

def pprint(e):
  print('---')
  print("||%s: %s" % (type(e), e))
  print('---')
  for i in dir(e):
    print("  %s: %s: %s" % (i, type(getattr(e, i)), getattr(e, i)))
  print('===')

#  def get_lineno(fm):
#    #  lineno = "%s" % fm.f_lineno
#    #  while fm.f_back is not None:
#    #    if fm.f_code.co_filename == __file__:
#    #      lineno += " %s" % fm.f_back.f_lineno
#    #      fm = fm.f_back
#    #    else:
#    #      break
#    #  return lineno
#    #  if fm.f_back is not None:
#    #    fm = fm.f_back
#    return f"{fm.f_code.co_name} {fm.f_lineno}"


FILE=os.path.abspath(__file__)

def get_lineno(e=None, fs=None):
  if e is None:
    fm = sys._getframe()
    fm = fm.f_back
    if fm is None:
      return
  else:
    tb = e.__traceback__
    if fs is not None:
      fs.add(tb.tb_frame.f_code.co_name)
    maybe = tb
    n= tb.tb_next
    while n is not None:
      if n.tb_frame.f_code.co_filename != FILE:
        #  print(last.tb_frame.f_code.co_filename, " != ", os.path.abspath(__file__))
        tb = n
      else:
        tb = n
        maybe = tb
        if fs is not None:
          fs.add(tb.tb_frame.f_code.co_name)
      n= tb.tb_next
    if tb != maybe:
      tb = maybe
    fm = tb.tb_frame
  if fs is not None:
    return f"{fm.f_code.co_name} {fm.f_lineno}", fs, fm
  else:
    return f"{fm.f_code.co_name} {fm.f_lineno}"

def info0(s):
  print(short("%s \r" % s.replace("\n", " ")), end='')

def info1(s):
  print(s.replace("\n", " "), end='')

def info2(s):
  print(s.replace("\n", " "))

info = logger.info

def err(text=None, no_send=False, e=None, exc_info=True, stack_info=True):
  if e is not None:
    text = "{} {}: {!r}".format(get_lineno(e=e), text, e)
  logger.error(text, exc_info=exc_info, stack_info=stack_info)
  #  raise ValueError
  if no_send:
    pass
  else:
    text = f"E: {text}"
    if e is None:
      fm = sys._getframe()
      fm = fm.f_back
      send_log(text, fm=fm, delay=2)
    else:
      #  text = "%s %s %s" % (get_lineno(e=e), text, e)
      send_log(text)


def warn(text=None, more=False, no_send=True, e=None, exc_info=True, stack_info=True):
  if e is not None:
    text = "{} {}: {!r}".format(get_lineno(e=e), text, e)
  if more:
    logger.warning(text, exc_info=exc_info, stack_info=stack_info)
  else:
    #  text = f"{fm.f_code.co_name} {fm.f_lineno} {text}"
    logger.warning(text)
  if no_send:
    pass
  else:
    text = f"W: {text}"
    if e is None:
      fm = sys._getframe()
      fm = fm.f_back
      send_log(text, fm=fm)
    else:
      #  text = "%s %s %s" % (get_lineno(e=e), text, e)
      send_log(text)

#  def dbg(text):
#    logger.debug(text)
dbg=logger.debug

def get_cmd(text):
  if text.endswith(": "):
    text = text[:-2]
  tmp = ""
  #  for i in range(len(text)):
    #  c = text[i]
  qn = 0
  #  qq = None
  #  qq = "\\"
  need_escape = False
  in_quote = False
  cmd = []
  for c in text:
    if need_escape is True:
      need_escape = False
      if c == ' ' and in_quote is False:
        tmp = tmp[:-1] + ' '
        continue
    if in_quote is True:
      if c == '"':
        in_quote = False
    else:
      if c == '\\':
        need_escape = True
      elif c == '"':
        in_quote = True
      elif c == ' ':
        cmd.append(tmp)
        tmp = ""
        continue
      elif c == '\n':
        if len(cmd) == 0:
          cmd.append(tmp)
          tmp = ""
          continue
        elif len(cmd) == 1:
          if tmp == "":
            continue
    tmp += c
  if len(tmp) > 0:
    cmd.append(tmp)
  info(f"return cmd {len(cmd)}: {cmd}")
  return cmd


#  def get_cmd(text):
#    if text.endswith(": "):
#      text = text[:-2]
#    cmd = text.split(' ')
#    tmp = []
#    for i in cmd:
#      if tmp:
#        ii = tmp[-1].split("\\\\")[-1]
#        if ii and ii[-1] == "\\":
#          tmp[-1] = tmp[-1][:-1] + " " + i
#        else:
#          #  if i:
#          tmp.append(i)
#      else:
#        if i:
#          tmp.append(i)
#    if tmp:
#      cmd = tmp
#      info(f"return cmd {len(cmd)}: {cmd=}")
#    return cmd

def check_str(nick, nicks):
  for i in nicks:
    if i in nick:
      return True
  return False

def generand(N=4, M=None, *, no_uppercase=False):
  #  return ''.join(random.choice(string.ascii_lowercase+ string.digits) for x in range(N))
  if no_uppercase:
    l = string.ascii_lowercase + string.digits
  else:
    l = string.ascii_letters + string.digits
  if M is not None:
    N = random.randint(N, M)
  return ''.join(random.choice(l) for x in range(N))



#  api_id = int(get_my_key("TELEGRAM_API_ID"))

MY_ID = int(get_my_key("TELEGRAM_MY_ID"))

CHAT_ID = int(get_my_key("TELEGRAM_GROUP_LIQS"))
GROUP_ID = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

GROUP2_ID = int(get_my_key("TELEGRAM_GROUP_PEERS"))
GROUP2_TOPIC = int(get_my_key("TELEGRAM_GROUP_PEERS_TOPIC"))

#  gpt_bot = int(get_my_key("TELEGRAM_GPT_ID"))
gpt_bot = 6226014461
gpt_bot_name = 'littleb_gptBOT'

#  rss_id = int(get_my_key("TELEGRAM_RSS_ID"))
rss_bot = 284403259
music_bot = 1404457467
music_bot_name = 'Music163bot'



MAX_MSG_BYTES = 8000
MAX_MSG_BYTES_TG = 4000
# https://github.com/TokTok/c-toxcore/blob/81b1e4f6348124784088591c4fe9ab41e273031d/toxcore/tox.h#L292
MAX_MSG_BYTES_TOX = 1372
MAX_MSG_BYTES_IRC = 512

HTTP_RES_MAX_BYTES = 15*2**20
HTTP_FILE_MAX_BYTES = 50*2**20

FILE_DOWNLOAD_MAX_BYTES = 100*2**20
TMP_PATH=f"{HOME}/tera/tmp"

DOWNLOAD_PATH0 = "/var/www/dav/tmp"
DOWNLOAD_PATH = f"{HOME}/t"
URL_PATH = ""

#  DOWNLOAD_PATH = "/var/www/dav/home"
#  URL_PATH = "/public"

SH_PATH='/run/user/1000/bot'

DATA_PATH=f"{HOME}/xmpp.data"

#  gpt_chat=None

#  UA = 'Chrome Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) Apple    WebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
#  UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
UA = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
urlre = re.compile(r'(^|\n|\s+)(https?://((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|\[[\da-fA-F:]{4,}\])(:\d+)?(/[^\s]+)*/?)')
url_only_re = re.compile(r'^(https?://((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|\[[\da-fA-F:]{4,}\])(:\d+)?(/[^\s]+)*/?)$')
url_md_left=re.compile(r'\[[^\]]+\]\([^\)]+')
#  shell_color_re=re.compile(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')
#  shell_color_re=re.compile(r'\x1B|\[([0-9]{1,2}(;[0-9]{1,2}(;[0-9]{1,3}))??)?[m|K]')
shell_color_re=re.compile(r'\x1B|\[([0-9]{1,2}(;[0-9]{1,3})*)?(m|K)')

qre = re.compile(r'^(>( .+)?)$', re.M)

#  gptmode=[]
#  CLEAN = "/new_chat"

#  queue = asyncio.Queue(512)

#  queue = {}
#  stuck= {}
queues = {}
nids = {}
mt_send_lock = None
#  mt_send_lock = asyncio.Lock()
#  mt_send_lock2 = asyncio.Lock()
downlaod_lock = asyncio.Lock()
bash_lock = asyncio.Lock()
tg_send_lock = asyncio.Lock()
tg_send_lock2 = asyncio.Lock()

rss_lock = asyncio.Lock()


#  gid_src = {}
mtmsgsg={}
# mtmsgsg: {jid/gateway: mtmsgs}
# mtmsgs: {chat_id: [name for reply, buttons, set(tg msg.id), ...]}


print_msg = False


#  LOADING="思考你发送的内容..."
#  LOADING2="Thinking about what you sent..."
#  LOADINGS="\n\n"+LOADING
#  LOADINGS2="\n\n"+LOADING2
#    #  elif text == "处理图片请求并获得响应可能需要最多5分钟，请耐心等待。" or text == "It may take up to 5 minutes to process image request and give a response, please wait patiently.":
#
#  loadings = (
#      LOADING,
#      LOADING2,
#      """思考你发送的内容...
#  If the bot doesn't respond, please /new_chat before asking.""",
#      "Thinking about what you sent...\nIf the bot doesn't respond, please /new_chat before asking.",
#  "处理图片请求并获得响应可能需要最多5分钟，请耐心等待。",
#  "It may take up to 5 minutes to process image request and give a response, please wait patiently.",
#  )

#  UB.parse_mode = None
#  UB.parse_mode = 'html'






# https://xtxian.com/ChatGPT/prompt/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98.html#%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98
#  PROMPT_TR_ZH = '''我想让你充当中文翻译员、拼写纠正员和改进员我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答我希望你用更优美优雅的高级中文描述保持相同的意思，但使它们更文艺。
#
#  你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。
#
#  我要你只回复更正、改进，不要写任何解释我的第一句话是'''
#
#  PROMPT_TR_MY_S = '请翻译引号中的内容，你要检测其原始语言，如果是中文就翻译成英文，否则就翻译为中文:'
#
#  PROMPT_TR_MY = '请翻译引号中的内容，你要检测其原始语言是不是中文，如果原始语言是中文就翻译成英文，否则就翻译为中文。你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。 我要你只回复更正、改进，不要写任何解释我的第一句话是：\n'



def cross_thread(func=None, *, need_main=True):
  if func is not None:
    return _cross_thread(func)
  def _(func):
    return _cross_thread(func, need_main=need_main)
  return _

def _cross_thread(func, *, need_main=True):
  if asyncio.iscoroutinefunction(func):
    #  res = await run_run(coro, need_main=need_main)
    #  fu = run_cb_in_thread(func, *args, **kwargs)
    #  res = await fu
    if need_main is True:
      async def _(*args, **kwargs):
        coro = func(*args, **kwargs)
        if in_main_thread():
            info(f"在主线程执行: {func}")
            return await coro
        else:
          #  return loop.run_until_complete(func(*args, **kwargs))
          info(f"跨线程在主线程执行: {func}")
          return await run_coro(coro, loop2, loop)
    else:
      async def _(*args, **kwargs):
        coro = func(*args, **kwargs)
        if in_main_thread():
            info(f"跨线程在副线程执行: {func}")
            return await run_coro(coro, loop, loop2)
        else:
          info(f"在副线程执行: {func}")
          return await coro
  else:
    if need_main is True:
      def _(*args, **kwargs):
        if in_main_thread():
            info(f"在主线程执行: {func}")
            return func(*args, **kwargs)
        else:
          #  return loop.run_until_complete(func(*args, **kwargs))
          #  def _(*args, **kwargs):
          info(f"跨线程在主线程执行: {func}")
          return run_cb3(loop, func, *args, **kwargs)
    else:
      def _(*args, **kwargs):
        if in_main_thread():
            info(f"跨线程在副线程执行: {func}")
            return run_cb3(loop2, func, *args, **kwargs)
        else:
          #  def _(*args, **kwargs):
          info(f"在副线程执行: {func}")
          return func(*args, **kwargs)
    #  def _(*args, **kwargs):
      #  return func(*args, **kwargs)
      #  if need_main:
      #    return run_cb_in_main(func, *args, **kwargs)
      #  else:
      #    return run_cb_in_thread(func, *args, **kwargs)
      #  res = run_cb(func, *args, **kwargs, need_main=need_main)
      #  info(f"done: {res}")
      #  return res
  #  return _
  return wraps(func)(_)

def auto_task(func, return_task=False):
  # for callback
  if asyncio.iscoroutinefunction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      t = asyncio.create_task(func(*args, **kwargs), name=f"auto_task_{func.__name__}")
      if return_task:
        return t
      return True
  else:
    err(f"fixme: {func=} 不是异步函数")
    return
  return wrapper



def exceptions_handler(func=None, *, no_send=False):
  if func is not None:
    return __exceptions_handler(func)
  def _(func):
    return __exceptions_handler(func, no_send)
  return _

def __exceptions_handler(func, no_send=False):
  if asyncio.iscoroutinefunction(func):
    async def _(*args, **kwargs):
      try:
        return await func(*args, **kwargs)
      #  except Exception as e:
      except BaseException as e:
        return  _exceptions_handler(e, func, no_send, *args,  **kwargs)
  else:
    def _(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      #  except Exception as e:
      except BaseException as e:
        return  _exceptions_handler(e, func, no_send, *args,  **kwargs)
  return wraps(func)(_)

def _exceptions_handler(e, func=None, no_send=False, *args, **kwargs):
  #  no_send = _no_send
  more = True
  #  no_send = False
  no_send_tg = False
  no_send_xmpp = False
  #  res = f'内部错误: {e=} line: {e.__traceback__.tb_next.tb_lineno}'
  #  lineno = get_lineno2(tb)
  #  lineno = "%s" % tb.tb_lineno
  fs = set()
  lineno, fs, fm = get_lineno(e, fs)
  #  while tb.tb_next is not None:
  #    lineno += " %s" % tb.tb_next.tb_lineno
  #    last_num = tb.tb_next.tb_lineno
  #    tb = tb.tb_next
  #  res = f'{tb.tb_frame.f_code.co_name} {tb.tb_frame.f_code.f_lineno} 内部错误 {e=}'
  #  res = f'{lineno} {e=}'
  # https://docs.python.org/zh-cn/3.11/library/string.html#formatstrings
  res = '{} {!r}'.format(lineno, e)
  #  print("print use logger")
  #  logger.error(res, exc_info=e, stack_info=True)
  #  print("print use logger ok")
  try:
    #  res = f'{e=} line: {e.__traceback__.tb_next.tb_next.tb_lineno}'
    #  raise e
    raise
  except KeyboardInterrupt:
    info("W: 手动终止")
    raise
  except SystemExit:
    err(res, exc_info=True, stack_info=True)
    raise

  except asyncio.CancelledError:
    info("该任务被要求中止: {!r}, fs: {}".format(e, fs))
    raise

  except GeneratorExit:
    # https://docs.python.org/zh-cn/3.13/library/exceptions.html#GeneratorExit
    warn("fixme: {!r}, fs: {}, func: {}(*{}, **{})".format(e, fs, func, args, kwargs))

  except RuntimeError:
    warn("fixme: {!r}, fs: {}, func: {}(*{}, **{})".format(e, fs, func, args, kwargs))

  except AttributeError:
    pass
  except urllib.error.HTTPError:
    res += ' Data not retrieved because %s\nURL: %s %s' % (e, args, kwargs)
  except urllib.error.URLError:
    if isinstance(e.reason, socket.timeout):
      res += ' socket timed out: urllib.error.URLError'
    else:
      res += ' some other error happened'
  except socket.timeout:
    res += ' socket timed out'
  except ConnectionError:
    no_send = True
    #  err("链接问题，退出吧 %s" % res, exc_info=True, stack_info=True)
    #  raise
    more = False
    if e.args[0] == 'stream is not ready':
      # sending xmpp msg
      more = False
    elif e.args[0] == 'disconnected':
      # sending xmpp msg
      more = False
    elif e.args[0] == 'client is not running':
      more = False
    else:
      pass
  except UnicodeDecodeError:
    info("unicode 接码出错")
  except rpcerrorlist.FloodWaitError:
    no_send = True
    info(f"消息发送太快，被服务器当作洪水信息攻击了。")
    global msg_delay_default
    msg_delay_default += (300 - msg_delay_default)/2
    async def f():
      global msg_delay_default
      await sleep(60)
      msg_delay_default -= (300 - msg_delay_default)/2
      if msg_delay_default < 0:
        msg_delay_default = 0.4
    asyncio.create_task(f())
    return True
  except OSError:
    no_send = True
    err("出错啦 OSError %s" % res, True)
    #  raise
  except Exception:
    pass
  except BaseException:
    err("出错啦 %s" % res)
    raise
    #  err(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    #  print(f"W: {repr(e)} line: {e.__traceback__.tb_next.tb_next.tb_lineno}")

  res = f"已忽略异常: {res}"
  if not no_send:
    info("check send_tg: {}".format(send_tg.__name__ in fs))
    info("check send_xmpp: {}".format(send_xmpp.__name__ in fs))
    if _send_tg.__name__ in fs:
      no_send = True
      info(f"fixme: 要刷屏了 fs: {fs} res: {res} e: {e=}")
    elif _send_xmpp.__name__ in fs:
      no_send = True
      info(f"fixme: 要刷屏了 fs: {fs} res: {res} e: {e=}")
    elif send_xmpp.__name__ in fs:
      no_send = True
      info(f"fixme: 要刷屏了 fs: {fs} res: {res} e: {e=}")

    elif send_log.__name__ in fs:
      info(f"send_log is busy: {res}")
      no_send = True

  if no_send:
    if more:
      err(res, True)
    else:
      warn(res)
  else:
    err(res)
    # wait is ok
    #  await sleep(5)
    #  send_log(res, 9)
    #  if not no_send_tg:
    #    send_log(res, CHAT_ID, 3)
    #
    #  if not no_send_xmpp:
    #    send_log(res, log_group_private, 2)

  if no_send:
    return res
  return


# https://www.utf8-chartable.de/unicode-utf8-table.pl
chr_list = ["\u200b"]

chr_list.append("\u180e")
chr_list.append("\ufeff")

# chr_list.append("\u200b") # added
chr_list.append("\u200c")
# chr_list.append("\u200d") # need test
# chr_list.append("\u200e") # fuck telegram
#chr_list.append("\u200f") # not good

chr_list.append("\u2060")
chr_list.append("\u2061")
chr_list.append("\u2062")
chr_list.append("\u2063")
chr_list.append("\u2064")
#    chr_list.append("\u2065")
chr_list.append("\u2066")
#chr_list.append("\u2067") # not good
chr_list.append("\u2068")
chr_list.append("\u2069")

#chr_list.append("\u206a") # not good

chr_list.append("\u206b")

chr_list.append("\u206c")
chr_list.append("\u206d")
chr_list.append("\u206e")
chr_list.append("\u206f")

num_jz = len(chr_list)



def ennum(k):
    # convert num to zero width spaces

    if type(k) != int:
        return None
    s = chr_list[k%num_jz]
    k = k//num_jz
    if k > 0:
        s = ennum(k)+s
    return s

def denum(s):
    # convert zero width spaces to num
    if not s:
        return None
    s = s.replace('"', '')
    try:
        kk = chr_list.index(s[-1])
        if len(s) > 1:
            k = denum(s[:-1])*num_jz+kk
        else:
            k = kk
    except IndexError:
        return None
    except ValueError:
        return None
    return k


def denum_auto(ss):
    s = ""
    n = False
    for i in ss:
        if i in chr_list:
            if n:
                s = i
                n = False
            else:
                s += i
        else:
            if s:
                n = True
    if n == "":
        return None
    return denum(s)

def enstr(s):
    # return ennum(int(s.encode().hex(),16))
    return ennum(byte2num(s.encode()))


def destr(s):
    if not s:
        return None
    try:
        s = s.replace('"', '')
    except AttributeError:
        pass

    try:
        # return bytes().fromhex(hex(denum(s))[2:]).decode()
        # return bytes.fromhex(hex(denum(s))[2:]).decode()
        #  return num2byte(denum(s)).decode()
        return num2byte(denum_auto(s)).decode()
    except TypeError:
        # (<class 'TypeError'>, TypeError("'NoneType' object cannot be interpreted as an integer"), <traceback object at 0xb5793bc8>)
        return None
    except AttributeError:
        # 'NoneType' object has no attribute 'decode'
        return None
    except UnicodeDecodeError as e:
        raise
        info = f"error: {e=}"



#  def num2byte(num):
#      return bytes.fromhex(hex(num)[2:])
#
#  def byte2num(b):
#      return int(b.hex(), 16)


# def int_to_bytes(x: int) -> bytes:
def num2byte(x):
    if type(x) == int:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    else:
        warn("type error")
        return b""
    
# def int_from_bytes(xbytes: bytes) -> int:
def byte2num(b):
    if isinstance(b, bytes):
        return int.from_bytes(b, 'big')
    else:
        warn("type error")
        return -1



# https://stackoverflow.com/a/9807138
def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

  :param data: Base64 data as an ASCII byte string
  :returns: The decoded byte string.

  """
    #  if type(data) == str:
    if isinstance(data, str):
        data = data.encode()
    #  if type(data) != bytes:
    if not isinstance(data, bytes):
        err(f"wtf: {data=}")
        err(f"wtf: {type(data)}")
        return
    data = bytes(data)
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    try:
        return base64.b64decode(data, altchars)
    except binascii.Error as e:
        err(e=e)


def encode_base64(data, altchars=b'+/'):
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data, altchars=altchars).decode().rstrip("=")

_compress_funcs={
    "zstd": zstandard.compress,
    "br": brotli.compress,
    "gzip": gzip.compress,
    "deflate": zlib.compress,
    }

_decompress_funcs={
    "zstd": zstandard.decompress,
    "br": brotli.decompress,
    "gzip": gzip.decompress,
    "deflate": zlib.decompress,
    }

#  @exceptions_handler
#  @cross_thread(need_main=False)
async def compress(data, m="zst"):
  if isinstance(data, str):
    data = data.encode()
  if m in _decompress_funcs:
    #  return _compress_funcs[m](data)
    #  return run_cb_in_thread(_compress_funcs[m], data)
    #  @exceptions_handler
    #  async def f():
    #    return _compress_funcs[m](data)
    #  d = await run_run(f(), False)
    info(f"start to compress: {len(data)} {short(data)}")
    #  fu = run_cb_in_thread(_compress_funcs[m], data)
    #  d = run_cb(_compress_funcs[m], data, need_main=False)
    fu = run_cb2(_compress_funcs[m], data, need_main=False)
    d = await fu
    #  d =  _compress_funcs[m](data)
    #  d = run_cb_in_thread(_compress_funcs[m], data)
    if d:
      info(f"压缩成功: {m} {len(data)} {short(data)} -> {len(d)} {short(d)}")
      return d
    else:
      info(f"压缩失败: {m} {short(data)}")
      return data
  err(f"unknown encoding: {m}")
    #  if m == "zst":
    #      return zstandard.compress(data, level=22)
    #  if m == "br":
    #      return brotli.compress(data)
    #  if m == "gzip":
    #      return gzip.compress(data)
    #  if m == "deflate":
    #      return zlib.compress(data)
#  return zlib.compress(data,level=9)

#  @exceptions_handler
async def decompress(data, m):
  if isinstance(data, str):
    data = data.encode()
  #  return zstandard.decompress(data)
  if m in _decompress_funcs:
    #  return _decompress_funcs[m](data)
    #  return run_cb_in_thread(_compress_funcs[m], data)
    #  @exceptions_handler
    #  async def f():
    #    return _decompress_funcs[m](data)
    #  d = await run_run(f(), False)
    info(f"start to decompress: {len(data)} {short(data)}")
    #  fu = run_cb_in_thread(_decompress_funcs[m], data)
    #  d = run_cb(_decompress_funcs[m], data, need_main=False)
    fu = run_cb2(_decompress_funcs[m], data, need_main=False)
    d = await fu
    #  d =  _decompress_funcs[m](data)
    if d:
      info(f"解压成功: {m} {short(data)} -> {short(d)}")
      return d
    else:
      info(f"解压失败: {m} {short(data)}")
  else:
    err(f"unknown encoding: {m}")
  return data



def raise_error(error: str):
    error = "-" * 24 + f"\nerror:\n" + "-" * 24 + f"\n{error}" + "-" * 24
    #            logger.exception(info)
    logger.critical("\n" + error)
    raise SystemExit(error)

#  def get_sh_path(path='SH_PATH'):
def read_file_1line(path='SH_PATH'):
  # f = open(os.getcwd() + "/SH_PATH")
  # p = Path(__package__).absolute()
  # p = p.parent
  # f = p / "SH_PATH"
  #  p = "/".join(__file__.split("/")[:-2])
  #  p = "/".join(__file__.split("/")[:-3])
  #  #  f = p + "/SH_PATH"
  #  f = p + "/" + path
  if path[0:1] != '/':
    path = PARENT_DIR / path
    path = path.as_posix()

  with open(path) as f:
      line = f.readline()
      line = line.rstrip('\n')
  if line:
      return line
  else:
    raise_error("E: can't find file: SH_PATH")
    return None


async def read_file(path='SH_PATH', *args, **kwargs):
  if path[0:1] != '/':
    path = PARENT_DIR / path
    path = path.as_posix()
  if not os.path.exists(path):
    warn(f"文件不存在: {path}")
    return
  async with aiofiles.open(path, *args, **kwargs) as file:
      return await file.read()

async def write_file(text, path='config.json', *args, **kwargs):
  if path[0:1] != '/':
    path = PARENT_DIR / path
    path = path.as_posix()
  async with aiofiles.open(path, *args, **kwargs) as file:
      return await file.write(text)

async def split_long_text(text, msg_max_length=MAX_MSG_BYTES_TG, tmp_msg=False):
  max_list = 5
  texts = []
  if len(text.encode()) > msg_max_length:
    def _():
      ls = text.splitlines()
      tmp = None
      for l in ls:
        if tmp is not None:
          if len((tmp+l).encode()) > msg_max_length:
            texts.append(tmp)
            if len(texts) > max_list:
              return
            print(f"texts1: {len(texts)} {len(tmp)}")
          else:
            tmp += '\n'+l
            continue
        while len(l.encode()) > msg_max_length:
          tmp = l[:msg_max_length]
          while len(tmp.encode()) > msg_max_length:
            tmp = tmp[:-int( (len(tmp.encode())-msg_max_length)/2 + 1 )]
          texts.append(tmp)
          if len(texts) > max_list:
            return
          print(f"texts2: {len(texts)} {len(tmp)}")
          l = l[len(tmp):]
        tmp = l
      if tmp:
        texts.append(tmp)
    _()
  else:
    texts = [text]
  if len(texts) > max_list:
    info(f"文本过长，使用pb: {short(text)}")
    url =await pastebin(text)
    return ["文本过长，请打开链接查看: {}\n{}".format(url, short(text))]
  if len(texts) > 1:
    if tmp_msg:
      return [short(text, 500)]
  return texts

async def my_split(path, is_str=False):
  if is_str:
    text = path
  else:
    if os.path.exists(path):
      text = await read_file(path)
      info(f"{path}: {short(text)}...")
    else:
      warn(f"文件不存在: {path}")
      return []

  if text:
    pass
  else:
    warn(f"error text: {text=} {path=} {is_str=}")
    return []
  if text[-1] == '\n':
    text = text[:-1]
  if not text:
    warn(f"empty file: {path}")
    return []

  l = text.splitlines()
  tmp = []
  for i in l:
    if i:
      if i.strip(' ').strip('\t'):
        tmp.append(i.lstrip(' ').lstrip('\t'))
  l = tmp

  tmp = []
  for i in l:
    if i.startswith("#"):
      tmp.append(i)
    elif i.startswith("/* "):
      tmp.append(i)
    elif i.startswith("// "):
      tmp.append(i)
  for i in tmp:
    l.remove(i)
  return l


#async def ipfs_add(data, filename=None, url="https://ipfs.infura.io:5001/api/v0/add?cid-version=1", *args, **kwargs):
async def ipfs_add(data, filename=None, url="https://ipfs.pixura.io/api/v0/add", *args, **kwargs):
#  res = data2url(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
  if isinstance(data, str):
    data = data.encode()
  data = {"file": data}
  res = await http(url=url, method="POST", data=data, **kwargs)
  if not res:
    err("E: fail to ipfs")
    return

  url = res.strip()
  info(res)
#  url = json.loads(url)
  try:
    url = load_str(url)
  except SyntaxError as e:
    res = f"{e=}\n\n{url}"
    print(res)
    return
#  url = url["Hash"]
  #  url = "https://{}.ipfs.infura-ipfs.io/".format(url["Hash"])
  url = "https://ipfs.pixura.io/ipfs/{}".format(url["Hash"])
  if filename:
  #  url += "?filename={}".format(parse.urlencode(filename))
    url += "?filename={}".format(urllib.parse.quote(filename))
#  await session.close()
  return url

def file_for_post(data, filename=None, fieldname="c", mimetype=None, **kwargs):
#  file = aiohttp.FormData()
  file = FormData(kwargs)
  if not mimetype:
    #  mimetype = 'text/plain'
    #  mimetype = 'application/octet-stream'
    if filename:
      if isinstance(filename, str) and filename == "-":
          mimetype = 'text/plain'
      else:
        mimetype = mimetypes.guess_type(filename)[0]
  if not mimetype:
    mimetype = 'application/octet-stream'
#  for i in kwargs:
#    file.add_fields((i, kwargs[i]))
  file.add_field(fieldname, data, filename=filename, content_type=mimetype)
  return file


async def pb_0x0(data, filename=None, *args, **kwargs):
  url = "https://0x0.st/"
  if isinstance(data, str):
    data = data.encode()
    if not filename:
      filename = "0.txt"
  return await pastebin(data, url=url, filename=filename, fieldname="file", *args, **kwargs)


async def itzmx(data, filename=None, *args, **kwargs):
  # https://send.itzmx.com/?info
  # 7z, exe, gif, jpg, png, rar, torrent, zip
  allowed = ("7z", "exe", "gif", "jpg", "png","rar","torrent","zip")
  url = "https://send.itzmx.com/api.php?d=upload-tool"
  if isinstance(data, str):
    data = data.encode()
    #  if not filename:
    #    filename = "0.txt"
    #  data = compress(data, "zst")
    #  if not filename:
    #    filename = "bin_zst.zip"
    if not filename:
      filename = "txt_not_zip.zip"
  extra = {}
  if filename and filename.split(".")[-1] not in allowed:
    #  extra = { "randomname": "on" }
    filename += "_not_zip.zip"
  fieldname = "file"
  res = await pastebin(data, url=url, filename=filename, fieldname=fieldname, extra=extra, *args, **kwargs)
  return res

async def transfer1(data, filename=None, *args, **kwargs):
  url = "https://transfer.sh"
  if isinstance(data, str):
    data = data.encode()
    if not filename:
      filename = "0.txt"
  if filename:
    url = "https://transfer.sh/"+filename
  headers = {}
  headers['Max-Days'] = str(64)
  headers['Max-Downloads'] = str(64)
  res = await http(url=url, method="PUT", data=data, headers=headers,  **kwargs)
  return res

async def transfer(data, filename=None, *args, **kwargs):
  url = "https://transfer.sh"
  if isinstance(data, str):
    data = data.encode()
    if not filename:
      filename = "0.txt"
  if not filename:
    filename = "file"
  return await pastebin(data, url=url, fieldname=filename, *args, **kwargs)

async def file_io(data, filename=None, *args, **kwargs):
  url = "https://file.io"
  if isinstance(data, str):
    data = data.encode()
    if not filename:
      filename = "0.txt"
  res = await pastebin(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
#  return load_str(res)["link"]
  try:
    d = load_str(res, no_ast=True)
  except SyntaxError as e:
    info = f"{e=}\n\n{url}"
    print(info)
    return
  return d["link"]


async def catbox(data, filename=None, tmp=False, *args, **kwargs):
  # https://catbox.moe/tools.php
  # https://litterbox.catbox.moe/tools.php
  if tmp:
    url = "https://litterbox.catbox.moe/resources/internals/api.php"
  else:
    url = "https://catbox.moe/user/api.php"
  reqtype = "fileupload"
  fieldname = "fileToUpload"
  if isinstance(data, str):
    if not tmp and url_only_re.match(data):
      # litterbox disallow upload via url
      reqtype = "urlupload"
      fieldname = "url"
    else:
      data = data.encode()
      if not filename:
        filename = "0.txt"
  extra = {
#      "userhash": "",
      "reqtype": reqtype
      }
  if tmp:
    extra["time"] = "72h"
  res = await pastebin(data, url=url, filename=filename, fieldname=fieldname, extra=extra, *args, **kwargs)
  if res:
    if "https://files.catbox.moe/" in res:
      res = res.replace("https://files.catbox.moe/", "https://de.catbox.moe/")
    return res

def tmp_save(data, ex=""):
  #  from ..config import SH_PATH
  name = "{}/{}{}".format(SH_PATH, time.time(), ex)
  if not isinstance(data, bytes):
    err("need bytes")
    return
  data = bytes(data)
  with open(name, "wb") as file:
    file.write(data)
  return name

@exceptions_handler
def load_str(msg, no_ast=False):
  """str to dict"""
  msg = msg.strip()
  if no_ast:
    import json
    return json.loads(msg)
  try:
    return ast.literal_eval(msg)
  except (ValueError, SyntaxError) as e:
    warn(f"faild: {e=} {msg=}")
    import json
    try:
      return json.loads(msg)
    except Exception as e:
      err(f"failed2: {msg=}")
      #  raise e
      return {}



def format_byte(num):
  if not isinstance(num, (int, float)):
    num = int(num)
  if num < 0:
    s = "-"
    num = -1*num
  else:
    s = ""
  if num < 1000:
    u = "B"
    num = f"{num:.3g}"
  #  elif num < 1024*1024:
  elif num < 1024*1000:
    u = "KB"
    num = f"{num/1024:.3g}"
  elif num < 1024**2*1000:
    u = "MB"
    num = f"{num/1024/1024:.3g}"
  else:
    u = "GB"
    num = f"{num/1024/1024/1024:.3g}"
  return s+num+u





#  async def update_stdouterr(data):
#    while data[2].poll() == None:
#      try:
#        data[0], data[1] = data[2].communicate(timeout=2)
#      except subprocess.TimeoutExpired as e:
#        if e.stdout:
#          data[0] = e.stdout.decode("utf-8")
#        if e.stderr:
#          data[1] = e.stderr.decode("utf-8")
#      await sleep(1)
#
#
#  async def update_stdout(data):
#    while True:
#      print(1)
#      await sleep(3)
#      tmp = await data[2].stdout.readline()
#      if tmp:
#        data[0] = data[0] + tmp.decode("utf-8")
#      else:
#        break
#    info(11)
#
#
#  async def update_stderr(data):
#    while True:
#      print(2)
#      await sleep(2.5)
#      tmp = await data[2].stderr.readline()
#      if tmp:
#        data[1] = data[1] + tmp.decode("utf-8")
#      else:
#        break
#    info(22)
#
#
#  async def my_popen(cmd,
#             shell=True,
#             max_time=60,
#             client=None,
#             src=None,
#             combine=True,
#             return_msg=False,
#             executable='/bin/bash',
#             **args):
#
#    async with bash_lock:
#      #  info(cmd)
#      #    args=shlex.split(message.text.split(' ',1)[1])
#
#      #    p=subprocess.Popen(message.text.split(' '))
#      #    p=subprocess.Popen(message.text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
#      #    p=subprocess.Popen(shlex.split(message.text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)
#
#      #    p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
#      #    p=Popen(args,text=True,universal_newlines=True,bufsize=1,stdout=PIPE, stderr=PIPE)
#      #    p=Popen(args,text=True,stdout=PIPE, stderr=PIPE)
#      #    p=await asyncio.create_subprocess_shell(message.text.split(' ',1)[1],stdout=PIPE, stderr=PIPE)#limit=None
#      #    p=Popen(args,stdout=PIPE, stderr=PIPE,bufsize=8000000)
#      #    p=Popen(args,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
#      #  p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
#      p = Popen(cmd,
#            shell=shell,
#            stdout=PIPE,
#            stderr=PIPE,
#            text=True,
#            encoding="utf-8",
#            errors="ignore",
#            executable=executable)
#
#      start_time = time.time()
#      res = ""
#      errs = ""
#      data = ["", "", p]
#      asyncio.create_task(update_stdouterr(data))
#      await sleep(1)
#      info(f"popen cmd: {p.args}")
#      if type(cmd) == list:
#        if len(cmd) == 6 and "bcmd.sh" in cmd[1]:
#          cmd_str = cmd[4]
#        else:
#          cmd_str = " ".join(cmd)
#      else:
#        cmd_str = cmd
#      if len(str(cmd_str)) > 512:
#        cmd_str = "%s..." % cmd_str[:512]
#      tmp_last = None
#      while True:
#        #  if p.poll() == None and p.returncode == None:
#        if p.poll() == None:
#          pass
#        else:
#          break
#        #  await sleep(0.5)
#        res = data[0]
#        errs = data[1]
#
#        #  if msg:
#        #    if tmp != msg.text:
#        if src:
#          if res:
#            if len(res) > 512:
#              res = "%s..." % res[:512]
#          else:
#            res = '...'
#          #  tmp = "...\n" + res + "\n==\nE: \n" + errs
#          tmp = "正在执行(%ss): %s\n%s\nE: ?\n%s" % (int(time.time()-start_time), cmd_str, res, errs)
#          tmp = tmp.strip()
#          if tmp != tmp_last:
#            try:
#              tmp = re.sub(shell_color_re,  "", tmp)
#              info(f"临时输出: {tmp}")
#              #  msg = await cmd_answer(tmp, client, msg, **args)
#              #  info(f"临时输出: {tmp}")
#              send(tmp, src, xmpp_only=True, correct=True)
#              tmp_last = tmp
#            except Exception as e:
#              #  err(f"can not send tmp: {e=}")
#              #  msg = await client.send_message(MY_ID, tmp)
#              warn(f"无法发送临时输出: {tmp} {e=}")
#        await sleep(interval)
#        if time.time() - start_time > max_time:
#          p.kill()
#          res = "my_popen: timeout, killed, cmd: {}\nres: {}".format(cmd, res)
#          warn(res)
#          if src:
#            send(f"E: killed(timeout): {cmd_str}", src)
#          #  await cmd_answer(res, client, msg)
#          #  info(f"最终输出: {res}")
#          break
#
#      try:
#        res, errs = p.communicate(timeout=3)
#      except subprocess.TimeoutExpired as e:
#        err("timeout")
#        res = e.stdout
#        if res:
#          res = res.decode("utf-8")
#        errs = e.stderr
#        if errs:
#          errs = errs.decode("utf-8")
#
#      info(f"popen exit: {p.returncode} {res=} {errs=}")
#      if res:
#        res = res.strip()
#      if errs:
#        errs = errs.strip()
#      #  if res:
#      #    if isinstance(res, bytes):
#      #      res = res.decode("utf-8")
#      #  if errs:
#      #    if isinstance(errs, bytes):
#      #      errs = errs.decode("utf-8")
#      #  if not res:
#      #    return False
#
#      #  if msg:
#      #    #  msg = await cmd_answer(res, client, msg, **args)
#      #    info(f"发送: {res}")
#      #    if return_msg:
#      #      return msg
#      if combine:
#        if errs:
#          res = "%s\n\nE: %s\n%s" % (res, p.returncode, errs)
#        elif p.returncode:
#          res = "%s\n\nE: %s" % (res, p.returncode)
#        if res:
#          if len(res) > MAX_MSG_BYTES:
#            res = await pastebin(res)
#          return res
#        else:
#          return
#          return "None"
#      else:
#        return p.returncode, res, errs



#  async def _init_myshell():
#    #  if "myshell_p" not in globals():
#    info("start my shell...")
#    global myshell_p, myshell_lock
#    myshell_lock = asyncio.Lock()
#    #  myshell_p = await asyncio.create_subprocess_shell("bash", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, preexec_fn=os.setpgrp)
#    myshell_p = await asyncio.create_subprocess_shell("bash", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
#    #  info("close stdin...")
#    #  myshell_p.stdin.close()
#    #  await myshell_p.stdin.wait_closed()
#    #  info("close stdin ok")
#    #  loop.add_signal_handler(signal.SIGINT, lambda: myshell_p.terminate())
#    info("wait for steam ok...")
#    t1 = asyncio.create_task(myshell_p.stdout.read())
#    t2 = asyncio.create_task(myshell_p.stderr.read())
#    try:
#      await sleep(2)
#      if t1.done() or t2.done():
#        info(f"fixme: 管道无法保持开启")
#        if myshell_p.returncode is None:
#          await stop_sub(myshell_p)
#        return False
#    finally:
#      if not t1.done():
#        t1.cancel()
#      if not t2.done():
#        t2.cancel()
#    return True
#
#
#    if myshell_p.returncode is None:
#      info("use old shell...")
#    else:
#      info(f"fixme: shell is closed")
#      return False
#    return True
#


#  async def myshell(cmd, max_time=run_shell_time_max, src=None):
#    if await init_myshell():
#      pass
#    else:
#      return
#    p = myshell_p
#    if myshell_lock.locked():
#      warn(f"myshell is busy: {cmd=}")
#      if src:
#        send("前一次任务还没结束", src, correct=True)
#    async with myshell_lock:
#      #  info("send \\n...")
#      #  p.stdin.write(b"\n")
#      #  await p.stdin.drain()
#      #  info("wait for steam ok...")
#      #  t1 = asyncio.create_task(p.stdout.read())
#      #  t2 = asyncio.create_task(p.stderr.read())
#      #  try:
#      #    await sleep(0.3)
#      #    start_time = time.time()
#      #    if t1.done() or t2.done():
#      #      #  err(f"管道关闭，无法接受返回数据，终止执行 {cmd}")
#      #      #  return
#      #      warn(f"管道关闭，无法接受返回数据 now: {cmd}")
#      #      if p.returncode is None:
#      #        await stop_sub(p)
#      #        info("start another shell...")
#      #        if await init_myshell():
#      #          pass
#      #        else:
#      #          return
#      #        p = myshell_p
#      #  finally:
#      #    if not t1.done():
#      #      t1.cancel()
#      #    if not t2.done():
#      #      t2.cancel()
#      #  await sleep(0.1)
#
#
#      #  o = b""
#      #  e = b""
#      #  t1 = asyncio.create_task(p.stdout.readline())
#      #  t2 = asyncio.create_task(p.stderr.readline())
#      def f1():
#        return asyncio.create_task(p.stdout.readline())
#      def f2():
#        return asyncio.create_task(p.stderr.readline())
#      t1 = f1()
#      t2 = f2()
#      ts = [t1, t2]
#
#      async def pr(d, tmp):
#        d = d.decode("utf-8", errors="ignore")
#        info(f"got: {d=}")
#        d = re.sub(shell_color_re,  "", d)
#        info(f"got re: {d=}")
#        ds = d.strip()
#        if ds:
#          if tmp:
#            ds = tmp + "\n" + d
#            tmp = ""
#            ds = d.strip()
#          send(ds, src)
#        else:
#          tmp += d
#        return tmp
#
#      #  cmd = list( x.encode()+b" " for x in cmd )
#      info(f"send cmd: {cmd}")
#      start_time=time.time()
#      tmp = ""
#      l = len(cmd)
#      try:
#        #  p.stdin.writelines( cmd )
#        for c in cmd:
#          p.stdin.write( c.encode() )
#          info("send ok")
#          await p.stdin.drain()
#          info("wait res...")
#
#
#          while True:
#            #  try:
#              #  for _ in asyncio.as_completed([t1, t2]):
#              #    break
#            done, pending = await asyncio.wait(ts, timeout=interval/l, return_when=asyncio.FIRST_COMPLETED)
#            #  except TimeoutError as e:
#            if t2.done():
#              d = await t2
#              try:
#                while True:
#                  d += await asyncio.wait_for(p.stderr.readline(), timeout=0.6)
#              except TimeoutError as e:
#                info("stderr end")
#              info(f"got stderr: {d}")
#              tmp = await pr(d, tmp)
#              #  d = d.decode("utf-8", errors="ignore")
#              #  d = re.sub(shell_color_re,  "", d)
#              #  send(d, src)
#              #  e += await t2
#              t2 = f2()
#              ts[1] = t2
#            if t1.done():
#              d = await t1
#              try:
#                while True:
#                  d += await asyncio.wait_for(p.stdout.readline(), timeout=0.6)
#              except TimeoutError as e:
#                info("stdout end")
#                pass
#              info(f"got stdout: {d}")
#              tmp = await pr(d, tmp)
#              #  o += await t1
#              t1 = f1()
#              ts[0] = t1
#            l -= 1
#            if len(done) == 0:
#              break
#            else:
#              info("got a line of res")
#            if time.time() - start_time > max_time:
#              send("结束。", src)
#              return
#      finally:
#        if not ts[0].done():
#          ts[0].cancel()
#        if not ts[1].done():
#          ts[1].cancel()
#        #  info("close stdin...")
#        #  myshell_p.stdin.close()
#        #  await myshell_p.stdin.wait_closed()
#        #  info("close stdin ok")
#      send("结束", src)

#  async def init_myshell():
#    return await run_run(_init_myshell(), False)
#    #  asyncio.create_task( run_run(_init_myshell(), False) )
#    #  await sleep(1)
#    #  if myshell_p.returncode is None:
#    #    return True

#  @cross_thread(need_main=False)
async def init_myshell():
  #  if "myshell_p" not in globals():
  info("start my shell...")
  global myshell_p, myshell_lock
  myshell_lock = asyncio.Lock()
  #  myshell_p = await asyncio.create_subprocess_shell("bash", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, preexec_fn=os.setpgrp)
  #  myshell_p = await asyncio.create_subprocess_shell("bash -i", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  myshell_p = await asyncio.create_subprocess_shell("bash", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  #  myshell_p = await asyncio.create_subprocess_shell("bash", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, limit=64000000)
  #  p = myshell_p
  #  def wrap_read(func):
  #    @wraps(func)
  #    async def wrapper(*args, **kwargs):
  #      d = await func(*args, **kwargs)
  #      print(len(d), d)
  #      await myshell_queue.put(d)
  #      #  asyncio.create_task( queue.put(d) )
  #      return d
  #    return wrapper
  #  p.stdout.readline = wrap_readline( p.stdout.readline)
  #  p.stderr.readline = wrap_readline( p.stderr.readline)
  #  myshell_queue = asyncio.Queue()
  #  async def pr(f, n=1):
  #    await sleep(1)
  #    #  if t1.done() or t2.done() or p.returncode is not None:
  #    if p.returncode is not None:
  #      warn(f"fixme: 管道无法保持开启")
  #      if myshell_p.returncode is None:
  #        await stop_sub(myshell_p)
  #      return
  #    info(f"myshell is ok, task of reading is running {f}")
  #    #  while True:
  #    while myshell_p.returncode is None:
  #      d = await f()
  #      await myshell_queue.put((n, d))
  #    warn(f"myshell is killed, returncode: {myshell_p.returncode}")
  #
  #  #  myshell_p.stdin.close()
  #  #  await myshell_p.stdin.wait_closed()
  #  #  info("close stdin ok")
  #  #  loop.add_signal_handler(signal.SIGINT, lambda: myshell_p.terminate())
  #  #  info("wait for steam ok...")
  #  #  t1 = asyncio.create_task(myshell_p.stdout.readline())
  #  #  t2 = asyncio.create_task(myshell_p.stderr.readline())
  #  t1 = asyncio.create_task(pr(p.stdout.readline, 1))
  #  t2 = asyncio.create_task(pr(p.stderr.readline, 2))
  #  myshell_queue1 = asyncio.Queue()
  data = deque()
  data_ok = asyncio.Event()

  async def pr(f, n=1):
    await sleep(1)
    #  if t1.done() or t2.done() or p.returncode is not None:
    if myshell_p.returncode is not None:
      warn(f"fixme: 管道无法保持开启")
      if myshell_p.returncode is None:
        await stop_sub(myshell_p)
      return
    info(f"myshell is ok, task of reading is running {f}")
    #  while True:
    while myshell_p.returncode is None:
      d = await f(HTTP_FILE_MAX_BYTES)
      data.append((n, d))
      data_ok.set()
      #  await myshell_queue1.put((n, d))
      #  print(f"put: {n} {len(d)} {short(d)}")
    warn(f"myshell is killed, returncode: {myshell_p.returncode}")
  
  global myshell_queue
  myshell_queue = asyncio.Queue()
  #  @cross_thread
  async def prr():
    tmp1 = b""
    tmp2 = b""
    tmp = b""
    o = None
    while myshell_p.returncode is None:
      #  n,d = await myshell_queue1.get()
      if len(data) == 0:
        await data_ok.wait()
        data_ok.clear()
      n,d = data.popleft()

      if n == 1:
        tmp = tmp1
      else:
        tmp = tmp2

      #  ds = []
      if d[-1:] == b"\n": # 不能用d[-1]: int
        if d == b"\n" or d[-2:-1] == b"\n":
          d = tmp + d
        else:
          ds = d.rsplit(b"\n", 2)
          #  info(f"{ds=}")
          if len(ds) > 2:
            o = ds[-2] + b"\n"
          d = tmp + ds[0] + b"\n"
        tmp = b""
      else:
        ds = d.rsplit(b"\n", 1)
        #  info(f"{ds=}")
        if len(ds) == 1:
          tmp += ds[0]
          d = None
        else:
          d = tmp + ds[0] + b"\n"
          tmp = ds[-1]

      #  info(f"{d=} {o=}")
      if d is not None:
        await myshell_queue.put((n, d))
        d = None
        if o is not None:
        #  if len(ds) > 2:
          await myshell_queue.put((n, o))
          o = None

      if n == 1:
        tmp1 = tmp
      else:
        tmp2 = tmp


      #  while b"\n" in d:
      #  if d[-1] == b"":
      #    d = d[0].rsplit(b"\n", 1)
      #  o = d[1]
      #  d = d[0]
      #    if n == 1:
      #      tmp1 += d + b"\n"
      #      #  info(f"send data {tmp1}")
      #      await myshell_queue.put((n, tmp1))
      #      tmp1 = b""
      #    else:
      #      tmp2 += d + b"\n"
      #      #  info(f"send data {tmp2}")
      #      await myshell_queue.put((n, tmp2))
      #      tmp2 = b""
      #  d = o
      #  if n == 1:
      #    tmp1 += d
      #  else:
      #    tmp2 += d
    warn(f"myshell is killed, returncode: {myshell_p.returncode}")
  asyncio.create_task(prr())

  #  myshell_p.stdin.close()
  #  await myshell_p.stdin.wait_closed()
  #  info("close stdin ok")
  #  loop.add_signal_handler(signal.SIGINT, lambda: myshell_p.terminate())
  #  info("wait for steam ok...")
  #  t1 = asyncio.create_task(myshell_p.stdout.readline())
  #  t2 = asyncio.create_task(myshell_p.stderr.readline())
  asyncio.create_task(pr(myshell_p.stdout.read, 1))
  asyncio.create_task(pr(myshell_p.stderr.read, 2))


  cmds = "source ~/.bash_profile"
  res = await myshell(cmds)
  info(f"init bash: {res}")

  cmds = "type dddd; type cv"
  res = await myshell(cmds)
  info(f"check: {res}")
  #  info("clean...")
  #  await sleep(1)
  #  while not myshell_queue.empty():
  #    info(await myshell_queue.get())
  #  info("clean ok")
  #  try:
    # 据说会死锁，有问题就换成 while True
    #  r = await myshell_p.wait()
    #  warn(f"myshell is killed, returncode: {r}")
  #  finally:
  #    if not t1.done():
  #      t1.cancel()
  #    if not t2.done():
  #      t2.cancel()
  return True

#  @exceptions_handler
#  async def myshell(*args,  **kwargs):
#    return await run_run(_myshell(*args,  **kwargs) , False)


SHELL_CMD_LINE_MAX = 1024
#  async def myshell(cmd, max_time=interval, src=None):
#  @cross_thread(need_main=False)
@cross_thread
@exceptions_handler
async def myshell(cmds, max_time=run_shell_time_max, src=None):
  # 有个问题，不知道何时运行结束，目前想到两种方案：bash -i和最后发送echo end然后等出现end提示。
  #  if await init_myshell():
  #    pass
  #  else:
  #    return
  p = myshell_p
    #  o = b""
    #  e = b""
    #  t1 = asyncio.create_task(p.stdout.readline())
    #  t2 = asyncio.create_task(p.stderr.readline())
    #  def f1():
    #    return asyncio.create_task(p.stdout.readline())
    #  def f2():
    #    return asyncio.create_task(p.stderr.readline())
    #  t1 = f1()
    #  t2 = f2()
    #  ts = [t1, t2]
          #  try:
          #    async with asyncio.timeout() as cm2:
          #      while True:
          #        n, d = await myshell_queue.get()
          #        if cm2.when() is None:
          #          cm2.reschedule(asyncio.get_running_loop().time()+0.1)
          #        else:
          #          cm2.reschedule(asyncio.get_running_loop().time()+0.01)
                #  if cm2.when() is None:
                #  if tmp is None:
          #        tmp += d
          #        info(f"got{n}: {d[:16]}")
          #  except TimeoutError:
          #    pass

  #  try:
  #    async with asyncio.timeout(interval) as cm:
  if isinstance(cmds, str):
    info(f"收到字符串命令: {cmds}")
    #  cmds = get_cmd(cmds)
  else:
    #  cmds = list(shlex.quote(x) for x in cmds)
    #  cmds = ' '.join(cmds)
    info("original cmds: {!r}".format(cmds))
    cmds = shlex.join(cmds)
  cmds = cmds.splitlines()
  tmp = []
  for l in cmds:
    while len(l) > SHELL_CMD_LINE_MAX:
      tmp.append(l[:SHELL_CMD_LINE_MAX]+"\\")
      l = l[SHELL_CMD_LINE_MAX:]
    tmp.append(l)
  cmds = tmp
  info("run shell cmds: {!r}".format(cmds))

  cmds = list(f"{x}\n" for x in cmds)
  cmds.append("echo $?\n")
  eof = generand(16) + "\n"
  #  cmd.append(f"echo EOF\n")
  cmds.append(f"echo "+eof)

  eof = eof.encode()
  k =  len(cmds)
  #  tmp = ""
  tmp = b""
  res = ""
  o = b""
  e = b""
  r = None
  ds = None
  d = None

  if myshell_lock.locked():
    if src == CHAT_ID:
      warn(f"shell is busy: {cmds=}")
    else:
      send("前一次任务还没结束", src, tmp_msg=True)
  async with myshell_lock:

    if not myshell_queue.empty():
      warn("clean shell")
      #  await sleep(1)
      while not myshell_queue.empty():
        info("drop: %s" % str(await myshell_queue.get()) )
      info("clean ok")



    p.stdin.write( cmds[-1].encode() )
    await p.stdin.drain()
    info(f"send eof: check: shell is ok: {eof}")
    try:
      async with asyncio.timeout(run_shell_time_max) as cm:
        while True:
          #  n, d = await asyncio.wait_for( myshell_queue.get(), timeout=run_shell_time_max )
          n, d = await myshell_queue.get()
          if n == 1 and d == eof:
            info(f"shell is ok, got: {eof}")
            break
          warn("drop: %s: %s" % (n, d) )
          cm.reschedule(min(cm.when()+max_time/3, loop.time()+run_shell_time_max))
    except TimeoutError:
      warn("shell is busy")
      return -512, None, None

    start_time = time.time()
    last_send = start_time
    for c in cmds:
      p.stdin.write( c.encode() )
      info(f"send {k}: {short(c)}")
      k -= 1
      while r is None:
        #  if time.time() - start_time > run_shell_time_max*10:
        #  if time.time() - start_time > max_time:
        #    res = "end"
        #    send(res, src)
        #    r = 0
        #    break
        if k > 1:
          if myshell_queue.empty():
            await p.stdin.drain()
            await sleep(0.001)
            info("wait for more")
            if myshell_queue.empty():
              await sleep(0.01)
              info("wait for more 2")
              if myshell_queue.empty():
                await sleep(0.5)
                info("wait for more 3")
                if myshell_queue.empty():
                  info("wait for more fail")
                #  if k > 0:
                  break
        #  n, d = await myshell_queue.get()
        try:
          #  n, d = await asyncio.wait_for( myshell_queue.get(), timeout=interval/(k+1))
          #  n, d = await asyncio.wait_for( myshell_queue.get(), timeout=max_time/(k+1))
          #  n, d = await asyncio.wait_for( myshell_queue.get(), timeout=max(0.3, min(start_time - time.time() + max_time, max_time)))
          timeout = time.time()-start_time
          if timeout + 1 < max_time:
            timeout = max_time - timeout
          else:
            timeout = max_time/timeout/10 
          info(f"waiting({timeout}s)...")
          n, d = await asyncio.wait_for( myshell_queue.get(), timeout=timeout )
          if n == 1:
            if k == 0:
              #  if d == b'EOF\n':
              if d == eof:
                info(f"found EOF")
                r = True
                break
            #  elif k == 1:
            #    if d == b'0\n':
            #      info(f"found returncode")
            o += d
          else:
            e += d
          tmp += d 
          info(f"got{n}: {d}")
        except TimeoutError:
          if k > 0:
            info(f"fixme: timeout, skip: {c}")
            await p.stdin.drain()
            break
          #  if k > 0:
          #    await sleep(0.001)
          #    await p.stdin.drain()
          #    info(f"fixme: timeout: {c=} {cmd}")
          #    break
          warn(f"timeout: {cmds}")
          res = "shell: 结束等待"
          send(res, src)
          # fixme: 不知道该设为多少
          r = -512
          break
        #  if k > 1:
        #    if myshell_queue.empty():
        #      await sleep(0.001)
        #  info(time.time())
        # 0.0006s
        #  while not myshell_queue.empty():
        #    n, d = await myshell_queue.get()
            #  await sleep(0.001)
        try:
          while True:
            #  if len(tmp) > MAX_MSG_BYTES_TG:
            #    warn(f"res is too loog: {len(tmp)} {tmp[:54]}")
            #    break
            #  n, d = await asyncio.wait_for( myshell_queue.get(), timeout=0.001)
            #  n, d = await asyncio.wait_for( myshell_queue.get(), timeout=0.01)
            n, d = await asyncio.wait_for( myshell_queue.get(), timeout=0.1)
            if n == 1:
              if k == 0:
                if d == eof:
                  print(f"found EOF?")
                  #  o = o[:-(len(eof))]
                  #  tmp = tmp[:-(len(eof))]
                  r = True
                  break
              #  elif k == 1:
              #    if d == b'0\n':
              #      print(f"found returncode?")
              #      #  r = int(d[:-1])
              #      #  break
              o += d
            else:
              e += d
            tmp += d 
            print(f"got{n}: {d}")
            if len(tmp) > MAX_MSG_BYTES_TG * 10:
              info(f"too long: {short(tmp)}")
              break
          if d == eof:
            break
          info(f"附带消息: {d}")
        except TimeoutError:
          info(f"no more")
          # 至少还有一条待执行的命令
        #  if r is not None:
        #    info(f"break: {r=}")
        #    break
        #  if k > 2:
        if k == 1:
          if d == b"0\n":
            info(f"skip sending of returncode 0")
            break
        else:
          if k > 1:
            #  if len(tmp) < 512:
            if len(tmp) < MAX_MSG_BYTES_TG:
              if time.time() - last_send < 1:
                info(f"等一下，合并后续消息")
                #  if not e:
                break
          if src is not None and len(tmp) > 0:
            ds = tmp.decode("utf-8", errors="ignore")
            #  info(f"got{n}: {ds[:16]}")
            ds = re.sub(shell_color_re,  "", ds)
            #  info(f"got{n}>: {ds[:16]}")
            #  res += "\n" + ds
            ds = ds.strip()
            if ds:
              #  info(f"send: {src} {type(ds)} {ds[:16]}")
              #  send(f"```\n{ds}```", src)
              send(ds, src)
              last_send = time.time()
              tmp = b""
        if k > 0:
          #  if k == 1:
          #    info(f"res {n}: {d}")
          await p.stdin.drain()
          if myshell_queue.empty():
            break
        #  if k > 0:
          #  await p.stdin.drain()
          #  if myshell_queue.empty():
          #    await sleep(0.01)
          #    info("wait for more")
          #    if myshell_queue.empty():
          #      break
  #  if o:
  if len(o) > 0:
    o = o.decode("utf-8", errors="ignore")
    o = o.strip()
    if r is True:
      s = o.splitlines()
      r = int(s[-1])
      o = '\n'.join(s[:-1])
  else:
    o = None

  if len(tmp) > 0:
    ds = tmp.decode("utf-8", errors="ignore")
    ds = re.sub(shell_color_re,  "", ds)
    ds = ds.strip()
    #  if ds:
    if len(ds) > 0:
      info(f"{r=}")
      if type(r) is int:
        if r == 0:
          #  if ds.endswith("\n0"):
          ds = ds[:-2]
        elif r == -512:
          pass
        else:
          ds = ds.rsplit("\n", 1)[0] + f"\n\nE: {r}"
      send(ds, src)
  #  if e:
  if len(e) > 0:
    e = e.decode("utf-8", errors="ignore")
    #  e = re.sub(shell_color_re,  "", e)
    e = e.strip()
  else:
    e = None
    
  #  if r is not None:
  #    return  (r, o, e)
  return  (r, o, e)
  return res.strip()


    #  async def pr(f, p=""):
    #    tmp = ""
    #    while True:
    #      d = await f()
    #      await queue.put(d)
    #      d = d.decode("utf-8", errors="ignore")
    #      info(f"got{p}: {d=}")
    #      d = re.sub(shell_color_re,  "", d)
    #      ds = d.strip()
    #      info(f"got re: {d=}")
    #      now = time.time()
    #      if ds and now - ress[0] > 0.3:
    #        ress[0] = now
    #        if tmp:
    #          ds = tmp + "\n" + d
    #          tmp = ""
    #          ds = d.strip()
    #        await send(ds, src)
    #
    #      else:
    #        #  tmp += d
    #        tmp = tmp + d
    #
    #  ress = [time.time()]
    #  #  asyncio.create_task(p.stdout.readline())
    #  t1 = asyncio.create_task(pr(p.stdout.readline, " out"))
    #  t2 = asyncio.create_task(pr(p.stderr.readline, " err"))
    #  try:
    #    info("wait res...")
    #    for c in cmd:
    #      p.stdin.write( c.encode() )
    #      info("send ok")
    #      await p.stdin.drain()
    #      #  done, pending = await asyncio.wait(ts, timeout=interval/l, return_when=asyncio.FIRST_COMPLETED)
    #      l = ress[0]
    #      await sleep(0.5)
    #      if ress[0] == l:
    #        continue
    #    while True:
    #      info("wait for finally res...")
    #      await sleep(interval+1)
    #      if time.time() - ress[0] > interval:
    #        info("timeout")
    #        break
    #      else:
    #        info(f"{time.time()} << {ress[0]} + {interval}")
    #  finally:
    #    if not ts[0].done():
    #      ts[0].cancel()
    #    if not ts[1].done():
    #      ts[1].cancel()
    #  return
    #
    #  #  cmd = list( x.encode()+b" " for x in cmd )
    #  info(f"send cmd: {cmd}")
    #  start_time=time.time()
    #  tmp = ""
    #  l = len(cmd)
    #  try:
    #    #  p.stdin.writelines( cmd )
    #    for c in cmd:
    #      p.stdin.write( c.encode() )
    #      info("send ok")
    #      await p.stdin.drain()
    #      info("wait res...")
    #
    #
    #      while True:
    #        #  try:
    #          #  for _ in asyncio.as_completed([t1, t2]):
    #          #    break
    #        done, pending = await asyncio.wait(ts, timeout=interval/l, return_when=asyncio.FIRST_COMPLETED)
    #        #  except TimeoutError as e:
    #        if t2.done():
    #          d = await t2
    #          try:
    #            while True:
    #              d += await asyncio.wait_for(p.stderr.readline(), timeout=0.6)
    #          except TimeoutError as e:
    #            info("stderr end")
    #          info(f"got stderr: {d}")
    #          tmp = await pr(d, tmp)
    #          #  d = d.decode("utf-8", errors="ignore")
    #          #  d = re.sub(shell_color_re,  "", d)
    #          #  send(d, src)
    #          #  e += await t2
    #          t2 = f2()
    #          ts[1] = t2
    #        if t1.done():
    #          d = await t1
    #          try:
    #            while True:
    #              d += await asyncio.wait_for(p.stdout.readline(), timeout=0.6)
    #          except TimeoutError as e:
    #            info("stdout end")
    #            pass
    #          info(f"got stdout: {d}")
    #          tmp = await pr(d, tmp)
    #          #  o += await t1
    #          t1 = f1()
    #          ts[0] = t1
    #        l -= 1
    #        if len(done) == 0:
    #          break
    #        else:
    #          info("got a line of res")
    #        if time.time() - start_time > max_time:
    #          send("结束。", src)
    #          return
    #  finally:
    #    if not ts[0].done():
    #      ts[0].cancel()
    #    if not ts[1].done():
    #      ts[1].cancel()
    #    #  info("close stdin...")
    #    #  myshell_p.stdin.close()
    #    #  await myshell_p.stdin.wait_closed()
    #    #  info("close stdin ok")
    #  send("结束", src)






async def my_sexec(cmds, max_time=run_shell_time_max, src=None):
  #  p = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  info(f"run shell cmds: {cmds}")
  p = await asyncio.create_subprocess_exec(*cmds, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  return await my_subprocess(p, max_time=max_time, src=src)


async def my_sshell(cmd, max_time=run_shell_time_max, src=None):
  info(f"run shell cmd: {cmd}")
  p = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  #  p = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  return await my_subprocess(p, max_time=max_time, src=src)


def wrap_read(func, src, ress):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    data = await func(*args, **kwargs)
    now = time.time()
    ress[1] += data
    if data:
      if now - ress[0] > interval/2:
        ress[0] = now
        #  if src and ress[1].strip():
        if ress[1].strip():
          send( "执行中，临时输出: \n%s" % ress[1].decode("utf-8", errors="ignore"), src, tmp_msg=True)
        ress[1] = b""
      #  print(f"{len(data)}")
    return data
  return wrapper

async def my_subprocess(p, max_time=run_shell_time_max, src=None):
  start_time = time.time()
  ress = [start_time, b""]
  p.stdout.read = wrap_read( p.stdout.read, src, ress)
  #  ress = [start_time, b""]
  p.stderr.read = wrap_read( p.stderr.read, src, ress)
  #  tmp = await p.communicate()
  t = asyncio.create_task( p.communicate() )
  o = None
  e = None
  while True:
    #  await sleep(interval)
    #  if t.done():
    #    o, e = t.result()
    #    break
    try:
      ts = asyncio.shield(t)
      o, e = await asyncio.wait_for(ts, interval+1)
      info(f"执行结束: {p} {o=} {e=}")
      break
    #  start_timme = loop.time()
    #  async with asyncio.timeout(max_time) as cm:
    #    while True:
    #      tmp = await p.stdout.readline()
    #      if tmp:
    #        o += tmp
    #        cm.reschedule(loop.time()+max_time)
    #      tmp = await p.stderr.readline()
    #      if tmp:
    #        e += tmp
    #        cm.reschedule(loop.time()+max_time)
    #      if p.returncode is None:
    #        pass
    #      else:
    #        break
    except TimeoutError:
      #  warn(f"timeout: {args}")
      info(f"执行中: {p} {o=} {e=}")
    now = time.time()
    if now - ress[0] > interval:
      send( "执行中 %ss" % int(now-start_time), src, tmp_msg=True)
    if now - ress[0] < max_time and now - start_time < max_time*10:
      pass
    elif p.returncode is None:
      warn(f"执行超时，尝试停止: {p} {o=} {e=}")
      await stop_sub(p)
  if o:
    o = o.decode("utf-8", errors="ignore")
  else:
    o = None
  if e:
    e = e.decode("utf-8", errors="ignore")
  else:
    e = None
  #  print(o, e)
  info("my sub exec res: %s" % format_out_of_shell((p.returncode, o, e)))
  return p.returncode, o, e
    
def format_out_of_shell(res):
  r = res[0]
  o = res[1]
  e = res[2]
  info("%s\n\nE: %s\n%s" % (o, r, e))
  res = ""
  if e is None:
    if r == 0:
      return f"{o}"
  if o is not None:
    res = f"{o}\n\n"
  res += f"E: {r}"
  if e is not None:
    res += f"\n{e}"
  return res

  if res[2] is None:
    if res[0] == 0:
      return "%s" % res[1]
  if res[1] is None:
    return "E: %s\n%s" % (res[0], res[2])
  return "%s\n\nE: %s\n%s" % (res[1],res[0], res[2])







#  async def run_my_bash(cmd, shell=True, max_time=120):
#    p = Popen(cmd,
#          shell=shell,
#          stdout=PIPE,
#          stderr=PIPE,
#          text=True,
#          encoding="utf-8",
#          errors="ignore")
#
#    start_time = time.time()
#    res = ""
#    errs = ""
#    await sleep(0.5)
#    if p.poll() == None and p.returncode == None:
#      while p.poll() == None and p.returncode == None:
#        if time.time() - start_time > max_time:
#          p.kill()
#          break
#        await sleep(1)
#
#    try:
#      res, errs = p.communicate(timeout=3)
#    except subprocess.TimeoutExpired as e:
#      res = e.stdout
#      errs = e.stderr
#    info("%s\n==\nE: %s\n%s" % (res, p.returncode, errs))
#    #  if not res:
#    #    res = None
#    #  res = str(res)
#    if p.returncode:
#      #  res = res + "\n==\nE: " + str(p.returncode)
#      res = "%s\n==\nE: %s" % (res, p.returncode)
#      if errs:
#        res = res + "\n" + errs
#      #await msg.delete()
#    else:
#      return
#    if len(res) > MAX_MSG_BYTES:
#      res = await pastebin(res)
#    return res
#


#  @exceptions_handler
@cross_thread(need_main=False)
async def my_py(cmd, src=None, client=None, **args):
  #  exec(cmd) #return always is None
  #  p=Popen("my_exec.py "+message.text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
  #  await my_popen(["python3", "my_exec.py", cmd], shell=False, msg=msg)
  #  await my_popen([ SH_PATH + "/my_exec.py", cmd], shell=False, msg=msg, executable="/usr/bin/python3")
  #  res = await my_popen(cmd,
  #             shell=True,
  #             client=client,
  #             src=src,
  #             executable="/usr/bin/python3",
  #             **args)
  #  cmd = ["python3", "-c", " ".join(cmd)]
  cmd = ["python3", "-c", cmd]
  res = await my_sexec(cmd, src=src)
  res = format_out_of_shell(res)
  return res

#  @exceptions_handler
async def my_exec(cmd, src=None, client=None, **args):
  #  res = """if "res" in locals():
  #  return res"""
  # https://stackoverflow.com/a/53255739
  exec(
      f'async def _():' +
    ''.join(f'\n {l}' for l in cmd.split('\n'))
    #  + "\n return 'end'"
    #  + "\n" + ''.join(f'\n {l}' for l in res.split('\n'))
  )

  # Get `__ex` from local variables, call it and return the result
  res = await locals()['_']()
  info(f"exec res: {res}")
  #  if res is not None:
  return "{!r}".format(res)


my_exec2 = cross_thread(need_main=False)(my_exec)

#  @exceptions_handler
#  @cross_thread(need_main=False)
#  async def my_exec(cmd, src=None, client=None, **args):
#    #  exec(cmd) #return always is None
#    #  p=Popen("my_exec.py "+message.text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
#    #  await my_popen(["python3", "my_exec.py", cmd], shell=False, msg=msg)
#    #  await my_popen([ SH_PATH + "/my_exec.py", cmd], shell=False, msg=msg, executable="/usr/bin/python3")
#    #  res = await my_popen(cmd,
#    #             shell=True,
#    #             client=client,
#    #             src=src,
#    #             executable="/usr/bin/python3",
#    #             **args)
#    #  cmd = ["python3", "-c", " ".join(cmd)]
#    #  cmd = ["python3", "-c", cmd]
#    #  res = await my_sexec(cmd, src=src)
#    #  res = format_out_of_shell(res)
#    # https://www.runoob.com/python3/python3-func-exec.html
#    #  local_vars = {}
#    #  await asyncio.to_thread()
#    #  await exec(cmd, globals(), local_vars)
#    #  if "res" in local_vars:
#    #    return local_vars["res"]
#    #  return local_vars
#
#    res = """if "res" in locals():
#    return res"""
#    # https://stackoverflow.com/a/53255739
#    exec(
#      f'async def __ex(): ' +
#      ''.join(f'\n {l}' for l in cmd.split('\n'))
#      + "\n" + ''.join(f'\n {l}' for l in res.split('\n'))
#    )
#
#    # Get `__ex` from local variables, call it and return the result
#    return await locals()['__ex']()


#  @exceptions_handler
@cross_thread(need_main=False)
async def my_eval(cmd):
  res = eval(cmd)
  #  info("%s %s" % (res, type(res)))
  info("%s %s" % (type(res), short(res)))
  #  res = await cmd_answer(str(res), client=client, msg=msg, **args)
  return res

async def send_cmd_to_bash(gateway, name, text):
  # for msg for mt api

  #  if not text:
  #    warn("skip bash cmd, text is empty: {}".format(msg))
  #    return
    #  text = msg[2]
    #  name = msg[1]
    #  gateway = msg[0]
  msg = {
    "gateway": gateway,
    "username": "{}".format(name),
    "text": "{}".format(text),
  }
  #  if isinstance(msg, str):
  #    shell_cmd = ["bash", SH_PATH + "/bcmd.sh"]
  #    shell_cmd.append("just_get_reply")
  #    shell_cmd.append(msg_mt)
  #  else:
  # [gateway, username, text]
  #  if type(msg) == list:
    #  if not " " in msg[1]:
  #  if msg[1]:
  #    if len(msg[1]) < 2 or msg[1][1] != ' ':
  #      msg[1] = "X " + msg[1]
  #  if name.startswith("C "):
  #    return
  #  info("msg_mt: {}".format(msg))
  #  shell_cmd="{} {} {} {}"
  #  shell_cmd = ["bash -l", SH_PATH + "/bcmd.sh"]
  #  shell_cmd = ["bash", SH_PATH + "/bcmd.sh"]
  #  shell_cmd = [SH_PATH + "/bcmd.sh"]
  #  cmds = [f"{SH_PATH}/bcmd.sh", str(gateway), shlex.quote( name ), shlex.quote( text ), repr(msg)]
  cmds = [f"{SH_PATH}/bcmd.sh", str(gateway), name, text, repr(msg)]

  #  if shell_cmd[1] == "gateway1":
  #    #  if my_host_re.match(shell_cmd[3]):
  #    if urlre.match(shell_cmd[3]):
  #      print("my url")
  #      shell_cmd[3] = ".ipfs {} only".format(shell_cmd[3])
  #      #  shell_cmd[1] = "gateway4"
  #    elif tw_re.match(shell_cmd[3]):
  #      print("a twitter")
  #      shell_cmd[3] = ".tw {}".format(shell_cmd[3])
  #      #  shell_cmd[1] = "gateway4"
  #    elif pic_re.match(shell_cmd[3]):
  #      print("a pic")
  #      shell_cmd[3] = ".ipfs {} only".format(shell_cmd[3])
  #      #  shell_cmd[1] = "gateway4"
  #    elif url_only_re.match(shell_cmd[3]):
  #      print("a url")
  #      shell_cmd[3] = ".ipfs {} autocheck".format(shell_cmd[3])
  #      #  shell_cmd[1] = "gateway4"
  #  warn("bash cmd: {}".format(shell_cmd))
  #  await run_my_bash(shell_cmd, shell=False)
  #  await my_popen(shell_cmd, shell=False)
  #  await my_popen(" ".join(shell_cmd))
  #  res = await my_popen(shell_cmd, shell=False, src=gateway)
  #  r, o, e = await my_sexec(shell_cmd, src=gateway)
  r, o, e = await myshell(cmds, src=gateway)
  if r == 0:
    if o:
      return re.sub(shell_color_re,  "", o)
    else:
      return o
  else:
  #  info(res)
    return format_out_of_shell((r, o, e))

#  @exceptions_handler
#  async def send2mt(client, message):
#      "get msg for matterbridge api"
#      chat_id = get_chat_id(message)
#      if chat_id in MT_GATEWAY_LIST_for_tg:
#          sender_id = get_sender_id(message)
#  #        warn(f"send 2 mt: {message.raw_text}")
#          logger.debug("start to mt")
#  #        if message.fwd_from:
#          if is_forward(message):
#              if sender_id == cid_tw:
#                  info("I: ignore a msg from tw")
#                  raise StopPropagation
#  #        if message.sender_id == 1494863126:
#              # wtfipfsbot
#  #            pass
#          if sender_id == 420415423:
#              # t2bot
#              if message.text.startswith("bot: "):
#                  await message.delete()
#                  raise StopPropagation
#          if MT_GATEWAY_LIST_for_tg[chat_id] == "gateway5":  # need not to send in order
#              if is_edit(message):
#                  raise StopPropagation
#              msg = await parse_msg_for_mt(client, message)
#              if msg:
#                  await mt_send(msg[0], msg[1], msg[2], msg[3])
#          else:
#              global locks
#              if chat_id in locks:
#                  pass
#              else:
#                  locks.update({chat_id: asyncio.Lock()})
#              lock = locks[chat_id]
#              async with lock:
#                  msg = await parse_msg_for_mt(client, message)  # return [text, username, gateway, qt]
#                  if msg:
#                      if sender_id == BOT_ID:
#                          pass
#                      elif sender_id == TG_BOT_ID_FOR_MT:
#                          pass
#                      elif await parse_bridge_name(msg[1].rstrip(": ")):
#                          msg[1] = await parse_bridge_name(msg[1].rstrip(": "))
#                      else:
#                          #  if is_my_group(client, message):
#                          # if is_me(client, message):
#                              #  print(message)
#                              #  print(msg)
#                          await mt_send(msg[0], msg[1], msg[2], msg[3])
#                      #  if message.media is not None:
#                      #      return
#                      if not is_my_group(client, message):
#                          return
#                      if msg[2] == "gateway11":
#                          msg[2] = "gateway1"
#                      #for cmd answer
#                      if msg[1].endswith(": "):
#                          msg[1] = msg[1].strip(": ")
#                      if msg[1] != "C bot":
#                          if await CMD.check_cmd(client, message):
#                              logger.debug("cmd ok")
#                              pass
#                          else:
#                              text = msg[0]
#                              #  cmd = text.split(': ', 1)[1]
#                              cmd = text
#                              faq = await faq_get(cmd)
#                              if faq:
#                                  await cmd_answer_for_my_group(faq, message)
#
#                              elif cmd.startswith('.'):
#                                  info("use bash")
#                                  asyncio.create_task(send_cmd_to_bash(msg))
#                                  raise StopPropagation
#  #        if message.out:
#  #            raise StopPropagation




async def load_config():
  path = PARENT_DIR / "config.json"
  config = await read_file(path.as_posix())
  config = load_str(config)

  #  info("config\n%s" % json.dumps(config, indent='  '))
  
  if config is None:
    warn("配置文件有问题: config.json")
    return
  try:
    config["sync_groups_all"].append(config["public_groups"])
    config["sync_groups_all"].append(config["bot_groups"])

    config["public_groups"] = config["public_groups"] + config["rss_groups"] + config["bot_groups"] + config["extra_groups"] + [config["acg_group"], config["log_group"]]

    config["my_groups"] = config["my_groups"] + config["public_groups"]


    #  jid = get_my_key("JID")
    #  config['ME'] = jid

    #  info("loaded config\n%s" % json.dumps(config, indent='  '))

    for i in config:
      if type(config[i]) is list:
        if config[i]:
          if type(config[i][0]) is str:
            config[i] = set(config[i])
          elif type(config[i][0]) is list:
            tmp = []
            for j in config[i]:
              tmp.append(set(j))
            config[i] = tmp

    globals().update(config)
    global gd
    try:
      data = await read_file(DATA_PATH, "rb")
      if data:
        gd = pickle.loads(data)
        #  info(f"loaded gd: {gd}")
      else:
        gd = {}
    except Exception as e:
      err(e=e)
      gd = {}

    if "mtmsgsg" in gd:
      info("load msg history: %s" % gd["users"])
    else:
      warn("not found msg history")

    if "users" not in gd:
      gd["users"] = {}

    if "bridges" not in gd:
      gd["bridges"] = {
          # chat_id fo tg: jid of xmpp/gateway
          -1001577701755: acg_group,
          rss_bot: rss_group,
          #  gpt_bot: "gateway1",
          # 临时通道 jid of xmpp/gateway: chat_id fo tg
          }
    if "mtmsgsg" not in gd:
      gd["mtmsgs"] = {
          "gateway1": {}
          }

    #  info("loaded gd\n%s" % json.dumps(gd, indent='  '))
    globals().update(gd)

    for muc in my_groups:
      if muc not in users:
        users[muc] = {}
      #  rooms[muc] = None

    for muc in users:
      #  if muc not in public_groups:
      #    continue
      jids = users[muc]
      tmp = []
      for jid in jids:
        j = jids[jid]
        if len(j) < 3:
          tmp.append(jid)
        else:
          set_default_value(j)
          if j[4][0] < 0:
            j[4][0] = 0

      for jid in tmp:
        jids.pop(jid)

    #  for chat_id in bridges:
    #    target = bridges[chat_id]
    #    if type(target) is dict:
    #      target.clear()

    info(f"my_groups: {my_groups=}")

    return True
  except Exception as e:
    warn(f"配置文件有问题: config.json {e=}")
    raise e

#  asyncio.run(load_config())


def set_default_value(j=None, m=None):
  if j is None:
    j = []
  elif type(j) is not list:
    m = j
    j = []
  if m is not None:
    if j:
      j[0] = m.nick
      j[1] = m.affiliation
      j[2] = m.role
    else:
      j.extend([m.nick, m.affiliation, m.role])
  if len(j) < 4:
    j.append( time.time() )
  else:
    j[3] = time.time()
  if len(j) < 5:
    #  j.append( [2*wtf_time/(time.time()-j[3]), 0] )
    j.append( [wtf_time/4, 0] )
  return j


async def save_data():
  data = pickle.dumps(gd)
  if await write_file(data, DATA_PATH, "wb"):
    info("已保存临时数据")
    return True
  else:
    #  warn("保存失败")
    info("保存失败", exc_info=True, stack_info=True)







#  urltitle_config.REQUEST_TIMEOUT = 8
#  urltitle_config.MAX_REQUEST_ATTEMPTS = 2


#  urltitle_config.DEFAULT_REQUEST_SIZE = 1024 ** 2
#  urltitle_config.DEFAULT_REQUEST_SIZE = 1024 ** 2 * 16

#  MiB = 1024 ** 2
#  urltitle_config.MAX_REQUEST_SIZES = {"html": MiB, "ipynb": 8 * MiB, "pdf": 8 * MiB}  # Title observed toward the bottom.
#  #  print(urltitle_config)
#  #  print(urltitle_config.MAX_REQUEST_SIZES)
#  urltitle_config.MAX_REQUEST_SIZES.update({ 'html': 1024 ** 2 * 16 })

# Titles for HTML content
#  reader = URLTitleReader(verify_ssl=True)

#  EXTRA_HEADERS = {
#      #  "Accept": "*/*",
#      #  "Accept-Language": "en-US,en;q=0.5",
#      "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
#  }

#  async def get_title(url):
#    try:
#      #  res = reader.title(url)
#      netloc = reader.netloc(url)
#      if netloc not in urltitle_config.NETLOC_OVERRIDES:
#        urltitle_config.NETLOC_OVERRIDES[netloc] = {"extra_headers": {}}
#      elif "extra_headers" not in urltitle_config.NETLOC_OVERRIDES[netloc]:
#        urltitle_config.NETLOC_OVERRIDES[netloc]["extra_headers"] = {}
#      EXTRA_CONFIG_HEADERS = urltitle_config.NETLOC_OVERRIDES[netloc]["extra_headers"]
#      EXTRA_CONFIG_HEADERS.update(EXTRA_HEADERS)
#      res = await asyncio.to_thread(reader.title, url)
#    except TypeError as e:
#      res=f"{e=}"
#      #  info(res)
#      warn(res)
#      #  prof.cons_show(res)
#    #  except urltitle.urltitle.URLTitleError as e:
#    except URLTitleError as e:
#      res=f"URLTitleError: {e=}"
#      #  prof.cons_show(res)
#      warn(res)
#    except Exception as e:
#      #  warn(f"E: {e=}", exc_info=True, stack_info=True)
#      res=f"{e=}"
#      #  prof.cons_show(res)
#      warn(res)
#    return res

async def shasum(path):
  shell_cmd=["shasum", path]
  res = await myshell(shell_cmd)
  if res:
    info(f"res: {res} {shell_cmd}")
    res = res[1]
    res = res.split(" ")[0]
    return res
  else:
    return str(int(time.time()))

async def backup(path, src=None, delete=False, no_wait=False, rename=False):
  if rename:
    name = path.split("/")[-1]
    if "." in name:
      ext = "." + name.split(".")[-1]
    else:
      ext = ""
    name = await shasum(path) + ext
    npath = path.rsplit("/", 1)[0] + "/" + name
  else:
    npath = path
  #  if name is not None:
  #    npath = path.rsplit("/", 1)[0] + "/" + name
  #  else:
  #    npath = path
  url = "https://%s%s/%s" % (DOMAIN, URL_PATH, (urllib.parse.urlencode({1: npath[len(DOWNLOAD_PATH):]})).replace('+', '%20')[5:])
  info(f"url: {url}")
  #  shell_cmd=["/usr/bin/mv", path, DOWNLOAD_PATH0+"/"]
  if delete:
    info(f"delete: {path}")
    shell_cmd=["rm", path]
  else:
    #  if name is not None:
    if rename:
      info(f"backup: {path} rename to: {name}")
      shell_cmd=["cp", path, DOWNLOAD_PATH0+"/"+name]
    else:
      info(f"backup: {path}")
      shell_cmd=["cp", path, DOWNLOAD_PATH0+"/"]
  #  res = await run_my_bash(shell_cmd, shell=False)
  #  res = await my_sexec(shell_cmd)
  if no_wait:
    t = asyncio.create_task( myshell(shell_cmd) )
    return url, t
  else:
    res = await myshell(shell_cmd)
  if res:
    info(f"res: {res} {shell_cmd}")
    if src:
      send(url, src)
  return url

@exceptions_handler
async def get_twitter(url, src=None, opts=[], max_time=run_shell_time_max):
  #  elif url.startswith("https://x.com/"):
  #  elif url.startswith("https://twitter.com/"):
  cmds = [f"{SH_PATH}/twitter_to_text.sh", url]
  return format_out_of_shell( await myshell(cmds, src=src, max_time=max_time))

@exceptions_handler
async def get_title(url, src=None, opts=[], max_time=run_shell_time_max):
  # also download
  #  cmds = ["bash", f"{SH_PATH}/title.sh"]
  #  cmds = [f"{SH_PATH}/title.sh", shlex.quote(url)]
  #  cmds = shlex.join(opts)
  cmds = [f"{SH_PATH}/title.sh", url]
  cmds.extend(opts)
#  cmds.append(shlex.quote(url))
  #  r, o, e = await my_sexec(shell_cmd, src=src, max_time=max_time)
  #  if r == 0:
  #  res = await run_run(myshell(cmds, src=src) , False)
  r, o, e = await myshell(cmds, src=src, max_time=max_time)
  if o:
    s = o.splitlines()
    if len(s) > 0:
      if o.startswith(DOWNLOAD_PATH):
        if os.path.exists(s[0]):
          path = s.pop(0)
          info("found file: %s" % path)
          try:
            t = asyncio.create_task(backup(path))
            url = await upload(path, src)
            url2 = await t
            #  s.append("")
            if url:
              #  s[0] = f"\n- {url}"
              #  s.append(f"- {url}")
              s.append(s.pop() + f" [[xmpp]]({url})")
              info("add xmpp file url: %s" % url)
            #  s.append(f"- {url2}")
            #  s.append(f"- {url2}")
            s.append(s.pop() + f" [[vps]]({url2})")
          finally:
            asyncio.create_task(backup(path, delete=True))
        else:
          warn("not found file: %s" % s.pop(0))
      else:
        warn("wtf: %s" % s.pop(0))
  #  if res:
  #    o = res
  if r == 0:
    if o:
      if len(s) > 0:
        #  path = s[-1]
        #  return "\n".join(s)
        return html.unescape("\n".join(s))
      else:
        warn(f"fixme: {o=} {url=}")
        return
        return s[-1]
    else:
      warn("empty out: %s\n\nE: %s\n%s" % (o, r, e))
      return
  elif r == -512:
    if o:
      if len(s) > 0:
        return html.unescape("\n".join(s))
      else:
        warn(f"fixme: {o=} {url}")
        return "timeout"
      #  return "\n".join(s)
    else:
      warn(f"fixme: {o=} {url}")
      return "timeout"
  else:
    if o is not None:
      o = html.unescape(o)
    if e is not None:
      e = html.unescape(e)
    return format_out_of_shell((r, o, e))
    #  warn("%s\n\nE: %s\n%s" % (o, r, e))
    #  return "%s\n\nE: %s\n%s" % (o, r, e)



#  async def get_title(url, src=None, opts=[]):
#    shell_cmd = ["bash", f"{SH_PATH}/title.sh"]
#    shell_cmd.append(url)
#    #  while opts:
#    #    shell_cmd.append(opts.pop(0))
#    shell_cmd.extend(opts)
#    #  if down:
#    #    #  shell_cmd.append("%s" % (2**20*1000))
#    #    while True:
#    #      if len(shell_cmd) < 5:
#    #        shell_cmd.append("")
#    #      else:
#    #        break
#    #    shell_cmd.append("down")
#    if len(shell_cmd) == 6:
#      max_time = 600
#    else:
#      max_time = 60
#    r, out, err = await my_popen(shell_cmd, shell=False, src=src, combine=False, max_time=max_time)
#    if r == 0:
#      s = out.splitlines()
#      if len(s) > 1:
#        path = s[-1]
#        if os.path.exists(path):
#          url = await upload(path, src)
#          t = asyncio.create_task(backup(path))
#          await t
#          asyncio.create_task(backup(path, delete=True))
#          if url:
#            s[-1] = f"\n- {url}"
#          else:
#            s.pop(-1)
#        else:
#          s.pop(-1)
#        return "\n".join(s)
#      else:
#        return out
#    else:
#      #  if err:
#      warn("%s\n\nE: %s\n%s" % (out, r, err))
#      return "%s\n\nE: %s\n%s" % (out, r, err)



#  async def other_init():
#    info("开始初始化其他组件")
#    res = await asyncio.to_thread(_other_init)
#    info(res)
#  #  allright.set()
#    if res is True:
#      global allright_task
#      allright_task -= 1
#
#  @exceptions_handler
#  def _other_init():
#    return True


#  #  global G1PSID
#  #  BING_U = get_my_key("BING_U")
#  G1PSID = get_my_key('BARD_COOKIE_KEY')
#
#  from g4f.cookies import set_cookies
#
#  #  set_cookies(".bing.com", {
#  #    "_U": "%s" % BING_U
#  #  })
#  set_cookies(".google.com", {
#    "__Secure-1PSID": G1PSID
#  })
#
#
#  from g4f import models, Provider
#  from g4f.client import Client as Client_g4f
#
#  #  def ai_img(prompt, model="gemini", proxy=None):
#  async def ai_img(prompt, model="gemini"):
#    try:
#      global g4fclient
#      if "g4fclient" not in globals():
#        g4fclient = Client_g4f()
#      #  response = client.images.generate(
#        #  response = await client.images.generate(
#      response = await asyncio.to_thread(g4fclient.images.generate,
#        model=model,
#        #  prompt="a white siamese cat",
#        prompt=prompt,
#      )
#    except Exception as e:
#      image_url = f"{e=}"
#    else:
#      image_url = response.data[0].url
#    #  print(image_url)
#    return image_url
#
#  async def ai(prompt, provider=Provider.You, model=models.default, proxy=None):
#    try:
#      global g4fclient
#      if "g4fclient" not in globals():
#        g4fclient = Client_g4f()
#      #  response = client.chat.completions.create(
#        #  response = await client.chat.completions.create(
#        #  s = await asyncio.to_thread(run_ocr, img=res)
#      response = await asyncio.to_thread(g4fclient.chat.completions.create,
#        model=model,
#        messages=[{"role": "user", "content": prompt}],
#        provider=provider,
#        proxy=proxy,
#      )
#    except Exception as e:
#      image_url = f"{e=}"
#    else:
#      image_url  = response.choices[0].message.content
#    #  print(image_url)
#    return image_url
#
#
#
#
#
#
#
#
#  from gradio_client import Client as Client_hg
#
#  HF_TOKEN = get_my_key('HF_TOKEN')
#
#  from huggingface_hub import InferenceClient
#
#  dsclient = InferenceClient(
#    provider="novita",
#    api_key=HF_TOKEN
#  )
#  async def hgds(text):
#    messages = [
#      {
#        "role": "user",
#        #  "content": "What is the capital of France?"
#        "content": text
#      }
#    ]
#
#  #  completion = client.chat.completions.create(
#  #      model="deepseek-ai/DeepSeek-R1",
#  #    messages=messages,
#  #    max_tokens=500,
#  #  )
#    result = await asyncio.to_thread(dsclient.chat.completions.create,
#      model="deepseek-ai/DeepSeek-R1",
#      messages=messages,
#      max_tokens=500,
#    )
#    #  print(completion.choices[0].message)
#    res = completion.choices
#    if res:
#      return "%s" % res[0].message
#    else:
#      return "E: %s" % res
#
#
#  async def hg(prompt, provider=Provider.You, model=models.default, proxy=None):
#    try:
#      global hgclient
#      if "hgclient" not in globals():
#        hgclient = Client_hg(api_key=HF_TOKEN)
#      #  response = client.chat.completions.create(
#      response = await hgclient.chat.completions.create(
#        model=model,
#        messages=[{"role": "user", "content": prompt}],
#        provider=provider,
#        proxy=proxy,
#      )
#    except Exception as e:
#      image_url = f"{e=}"
#    else:
#      image_url  = response.choices[0].message.content
#    #  print(image_url)
#    return image_url
#
#
#  async def qw(text):
#    try:
#      global qw_client
#      if "qw_client" not in globals():
#        qw_client = Client_hg("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/")
#      #  result = qw_client.predict(
#      result = await asyncio.to_thread(qw_client.predict,
#          #  sys.argv[1],	# str  in 'Input' Textbox component
#          text,	# str  in 'Input' Textbox component
#          #  [[sys.argv[1], sys.argv[1]]],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
#          [],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
#          "You are a helpful assistant.",	# str  in 'parameter_9' Textbox component
#          api_name="/model_chat"
#      )
#      #  print(result)
#      #  print(result[1][1][1])
#      #  print(result[1][0][1])
#      res = result[1][0][1]
#    except Exception as e:
#      res = f"{e=}"
#    return res
#
#  async def qw2(text):
#    try:
#      global qw2_client
#      if "qw2_client" not in globals():
#        qw2_client = Client_hg("Qwen/Qwen1.5-110B-Chat-demo")
#      #  result = qw2_client.predict(
#      result = await asyncio.to_thread(qw2_client.predict,
#          #  query=sys.argv[1],
#          query=text,
#          history=[],
#          system="You are a helpful assistant.",
#          api_name="/model_chat"
#      )
#      #  print(result)
#      #  print(result[1][1][1])
#      #  print(result[1][0][1])
#      res = result[1][0][1]
#    except Exception as e:
#      res = f"{e=}"
#    return res


#  def send_log(text, jid=CHAT_ID, delay=1, fm=None):
#  @cross_thread(need_main=True)
def send_log(text, jid=None, delay=1, fm=None):
  if fm is None:
    fm = sys._getframe()
    fm = fm.f_back
  if fm is None:
    return False
  if fm.f_code.co_name != "_exceptions_handler":
    text = f"{fm.f_code.co_name} {fm.f_lineno} {text}"
  #  if jid is None:
  #    if send_log(text, CHAT_ID, delay, fm) is True:
  #      if send_log(text, log_group_private, delay, fm) is True:
  #        return True
  #    return False
  m = 0
  n = 0
  # https://docs.python.org/zh-cn/3/library/asyncio-task.html#introspection
  for j in asyncio.all_tasks(loop):
    if j.get_name() == "send_log_tg":
      m += 1
    elif j.get_name() == "send_log_xmpp":
      n += 1

  if jid is None:
    tjid = CHAT_ID
    jid = log_group_private
  else:
    tjid = jid

  #  if jid is None or isinstance(jid, int):
  if isinstance(tjid, int):
    if m > 0:
      warn(f"send_log tg is busy: {m} text: {short(text)}")
      #  await sleep(delay*m)
    else:
      info(f"send_log tg: {text}")
    t = asyncio.create_task(send_tg(text, tjid, delay=(delay+1)**m), name="send_log_tg")
  #  if isinstance(jid, int) is False:
  #  else:
  if not isinstance(jid, int):
    if n > 0:
      warn(f"send_log xmpp is busy: {n} text: {short(text)}")
    else:
      info(f"send_log xmpp: {text}")
    t = asyncio.create_task(send_xmpp(text, jid, delay=(delay+1)**m), name="send_log_xmpp")

  #  if jid is None:
  #    #  asyncio.create_task(send_tg(text, CHAT_ID, delay=(delay+1)**k), name="send_log")
  #    #  asyncio.create_task(send_xmpp(text, log_group_private, delay=(delay+1)**k), name="send_log")
  #    asyncio.create_task(send_tg(text, CHAT_ID, name="send_log")
  #    asyncio.create_task(send_xmpp(text, log_group_private, name="send_log")
  #  else:
  #    #  asyncio.create_task(send(text, jid, delay=(delay+1)**k), name="send_log")
  #    if isinstance(jid, int):
  #      asyncio.create_task(send_tg(text, CHAT_ID, name="send_log")
  #    else:
  #      asyncio.create_task(send_xmpp(text, log_group_private, name="send_log")
  #  return await t
  return True


@exceptions_handler
def sendme(*args, to=1, **kwargs):
  if to != 2:
    #  send(*args, jid=CHAT_ID, **kwargs)
    #  asyncio.create_task(send_tg(*args, chat_id=MY_ID, **kwargs))
    asyncio.create_task(send_tg(*args, **kwargs))
  if to != 1:
    send(*args, jid=ME, **kwargs)
  #  asyncio.create_task(run_run(send_t(text)))

#  async def send(text, jid=None, *args, **kwargs):
#    if jid is None:
#      if isinstance(text, str):
#        return False
#    elif isinstance(jid, int):
#      #  return await send_t(text, jid, *args, **kwargs)
#      return await run_run(send_tg(text=text, jid=jid, *args, **kwargs), need_main=True)
#    return await run_run(send_x(text=text, jid=jid, *args, **kwargs), need_main=True)
#    #  if threading.current_thread() is loop2_thread:
#      #  asyncio.run_coroutine_threadsafe(coro, loop)


#  async def send_x(text, jid=None, *args, **kwargs):
#  async def send(text, jid=None, *args, **kwargs):
@exceptions_handler
def send(text, jid=None, *args, **kwargs):
  if jid is None:
    if isinstance(text, str):
      return False
  elif isinstance(jid, int):
    if "tg_msg_id" in kwargs:
      kwargs.pop("tg_msg_id")
    #  return await send_tg(text=text, chat_id=jid, *args, **kwargs)
    asyncio.create_task(send_tg(text=text, chat_id=jid, *args, **kwargs) )
    return True
  #  if  type(jid) is int:
    #  if jid == CHAT_ID:
    #    #  await send_t(text, *args, **kwargs)
    #    sendme(text, *args, **kwargs)
    #    jid = log_group_private
    #  else:
    #    return await send_t(text, jid, *args, **kwargs)

  if 'name' in kwargs:
    name = kwargs["name"]
    #  kwargs.pop("name")
  else:
    name = "**C bot:** "

  #  muc = None
  muc = jid
  if isinstance(text, aioxmpp.Message):
    if jid is None:
      #  warn(f"fixme: 该消息为xmpp专用，不能发往telegram, 日志可能会缺失 {text}")
      if text.type_ == MessageType.GROUPCHAT:
        muc = str(text.to.bare())
        #  jid = muc
      #  await send_t(text0, *args, **kwargs)
      #  sendme(text0, *args, **kwargs)
    #  info(f"该消息为xmpp专用，不能发往telegram, {text}")
    #  text0 = text.body[None]
    text0 = text.body.any()
    #  text.body[None] = f"{name}{text0}"
    for i in text.body:
      text.body[i] = f"{name}{text0}"
      break
  else:
    #  if jid is None:
    #    return
    text0 = text
    text = f"{name}{text}"

  if name:
    kwargs["name"] = name[2:-4]
    nick = name[2:-4]
  else:
    kwargs["name"] = None
    nick = name

  if 'xmpp_only' in kwargs:
    xmpp_only = kwargs["xmpp_only"]
  else:
    xmpp_only = False

  ms = get_mucs(muc)
  if ms:
  #  if muc in my_groups:
    #  info(f"准备发送同步消息到: {ms} {text=}")
    if main_group in ms:
      asyncio.create_task( send_tg(f"{name}{text0}", GROUP_ID) )
      asyncio.create_task( send_tg(f"{name}{text0}", GROUP2_ID, topic=GROUP2_TOPIC) )
      if xmpp_only:
        #  for m in ms:
        #    #  send_typing(m)
        #    asyncio.create_task( send_typing(m) )
        #  await send1(text, jid=log_group_private, *args, **kwargs)
        asyncio.create_task( send_xmpp(text, jid=log_group_private, *args, **kwargs) )
        return True
        ms = set()
      else:
        asyncio.create_task( mt_send_for_long_text(text0, name=nick) )
    for m in ms:
      #  if await send1(text, jid=m, *args, **kwargs):
      #    if isinstance(text, aioxmpp.Message):
      #      text = text.body[None]
      asyncio.create_task( send_xmpp(text, jid=m, *args, **kwargs) )
      if isinstance(text, aioxmpp.Message):
        #  text = text.body[None]
        text = text.body.any()
    return True
  else:
    #  info(f"准备发送到: {muc=} {jid=}")
    #  return await send1(text, jid=jid, *args, **kwargs)
    asyncio.create_task( send_xmpp(text, jid=jid, *args, **kwargs) )
    return True

@exceptions_handler(no_send=True)
async def send_xmpp(text, jid=None, *args, **kwargs):
  # for short msg
  if type(text) is str:
    #  if name:
    #    text = f"{name}{text}"
    if jid is None:
      #  jid = ME
      jid = log_group_private
    else:
      if type(jid) is JID:
        jid = get_jid(jid, True)

    #  texts = await split_long_text(text, 4096)
    #  for i in texts:
    if jid in my_groups:
      msg = aioxmpp.Message(
          to=JID.fromstr(jid),  # recipient_jid must be an aioxmpp.JID
          type_=MessageType.GROUPCHAT,
      )
    else:
      msg = aioxmpp.Message(
          to=JID.fromstr(jid),  # recipient_jid must be an aioxmpp.JID
          type_=MessageType.CHAT,
      )
    msg.body[None] = text
    if await _send_xmpp(msg, *args, **kwargs) is not True:
      return False
    return True
  elif isinstance(text, aioxmpp.Message):
    #  info(f"send1: {jid=} {text=}")
    msg = text
    #  if name:
    #    msg.body[None] = f"{name}{msg.body[None]}"
    if msg.type_ == MessageType.GROUPCHAT:
    #    if msg.to.resource is not None:
      if jid is not None:
        msg.to = JID.fromstr(jid)
      if not msg.to.is_bare:
          #  msg.to.resource = None
        #  if '/' in get_jid(msg.to, True):
          #  msg.to = JID.fromstr(get_jid(msg.to))
          #  msg.to = msg.to.replace(resource=None)
        orig = msg.to
        msg.to = msg.to.bare()
        info(f"已修正地址错误: {orig} -> {msg=}")
    return await _send_xmpp(msg, *args, **kwargs)
  else:
    err(f"text类型不对: {type(text)}")
    return False


on_nick_changed_futures = {}

def on_nick_changed(member, old_nick, new_nick, *, muc_status_codes=set(), **kwargs):
  #  jid = str(member.conversation_jid)
  #  jid = str(member.direct_jid.bare())
  muc = str(member.conversation_jid.bare())
  #  info(f"nick changed: {muc} {jid} {old_nick} -> {new_nick} {member.conversation_jid}")
  #  if (jid, muc) in on_nick_changed_futures:
  if muc in on_nick_changed_futures:
    try:
      on_nick_changed_futures[muc].set_result(new_nick)
    except asyncio.exceptions.InvalidStateError as e:
      info(f"无法保存nick到future: {muc} {on_nick_changed_futures[muc]} {e=}")
      #  on_nick_changed_futures.pop(muc)
  #  info(f"nick changed: {jid} {muc} {old_nick} -> {new_nick}")



#  def clean_forwarded_tg_msg_ids(jid):
#    d = set()
#    for i in forwarded_tg_msg_ids:
#      s = forwarded_tg_msg_ids[i]
#      if jid in s:
#        s.remove(jid)
#        info(f"delete forward log for {jid}: {i}")
#        if len(s) == 0:
#          info(f"delete empty log: {i}")
#          d.add(i)
#    for i in d:
#      forwarded_tg_msg_ids.pop(i)
#



send_locks = {}
#  @cross_thread(need_main=True)
#  @exceptions_handler(no_send=True)
@cross_thread
async def _send_xmpp(msg, client=None, room=None, name=None, correct=False, fromname=None, nick=None, delay=None, xmpp_only=False, tmp_msg=False, tg_msg_id=None, qt=None):
  #  info(f"{msg}")
  muc = str(msg.to.bare())
  #  if muc not in rooms:
  #    info(f"not found room: {muc}")
  #    return False
  jid = str(msg.to)
  if jid not in send_locks:
    send_locks[jid] = asyncio.Lock()
  async with send_locks[jid]:
    msg.from_ = None
    if msg.type_ == MessageType.GROUPCHAT:

      if room is None:
        if muc in rooms:
          room = rooms[muc]

      if nick is None:
        if fromname is None:
          if name is None:
            pass
          else:
            nick = name
        else:
          nick = fromname

      # https://stackoverflow.com/questions/69778194/how-can-i-check-whether-a-unicode-codepoint-is-assigned-or-not
      if room is not None and nick is not None:
      #  if None:
        #  room = rooms[muc]
        #  if muc in rooms:
        #  if room is not None:
        #  await set_nick(room, fromname)
        nick = wtf_str(nick)
        #  nick_old = room.me.nick

        jids = users[muc]
        if myjid not in jids:
          #  jids[myjid] = [nick_old, room.me.affiliation, room.me.role]
          #  j = []
          #  jids[myjid] = []
          #  set_default_value(j, room.me)
          jids[myjid] = set_default_value(m=room.me)
          warn(f"不存在nick记录，已添加: {muc} {myjid} {msg} {jids[myjid]}")
        nick_old = jids[myjid][0]
        #  if nick_old != nick:
        if False:
          fu = asyncio.Future()
          #  jid = str(room.me.direct_jid)
          on_nick_changed_futures[muc] = fu
          try:
            await room.set_nick(nick)
          except ValueError as e:
            jids[myjid][0] = nick
            warn(f"改名失败, 不支持特殊字符: {nick=} {e=}")
          else:
            #  await fu
            try:
              #  await asyncio.wait_for(await asyncio.shield(fu), timeout=8)
              await asyncio.wait_for(fu, timeout=3)
            #  except Exception as e:
            except TimeoutError as e:
              on_nick_changed_futures.pop(muc)
              jids[myjid][0] = nick
              warn(f"改名失败(超时)：{muc} {nick_old} -> {nick} {e=}")
            else:
              on_nick_changed_futures.pop(muc)
              jids[myjid][0] = fu.result()
              if fu.result() != nick:
                warn(f"改名结果有问题: {muc} {fu.result()=} != {nick=}")
              #  else:
              #    info(f"set nick: {muc} {nick_old} -> {nick}")
            #  else:
            #    info(f"same nick: {str(msg.to.bare())} {room.me.nick} = {nick}")
            #  else:
            #    info(f"not found room: {msg.to}")

    text = None
    #  text = msg.body.any() # ValueError("any() on empty map")
    for i in msg.body:
      text = msg.body[i]
      if text:
        if qt is not None:
          text = "> %s\n%s" % ("\n> ".join(qt), text)
          msg.body[i] = text
        break

    if text:
      #  if jid == log_group_private:
      msgs = []
      for text in await split_long_text(text, MAX_MSG_BYTES, tmp_msg):
        if msgs:
          msg = aioxmpp.Message(
              to=msg.to,
              type_=msg.type_,
          )
        msg.body[None] = text
        msgs.append(msg)
        #  if correct:
        if xmpp_only:
          break
    else:
      msgs = [msg]

    if len(msgs) > 1:
      tmp_msg = False
      info("没办法同时更正多条消息")
    msg.autoset_id()
    if jid not in last_outmsg:
      correct = False
      if jid in tmp_msg_chats:
        tmp_msg_chats.remove(jid)

    for msg in msgs:
      await sleep(msg_delay_default)
      if tg_msg_id in deleted_tg_msg_ids:
        return True
      if text:
        #  info(f"{jid=} {text=} {tmp_msg=} {correct=}")
        #  add_id_to_msg(msg, correct, tmp_msg)
        #  j = get_msg_jid(msg)
        msg.xep0085_chatstate = chatstates.ChatState.ACTIVE
        if correct or jid in tmp_msg_chats:
          r = aioxmpp.misc.Replace()
          r.id_ = last_outmsg[jid]
          msg.xep0308_replace = r
        else:
          last_outmsg[jid] = msg.id_

      try:
        if msg.to.is_bare or msg.type_ == MessageType.GROUPCHAT or str(msg.to.bare()) not in my_groups:
        #  if gpm is False:
          if client is not None:
            # https://docs.zombofant.net/aioxmpp/devel/api/public/node.html?highlight=client#aioxmpp.Client.send
            res = await client.send(msg)
            #  if res is None:
            #    return True
          elif room:
            # https://docs.zombofant.net/aioxmpp/devel/api/public/muc.html?highlight=room#aioxmpp.muc.Room.send_message
            # res=<StanzaToken id=0x00007f2a3083eca0>
            #  res = room.send_message(msg)
            res = await room.send_message(msg)
          else:
            client = XB
            res = await client.send(msg)
            #  if res is None:
            #    return True
        else:
          # https://docs.zombofant.net/aioxmpp/devel/api/public/im.html#aioxmpp.im.conversation.AbstractConversation.send_message
          if client is None:
            client = XB
          p2ps = client.summon(im.p2p.Service)
          c = p2ps.get_conversation(msg.to)
          #  stanza = c.send_message(msg)
          #  elif type(res) is stream.StanzaToken:
          #  res2 = await res
          res = await c.send_message(msg)
      except ValueError as e:
        if e.args[0] == 'control characters are not allowed in well-formed XML':
          #  err(f"发送xmpp消息失败: {e=} {jid=} [msg=] {text=}", exc_info=True, stack_info=True)
          info(f"发送xmpp消息失败，不支持特殊字符: {e=} {jid=} [msg=] {text=}")
        else:
          err(f"发送xmpp消息失败: {e=} {jid=} [msg=] {text=}", no_send=True)
        return False
      except Exception as e:
        err(f"发送xmpp消息失败: {e=} {jid=} [msg=] {text=}", no_send=True)
        return False
        #  return False
      #  if isawaitable(res):
      #  info(f"{type(res)}: {res} {msg}")
      if res is None:
        info(f"sent: {jid} {short(text)}")
      #  elif asyncio.iscoroutine(res) or type(res) is stream.StanzaToken:
      else:
        warn(f"res is not None: {res=} {client=} {room=} {jid=} {msg=}")
      #  elif type(res) is stream.StanzaToken:
      #    #  dbg(f"client send: {res=}")
      #    try:
      #      res2 = await res
      #    if res2 is None:
      #      info(f"send xmpp msg ok: finally: {res=}")
      #    #  elif hasattr(res, "stanza") and res.stanza and res.stanza.error is None:
      #    #    # 群内私聊
      #    #    info(f"send gpm msg: finally: {res=}")
      #    #    return True
      #      #  return True
      #    else:
      #      info(f"send xmpp msg: finally: {res=} {res2=}")
      #      return False
      #  else:
      #    info(f"res is not coroutine: {res=} {client=} {room=} {msg=}")
      #  return False
      if tg_msg_id is None:
        if tmp_msg is False:
          #  clean_forwarded_tg_msg_ids(jid)
          d = set()
          for i in forwarded_tg_msg_ids:
            s = forwarded_tg_msg_ids[i]
            if jid in s:
              s.remove(jid)
              info(f"delete forward log for {jid}: {i}")
              if len(s) == 0:
                info(f"delete empty log: {i}")
                d.add(i)
          for i in d:
            forwarded_tg_msg_ids.pop(i)
        #  forwarded_tg_msg_ids.clear()
      elif tg_msg_id in deleted_tg_msg_ids:
        tmp_msg_chats.add(jid)
        return
      else:
        #  clean_forwarded_tg_msg_ids(jid)
        for i in forwarded_tg_msg_ids:
          s = forwarded_tg_msg_ids[i]
          if jid in s:
            s.remove(jid)
            info(f"delete forward log for {jid}: {i}")
        if tg_msg_id not in forwarded_tg_msg_ids:
          forwarded_tg_msg_ids[tg_msg_id] = set()
        forwarded_tg_msg_ids[tg_msg_id].add(jid)

      if tmp_msg is True:
        tmp_msg_chats.add(jid)
      elif jid in tmp_msg_chats:
        tmp_msg_chats.remove(jid)
      # 为了同步tg消息的删除，当tg删除消息时，这边会根据l[2]把xmpp这边的最后消息标记为临时待更正消息，但如果标记之前发送了别的xmpp正常消息，就不能进行该动作了(镜像群也要处理)，所以l[2]记录应该清除，而且对也确实没用了
      #  if jid in mtmsgsg:
      #    mtmsgs = mtmsgsg[jid]
      #    for i in mtmsgs:
      #      l = mtmsgs[i]
      #      if len(l) > 2:
      #        #  l[2] = set()
      #        l[2].clear()
      #        tmp_msg_chats.difference_update( get_mucs(jid) )
      #        info("tmp_msg_chats, remove: {jid} and mirror group")
      if delay is not None:
        await sleep(delay)
  return True








slow_mode_task = None

async def _slow_mode(timeout=300):
  global msg_delay_default, slow_mode_task
  msg_delay_default = timeout/100
  await sleep(timeout)
  k = timeout/100/300*10
  while msg_delay_default > 0:
    msg_delay_default -= k
    await sleep(10)
  msg_delay_default = 0
  slow_mode_task = None
  warn("slow mode off")

async def slow_mode(client, timeout=300):
  global slow_mode_task
  if slow_mode_task is not None:
    slow_mode_task.cancel()
  warn("slow mode on")
  if msg_delay_default == 0:
    if client is TB:
      await send_tg2("slow mode on", CHAT_ID)
    else:
      await send_tg("slow mode on", CHAT_ID)
  slow_mode_task = asyncio.create_task(_slow_mode(timeout))
  await sleep(timeout)
  warn("slow mode off")
  if msg_delay_default == 0:
    if client is TB:
      await send_tg2("slow mode off", CHAT_ID)
    else:
      await send_tg("slow mode off", CHAT_ID)
  return True




#  @exceptions_handler(no_send=True)
@cross_thread
async def _send_tg(client, lock, last, chats, text, chat_id=CHAT_ID, correct=False, tmp_msg=False, delay=None, topic=None, qt=None, parse_mode="md", name=None):
  # tmp_msg: 标记该条消息为临时消息，会被下一条消息覆盖

  if qt is not None:
    qtr = "\n".join(qt)
    if qtr.startswith("**G "):
      qtr = qtr.split(":** ", 1)[1]
      if qtr.startswith(f"https://{DOMAIN}") and urlre.fullmatch(qtr):
        qtr = None
    info(f"{qtr=}")
    topic_orig = topic
    k = 0
    if qtr is not None:
      if topic is None:
        async for msg in client.iter_messages(chat_id):
          text = msg.text
          if text:
            if text.startswith("**G "):
              text = text.split(":** ", 1)[1]
            if similarity(text, qtr) > 0.9:
              info(f"found: {text=} {qtr=}")
              topic = msg.id
              break
            info(f"skip: {text=}")
          k += 1
          if k > 9:
            break
      else:
        async for msg in client.iter_messages(chat_id, reply_to=topic):
          text = msg.text
          if text:
            if text.startswith("**G "):
              text = text.split(":** ", 1)[1]
            if similarity(text, qtr) > 0.9:
              info(f"found: {text=} {qtr=}")
              topic = msg.id
              break
            info(f"skip: {text=}")
          k += 1
          if k > 9:
            break

    if topic_orig == topic:
      info("not found")
      if parse_mode ==  "md":
        parse_mode = "html"
      if parse_mode ==  "html":
        text = "<blockquote>%s</blockquote>\n%s" % ("\n".join(qt), text)
      else:
        text = "%s\n%s" % ("\n> ".join(qt), text)

  if name is not None:
    text = f"{name}{text}"
  #  else:
  #    if parse_mode ==  "md":
  #      parse_mode = client.parse_mode
  #  info(f"parse_mode: {parse_mode}")
  ts = await split_long_text(text, MAX_MSG_BYTES_TG, tmp_msg)
  if len(ts) > 1:
    tmp_msg = False
  k = 0
  resend = False
  async with lock:
    #  info0(f"send: {chat_id}: {text}")
    for t in ts:
      await sleep(msg_delay_default)
      try:
        if chat_id in last:
          omsg = last[chat_id]
          if correct is True:
            msg = await omsg.edit(t)
            correct = False
          elif chat_id in chats:
            msg = await omsg.edit(t, parse_mode=parse_mode)
          else:
            msg = await client.send_message(chat_id, t, reply_to=topic, parse_mode=parse_mode)
        else:
          msg = await client.send_message(chat_id, t, reply_to=topic, parse_mode=parse_mode)
        k += 1
        if k == len(ts):
          last[chat_id] = msg
          if tmp_msg:
            chats.add(chat_id)
          elif chat_id in chats:
            chats.remove(chat_id)

        elif len(ts) > 1:
          await sleep(0.5)
        if delay is not None:
          await sleep(delay)
      except rpcerrorlist.FloodWaitError as e:
        warn(f"消息发送过快，被服务器拒绝，等待300s: {e=} {chat_id} {t}")
        await slow_mode(client)
        return False
      except rpcerrorlist.MessageTooLongError as e:
        warn(f"消息过长，被服务器拒绝: {e=} {chat_id} {short(t)}")
        await sleep(5)
        return False
      except rpcerrorlist.EntityBoundsInvalidError as e:
        if parse_mode ==  "md":
          err(f"failed to send tg msg: {chat_id=} {text=} {e=}", no_send=True)
          resend = True
          parse_mode = None
        else:
          err(f"failed to send tg msg({parse_mode=}): {chat_id=} {text=} {e=}", no_send=True)
      except ValueError as e:
        if e.args[0] == 'Failed to parse message':
          err(f"发送tg消息失败: {chat_id} {type(t)} {e=} {t=}")
        return False
      except Exception as e:
        if client is TB:
          no_send = True
        else:
          no_send = False
        err(f"发送tg消息失败: {chat_id} {e=} {t=}", no_send)
        return False

  if resend:
    return await _send_tg(client, lock, last, chats, text, chat_id, correct, tmp_msg, delay, topic, parse_mode=parse_mode, name=name)
  info(f"sent: {chat_id}: {short(text)}")
  return True


@exceptions_handler(no_send=True)
async def send_tg(*args, **kwargs):
  return await _send_tg(TB, tg_send_lock, last_outmsg, tmp_msg_chats, *args, **kwargs)
#  @cross_thread
#  async def send_tg(text, chat_id=CHAT_ID, correct=False, tmp_msg=False, delay=None, topic=None, qt=None):
  #  if qt is not None:
  #    parse_mode = "html"
  #    text = "<blockquote>%s</blockquote>\n%s" % ("\n".join(qt), text)
  #  else:
  #    parse_mode = TB.parse_mode
  #  async with tg_send_lock:
  #    ts = await split_long_text(text, MAX_MSG_BYTES_TG, tmp_msg)
  #    if len(ts) > 1:
  #      tmp_msg = False
  #    info(f"send to tg: {chat_id}: {short(text)}")
  #    k = 0
  #    for t in ts:
  #      await sleep(msg_delay_default)
  #      try:
  #        if chat_id in last_outmsg_bot:
  #          omsg = last_outmsg_bot[chat_id]
  #          if correct is True:
  #            msg = await omsg.edit(t)
  #            correct = False
  #          elif chat_id in tmp_msg_chats_bot:
  #            msg = await omsg.edit(t, parse_mode=parse_mode)
  #          else:
  #            msg = await TB.send_message(chat_id, t, reply_to=topic, parse_mode=parse_mode)
  #        else:
  #          msg = await TB.send_message(chat_id, t, reply_to=topic, parse_mode=parse_mode)
  #        k += 1
  #        if k == len(ts):
  #          last_outmsg_bot[chat_id] = msg
  #          if tmp_msg:
  #            tmp_msg_chats_bot.add(chat_id)
  #          elif chat_id in tmp_msg_chats_bot:
  #            tmp_msg_chats_bot.remove(chat_id)
  #
  #        elif len(ts) > 1:
  #          await sleep(0.5)
  #        if delay is not None:
  #          await sleep(delay)
  #      except rpcerrorlist.FloodWaitError as e:
  #        warn(f"消息发送过快，被服务器拒绝，等待300s: {e=} {chat_id} {t}")
  #        await slow_mode()
  #        return False
  #      except rpcerrorlist.MessageTooLongError as e:
  #        warn(f"消息过长，被服务器拒绝: {e=} {chat_id} {short(t)}")
  #        await sleep(5)
  #        return False
  #      except ValueError as e:
  #        if e.args[0] == 'Failed to parse message':
  #          err(f"发送tg消息失败: {chat_id} {type(t)} {e=} {t=}")
  #        return False
  #      except Exception as e:
  #        err(f"发送tg消息失败: {chat_id} {e=} {t=}")
  #        return False
  #  info(f"send ok: {chat_id} {short(text)}")
  #  return True


last_outmsg2 = {}
tmp_msg_chats2 = set()


@exceptions_handler(no_send=True)
async def send_tg2(*args, **kwargs):
  return await _send_tg(UB, tg_send_lock2, last_outmsg2, tmp_msg_chats2, *args, **kwargs)
#  @cross_thread
#  async def send_tg2(text, chat_id=CHAT_ID, correct=False, tmp_msg=False, delay=None):
#    #  if chat_id == GROUP_ID:
#    #    global tg_msg_cache_for_bot2
#    #    if "bot: " + text == tg_msg_cache_for_bot2:
#    #      tg_msg_cache_for_bot2 = None
#    #      info("重复消息，停止发送")
#    #      return True
#    async with tg_send_lock2:
#      ts = await split_long_text(text, MAX_MSG_BYTES_TG, tmp_msg)
#      if len(ts) > 1:
#        tmp_msg = False
#      #  if chat_id in last_outmsg:
#      #    omsg = last_outmsg[chat_id]
#      #  else:
#      #    omsg = None
#      k = 0
#      for t in ts:
#        await sleep(msg_delay_default)
#        try:
#          #  if type(chat_id) is int and chat_id > 0:
#          #    # chat_id 此处可以不考虑符号
#          #    peer = await UB.get_input_entity(chat_id)
#          #  if omsg is not None and ( correct is True or chat_id in tmp_msg_chats ):
#          #      msg = await omsg.edit(t)
#          if chat_id in last_outmsg:
#            omsg = last_outmsg[chat_id]
#            if correct is True:
#              msg = await omsg.edit(t)
#              correct = False
#            elif chat_id in tmp_msg_chats:
#              msg = await omsg.edit(t)
#            else:
#              msg = await UB.send_message(chat_id, t)
#            #  omsg = None
#            #  last_outmsg.pop(chat_id)
#          else:
#            msg = await UB.send_message(chat_id, t)
#            #  msg = await UB.send_message(await get_entity(chat_id), t)
#          k += 1
#          if k == len(ts):
#            #  if chat_id == GROUP_ID:
#            #    #  wait_for_msg_form_bot2(msg, chat_id)
#            #    asyncio.create_task(wait_for_msg_form_bot2(msg, chat_id))
#            last_outmsg[chat_id] = msg
#            if tmp_msg:
#              tmp_msg_chats.add(chat_id)
#            elif chat_id in tmp_msg_chats:
#              tmp_msg_chats.remove(chat_id)
#
#          elif len(ts) > 1:
#            await sleep(0.5)
#          if delay is not None:
#            await sleep(delay)
#        except rpcerrorlist.FloodWaitError as e:
#          warn(f"消息发送过快，被服务器拒绝，等待300s: {e=} {chat_id} {t}")
#          #  await sleep(300)
#          await slow_mode()
#          return False
#        except rpcerrorlist.MessageTooLongError as e:
#          warn(f"消息过长，被服务器拒绝: {e=} {chat_id} {short(t)}")
#          await sleep(5)
#          return False
#        except ValueError as e:
#          if e.args[0] == 'Failed to parse message':
#            err(f"发送tg消息失败: {chat_id} {type(t)} {e=} {t=}")
#          return False
#        except Exception as e:
#          err(f"发送tg消息失败: {chat_id} {e=} {t=}")
#          return False
#          #  raise
#        #  await sleep(len(t.encode())/MAX_MSG_BYTES_TG+0.2+msg_delay_default)
#      #  if correct:
#      #    last_outmsg[chat_id] = msg
#    info(f"send ok: {chat_id} {short(text)}")
#    return True
#    chat = await get_entity(CHAT_ID, True)
#    await UB.send_message(chat, text)

@exceptions_handler(no_send=True)
@cross_thread
async def sendg(text, jid=None, room=None, client=None, name="**C bot:** ", **kwargs):
  if name:
    text = f"{name}{text}"
  #  sendme(text)
  info(f"sending xmpp group msg: {jid} {text}")
  if jid is None:
    jid = log_group_private
  recipient_jid = JID.fromstr(jid)
  msg = aioxmpp.Message(
      to=recipient_jid,  # recipient_jid must be an aioxmpp.JID
      type_=aioxmpp.MessageType.GROUPCHAT,
  )
  # None is for "default language"
  msg.body[None] = text

  return await __send(msg, client=client, room=rooms[jid], **kwargs)
  #  room = rooms[jid]
  #  if room is not None:
  #    return await __send(msg, client=client, room=room, **kwargs)
  #
  #  if client is None:
  #    client = XB
  #  #  return await client.send(msg)
  #  #  if client is not None:
  #  return await __send(msg, client, **kwargs)
    #  res = room.send_message(msg)
    #  # https://docs.zombofant.net/aioxmpp/devel/api/public/muc.html?highlight=room#aioxmpp.muc.Room.send_message
    #  if asyncio.iscoroutine(res):
    #    res = await res
    #    if res is None:
    #      dbg(f"room send: finally: {res=}")
    #      return True
    #    else:
    #      info(f"room send: finally: {res=}")
    #      return False
    #  else:
    #    info(f"room send res is not coroutine: {res=}")
    #    return False
  #  else:
  #    warn(f"need client or room")
  #    return False


@exceptions_handler
async def mt_read():
  # api.xmpp
  MT_API = "127.0.0.1:4247"
  url = "http://" + MT_API + "/api/stream"
  #  session = await init_aiohttp_session()
  info("start read msg from mt api...")
  line = None
  while True:
    try:
      async with aiohttp.ClientSession() as session:
        #  async with session.get(url, timeout=0, read_bufsize=2**20) as resp:
          #  print("N: mt api init ok")
          #  resp.content.read()
          #  async for line in resp.content:
          #    #  info("I: got a msg from mt api: %s", len(line))
          #    #  print(f"I: original msg: %s" % line)
          #    await mt2tg(line)

        async with session.get(url, timeout=0, read_bufsize=2**20*4, chunked=True) as resp:
          info("mt api init ok")
          #  await mt_send("N: tggpt: mt read: init ok")
          line = b""
          async for data, end_of_http_chunk in resp.content.iter_chunks():
            line += data
            #  info(f"read bytes: {len(data)}")
            if end_of_http_chunk:
              #  info(f"read end: {len(line)}")
              # # print(buffer)
              # await send_mt_msg_to_queue(buffer, queue)
              #  await mt2tg(line)
              #  asyncio.create_task(mt2tg(line))
              asyncio.create_task(msgmt(line))
              info(f"from mt: {len(line)}")
              line = b""

    except ClientPayloadError:
      err("mt closed, data lost")
    except ClientConnectorError:
      warn("mt api is not ok, retry...")
    except asyncio.CancelledError as e:
      info(f"该任务被要求中止")
      raise
    except ValueError as e:
      #  print("W: maybe a msg is lost")
      err(f"{e=} line: {line}")
      raise
    except Exception as e:
      err(f"{e=} line: {line}")
      raise
    await sleep(5)

#  @exceptions_handler
#  async def titlebot(msgd):
#
#    await sleep(5)
#    text = msgd['text']

@exceptions_handler
async def msgmt(msg):
  '''
  #       Data sent: 'GET /api/stream HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
  #      Data received: 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nDate: Wed, 19 Jan 2022 02:03:29 GMT\r\nTransfer-Encoding: chunked\r\n\r\nd5\r\n{"text":"","channel":"","username":"","userid":"","avatar":"","account":"","event":"api_connected","protocol":"","gateway":"","parent_id":"","timestamp":"2022-01-19T10:03:29.666861315+08:00","id":"","Extra":null}\n\r\n'
  2024-05-07 17:26:25,343 [INFO] tggpt.bot [bot.info:157]: msg of mt_read: {'text': 'ping', 'channel': 'bebat', 'username': 'X liqsliu_: ', 'userid': 'bebat@muc.pimux.de/liqsliu_', 'avatar': 'https://wtfipfs.eu.org/0789fa8d/bebat_muc_pimux_de_liqsliu_.png', 'account': 'xmpp.pimux', 'event': '', 'protocol': 'xmpp', 'gateway': 'test', 'parent_id': '', 'timestamp': '2024-05-07T17:26:25.22885781+08:00', 'id': '', 'Extra': None}
  2024-05-07 17:26:25,778 [INFO] tggpt.bot [bot.mt_send:1806]: res of mt_send: {"text":"pong. now tasks: 0/0","channel":"api","username":"C bot","userid":"","avatar":"","account":"api.cmdres","event":"","protocol":"api","gateway":"test","parent_id":"","timestamp":"2024-05-07T17:26:25.367596549+08:00","id":"","Extra":null}
  '''
  try:
      msg = msg.decode()
      if not msg or msg.startswith("HTTP/1.1"):
        info("I: ignore init msg")
        return

      msgd = json.loads(msg)
  except json.decoder.JSONDecodeError:
      err("fail to decode msg from mt")
      print("################")
      print(msg)
      print("################")
      #  info = "E: {}\n==\n{}\n==\n{}".format(sys.exc_info()[1], traceback.format_exc(), sys.exc_info())
      #  err(info)
      err("E: failed to decode msg from mt...", exc_info=True, stack_info=True)
      return

  account = msgd["account"]
  #  if account == "api.cmdres":
  #    info("I: ignore msg from cmdres")
  #    return
  name = msgd["username"]
  text = msgd["text"]
  gateway = msgd["gateway"]
  #  if gateway == 'me':
  #    if text:
  #      global last_mt_res_jid
  #      if text.startswith("X "):
  #        tmp = text.splitlines()[0]
  #        if ': ' in tmp:
  #          tmp = tmp.split(': ', 1)[0]
  #          if ' ' in tmp:
  #            tmp = tmp.split(' ', 1)[1]
  #            if tmp in me:
  #              last_mt_res_jid = tmp
  #              text = text.split(': ', 1)[1]
  #      warn(f"reply to {last_mt_res_jid}")
  #      if last_mt_res_jid:
  #        await send(text, last_mt_res_jid)
  #    return

  if msgd["Extra"]:
    dbg("original msg of mt_read: %s" % msgd)
    # file
    #,"id":"","Extra":{"file":[{"Name":"proxy-image.jpg","Data":"/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAA ... 6P9ZgOT6tI33Ff5p/MAOfNnzPzQAN4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAGQAAYAkAAGTGAAAAAAAAwsAAHLAAAK//9k=","Comment":"","URL":"https://liuu.tk/ddb833ad/proxy_image.jpg","Size":0,"Avatar":false,"SHA":"ddb833ad"}]}}\n\r\n'
    files = msgd["Extra"]["file"]
    for file in files:
      if text:
        if text == file["Name"]:
          text = ""
        else:
          text += "\n\n"
      if file["Comment"]:
        text += file["Comment"]
        text += " "
        #  if text:
        #  else:
        #    text = file["Comment"]
        #    text += " "
      else:
        if text:
          pass
        elif len(files) == 1:
          text = "{}".format(file["URL"])
          break
      text += "[{}]({})".format(file["Name"], file["URL"])
    msgd.pop("Extra")
    msgd['text'] = text
    info("removed file info from mt api(saved url)")
  else:
      msgd.pop("Extra")
      info("removed file info from mt api(empty)")

  #  print(f"I: got msg: {name}: {text}")
  if not text:
    info(f"I: ignore msg: no text {msgd=}")
    return
  if not name:
    info(f"I: ignore msg: no name {msgd=}")
    return

  #  if name == "C twitter: ":
  #      return
  #  if name.startswith("C "):
  #    info("I: ignore msg: C ")
  #    return
  #  if name.startswith("X "):
  #    info("I: ignore msg: X ")
  #    return
  #  if name.startswith("**C "):
  #    info("I: ignore msg: **C ")
  #    return

  #  if len(username.splitlines()) > 1:
  #    pass
  #  # need fix
  #  if "gateway11" in MT_GATEWAY_LIST:
  #      if gateway == "gateway1":
  #          gateway = "gateway11"

  #  if gateway == "test":
  #    pass
  #  else:
  #    return
  info("msg from mt: %s" % msgd)

  #  info("got msg from mt: {}".format(msgd))
  #      if name == "C Telegram: ":
  if gateway == "gateway1":

    qt = name.splitlines()
    #  if '\n' in name:
    if len(qt) > 1:
      name = qt.pop(-1)
      #  rname = name[:-2]
      #  qt = '\n'.join(ls[:-1])
      #  text = f"{text}\n\n{qt}"
      #  qt = '\n> '.join(ls[:-1])
      #  name2 = f"> {qt}\n**{rname}:** "
    else:
      qt = None

    rname = name[:-2]
    name2 = f"**{rname}:** "

    text2 = f"{name2}{text}"

    for m in get_mucs(main_group):
      #  if await send1(text2, m, nick=rname) is False:
      #    warn(f"failed: {m} {text1}")
      #    return
      asyncio.create_task( send_xmpp(text2, m, nick=rname, qt=qt) )


    await send_tg(text2, GROUP_ID, qt=qt)
    await send_tg(text2, GROUP2_ID, topic=GROUP2_TOPIC, qt=qt)


    #  res = await run_cmd("{}\n\n{}".format(text, "\n".join(qt)), gateway, name, qt=qt)
    res = await run_cmd(text, gateway, name, qt=qt)
    if res is True:
      return
    if res:
      #  await mt_send_for_long_text(res, gateway)
      asyncio.create_task( mt_send_for_long_text(res, gateway) )
      res = f"**C bot:** {res}"
      for m in get_mucs(main_group):
        #  if await send1(res, m, nick="C bot") is False:
        #    warn(f"failed: {m} {res}")
        #    return
        asyncio.create_task( send_xmpp(res, m, nick="C bot") )
      await send_tg(res, GROUP_ID)
      await send_tg(res, GROUP2_ID, topic=GROUP2_TOPIC)
    #    if await send1(f"{name}{text}", m, name) is False:
    #      return
    #    if res:
    #      if await send1(f"{name}{res}", m, "C bot") is False:
    #        return


  #  except Exception as e:
  #    #  info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
  #    #  err(info)
  #    err("error: msg from mt to tg: ", exc_info=True, stack_info=True)
  #    #  await NB.send_message(MY_ID, info)
  #    await sleep(5)



@exceptions_handler
async def send_to_tg_bot(text, chat_id):
  peer = await get_entity(bot_name)
  #  chat = await get_entity(chat_id, True)
  msg = await UB.send_message(peer, text)
  #  if src:
  #    mtmsgsg[src][msg.id] = []
  #  info(f"res of send: {msg.stringify()}")
  #  gid_src[msg.id] = src
  #  if src not in mtmsgsg:
  #    mtmsgsg[src] = {}
  #  mtmsgsg[src][msg.id] = [msg]
  #  mtmsgsg[src][msg.id] = [None]
  return msg.id



@exceptions_handler
async def clear_history(src=None):
  #  music_bot_state.clear()
  #  await sleep(1)
  #  for g in queues:
  if src:

    if src in mtmsgsg:
      ms = mtmsgsg[src]
      ms.clear()
  else:
    for g in mtmsgsg:
      mtmsgs = mtmsgsg[g]
      mtmsgs.clear()
    #  await mt_send(f"cleaned: {mtmsgsg=}", gateway="test")
  info("reset ok")

#  import pb
#  pb.init()


import os, sys, argparse
import argcomplete
import pbincli.actions
from pbincli.api import PrivateBin
from pbincli.utils import PBinCLIException, PBinCLIError, validate_url_ending

@cross_thread(need_main=False)
def pvb_init(server=None):
  CONFIG_PATHS = [
    os.path.join(".", "pbincli.conf", ),
    os.path.join(os.getenv("HOME") or "~", ".config", "pbincli", "pbincli.conf")
  ]

  if sys.platform == "win32":
    CONFIG_PATHS.append(os.path.join(os.getenv("APPDATA"), "pbincli", "pbincli.conf"))
  elif sys.platform == "darwin":
    CONFIG_PATHS.append(os.path.join(os.getenv("HOME") or "~", "Library", "Application Support", "pbincli", "pbincli.conf"))


  def strtobool(value):
    try:
      return {
        'y': True, 'yes': True, 't': True, 'true': True, 'on': True, '1': True,
        'n': False, 'no': False, 'f': False, 'false': False, 'off': False, '0': False,
      }[str(value).lower()]
    except KeyError:
      raise ValueError('"{}" is not a valid bool value'.format(value))


  def read_config(filename):
    """Read config variables from a file"""
    settings = {}
    with open(filename) as f:
      for l in f.readlines():
        if len(l.strip()) == 0:
          continue
        try:
          key, value = l.strip().split("=", 1)
          if value.strip().lower() in ['true', 'false']:
            settings[key.strip()] = bool(strtobool(value.strip()))
          else:
            settings[key.strip()] = value.strip()
        except ValueError:
          PBinCLIError("Unable to parse config file, please check it for errors.")
    return settings

  parser = argparse.ArgumentParser(description='Full-featured PrivateBin command-line client')
  parser.add_argument("-d", "--debug", default=False, action="store_true", help="Enable debug output")

  subparsers = parser.add_subparsers(title="actions", help="List of commands")

  # a send command
  send_parser = subparsers.add_parser("send", description="Send data to PrivateBin instance")
  send_parser.add_argument("-t", "--text", help="Text in quotes. Ignored if used stdin. If not used, forcefully used stdin")
  send_parser.add_argument("-f", "--file", help="Example: image.jpg or full path to file")
  send_parser.add_argument("-p", "--password", help="Password for encrypting paste")
  send_parser.add_argument("-E", "--expire", default=argparse.SUPPRESS, action="store",
    choices=["5min", "10min", "1hour", "1day", "1week", "1month", "1year", "never"], help="Paste lifetime (default: 1day)")
  send_parser.add_argument("-B", "--burn", default=argparse.SUPPRESS, action="store_true", help="Set \"Burn after reading\" flag")
  send_parser.add_argument("-D", "--discus", default=argparse.SUPPRESS, action="store_true", help="Open discussion for sent paste")
  send_parser.add_argument("-F", "--format", default="plaintext", action="store",
    choices=["plaintext", "syntaxhighlighting", "markdown"], help="Format of text (default: plaintext)")
  send_parser.add_argument("-q", "--notext", default=False, action="store_true", help="Don't send text in paste")
  send_parser.add_argument("-c", "--compression", default="zlib", action="store",
    choices=["zlib", "none"], help="Set compression for paste (default: zlib). Note: works only on v2 paste format")
  ## URL shortener
  send_parser.add_argument("-S", "--short", default=argparse.SUPPRESS, action="store_true", help="Use URL shortener")
  send_parser.add_argument("--short-api", default=argparse.SUPPRESS, action="store",
    choices=["tinyurl", "clckru", "isgd", "vgd", "cuttly", "yourls", "custom"], help="API used by shortener service")
  send_parser.add_argument("--short-url", default=argparse.SUPPRESS, help="URL of shortener service API")
  send_parser.add_argument("--short-user", default=argparse.SUPPRESS, help="Shortener username")
  send_parser.add_argument("--short-pass", default=argparse.SUPPRESS, help="Shortener password")
  send_parser.add_argument("--short-token", default=argparse.SUPPRESS, help="Shortener token")
  ## Connection options
  send_parser.add_argument("-s", "--server", default=argparse.SUPPRESS, help="Instance URL (default: https://paste.i2pd.xyz/)")
  send_parser.add_argument("-x", "--proxy", default=argparse.SUPPRESS, help="Proxy server address (default: None)")
  send_parser.add_argument("--no-check-certificate", default=argparse.SUPPRESS, action="store_true", help="Disable certificate validation")
  send_parser.add_argument("--no-insecure-warning", default=argparse.SUPPRESS, action="store_true",
    help="Suppress InsecureRequestWarning (only with --no-check-certificate)")
  ## Authorization options
  send_parser.add_argument("--auth", default=argparse.SUPPRESS, action="store",
    choices=["basic", "custom"], help="Server authorization method (default: none)")
  send_parser.add_argument("--auth-user", default=argparse.SUPPRESS, help="Basic authorization username")
  send_parser.add_argument("--auth-pass", default=argparse.SUPPRESS, help="Basic authorization password")
  send_parser.add_argument("--auth-custom", default=argparse.SUPPRESS, help="Custom authorization header in JSON format")
  ##
  send_parser.add_argument("-R", "--random-server", default=argparse.SUPPRESS, help="Comma-separated list of servers with scheme, randomly chosen to to send paste to (default: None)")
  send_parser.add_argument("-L", "--mirrors", default=argparse.SUPPRESS, help="Comma-separated list of mirrors of service with scheme (default: None)")
  send_parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Enable verbose output")
  send_parser.add_argument("-d", "--debug", default=False, action="store_true", help="Enable debug output. Includes verbose output")
  send_parser.add_argument("--json", default=argparse.SUPPRESS, action="store_true", help="Print result in JSON format")
  send_parser.add_argument("--dry", default=False, action="store_true", help="Invoke dry run")
  send_parser.add_argument("stdin", help="Input paste text from stdin", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
  send_parser.set_defaults(func=pbincli.actions.send)

  # a get command
  get_parser = subparsers.add_parser("get", description="Get data from PrivateBin instance")
  get_parser.add_argument("pasteinfo", help="\"PasteID#Passphrase\" or full URL")
  get_parser.add_argument("-p", "--password", help="Password for decrypting paste")
  get_parser.add_argument("-o", "--output", default=argparse.SUPPRESS, help="Path to directory where decoded paste data will be saved")
  ## Connection options
  get_parser.add_argument("-s", "--server", default=argparse.SUPPRESS, help="Instance URL (default: https://paste.i2pd.xyz/, ignored if URL used in pasteinfo)")
  get_parser.add_argument("-x", "--proxy", default=argparse.SUPPRESS, help="Proxy server address (default: None)")
  get_parser.add_argument("--no-check-certificate", default=argparse.SUPPRESS, action="store_true", help="Disable certificate validation")
  get_parser.add_argument("--no-insecure-warning", default=argparse.SUPPRESS, action="store_true",
    help="Suppress InsecureRequestWarning (only with --no-check-certificate)")
  ## Authorization options
  get_parser.add_argument("--auth", default=argparse.SUPPRESS, action="store",
    choices=["basic", "custom"], help="Server authorization method (default: none)")
  get_parser.add_argument("--auth-user", default=argparse.SUPPRESS, help="Basic authorization username")
  get_parser.add_argument("--auth-pass", default=argparse.SUPPRESS, help="Basic authorization password")
  get_parser.add_argument("--auth-custom", default=argparse.SUPPRESS, help="Custom authorization header in JSON format")
  ##
  get_parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Enable verbose output")
  get_parser.add_argument("-d", "--debug", default=False, action="store_true", help="Enable debug output. Includes verbose output")
  get_parser.set_defaults(func=pbincli.actions.get)

  # a delete command
  delete_parser = subparsers.add_parser("delete", description="Delete paste from PrivateBin instance")
  delete_parser.add_argument("pasteinfo", help="Paste deletion URL or string in \"pasteid=PasteID&deletetoken=Token\" format")
  ## Connection options
  delete_parser.add_argument("-s", "--server", default=argparse.SUPPRESS, help="Instance URL (default: https://paste.i2pd.xyz/)")
  delete_parser.add_argument("-x", "--proxy", default=argparse.SUPPRESS, help="Proxy server address (default: None)")
  delete_parser.add_argument("--no-check-certificate", default=argparse.SUPPRESS, action="store_true", help="Disable certificate validation")
  delete_parser.add_argument("--no-insecure-warning", default=argparse.SUPPRESS, action="store_true",
    help="Suppress InsecureRequestWarning (only with --no-check-certificate)")
  delete_parser.add_argument("--auth", default=argparse.SUPPRESS, action="store",
    choices=["basic", "custom"], help="Server authorization method (default: none)")
  delete_parser.add_argument("--auth-user", default=argparse.SUPPRESS, help="Basic authorization username")
  delete_parser.add_argument("--auth-pass", default=argparse.SUPPRESS, help="Basic authorization password")
  delete_parser.add_argument("--auth-custom", default=argparse.SUPPRESS, help="Custom authorization header in JSON format")
  ##
  delete_parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Enable verbose output")
  delete_parser.add_argument("-d", "--debug", default=False, action="store_true", help="Enable debug output. Includes verbose output")
  delete_parser.set_defaults(func=pbincli.actions.delete)

  # Add argcomplete trigger
  argcomplete.autocomplete(parser)

  # parse arguments
  #  args = parser.parse_args()
  global pvb_args, pvb_client, pvb_CONFIG
  pvb_args = parser.parse_args( args=["send", "-t", "t", "--json"])

  pvb_CONFIG = {
    'server': 'https://paste.i2pd.xyz/',
    'random_server': None,
    'mirrors': None,
    'proxy': None,
    #  'expire': '1day',
    'expire': 'never',
    'burn': False,
    'discus': False,
    'format': None,
    'short': False,
    'short_api': None,
    'short_url': None,
    'short_user': None,
    'short_pass': None,
    'short_token': None,
    'output': None,
    'no_check_certificate': False,
    'no_insecure_warning': False,
    'compression': None,
    'auth': None,
    'auth_user': None,
    'auth_pass': None,
    'auth_custom': None,
    'json': False
  }

  for key in pvb_CONFIG.keys():
    var = "PRIVATEBIN_{}".format(key.upper())
    if var in os.environ: pvb_CONFIG[key] = os.getenv(var)
    # values from command line switches are preferred
    args_var = vars(pvb_args)
    if key in args_var:
      pvb_CONFIG[key] = args_var[key]

  #  args.text = "test"
  #  args.json = argparse.SUPPRESS
  #  args.func=pbincli.actions.send

  #  import io
  pvb_init2(server)

def pvb_init2(server=None):
  global pvb_args, pvb_client, pvb_CONFIG
  if server is not None:
    pvb_CONFIG["server"] = server
  pvb_client = PrivateBin(pvb_CONFIG)

#  def sendpv(text):
@exceptions_handler
@cross_thread(need_main=False)
async def pvb(text, server=None):
  if server is not None:
    pvb_init2(server)
  pvb_args.text = text
  try:
    orig = sys.stdout
    #  tmp_for_pvb_print.seek(0)
    tmp_for_pvb_print = io.StringIO()
    sys.stdout = tmp_for_pvb_print
    pbincli.actions.send(pvb_args, pvb_client, settings=pvb_CONFIG)
    #  args.func(args, api_client, settings=CONFIG)
  except PBinCLIException as pe:
    raise PBinCLIException("error: {}".format(pe))
  #  except Exception as e:
  #    #  print(f"E: {e=}")
  except SystemExit as e:
    sys.stdout = orig
    warn("failed", e=e)
  finally:
    sys.stdout = orig
  #  except BaseException as e:
  #    print(f"E: {e=}")
  #  return tmp_for_pvb_print.getvalue()
  res = tmp_for_pvb_print.getvalue()
  if "\n" in res:
    warn(f"wrong format res: {res=}")
    res = res.splitlines()[-1]

#  async def pvb(text):
  #  fu = run_cb_in_thread(pb.send, text)
  #  fu = run_cb_in_thread(sendpv, text)
  #  res = await fu
  try:
    j = load_str(res)
    if j["status"] == 0:
      return j["result"]["link"]
    return res
  except Exception as e:
    return f"{e=} {res=}"


pb_list = {
    #  "anon": ["https://api.anonfiles.com/upload", "file"],
    "0x0": ["https://0x0.st/", "file"],
    "senio": ["https://paste.sensio.no/", "file"],
    "senio_text": ["https://paste.sensio.no/", "text"],
    "senio_put": ["https://paste.sensio.no/"],
    "fars": ["https://fars.ee/?u=1", "c"],
    "fars1": ["https://fars.ee/", "c"]
    }
#async def pastebin(data="test", filename=None, url="https://fars.ee/?u=1", fieldname="c", extra={}, **kwargs):
#  @cross_thread
@exceptions_handler
async def pastebin(data=None, filename=None, url=pb_list["fars"][0], fieldname="c", extra={}, ce=None, use=None, **kwargs):
  #  use = "0x0"
  if not data:
    return False
  if use:
    if use not in pb_list:
      use = "fars"
    url = pb_list[use][0]
    fieldname = pb_list[use][1]
  if not ce:
    if url == pb_list["fars"][0]:
      ce = "br"

  headers = {}
  headers.update({'User-agent': "curl/8.12.1"})
  #  headers.update({'Accept': "application/json,text/x-yaml,text/plain,*/*"})
  headers.update({'Accept': "*/*"})

  #  if type(data) is str:
  if isinstance(data, str):
  #    if use == "fars" or use == "0x0":
  #      data = data.encode()
    #  if use == "fars":
    #    data = data.encode()
    #    filename = "-"
    if use == "0x0":
      data = data.encode()
      filename = "-"


  use_json = None
  if isinstance(data, str):
#  data = {"content": data}
#    data = zlib.compress(data)
#    headers = {'Content-Encoding': 'deflate'}
#    data = gzip.compress(data.encode())
#    headers = {'Content-Encoding': 'gzip'}
    if use == "senio_text":
      d = data
    else:
      if ce:
        b = await compress(data.encode(), ce)
        headers = {'Content-Encoding': ce}
        d = { fieldname: b }
      else:
        d = { fieldname: data }
      d.update(extra)
      #  if use == "0x0":
      #    use_json = True

  elif isinstance(data, bytes) or type(data) == BufferedReader or type(data) == TextIOWrapper or type(data) == BytesIO:
    if filename:
      d = file_for_post(data, filename=filename, fieldname=fieldname, **extra)
    else:
      d = {fieldname: data}
      d.update(extra)
  elif isinstance(data, dict):
    d = data
#  elif type(data) == aiohttp.formdata.FormData:
  elif type(data) == FormData:
    d = data
  else:
    return False
  if use_json:
    res, res_headers = await http(url=url, method="POST", json=d, headers=headers, return_headers=True, **kwargs)
  else:
    res, res_headers = await http(url=url, method="POST", data=d, headers=headers, return_headers=True, **kwargs)
#    res = res + "." + filename.split(".")[-1]
  res = res.strip()
  info(f"pb res: {res_headers=} {res}")
  if url == pb_list["fars"][0]:
    if 'Location' in res_headers:
      return res_headers['Location']
    if res.startswith("https://fars.ee/"):
      return res
    else:
      res = await pastebin(data=data, filename=filename, extra=extra, use="0x0", **kwargs)
      warn(f"fallback 0x0: {res}")
      if not res.startswith("https://0x0.st/"):
        warn(f"fallback pvb: {res}")
        return await pvb(text)
  elif url == pb_list["senio"][0]:
    # fixme
    return res
  return res

#  session = None
#  async def init_aiohttp_session():
#    global session
#    if session is None:
#      session = aiohttp.ClientSession()
#      warn("a new session")
#  @cross_thread

@exceptions_handler
async def http(url, method="GET", return_headers=False, *args, **kwargs):
  if "headers" in kwargs:
    headers = kwargs["headers"]
  else:
    headers = {}
    kwargs["headers"] = headers
  if "User-agent" not in headers:
    #  headers.update({'User-agent': "curl/8.12.1"})
    headers.update({'User-agent': UA})
  if "Accept" not in headers:
    headers.update({'Accept': "application/json,text/x-yaml,text/plain,text/html,*/*"})
  if "Accept-Encoding" not in headers:
    headers.update({
      #  "Accept-Encoding": "br;q=1.0, gzip;q=0.8, deflate;q=0.5"
      "Accept-Encoding": "gzip, deflate, br, zstd"
      #  "Accept-Encoding": "deflate"
      })
  res = None
  data = None
  html = None
  #  await init_aiohttp_session()
  async with aiohttp.ClientSession() as session:
    try:
      info(f"{method}: {url}")
      res = await session.request(url=url, method=method, *args, **kwargs)
    except asyncio.TimeoutError as e:
      #  raise
      err(f"请求超时 {e=} {url=}")
    except Exception as e:
      err(f"请求失败 {e=} {url=}")
    else:
      try:
        async with res:
          info(f"http status: {res.status} {res.reason} url: {res.url}")
      #    res.raise_for_status()
          if res.status == 304:
            text = await res.text()
            warn(f"W: http status: {res.status} {res.reason} {res.headers=} {res.url=} >> ignore: {text}")
          elif res.status != 200 and res.status != 201:
            text = await res.text()
            html = f"E: error http status: {res.status} {res.reason} headers: {res.headers} url: {res.url} res: {text}"
            err(html)
            #  return
          else:
            # print(type(res))
            # print("Status:", res.status)
            # print("Content-type:", res.headers['content-type'])
            # print("Content-Encoding:", res.headers['Content-Encoding'])
            # print('Content-Length:', res.headers['Content-Length'])
              # print(res)
              # print("q: ", res.request_info)
              # print("a: ",  res.headers)
            length =  0
            if 'Content-Length' in res.headers:
              length = int(res.headers['Content-Length'])
            #  if 'Content-Length' in res.headers and int(res.headers['Content-Length']) > HTTP_RES_MAX_BYTES:
            if length > HTTP_RES_MAX_BYTES:
              err(f"文件过大，终止下载: ({length}) {url}")
            elif 'Transfer-Encoding' in res.headers and res.headers['Transfer-Encoding'] == "chunked":
              #  async for data in res.content.iter_chunked(HTTP_RES_MAX_BYTES):
              #    break
              data = b""
              async for tmp, _ in res.content.iter_chunks():
                data += tmp
                info(f"http downlod chunk ok: ({length}) | {len(tmp)} > {len(data)}")
                if len(data) > HTTP_FILE_MAX_BYTES:
                  break
            else:
              info(f"http downlod ok: ({length})")
            # if res.headers['content-type'] == "text/plain; charset=utf-8":
              #  data = await res.read()
              data = await res.content.read(HTTP_FILE_MAX_BYTES)
      except ClientPayloadError as e:
        err(f"读取失败: {e=} {url=}")
        #  return
      #  except Exception as e:
      #    err(f"http connect error: {e=} {url=}")

      if data:
        info(f"http body data: {len(data)} {short(data)}")
        #  try:
        if "Content-Encoding" in res.headers:
          info(f"start to decompress: %s {type(data)} {short(data)}" % res.headers['Content-Encoding'])
          data = await decompress(data, res.headers['Content-Encoding'])
          #  if b:
          #    data = b
          #  else:
          #    warn("解压失败: {} url: {}\n".format(res.headers['Content-Encoding'], url))
            #  return data
        #  except brotli.error as e:
        #    err(f"解压时出现错误: {e=} {res.headers=} {data[:512]}")
        #  except Exception as e:
        #    err(f"解压时出现错误: {e=} {res.headers=} {short(data)}")
        try:
          # if "text/plain" in res.headers['content-type']:
          if "text" in res.headers['content-type']:
            # return await res.text()
            html = data.decode(errors='ignore')
          else:
            #  html = data.decode()
            #  html = data
            html = data.decode(errors='ignore')
          info(f"http res: {short(html)} url: {url}")
        except UnicodeDecodeError as e:
          err(f"docode failed: {e=} res data: {short(data)}")
          html = data
  if return_headers:
    if res:
      return html, res.headers
    else:
      return html, None
  else:
    return html

#  async def mt_send(*args, **kwargs):
#    asyncio.create_task(_mt_send(*args, **kwargs))
#    return True

#  async def mt_send(text="null", name="bot", gateway="test", qt=None):
@exceptions_handler
async def mt_send(text="null", gateway="gateway1", name="C bot", qt=None):
  #  # api.xmpp
  #  MT_API = "127.0.0.1:4247"
  #  #  if gateway == 'me':
  #  #    # api.xmpp
  #  #    MT_API_RES = "127.0.0.1:4247"
  #  #  else:
  #  #    # api.cmdres
  #  #    MT_API_RES = "127.0.0.1:4249"
  #  # send msg to matterbridge
  #  url = "http://127.0.0.1:4247/api/message"
  #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
  #  url="http://127.0.0.1:5555/api/message"
#  if not username.startswith("C "):
#    username = "T " + username
  if qt is not None:
    #  name = "{}\n\n{}".format("> " + "\n> ".join(qt.splitlines()), name)
    name = "> {}\n\n{}".format("\n> ".join(qt), name)
#  gateway="gateway0"
  data = {
    "text": "{}".format(text),
    "username": "{}".format(name),
    "gateway": "{}".format(gateway)
  }
  #  async with mt_send_lock:
  info(f"send to mt: {short(text)}")
  res = await http("http://127.0.0.1:4247/api/message", method="POST", json=data)
  #  info("res of mt_send: {}".format(res))
  return True
  return res

#  async def mt_send_for_long_text(text, gateway='test'):
#    fn='gpt_res'
#    async with queue_lock:
#      async with aiofiles.open(f"{SH_PATH}/{fn}", mode='w') as file:
#        await file.write(text)
#      #  os.system(f"{SH_PATH}/sm4gpt.sh {fn} {gateway}")
#      return await asyncio.to_thread(os.system, f"{SH_PATH}/sm4gpt.sh {fn} {gateway}")

@exceptions_handler
@cross_thread(need_main=False)
async def mt_send_for_long_text(text, gateway="gateway1", name="C bot", *args, **kwargs):
  if not isinstance(text, str):
    text = "%s" % text
  info(f"send to mt: {gateway} {text}")
  global mt_send_lock
  if mt_send_lock is None:
    mt_send_lock = asyncio.Lock()
  async with mt_send_lock:
    need_delete = False
    if os.path.exists(f"{SH_PATH}"):
      fn = f"{SH_PATH}/SM_LOCK_{gateway}"
      for _ in range(3):
        if os.path.exists(fn):
          info(f"busy: {gateway} {fn}")
          await sleep(1)
        else:
          break

      await write_file(text, fn, "w")
      need_delete = True

    for i in await split_long_text(text):
      #  if await send(i, *args, **kwargs) is not True:
      if await mt_send(i, gateway=gateway, name=name, *args, **kwargs) is not True:
        break
      #  await mt_send(res, gateway=gateway, name="")
      name = ""
    if need_delete:
      os.remove(fn)
      #  fu = run_cb_in_thread(os.remove, fn)
      #  await fu
  return True





#  @exceptions_handler
#  @UB.on(events.NewMessage(outgoing=True))
#  async def my_event_handler(event):
#    #  if 'hello' in event.raw_text:
#    #    await event.reply('hi!')
#    #  if 'new_chat' in event.raw_text:
#    #    print(event.stringify())
#    msg = event.message
#    text = msg.raw_text
#    if event.chat_id != gpt_bot:
#      if debug:
#        print("<%s %s" % (event.chat_id, text))
#      return
#    if event.chat_id != gpt_bot:
#      if debug:
#        print(">%s %s" % (event.chat_id, text))
#      return
#    if text:
#      print("me: %s" % text)


async def tg_upload_media(path=None, src=None, chat_id=CHAT_ID, caption=None, in_memory=False, max_time=download_media_time_max):
  if path is None:
    err(f"need file path: {path}")
    return
  if path.endswith(".mp4"):
    force_document = False
    supports_streaming = True
  else:
    force_document = True
    supports_streaming = False
  if not path.startswith("https://"):
    if type(path) is str:
      fp = Path(path)
      #  file_path = Path(file_path)
    else:
      fp = path
    cb = None
    length = os.path.getsize(path)
    send("准备上传: {} {}".format(hbyte(length), fp.name), src, tmp_msg=True)
    if length > 100000:
      last_time = [time.time(), 0]
      start_time = time.time()
      def cb(sent, total):
        last_time[1] = sent
        #  if len(last_time) == 2:
        #    last_time.append(total)
        #    asyncio.create_task(send("开始上传: {:.1f}MB".format(total-sent/1024/1024), src, correct=True))
        #  else:
          #  total = last_time[2]
        if sent == length:
          send("上传完成，用时: {}s".format(int(time.time()-start_time)), src, tmp_msg=True)
        else:
          now = time.time()
          if now - last_time[0] > interval:
            last_time[0] = now
            send("{}".format(hbyte(length-sent)), src, tmp_msg=True)
            info("剩余 {}".format(hbyte(length-sent)))
      #  async def update_tmp_msg():
      #    while True:
      #      await sleep(interval)
      #      if len(last_time) == 2:
      #        await send("准备中", src, correct=True)
      #        if time.time() - last_time[0] > 15:
      #          await send("准备超时，可能网络过慢或者文件太小", src, correct=True)
      #          break
      #      else:
      #        current = last_time[1]
      #        total = last_time[2]
      #        if current == total:
      #          await send("上传完成", src)
      #          break
      #        await send("{:.1f}M".format((total-current)/1024/1024), src, correct=True)
          #  if time.time() - last_time[0] > max_time:
          #    await send("超时", src, correct=True)
          #    break
      #  if src:
      #    t = asyncio.create_task(update_tmp_msg())
    h = await UB.upload_file(path, progress_callback=cb)
  else:
    h = path
    if h.endswith(".webp"):
      await UB.send_message(chat_id, h)
  try:
    res = await UB.send_file(chat_id, file=h, caption=caption, force_document=force_document, supports_streaming=supports_streaming)
  except Exception as e:
    res = await UB.send_file(chat_id, file=h, caption=caption, force_document=force_document)
  return res




def get_timeout(size):
  if size is None:
    return download_media_time_max
  #  timeout = size/1024/1024*1.5 + 15
  #  timeout = 11720/73-14553000/5329/(size/1024/1024+1250/73)
  #  if timeout > upload_media_time_max:
  #    timeout = upload_media_time_max
  #  elif timeout < 10:
  #    timeout = 10
  timeout = 247080/233-10768058155008000/54289/(size+43751833600/233)
  return timeout


def hbyte(size):
  if size > 512*1024:
    return "{:.1f}M".format(size/1024/1024)
  else:
    return "{:.0f}K".format(size/1024)

def short(text, length=64):
  # for log out
  if isinstance(text, bytes):
    text = text.decode("utf-8", errors="ignore")
  elif not isinstance(text, str):
    text = "{!r}".format(text)
  text = re.sub(shell_color_re,  "", text)
  #  text = text.strip()
  text = text.replace("\n", "\\n")
  if len(text) > length:
    return "{}...{}/{}".format(text[:length], length, len(text))
  else:
    return text

#  last_time = {}

tg_download_tasks = set()

async def tg_download_media(msg, src=None, path=f"{DOWNLOAD_PATH}/", in_memory=False, max_wait_time=download_media_time_max):
#  await client.download_media(message, progress_callback=callback)
  #  async with downlaod_lock:
  if msg.file:
    size = msg.file.size
    res = ''
    if size:
      res += f"{hbyte(size)}"
    if msg.file.name:
      res += f" {msg.file.name}"
    send("准备下载: {}".format(res), src, tmp_msg=True)
    timeout = get_timeout(size)
    if max_wait_time > timeout:
      timeout = max_wait_time
  else:
    warn(f"no file: {msg}")
    return
  #  await mt_send(f"{res} 下载中...", gateway=gateway)
  #  res = f"{res} 下载中..."
  #  if src and res:
  #    await send(res, src, xmpp_only=True, correct=True)
  #  last_time[src] = time.time()
  last_time = [time.time(), 0, size]

  # Printing download progress
  def cb(current, total):
    #  last_time[0] = time.time()
    last_time[1] = current
    info("剩余 {}".format(hbyte(total-current)))
    #  if len(last_time) == 2:
    #    last_time.append(total)
    #    asyncio.create_task(send("开始下载 {} {}".format(hbyte(size), res), src))
    #  print('Downloaded', current, 'out of', total,
    #    'bytes: {:.2%}'.format(current / total))
    #  if time.time() - last_time[src] > interval:
    #  if time.time() - last_time[0] > interval:
    #    #  await mt_send("{:.2%} %s/%s".format(current / total, current, total), gateway=gateway)
    #    #  asyncio.create_task(mt_send("{:.2%} {}/{} bytes".format(current / total, current, total), gateway=gateway))
    #    asyncio.create_task(send("{} {:.2%} {:.2f}/{:.2f}MB {:.1f}MB/s".format(res, current / total, current/1024/1024, total/1024/1024, (current-last_time[1])/(time.time()-last_time[0])/1024/1024), src, correct=True))
    #    #  last_time[src] = time.time()

  async def update_tmp_msg():
    start_time = last_time[0]
    last_current = 0
    while True:
      await sleep(interval)
      #  now = time.time()-start_time
      current = last_time[1]
      total = last_time[2]
      if current == total:
        send("下载完成：{} 用时: {}s".format(res), src, int(time.time()-start_time), tmp_msg=True)
        break
      #  await send("执行中({:.0f}s)：{} {:.2%} {:.2f}/{:.2f}MB {:.1f}MB/s".format(now, res, current / total, current/1024/1024, total/1024/1024, (current-last_current)/(time.time()-last_time[0])/1024/1024), src, xmpp_only=True, correct=True)
      #  await send("({:.0f}s)：{} {:.2%} {:.2f}/{:.2f}MB {:.1f}MB/s".format(now, res, current / total, current/1024/1024, total/1024/1024, (current-last_current)/(time.time()-last_time[0])/1024/1024), src, correct=True)
      send(hbyte(total-current), src, tmp_msg=True)
      last_time[0] = time.time()
        #  last_current = current


  async def _download_media(msg, path):
    try:
      return await asyncio.wait_for(msg.download_media(path, progress_callback=cb), timeout=timeout)
    except TimeoutError as e:
      err(f"下载失败(超时{timeout}s): {e=}")


  file_path = None
  try:
    if src:
      while src in tg_download_tasks:
        send("下载任务排队中 {}".format(res), src, tmp_msg=True)
        await sleep(interval)
      tg_download_tasks.add(src)
      t = asyncio.create_task(update_tmp_msg())
    t1 = asyncio.create_task(_download_media(msg, path))
    now = time.time()
    while True:
      await sleep(interval)
      if t1.done():
        file_path = t1.result()
        if file_path is None:
          res = f"下载失败(下载速度太慢): {res}"
        break
      if len(last_time) == 2 and time.time() - now > timeout/3:
          t1.cancel()
          file_path = None
          res = f"下载失败(等待超时): {res}"
          return res
        #  else:
        #    info(f"等待上游下载完成：{res}")
      elif time.time() - now > timeout:
        t1.cancel()
        file_path = None
        res = f"下载失败(超时): {res}"
        return res
      if src:
        if src in tg_download_tasks:
          continue
        #  if src not in music_bot_state or music_bot_state[src] < 3:
        #  if src in music_bot_state and music_bot_state[src] > 2:
        #    continue
        info(f"下载中止：{res}")
        path = None
        return f"下载取消: {res}"
  except Exception as e:
    err(f"下载失败 {e=}")
  finally:
    if file_path is None:
      text, nick, d = await print_tg_msg(msg)
      err(f"下载失败 file_path is None: file_msg: {nick}: {text}")
    else:
      if not file_path.startswith("/"):
        file_path = path + file_path
      info(f"下载完成：{res} {file_path}")
    if not t1.done():
      t1.cancel()
    if src:
      if not t.done():
        t.cancel()
      if src in tg_download_tasks:
        tg_download_tasks.remove(src)

  if file_path:
    return file_path
    res = await upload(path)

      #  path = "https://%s/%s" % (DOMAIN, (urllib.parse.urlencode({1: path[len(DOWNLOAD_PATH):]})).replace('+', '%20')[5:])
    t = asyncio.create_task(backup(path))
    await t
    if t.done():
      url = t.result()
    else:
      url = None
    if res:
      #  send(f"{res}\n{path}", src)
      #  send(f"{res}", src)
      info(f"xmpp server is ok: {res}")

      #  asyncio.create_task(backup(path, src))

      if url:
        res += f"\n\n{url}"

      return res
    else:
      warn(f"xmpp server is not ok: {res}")
      return url
  else:
    #  res = f"{res} 下载失败: {path}"
    if src:
      send(res, src)
    warn(res)

def get_buttons(bs):
  tmp = []
  for i in bs:
    if type(i) is list:
      tmp += get_buttons(i)
    else:
      if support(i):
        tmp.append(i)
  return tmp

def support(i):
  i = i.button
  if isinstance(i, KeyboardButton) or isinstance(i, KeyboardButtonCallback):
    return True
  else:
    info(f"ignore button: {i=}")
    return False

def print_buttons(bs, k=0):
  def format_button_text(k, text):
    #  if text[0].isnumeric():
    if text.isnumeric():
      return f"[{text}]"
    else:
      return f"{k}. {text}"
  #  if bs:
  if len(bs) == 1 and type(bs[0]) is list:
    bs = bs[0]
  text = ""
  tmp = []
  #  k = 0
  for i in bs:
    if type(i) is list:
      tmp2 = []
      for j in i:
        if support(j):
          k += 1
          #  t += f"\t{format_button_text(k, j.text)}"
          tmp2.append(format_button_text(k, j.text))
      #  if text != "":
      #    text += "\n%s" % t.strip("\t")
      if tmp2:
        tmp.append("\t".join(tmp2))
    #  else:
    #  elif isinstance(i, KeyboardButton):
    elif support(i):
      k += 1
      #  text += f"\n{k}. {i.text}"
      #  text += f"\n{format_button_text(k, i.text)}"
      tmp.append(format_button_text(k, i.text))
  if tmp:
    text = "\n\n回复序号\n%s" % "\n".join(tmp)
  return text


async def parse_tg_url(url, wtf=1):
  peer = None
  gid = None
  url = url.rstrip("?single")
  #  if "?comment=" in url:
  #    #需要先获取频道绑定的群，然后再在群里根据消息id找，麻烦，先不搞
  #    url = url.split("?comment")[0]
  if url.startswith("https://t.me/"):
    url = url[13:]
    if url.startswith("c/"):
      url = url[2:]
      if url:
        peer = url.split('/',1)[0]
        if peer.isnumeric():
          peer = int(peer)
    else:
      peer = url.split('/',1)[0]
    if peer:
      if "?comment=" in url:
        fpeer = await get_full_entity(peer)
        peer = fpeer.full_chat.linked_chat_id
        gid = url.rsplit('=', 1)[-1]
      elif '/' in url:
        gid = url.rsplit('/', 1)[-1]
  #  if peer:
  #    #  if peer[0] != "-":
  #    if peer.isnumeric():
  #      if wtf == 1:
  #        # channel or super group
  #        peer = f"-100{peer}"
  #        peer = int(peer)
  #      elif wtf == 2:
  #        peer = f"-{peer}"
  #        peer = int(peer)
  if gid:
    gid = int(gid)
  return peer, gid


async def get_commands(chat_id):
  res = await get_full_entity(chat_id)
  tmp = []
  if res.full_user.bot_info is None:
      info(f"not found commands: {res.stringify()}")
      return
  if res.full_user.bot_info.commands is None:
      info(f"not found commands: {res.stringify()}")
      return
  for i in res.full_user.bot_info.commands:
    tmp.append(f"/{i.command}: {i.description}")
  return "\n".join(tmp)

async def get_full_entity(chat_id):
  peer = await UB.get_input_entity(chat_id)
  if isinstance(peer, InputPeerChannel):
    # https://tl.telethon.dev/methods/channels/get_full_channel.html
    res = await UB( telethon.functions.channels.GetFullChannelRequest(channel=peer) )
  elif isinstance(peer, InputPeerChat):
    res = await UB( telethon.functions.messages.GetFullChatRequest(chat_id=peer) )
  else:
    res = await UB( telethon.functions.users.GetFullUserRequest(id=peer) )
  #  print(type(res))
  #  res = await res
  #  print(res.stringify())
  return res

async def get_entity(chat_id, id_only=True, client=None, return_gid=False):
  if client is None:
    client = UB
  #  if isinstance(peer, PeerUser):
  #    #  info(f"PeerUser: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, PeerChat):
  #    #  info(f"PeerChat: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, PeerChannel):
  #    #  info(f"PeerChannel: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, str):
  #    peer = await UB.get_input_entity(peer)
  #  else:
  gid = None
  try:
    if type(chat_id) is str:
      chat_id = load_chat_id(chat_id)
    url = chat_id
    #  chat_id = get_addr(chat_id)
    if type(chat_id) is int:
        peer = chat_id
      #  peer = await UB.get_input_entity(chat_id)
      #  if id_only:
      #    return peer
    elif type(chat_id) is str:
      if url.startswith("@"):
        #  peer = url[1:]
        peer = url
      #  elif url.isnumeric():
      #    peer = int(url)
      #  elif url.startswith("-") and  url[1:].isnumeric():
      #    peer = int(url)
      else:
        p, gid = await parse_tg_url(url)
        if p:
          peer = p
        else:
          peer = url
    elif chat_id is None:
      warn("chat_id is None")
      return
    else:
      peer = url
      #  return False
    if peer:
      info(f"search inputpeer: {peer}")
      try:
        peer = await client.get_input_entity(peer)
        if id_only:
        #  if gid is not None:
          if return_gid:
            return peer, gid
          return  peer
      except TypeError as e:
        err(f"E: {e=}, not found input entity: {peer}")
        return
      except ValueError as e:
        info(f"search inputpeer(use get_peer_id): {peer} {e=}")
        try:
          pid = await client.get_peer_id(peer)
          peer = await client.get_input_entity(pid)
          if id_only:
            if return_gid:
              return peer, gid
            return  peer
        except TypeError as e:
          err(f"E: {e=}, not found input entity(use get_peer_id): {peer}")
          return
        except ValueError as e:
          info(f"not found input entity: {peer} {e=}")

      info(f"search peer: {peer}")
      try:
        peer = await client.get_entity(peer)
        #  if gid is not None:
        if return_gid:
          return peer, gid
        return  peer
      except TypeError as e:
        err(f"E: {e=}, not found entity: {peer} {e=}")
      except ValueError as e:
        info(f"not found entity: {peer=} {e=}")
  except Exception as e:
    #  err(f"{e=}")
    err(e)
  #  raise ValueError(f"无法获取entity: {chat_id=} {peer=}")
  if return_gid:
    return None, gid


def print_entity(e):
  res = ""
  pid = utils.get_peer_id(e)

  if hasattr(e, "first_name"):
    res += "name: %s.%s " % (e.first_name, e.last_name)
  else:
    res += "title: %s " % e.title
  res += "\ntype: %s" % type(e)

  res += "\n"
  if e.username:
    res += "@%s" % e.username
    res += "\nhttps://t.me/%s/" % e.username
  else:
    #  if pid > 0:
    if hasattr(e, "first_name"):
      res += "[%s](tg://openmessage?user_id=%s)" % (pid, pid)
    else:
      res += "[%s](tg://openmessage?chat_id=%s)" % (pid, pid)

  #  res = "peer id: %s" % pid
  res += "\npeer id: `%s`" % pid

  # https://docs.telethon.dev/en/stable/concepts/chats-vs-channels.html#converting-ids
  # https://docs.telethon.dev/en/stable/modules/utils.html#telethon.utils.resolve_id
  res += "\nhttps://t.me/c/%s/" % utils.resolve_id(pid)[0]
  return res

async def parse_tg_file_msg(msg):
  path = None
  backup_task = None

  file = msg.file
  file_name = file.name
  if file.size:
    if file.size > FILE_DOWNLOAD_MAX_BYTES:
      file_info = f"文件过大，终止下载: ({hbyte(file.size)})"
    else:
      file_info = ""
      #  path = await tg_download_media(msg)
      path = await tg_download_media(msg, src=msg.chat_id, max_wait_time=get_timeout(msg.file.size))
      if path is not None:
        #  t = asyncio.create_task(backup(path))
        #  url = await t
        url, backup_task = await backup(path, no_wait=True)
        #  xmpp_url = await upload(path, src)
        #  if xmpp_url:
        #    url = f"- {xmpp_url}\n\n- {url}"
        #  file_info += "\n"
        if file_name:
          file_info += f"[{file_name}]({url})"
        else:
          file_info += url
  else:
    file_info = "文件大小未知，终止下载"
  return file_info, path, backup_task


async def print_tg_msg(msg, download_file=False):
  #  msg = event.message
  #  res = ''
  nick = ""
  if msg.is_private:
    delay = None
    #  res += "@"
    #  peer = await get_entity(event.chat_id, False)
    #  peer = await event.get_chat()
    peer = await msg.get_chat()
    if peer is not None:
      nick += "%s" % peer.first_name
      if peer.last_name is not None:
        #  res += " [%s %s]" % (peer.first_name, peer.last_name)
        #  nick = "G [%s %s]" % (peer.first_name, peer.last_name)
        nick += " %s" % peer.last_name
  else:

    peer = await get_entity(msg.chat_id, False)
    #  if event.is_group:
    if msg.is_group:
      delay = 2
      #  nick += "+"
      nick += "G "
    else:
      delay = 5
      #  if event.is_channel:
      nick += "#"

      #  peer = await event.get_chat()
      if peer is not None:
        #  res += " %s" % peer.title
        #  nick = "G %s" % peer.title
        nick += "%s" % peer.title
    #  print(event.chat_id, event.sender_id, event.from_id)
    #  if event.sender_id: # 如果和chat_id相同就没啥意义,这时候from_id是None

    if msg.from_id:
      #  peer = await get_entity(event.from_id)
      peer = await msg.get_sender()
      #  peer = await get_entity(event.sender_id, False)
      #  peer = await UB.get_input_entity(event.sender_id)
      #  peer = await UB.get_entity(event.from_id)
      if peer is not None:
        if isinstance(peer, User):
          nick += "%s" % peer.first_name
          if peer.last_name is not None:
            nick += " %s" % peer.last_name
        else:
        #  if isinstance(peer, Channel):
          #  res += " %s" % peer.title
          nick += "#%s" % peer.title
  if msg.text:
    text = msg.text
  else:
    text = ""
  if msg.file:
    if download_file is True:
      backup_task = None
      try:
        file_info, path, backup_task = await parse_tg_file_msg(msg)
        if file_info:
          if text:
            text += "\n\n"
          text += file_info

      finally:
        if backup_task is not None:
          await backup_task
          asyncio.create_task(backup(path, delete=True))
    else:
      if msg.file.size:
        text += " %s" % hbyte(msg.file.size)
      if msg.file.name:
        text += " %s" % msg.file.name
  return text, nick, delay



async def get_msg(url, client=None):
  if client is None:
    client = UB
  peer, ids = await get_entity(url, client=client, return_gid=True)
  if peer:
    #  ss = url.split('/')
    #  if len(ss) > 4:
      #  ids = int(ss[-1])
    if ids:
      msg = await client.get_messages(peer, ids=ids)
      if issubclass(type(msg), list):
        # https://docs.telethon.dev/en/stable/modules/helpers.html#telethon.helpers.TotalList
        if len(msg) > 0:
          return msg[0]
        return
      return msg




#  music_bot_state = {}

#  async def change_bridge(bot_name, src, text):
#    peer = await get_entity(bot_name)
#    pid = await UB.get_peer_id(peer)
#    if src not in mtmsgsg:
#      mtmsgsg[src] = {}
#    mtmsgs = mtmsgsg[src]
#
#    #  if pid not in bridges:
#    #    bridges[pid] = src
#    #  target = bridges[pid]
#    if pic not in mtmsgs:
#      mtmsgs[pid] = [src]
#
#    if target != src:
#      if type(target) is dict:
#        bridges[pid] = src
#        target = src
#      await send("coming", src, tmp_msg=True)
#      await send("...", src, tmp_msg=True)
#      if mtmsgs:
#        await sleep(5)
#      info(f"stop link to {target}")
#      await send("bye", target, tmp_msg=True)
#      info(f"link to {src}")
#      await send("typing", src, tmp_msg=True)
#
#      mtmsgs.clear()
#      bridges[pid] = src
#
#    gid = await send_tg(text, pid, return_id=True)
#    return mtmsgs, gid

deleted_tg_msg_ids = set()
forwarded_tg_msg_ids = {}

@exceptions_handler
async def msgtd(event):
  #  if not event.is_private:
  #    return
  #  chat_id = event.sender_id
  chat_id = event.chat_id
  info(f"delete: {chat_id}: {event.deleted_id if len(event.deleted_ids) == 1 else event.deleted_ids}")
  if chat_id == GROUP_ID:
    return
  if chat_id is None:
    warn("chat_id is None")
  elif chat_id not in bridges_tmp:
    #  info(f"chat_id is not in bridges: {chat_id}")
    return
  deleted_tg_msg_ids.update(event.deleted_ids)
  #  src = bridges[chat_id]
    #  if src not in tmp_msg_chats:
  #  if chat_id is None:
  for i in event.deleted_ids:
    if i in forwarded_tg_msg_ids:
      for src in forwarded_tg_msg_ids[i]:
        tmp_msg_chats.add(src)
        info(f"add {src} into tmp_msg_chats")
    else:
      warn(f"not found {i} in {forwarded_tg_msg_ids}")

      #  #  for src in mtmsgsg:
      #  for chat_id in bridges.copy():
      #    #  if chat_id in tmp_msg_chats:
      #    #    continue
      #    src = bridges[chat_id]
      #    if type(src) is dict:
      #      bridges.pop(chat_id)
      #      warn(f"delete old bridge: {src} - {chat_id}")
      #      continue
      #    #  if src in tmp_msg_chats:
      #    #    continue
      #    if src in mtmsgsg:
      #      mtmsgs = mtmsgsg[src]
      #      if chat_id in mtmsgs:
      #        l = mtmsgs[chat_id]
      #        if len(l) > 2:
      #          #  if i in l[2]:
      #          if i == max(l[2]):
      #            #  tmp_msg_chats.add(src)
      #            tmp_msg_chats.update(get_mucs(src))
      #            info(f"set tmp_msg ok, found msg id {i} in chat {src} - {chat_id}")
      #          else:
      #            info(f"unsupported, ignore, found msg id {i} != max({l[2]}) in chat {src} - {chat_id}")
      #        break

  #  if src in last_outmsg:
      #  tmp_msg_chats.add(j)



@exceptions_handler
async def msgtp(event):
  #  chat_id = event.sender_id
  # 私聊这俩都一样
  chat_id = event.chat_id
  if chat_id not in bridges_tmp:
    return
  #  if chat_id != 5815596965:
  #    return
  #  pprint(event)
  #  info(f"{event.is_private=}")
  info(f"{chat_id} update staus: {event}")
  #  if not event.is_private:
  #    return

  src = bridges_tmp[chat_id]
  #  if chat_id in bridges:
  #    src = bridges[chat_id]
  #  else:
  #    return
  send_typing(src)
  return
  res = await get_name(chat_id)
  if event.photo:
    #  await send(f"{bot_name} 正在发送图片", src, tmp_msg=True)
    res += " 正在发送图片"
  elif event.audio:
    res += " 正在发送音频文件"
  elif event.round:
    res += " 正在发送视频文件"
  elif event.sticker:
    res += " 正在发送表情贴纸"
  elif event.geo:
    res += " 正在发送位置"
  elif event.document:
    res += " 正在发送文档"
  elif event.uploading:
    res += " 正在上传文件"
  elif event.typing:
    res += " 正在输入"
  elif event.cancel:
    res += " 正在取消操作"
  else:
    res += "  ..."
  send(res, src, tmp_msg=True)

bot_names = {}
bot_cmds = {}

async def get_name(chat_id=None, username=None):
  if chat_id not in bot_names:
    info(f"get name: {chat_id} {username}")
    if username:
      peer = await get_entity(username, False)
      #  peer = await get_entity(username)
    else:
      peer = await get_entity(chat_id, False)
    chat_id = await UB.get_peer_id(peer)
    bot_names[chat_id] = f"{peer.first_name}"
    if peer.last_name is not None:
      bot_names[chat_id] += " " + peer.last_name
  return bot_names[chat_id]



tg_msg_cache_for_bot2=None
tg_msg_cache_for_bot2_lock=asyncio.Lock()
tg_msg_cache_for_bot2_event=asyncio.Event() # 默认已经clear()

async def wait_for_msg_form_bot2(msg, chat_id):
  global tg_msg_cache_for_bot2
  #  old_msg = None
  #  if chat_id in last_outmsg:
  #    old_msg = last_outmsg[chat_id]
  i = 0
  while i<15:
    if tg_msg_cache_for_bot2 is None:
      pass
    elif "bot: " + (msg.raw_text) != tg_msg_cache_for_bot2:
      tg_msg_cache_for_bot2 = None
    else:
      await msg.delete()
      tg_msg_cache_for_bot2 = None
      last_outmsg.pop(chat_id)
      if chat_id in tmp_msg_chats:
        tmp_msg_chats.remove(chat_id)
      info("found")
      break
    info("wait for bot2")
    await sleep(0.3)
    i+=1


@exceptions_handler
async def msgt(event):
  # msg to UB

  #  if event.chat_id not in id2gateway:
  #    #  print("W: skip: got a unknown: chat_id: %s\nmsg: %s" % (event.chat_id, msg.stringify()))
  #    return
  #  if event.chat_id in id2gateway:
  #  if chat_id == gpt_bot:
  #    pass
  #  if msg.buttons:
  #    info(f"buttons: {msg.buttons=}")
  # https://docs.telethon.dev/en/stable/modules/custom.html#telethon.tl.custom.chatgetter.ChatGetter
  chat_id = event.chat_id
  sender_id = event.sender_id
  msg = event.message
  #  text = msg.text
  text = event.text
  #  info(f"{chat_id} {sender_id}: {msg.id} {short(text) if text is not None else type(msg.file)}")
  #  info(f"{chat_id} {sender_id}: {msg.id} {short(text) if text else type(msg.media)}")
  #  text = msg.message
  info(f"{chat_id} {sender_id}: {short(text) if text is not None and len(text) > 0 else type(msg.media)}_{msg.id}")

  if chat_id is None:
    #  warn(f"chat_id is None")
    warn(f"chat_id is None: {chat_id} {sender_id}: {text}")
    chat_id = sender_id

  #  print(f"{chat_id} {sender_id}: {short(msg.text)}")
  if chat_id == GROUP_ID:
    # my group
    #  if msg.raw_text:
    #    text = msg.raw_text
    if text:
      text = text.replace("*", "")
      text = text.replace("`", "")
      global tg_msg_cache_for_bot2
      if sender_id == 420415423:
        # bot2: t2bot
        #  if text.startswith("bot: "):
        #    text = text[5:]
        if text.startswith("\u2067: "):
          info(f"bot original text: {text=}")
          text = text[3:]
          #  if text.startswith("\u2066"):
          while text.startswith("\u2066"):
            text = text[1:]
          if text[:2] == " \n":
            text = text[2:]
          elif text[0] == "\n":
            text = text[1:]
            info(f"bot original text(delete enter): {text=}")

          if text.startswith("M "):
            text = text.split(": ", 1)[1]
            if text.startswith("reply: "):
              text = text.split(": ", 1)[1]
          #  elif text.startswith("G "):
          #    warn(f"fixme: 多余的消息，mt的过滤规则需要修改: {text}")
          #    await msg.delete()
          #    return
          info(f"bot original text(2): {text=}")

        #  elif " " not in  text.splei(": ", 1)[0]:
        #  elif text[1] != " ":
        else:
          #  text = "M " + text
          text = text.split(": ", 1)[1]
          info(f"bot original text(3): {text=}")
        #  text = text.splitlines()[0]
        while "  " in text:
          text = text.replace("  ", " ")
        text = text.strip()
        #  if text[-1] == " ":
        #    text = text[:-1]
        async with tg_msg_cache_for_bot2_lock:
          i = 0
          #  while tg_msg_cache_for_bot2 is not None:
          await asyncio.sleep(0)
          while tg_msg_cache_for_bot2_event.is_set():
            if i>10:
              info(f"bot2 wait for clear timeout: {short(text)}")
              break
            info(f"bot2 wait for clear: {short(text)}")
            await sleep(0.8)
            i+=1
          await asyncio.sleep(0)
          tg_msg_cache_for_bot2 = text
          tg_msg_cache_for_bot2_event.set()
      elif sender_id == 5864905002:
        # msg from my tg bot received by tg user bot
        #  text2 = "bot: " + (msg.raw_text)
        while text.startswith("\u2066"):
          text = text[1:]
        #  text = text.splitlines()[0]
        #  text = text.strip()
        if text.startswith("M "):
          text = text.split(": ", 1)[1]
          if text.startswith("reply: "):
            text = text.split(": ", 1)[1]

        #  https://symbl.cc/cn/unicode/blocks/cjk-symbols-and-punctuation/
        #  text = text.replace("\u3000", " ")
        #  for i in set(text):
        #    #  if ord("\u3000") <= ord(i) <= ord("\u303f"):
        #    if 0x3000 <= ord(i) <= 0x303f:
        #      text = text.replace(i, " ")

        while "  " in text:
          text = text.replace("  ", " ")
        text = text.strip()
        #  start_time = time.time()
        try:
          while True:
            #  await tg_msg_cache_for_bot2_event.wait()
            await asyncio.wait_for(tg_msg_cache_for_bot2_event.wait(), timeout=300)
            await asyncio.sleep(0)
            #  if tg_msg_cache_for_bot2.startswith(text2):
            #  if text == tg_msg_cache_for_bot2:
            #  if jaccard_similarity(text, tg_msg_cache_for_bot2) > 0.9:
            #  if ratio(text, tg_msg_cache_for_bot2) > 0.9:
            r = similarity(text, tg_msg_cache_for_bot2)
            if r > 0.8:
              tg_msg_cache_for_bot2_event.clear()
              await msg.delete()
              #  tg_msg_cache_for_bot2 = None
              info(f"消息重复: {r=} {short(text)}")
              break
            else:
              tg_msg_cache_for_bot2_event.clear()
              #  if time.time() - start_time > 5:
              #  await sleep(0.2)
              #  info(f"bot1 miss: {short(text)} != {short(tg_msg_cache_for_bot2)}")
              info(f"匹配失败: {r=} {text=} != {tg_msg_cache_for_bot2=}")
              await asyncio.sleep(0)
        except TimeoutError as e:
          info(f"等待超时，未找到重复消息: {short(text)}")
        #  i = 0
        #  while i<18:
        #    if tg_msg_cache_for_bot2 is None:
        #      pass
        #    #  elif "bot: " + (msg.raw_text) != tg_msg_cache_for_bot2:
        #    #    info("miss: {msg.raw_text} != {tg_msg_cache_for_bot2}")
        #    #    tg_msg_cache_for_bot2 = None
        #    #  else:
        #    elif "bot: " + (msg.raw_text) == tg_msg_cache_for_bot2:
        #      await msg.delete()
        #      tg_msg_cache_for_bot2 = None
        #      info("found")
        #      break
        #    info("wait for bot2")
        #    await sleep(0.3)
        #    i+=1
    return

  if msg.edit_date is None:
    correct = False
  else:
    correct = True
  if chat_id in bridges_tmp:
    src = bridges_tmp[chat_id]
    if src not in mtmsgsg:
      warn(f"not found {src} in mtmsgsg")
      return
    mtmsgs = mtmsgsg[src]
    # 需要转发消息，约等于临时桥接通道, 发送消息的代码在 def run_cmd
    text = msg.text
    #  l = mtmsgs[qid]
    #  l = mtmsgs[src]
    l = mtmsgs[chat_id]
    bot_name = await get_name(chat_id)
    #  text = f"{l[0]}{bot_name}\n{text}"
    #  now = msg.date.timestamp()

    if len(l) == 1:
      l.append([])
    if msg.buttons:
      k = 0
      #  for k, v in mtmsgs.items():
      #    if k != chat_id:
      #      if len(v) > 1:
      #        mtmsgs.pop(k)
      #  if len(l) > 1:
      #    l[1] = msg.buttons
      #  else:
      #    l.append(msg.buttons)
      mtmsgs.clear()
      mtmsgs[chat_id] = l
      text += print_buttons(msg.buttons, k=len(get_buttons(l[1])))
      l[1].extend(msg.buttons)
      text = f"{bot_name}\n{text}"

    backup_task = None
    try:
      if msg.file:
        file_info, path, backup_task = await parse_tg_file_msg(msg)
        #  file = msg.file
        #  file_name = file.name
        #  if file_name:
        #    file_info = f"file: {file_name}"
        #  else:
        #    file_info = ""
        #  if file.size:
        #    if file.size > FILE_DOWNLOAD_MAX_BYTES:
        #      file_info += f"\n文件过大，终止下载({hbyte(file.size)})"
        #    else:
        #      #  path = await tg_download_media(msg)
        #      path = await tg_download_media(msg, src=src, max_wait_time=get_timeout(msg.file.size))
        #      if path is not None:
        #        #  t = asyncio.create_task(backup(path))
        #        #  url = await t
        #        url, backup_task = await backup(path, no_wait=True)
        #        #  xmpp_url = await upload(path, src)
        #        #  if xmpp_url:
        #        #    url = f"- {xmpp_url}\n\n- {url}"
        #        file_info += "\n"
        #        file_info += url
        #  else:
        #    file_info = "\n文件大小未知，终止下载"
        if file_info:
          if text:
            text += "\n\n"
          text += file_info

      text = f"{l[0]}{text}"
      if type(src) is int:
        send(text, src, correct=correct)
      else:
        gid = msg.id
        if gid - 1 in forwarded_tg_msg_ids:
          info(f"too many tg msg: {gid} for {chat_id}")
          await sleep(0.5)
        send(text, src, correct=correct, tg_msg_id=gid)
    finally:
      if backup_task is not None:
        await backup_task
        asyncio.create_task(backup(path, delete=True))
    return

  global bridges
  if chat_id in bridges:
    #  if chat_id == -1001354974109:
    #    err("fixme: 检查一下重复执行的原因: %s" % event.stringify())
    src = bridges[chat_id]
    #  if isinstance(src, dict):
    #    bridges.pop(chat_id)
    #    warn(f"delete old bridge: {src}")
    #    return
    res, nick, delay = await print_tg_msg(msg)
    if res:
      info(f"sync to xmpp: {chat_id} -> {src}: {short(res)}")
      gid = msg.id
      send(res, src, name=f"**{nick}:** ", nick=nick, delay=delay, correct=correct, tg_msg_id=gid)
    else:
      err(f"忽略空白信息: {res=} {nick=} {msg.text=}")
    return
  elif event.is_private:
    info(f"忽略私聊 {chat_id=} {short(msg.text)}")
    return
  else:
    #  info(f"{chat_id=} {short(msg.text)}")
    #  res, nick, delay = await print_tg_msg(event)
    if print_msg:
      await print_tg_msg(msg)
    #  if res:
    #    info(f"{nick}{res}")
    return

    #  elif event.is_private:
    #    pass
    #  else:
    #    res, nick, delay = await print_tg_msg(event)
    #    if res:
    #      #  await send(res, jid=log_group, name="", nick=nick, delay=delay)
    #      await send(res, jid=log_group, name="", delay=delay)
    #  return


async def save_tg_msg(tmsg, chat_id=CHAT_ID, opts=0, url=None):
  if opts == "fast":
    opts = 1
  elif opts == "tg":
    opts = 1
  elif opts == "direct":
    opts = 2
  elif opts == "xmpp":
    opts = 3
  elif opts == "vps":
    opts = 4
  elif opts == "raw":
    opts = 9
  else:
    opts = 0

  if opts == 9:
    send(tmsg.stringify(), chat_id)
  elif tmsg.file:
    file = tmsg.file
    file_size = file.size
    send(f"direct send...\nfile: {type(file)}\nname: {file.name}\nsize: {file.size}", chat_id)
    res = None
    #  if tmsg.text:
    # https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.uploads.UploadMethods.send_file
    # https://docs.telethon.dev/en/stable/modules/utils.html#telethon.utils.pack_bot_file_id
    try:
      if tmsg.document:
        info("use document")
        file = tmsg.document
      elif tmsg.video:
        info("use video")
        file = tmsg.video
      elif tmsg.photo:
        info("use photo")
        file = tmsg.photo
      else:
        info("use file")
        file = tmsg.file
      info(f"try send file type: {type(file)}")
      res = await UB.send_file(chat_id, file=file, caption=tmsg.text, force_document=True)

      if opts == 1:
        return True
    except rpcerrorlist.ChatForwardsRestrictedError as e:
      if e.args[0] == "You can't forward messages from a protected chat (caused by SendMediaRequest)":
        warn("内容被保护，无法直接转发")
      else:
        warn(f"fixme: {e=} {file=}")
    except AttributeError as e:
      err(f"fixme: {e=} {file=}")
    except Exception as e:
      err(f"fixme: {e=} {file=}")
      try:
        if tmsg.video:
          res = await UB.send_file(chat_id, file=tmsg.video, caption=tmsg.text, supports_streaming=True)
        elif tmsg.photo:
          res = await UB.send_file(chat_id, file=tmsg.photo, caption=tmsg.text)
        elif tmsg.media:
          res = await UB.send_file(chat_id, file=tmsg.media, caption=tmsg.text, force_document=True)
        if opts == 1:
          return True
      except Exception as e:
        err(f"fixme: {e=} {file=}")

    if res is None:
      file = None
      try:
        if tmsg.file:
          file = utils.pack_bot_file_id(tmsg.file)
        else:
          file = utils.pack_bot_file_id(tmsg.document)
      except AttributeError as e:
        err(f"fixme: {e=} {type(file)}")
      except Exception as e:
        err(f"fixme: {e=}")
      if file is None:
        try:
          # AttributeError("'PhotoSize' object has no attribute 'location'")
          #  file = utils.pack_bot_file_id(tmsg.file)
          if file is None and tmsg.photo:
            file = utils.pack_bot_file_id(tmsg.photo)
          if file is None and tmsg.document:
            file = utils.pack_bot_file_id(tmsg.document)
          if file is None and tmsg.media:
            file = utils.pack_bot_file_id(tmsg.media)
          if file is None:
            err(f"wtf: {tmsg.stringify()}")
            #  return
        except AttributeError as e:
          err(f"fixme: {e=}")
        except Exception as e:
          err(f"fixme: {e=}")
      if file is not None:
        res = await UB.send_file(chat_id, file=file, caption=tmsg.text)
        if opts == 1:
          return True
        
    #  src = log_group_private
    src = chat_id
    #  path = await tg_download_media(tmsg, src=log_group_private, max_wait_time=600)
    #  path = await tg_download_media(tmsg, src=chat_id, max_wait_time=download_media_time_max)
    path = await tg_download_media(tmsg, src=chat_id, max_wait_time=get_timeout(file_size))
    if path:
      if path.endswith(".tgs"):
        send(f"found tgs file: {path}", src, tmp_msg=True)
        fp = Path(path)
        filename = fp.name
        length = os.path.getsize(fp)
        shell_cmd = [f"{HOME}/.local/bin/lottie_convert.py", path, f"{fp.parent.as_posix()}/{filename[:-4]}.webp"]
        r, _, _ = await myshell(shell_cmd, max_time=get_timeout(length)*3+30, src=chat_id)
        if r == 0:
          asyncio.create_task(backup(path, delete=True))
          path = path[:-4]+".webp"
        else:
          info(f"转换失败 {path} {r}")

      #  t = asyncio.create_task(backup(path, name=str(int(time.time()))+path.split("/")[-1]))
      t = asyncio.create_task(backup(path, rename=True))
      try:

        #  if opts == 2 or res is None or opts == 0:
        if opts != 4 and opts != 2 and res is None:
          try:
            res = await tg_upload_media(path, src, chat_id=chat_id, caption=url, max_time=get_timeout(file_size))
            direct = True
            if opts == 2:
              return
          except Exception as e:
            err(f"上传失败 {e=}")
        else:
          if url:
            send(url, chat_id)


        #  res = None
        xmpp_url = None
        if res is None and opts == 4:
          send("上传到xmpp...", src, tmp_msg=True)
          try:
            xmpp_url = await upload(path)
            info(xmpp_url)
          except Exception as e:
            err(f"上传失败 {e=}")

        if xmpp_url:
          try:
            #  res = await UB.send_file(chat_id, file=url, caption=url)
            res = await tg_upload_media(xmpp_url, src, chat_id=chat_id, caption=url)
            if opts == 3:
              return True
          except rpcerrorlist.WebpageCurlFailedError as e:
            send(xmpp_url, chat_id)
            err(f"文件url有问题: {e=} {url}")
          except rpcerrorlist.WebpageMediaEmptyError as e:
            send(xmpp_url, chat_id)
            err(f"文件url有问题: {e=} {url}")
          except Exception as e:
            send(xmpp_url, chat_id)
            err(f"{e=} {url}")

        try:
          await t
          if t.done():
            url = t.result()
            if url:
             info(url)
             await sleep(1)
             res = await UB.send_file(chat_id, file=url, caption=url)
          else:
            err("wtf")
        except rpcerrorlist.WebpageCurlFailedError as e:
          err(f"文件url有问题: {e=} {url}")
        except rpcerrorlist.WebpageMediaEmptyError as e:
          err(f"文件url有问题: {e=} {url}")
        except Exception as e:
          err(f"{e=} {url}")

        if res is None or opts == 2:
          try:
            res = await tg_upload_media(path, src, chat_id=chat_id, caption=url, max_time=get_timeout(file_size))
            return True
          except Exception as e:
            send(url, chat_id)
            err(f"上传失败 {e=}")

      finally:
        await t
        if t.done():
          pass
        else:
          err(f"备份失败，等600s再删除: {path}")
          await sleep(600)
        asyncio.create_task(backup(path, delete=True))


  elif tmsg.text:
    #  res = await UB.send_message(chat_id, tmsg.text)
    await send_tg(tmsg.text, chat_id)
  else:
    await send_tg(tmsg.stringify(), chat_id)
  await send_tg("done", chat_id)


delete_next_msg = False

@exceptions_handler
async def msgtout(event):
  msg = event.message
  if delete_next_msg is True:
    res = await msg.delete()
    #  send("deleted", CHAT_ID)
    await msg.reply("deleted")
    return
  #  info(event.stringify())
  chat_id = event.chat_id
  #  if chat_id in last_outmsg:
  #    #  omsg = last_outmsg[chat_id]
  #    last_outmsg.pop(chat_id)

  if event.is_private:
    if chat_id in bridges_tmp:
      #  src = bridges_tmp[chat_id]
      #  if src in mtmsgsg:
      #    mtmsgs = mtmsgsg[src]
      #    if mtmsgs:
      #      mtmsgs.clear()
      #      #  await send(f"unlink {src}", CHAT_ID)
      #      warn(f"unlink {src} - (chat_id)")
      bridges_tmp.pop(chat_id)
  text = msg.text
  info(f"tg out msg: {chat_id}: {text}")
  if text == "/help":
    if event.is_reply:
      r = await msg.get_reply_message()
      #  sendme(f"{r.stringify()}")
      #  await msg.reply(f"{r.stringify()}")
      await send_tg(r.stringify())
    else:
      #  sendme(f"{event.chat_id}")
      await msg.reply(f"{event.chat_id}")
  elif text.startswith("$"):
    cmds = get_cmd(text)
    if cmds[0] == "$get":
      if cmds[1] == "id":
        #  await UB.send_message('me', f"{event.chat_id}")
        await msg.reply(f"{event.chat_id}")
      elif cmds[1] == "chat_id":
        await msg.reply(f"{event.chat_id}")
      elif cmds[1] == "event":
        await msg.reply(f"{event.stringify()}")
      elif cmds[1] == "msg":
        await msg.reply(f"{msg.stringify()}")
      elif cmds[1] == "chat":
        e = await event.get_chat()
        #  await msg.reply(f"{e.stringify()}")
        await send_tg(e.stringify(), chat_id, topic=msg.id)
      elif cmds[1] == "r":
        if event.is_reply:
          #  await msg.reply(event.reply_to.stringify())
          await send_tg("in event: %s" % event.reply_to.stringify(), chat_id, topic=msg.id)
        else:
          await send_tg(f"not a reply: {msg.stringify()}", chat_id, topic=msg.id)
      elif cmds[1] == "reply":
        if event.is_reply:
          e = await msg.get_reply_message()
          #  await msg.reply(f"{e.stringify()}")
          await send_tg(e.stringify(), chat_id, topic=msg.id)
        else:
          #  await msg.reply(f"not a reply: {msg.stringify()}")
          await send_tg(f"not a reply: {msg.stringify()}", chat_id, topic=msg.id)
      elif cmds[1] == "sender":
        if event.is_reply:
          e = await msg.get_reply_message()
          e = await e.get_sender()
          #  await msg.reply(f"{e.stringify()}")
          await send_tg(e.stringify(), chat_id, topic=msg.id)
        else:
          #  await msg.reply(f"not a reply: {msg.stringify()}")
          await send_tg(f"not a reply: {msg.stringify()}", chat_id, topic=msg.id)
      elif cmds[1] == "file":
        e = await msg.get_reply_message()
        tmsg = e
        opts = 0
        if len(cmds) == 3:
          opts = cmds[2]
        await save_tg_msg(tmsg, chat_id, opts)
    res = await msg.delete()
    info(f"delete userbot cmd: {res}")
    return

  #  if chat_id == MY_ID or chat_id == CHAT_ID:
  #  if chat_id == MY_ID or chat_id == CHAT_ID:
  if chat_id == CHAT_ID:
    tmsg = event
    if tmsg.document or tmsg.file or tmsg.media:
      #  file = tmsg.document
      await send_tg2(f"document type: {type(tmsg.document)}\nfile type: {type(tmsg.file)}\nmedia type: {type(tmsg.media)}\n$get reply/file", chat_id)
    if event.fwd_from:
      #  await msg.reply(event.fwd_from.stringify())
      #  await send_tg(event.fwd_from.stringify(), chat_id)
      opts = 0
      #  cmds = get_cmd(text)
      #  if len(cmds) == 3:
      #    opts = cmds[2]
      await save_tg_msg(tmsg, chat_id, opts)
        #  res = await UB.send_file(chat_id, file=file, caption=tmsg.text, force_document=True)
      return
    #  elif event.is_reply:
    #    sendme(event.reply_to.stringify())
    #    return
    #  if not text:
    #    return





async def my_event_handler(event):
  #  if 'hello' in event.raw_text:
  #    await event.reply('hi!')
  #  if 'new_chat' in event.raw_text:
  #    print(event.stringify())
  await read_res(event)


#  @exceptions_handler
#  @UB.on(events.MessageEdited(incoming=True))
#  async def my_event_handler(event):
#    #  if 'hello' in event.raw_text:
#    #    await event.reply('hi!')
#    #  if 'new_chat' in event.raw_text:
#    #    print(event.stringify())
#
#    await read_res(event)

def get_jid(i, full=False):
  if full:
    if i.resource:
      return f"{i.localpart}@{i.domain}/{i.resource}"
    else:
      return f"{i.localpart}@{i.domain}"
  else:
    return f"{i.localpart}@{i.domain}"

async def stop(client=None):
  if client is None:
    if UB.is_connected():
      info("开始断开UB")
      await UB.__aexit__()
    if TB.is_connected():
      info("开始断开TB")
      await TB.__aexit__()
    if 'XB' in globals():
      client = XB
    else:
      return
  jid = get_jid(client.local_jid)
  if client.running:
    info(f"开始断开账户: {jid}")
    client.stop()
    while True:
      if client.running:
        info(f"等待断开账户: {jid}")
        await sleep(0.5)
      else:
        info(f"已断开: {jid}")
        break
  else:
    info(f"已离线: {jid}")



async def disco_info(jid=None, node=None, client=None):
  if client is None:
    client = XB
  if jid is None:
    jid = XB.local_jid
  elif isinstance(jid, JID):
    pass
  else:
    jid = JID.fromstr(jid)
  dc = client.summon(aioxmpp.DiscoClient)
  #  res = await dc.query_info(JID.fromstr(jid))
  try:
    res = await dc.query_info(jid, node=node, timeout=5)
    #  pprint(res)
    #  print(jid, res.to_dict())
    return res
  except TimeoutError as e:
    warn(f"失败(超时)：{jid}, {e=}")
    raise
    return f"{e=}"

async def disco_item(jid=None, node=None, client=None):
  if client is None:
    client = XB
  if jid is None:
    jid = JID.fromstr(XB.local_jid.domain)
  elif isinstance(jid, JID):
    pass
  else:
    jid = JID.fromstr(jid)
  #  jid = test_group.rsplit('@', 1)[1]
  dc = client.summon(aioxmpp.DiscoClient)
  #  res = await dc.query_info(JID.fromstr(jid))
  try:
    res = await dc.query_items(jid, node=node, timeout=5)
    #  pprint(res)
    #  for i in res.items:
    #    print(i.name, i.node, i.jid)
    return res
  except TimeoutError as e:
    warn(f"失败(超时)：{jid}, {e=}")
    raise


async def get_server_name(jid):
  await sleep(0.5)
  res = await disco_info(jid)
  if res:
    if res.identities:
      return res.identities[0]



#  cross_thread_tasks = {}
#
#
#  async def thread2_loop():
#    info("副进程时间循环已启动")
#    while True:
#      await sleep(0.5)
#      info0("副进程时间循环运行中...")
#      for i in range(120):
#        await sleep(0.5)
#


def thread2_daemon():
  info("独立线程，启动...")
  #  info("判断是否在主线程，应该是False: %s" % str(main_thread.native_id == threading.get_native_id()))
  #  info("判断是否在副线程，应该是True: %s" % str(loop2_thread.native_id == threading.get_native_id()))
  #  info(f"ids: {main_thread.native_id}  {loop2_thread.native_id} {threading.get_native_id()}")
  global loop2
  loop2 = asyncio.new_event_loop()  # 创建新的事件循环
  asyncio.set_event_loop(loop2)  # 设置当前线程的事件循环
  #  loop2.create_task(thread2_loop())
  loop2.run_forever()  # 启动事件循环

def in_main_thread():
  if main_thread.native_id == threading.get_native_id():
    #  info(f"in main: ids: main: {main_thread.native_id}  loop2: {loop2_thread.native_id} now: {threading.get_native_id()}")
    return True
  #  info(f"not in main: ids: main: {main_thread.native_id}  loop2: {loop2_thread.native_id} now: {threading.get_native_id()}")
  #  if loop2_thread.native_id == threading.get_native_id():
  # fixme: 有可能第三个线程
  return False

def run_cb_in_main(cb, *args, **kwargs):
  # fixme: 不支持多线程
  if in_main_thread():
    info(f"在主线程执行: {cb}")
    #  return cb(*args, **kwargs)
    fu = asyncio.Future()
    @exceptions_handler
    def cb2():
      fu.set_result(cb(*args, **kwargs))
    loop.call_soon(cb2)
    return fu
  info(f"在副线程跨线程执行: {cb}")
  #  cb, fu = cb_for_future(cb, loop2, *args, **kwargs)
  cb, fu = cb_for_future(partial(cb, *args, **kwargs), loop2)
  loop.call_soon_threadsafe(cb)
  return fu

def run_cb_in_thread(cb, *args, **kwargs):
  # fixme: 不支持多线程
  if in_main_thread():
    info(f"在主线程跨线程执行: {cb}")
    #  fu = asyncio.Future()
    #  cb = cb_for_future(fu.set_result, cb, loop)
    #  loop2.call_soon_threadsafe(partial(cb, *args, **kwargs))
    #  cb, fu = cb_for_future(cb, loop, *args, **kwargs)
    cb, fu = cb_for_future(partial(cb, *args, **kwargs), loop)
    loop2.call_soon_threadsafe(cb)
    return fu
  info(f"在副线程执行: {cb}")
  #  return cb(*args, **kwargs)
  fu = asyncio.Future()
  @exceptions_handler
  def cb2():
    fu.set_result(cb(*args, **kwargs))
  loop2.call_soon(cb2)
  return fu

#  @exceptions_handler
def cb_for_future(cb, oloop):
  fu = asyncio.Future()
  # for multi thread
  #  @exceptions_handler
  def cb():
    #  oloop.call_soon_threadsafe(partial(fu.set_result, f()))
    try:
      f = exceptions_handler(no_send=True)(partial(fu.set_result, cb()))
      res = f()
      info(f"fu.result: {res}")
    except Exception as e:
      warn("failed", e=e)
      res = None
    oloop.call_soon_threadsafe(fu.set_result, res)
    info(f"done")
  return cb, fu

def run_cb(cb, *args, need_main=False, **kwargs):
  if need_main:
    if in_main_thread():
      info(f"在主线程执行: {cb}")
      safe = True
      lp = loop
    else:
      info(f"在副线程跨线程执行: {cb}")
      safe = False
      lp = loop
      olp = loop2
  else:
    if in_main_thread():
      info(f"在主线程跨线程执行: {cb}")
      safe = False
      lp = loop2
      olp = loop
    else:
      info(f"在副线程执行: {cb}")
      safe = True
      lp = loop2
  if safe:
    return cb(*args, **kwargs)
  else:

    @exceptions_handler
    async def cb2():
      return cb(*args, **kwargs)
    fu = asyncio.run_coroutine_threadsafe(cb2(), lp)
    return fu.result()

    fu = asyncio.Future()

  return fu

def run_cb2(cb, *args, need_main=False, **kwargs):
  # lp： 目标线程
  # olp： 当前线程
  # return future
  if need_main:
    if in_main_thread():
      info(f"在主线程执行: {cb}")
      safe = True
      lp = loop
    else:
      info(f"在副线程跨线程执行: {cb}")
      safe = False
      lp = loop
      olp = loop2
  else:
    if in_main_thread():
      info(f"在主线程跨线程执行: {cb}")
      safe = False
      lp = loop2
      olp = loop
    else:
      info(f"在副线程执行: {cb}")
      safe = True
      lp = loop2
  fu = asyncio.Future()
  if safe:

    @exceptions_handler
    def cb2():
      fu.set_result(cb(*args, **kwargs))
    lp.call_soon(cb2)
  else:

    @exceptions_handler
    async def cb2():
      return cb(*args, **kwargs)
    fu0 = asyncio.run_coroutine_threadsafe(cb2(), lp)

    @exceptions_handler
    def cb_for_fu_result(fu0):
      #  oloop.call_soon_threadsafe(partial(f, f2()))
      #  oloop.call_soon_threadsafe(partial(fu.set_result, fu0.result()))
      #  fu.set_result(fu0.result())
      olp.call_soon_threadsafe(fu.set_result, fu0.result())
    fu0.add_done_callback(cb_for_fu_result)
  return fu

async def _run_cb3(func, *args, **kwargs):
  try:
    res =  func(*args, **kwargs)
    info(f"fu.result: {res}")
  except Exception as e:
    #  warn("failed", e=e)
    res = _exceptions_handler(e, no_send=True)
  return res

def run_cb3(lp2, func, *args, **kwargs):
  fu = asyncio.run_coroutine_threadsafe(_run_cb3(func, *args, **kwargs), lp2)
  return fu.result()


async def run_coro(coro, lp, lp2):
  fu = asyncio.Event()
  ress = []
  #  @exceptions_handler
  async def f():
    #  return 0
    #  fu.set()
    info("run...")
    try:
      res = await coro
      info(f"fu.result: {res}")
    except Exception as e:
      #  warn("failed", e=e)
      res = _exceptions_handler(e, no_send=True)
      #  res = None
    ress.append(res)
    lp.call_soon_threadsafe(fu.set)
    info("done")
    #  return res
  #  info(f"lp2 is_running: {lp2.is_running()}")
  #  t = lp2.create_task(f())
  #  ts = []
  #  def f2():
  #    t= asyncio.create_task(f())
  #    ts.append(t)
  lp2.call_soon_threadsafe(asyncio.create_task, f())
  #  info(f"lp2 is_running: {lp2.is_running()}")
  await fu.wait()
  return ress[0]

#  @exceptions_handler(no_send=True)
async def run_run(coro, need_main=False):
  if need_main:
    #  if threading.current_thread() is loop2_thread:
      #  if asyncio.iscoroutine():
    if in_main_thread():
      info(f"在主线程执行: {coro}")
      return await coro
    elif loop2_thread.native_id == threading.get_native_id():
      info(f"在副线程跨线程执行: {coro}")
      fu = asyncio.run_coroutine_threadsafe(coro, loop)
      oloop = loop2
    else:
      # 未知线程
      warn("未知线程")
      fu = asyncio.run_coroutine_threadsafe(coro, loop)
      return
  else:
    #  if threading.current_thread() is loop2_thread:
    if in_main_thread():
      info(f"在主线程跨线程执行: {coro}")
      fu = asyncio.run_coroutine_threadsafe(coro, loop2)
      oloop = loop
    #  elif main_thread.native_id != threading.get_native_id():
    elif loop2_thread.native_id == threading.get_native_id():
      info(f"在副线程执行: {coro}")
      return await coro
    else:
      # 未知线程
      warn("未知线程")
      return await coro

  fua = asyncio.Future()
  #  async def cb2(fu, result=0):
  #    fu.set_result(result)
  #  def cb(fu2):
  #    if fu2.done():
  #      print("确实结束了")
  #      #  asyncio.run_coroutine_threadsafe(cb2(fu, fu2.result()), oloop)
  #      oloop.call_soon_threadsafe(partial(fu.set_result, fu2.result()))
  #    else:
  #      print("wtffffffffffffffffffffffffffffffffff, 还没结束")
  #      #  asyncio.run_coroutine_threadsafe(cb2(fu), oloop)
  #      oloop.call_soon_threadsafe(partial(fu.set_result, fu2.result()))
  #  cb = cb_for_future(fu.set_result, fu2.result, oloop)
  #  @exceptions_handler(no_send=True)

  @exceptions_handler
  def cb_for_fu_result(fu):
    #  oloop.call_soon_threadsafe(partial(f, f2()))
    #  oloop.call_soon_threadsafe(partial(fua.set_result, fu.result()))
    #  fua.set_result(fu.result())
    try:
      #  res = fu.result()
      #  f = exceptions_handler(no_send=True)(fu.result)
      res = fu.result()
      info(f"fu.result: {res}")
    except Exception as e:
      warn("failed", e=e)
      res = None
    #  fua.set_result(res)
    oloop.call_soon_threadsafe(fua.set_result, res)
    #  oloop.call_soon(fua.set_result, res)
    info(f"done")
  fu.add_done_callback(cb_for_fu_result)
  return await fua



  #  while True:
  #    await sleep(1)
  #    if fu2.done():
  #      break
  #    info(f"wait for result of fu: {coro}")
  #  return fu2.result()




@exceptions_handler
async def upload(file_path=f"{HOME}/t/1.jpg", src=None):
  # fixme: 整个函数可以放到副线程运行

  if UPLOAD is None:
    err(f"服务器不支持文件上传: {myjid}")
    return False

  if type(file_path) is str:
    fp = Path(file_path)
    #  file_path = Path(file_path)
  else:
    fp = file_path
  if not fp.is_file():
    err(f"文件路径错误: {file_path}")
    return
  #  httpupload = client.summon(aioxmpp.httpupload.Service)
  #  filename = file_path.split("/")[-1]
  filename = fp.name
  length = os.path.getsize(fp)
  if UPLOAD_MAX > 0:
    if length > UPLOAD_MAX:
      err(f"file is too big: {length} {file_path}")
      return False
  else:
    warn(f"unknown file size limit: {UPLOAD}")
  t = mimetypes.guess_type(fp)[0]
  if t is None:
    info(f"自动获取mimetypes失败")
        #  ft=$(file --mime-type -b -- "$fn")
    cmds = "file --mime-type -b --"
    cmds = cmds.split(" ")
    cmds.append(file_path)
    r, o, e = await my_sexec(cmds, src=src)
    if r == 0:
      if o:
        t = o
  if t is None:
    warn(f"获取mimetypes失败")
    #  return
    t = 'application/octet-stream'
  #  print("upload to xmpp: ", XB,UPLOAD, filename, os.path.getsize(fp), t, file_path)
  print("upload to xmpp: ", XB,UPLOAD, filename, os.path.getsize(fp), t, file_path)
  slot = await aioxmpp.httpupload.request_slot(XB,UPLOAD, filename, length, content_type=t)
  #  slot = await XB.send(aioxmpp.IQ(
  #      type_=aioxmpp.IQType.GET,
  #      to=UPLOAD,
  #      payload=aioxmpp.httpupload.Request(
  #          filename,
  #          os.path.getsize(fp),
  #          mimetypes.guess_type(fp)[0],
  #      )
  #  ))

  headers = slot.put.headers.copy()

  #  chunk_size = 1024 * 1024
  #  if length / chunk_size > 2:
  #    info(f"文件过大，开启进度显示: {length} > {chunk_size}")
  #  if False:
  #  async with aiofiles.open(fp, "rb") as file:
  #    data = await file.read()
  #  res = await http(slot.put.url, method="PUT", headers=headers, data=data, chunked=chunk_size)
  #  info(f"res: {res}\nslot: {slot}")
  #  return slot.get.url
  #  headers['Transfer-Encoding'] = 'chunked'
    #  async with aiohttp.ClientSession() as session:
    #    async with aiofiles.open(fp, "rb") as file:
    #      while chunk := await file.read(chunk_size):
    #        if len(last_time) == 2:
    #          last_time.append(total)
    #          asyncio.create_task(send("开始分块上传: {:.1f}MB".format(total/1024/1024), src))
    #        #  res = await http(slot.put.url, method="PUT", headers=headers, data=chunk)
    #        #  headers["Content-Length"] = str(length)
    #        #  headers["Content-Length"] = str(len(chunk))
    #        info("headers: %s" % headers)
    #        async with session.put(slot.put.url, data=chunk, headers=headers, chunked=chunk_size) as res:
    #          if res.status != 200 and res.status != 200:
    #            err(f"分块上传失败，返回状态：{res=} {slot.put.url=} {res.headers=} {await res.text()}")
    #            return
    #          info(f"res: {res}\nslot: {slot}")
    #          info(await res.text())
    #        last_time[1] += chunk_size


  headers["Content-Length"] = str(length)
  #  if src:
  info("开启进度刷新消息")
  send("开始上传: {} {}".format(hbyte(length), filename), src, tmp_msg=True)

    #  async def coro(slot, fp, timeout, headers):
  #  async def coro():
    #  async def update_tmp_msg2():
    #    while True:
    #      await sleep(1)
    #      print("上传线程没卡住")
    #  async def update_tmp_msg(file):
    #    #  asyncio.create_task(update_tmp_msg2())
    #    i = 0
    #    start_time = time.time()
    #    while True:
    #      await sleep(1)
    #      if file.closed:
    #        info(f"文件已关闭: {file.name}")
    #        return
    #      try:
    #        now = await file.tell()
    #      except ValueError as e:
    #        info(f"文件已关闭: {file.name}")
    #        break
    #      if now == length:
    #        info(f"end: {now}")
    #        return
    #      info(f"当前 {fp.name} {now}")
    #      #  await sleep(interval/2)
    #      i += 1
    #      if i < interval:
    #        continue
    #      i = 0
    #      info("剩余 {fp.name} {:.1f}M".format((length-now)/1024/1024))
    #      if src:
    #        send("{:.1f}M".format((length-now)/1024/1024), src)
    #      if time.time() - start_time > download_media_time_max:
    #        if src:
    #          await send("超时", src, correct=True)
    #        break
  ress = [time.time(), 0]
  def wrap_read(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      data = await func(*args, **kwargs)
      ress[1] += len(data)
      now = time.time()
      if now - ress[0] > interval:
        ress[0] = now
        info("剩余: {}".format(hbyte(length-ress[1])))
        #  sendme("{:.1f}M".format((length-ress[0])/1024/1024))
        send(hbyte(length-ress[1]), src, tmp_msg=True)
      #  print(f"{len(data)}")
      return data
    return wrapper

  #  def dc(func):
  #    @wraps(func)
  #    async def wrapper(*args, **kwargs):
  #      print(f"正在关闭")
  #      return await func(*args, **kwargs)
  #    return wrapper

  timeout = get_timeout(length)
  try:
    async with aiofiles.open(fp, "rb") as file:
      #  t = asyncio.create_task(update_tmp_msg(file))
      #  file.read = d(file.read)
      #  file.close = dc(file.close)
      file.readline = wrap_read(file.readline)
      #  await sleep(5)
      res = await http(slot.put.url, method="PUT", headers=headers, data=file, timeout=timeout)
      info(f"res: {res}\nslot: {slot}")
      send("上传完成", src, tmp_msg=True)
      #  res = await run_run(http(slot.put.url, method="PUT", headers=headers, data=file, timeout=timeout))
      #  coro = send("测试进程间通信 res: {}".format(res))
      #  fu2 = asyncio.run_coroutine_threadsafe(coro, loop)
      #  await send("测试进程间通信 res: {}".format(res))
      #  return res
  except FileNotFoundError as e:
    err(f"上传失败：{e=} {slot.put.url=}")
    return
  except Exception as e:
    err(f"上传失败：{e=} {slot.put.url=}")
    return
    #  finally:
    #    if not t.done():
    #      t.cancel()
  #  res = await run_run(coro(slot, fp, timeout, headers))
  #  res = await run_run(coro())

  #  else:
  #    # 流式上传需要手动设置Length
  #    headers["Content-Length"] = str(length)
  #    info("headers: %s" % headers)
  #    try:
  #      async with aiofiles.open(fp, "rb") as file:
  #        res = await http(slot.put.url, method="PUT", headers=headers, data=file, timeout=15)
  #        info(f"res: {res}\nslot: {slot}")
  #    except Exception as e:
  #      err(f"上传失败：{e=} {slot.put.url=}")
  #      return
  dbg(slot.put.headers)
  info(slot.get.url)
  return slot.get.url


async def regisger_handler(client):
#  class FooService(aioxmpp.service.Service):
#    feature = aioxmpp.disco.register_feature(
#      "some:namespace"
#    )
#
#    #  @aioxmpp.service.depsignal(aioxmpp.DiscoServer, "on_info_changed")
#    #  def handle_on_info_changed(self):
#    #    pass
#
#    #@aioxmpp.dispatcher.message_handler(aioxmpp.MessageType.CHAT, None)
#    @aioxmpp.service.depsignal(aioxmpp.MUCClient, "on_message")


#  @aioxmpp.dispatcher.message_handler(aioxmpp.MessageType.GROUPCHAT, None)
#  async def gmsg_in(msg):
#    info("\n>> group msg: %s\n" % msg)

  #  # obtain an instance of the service (we’ll discuss services later)
  message_dispatcher = client.summon(
     #  aioxmpp.dispatcher.SimpleMessageDispatcher
     dispatcher.SimpleMessageDispatcher
  )
  # register a message callback here
  #  message_dispatcher.register_callback(
  #      aioxmpp.MessageType.CHAT,
  #      None,
  #      msg_in,
  #  )
  message_dispatcher.register_callback(
      #  aioxmpp.MessageType.GROUPCHAT,
      None,
      None,
      msgx
  )
  #  message_dispatcher.register_callback(
  #      aioxmpp.MessageType.NORMAL,
  #      None,
  #      msg_in,
  #  )

  #  MUC = i.summon(aioxmpp.MUCClient)
  #  MUC.on_message.connect(gmsg)
  #  i.stream.register_message_callback(aioxmpp.MessageType.GROUPCHAT, None, gmsg_in)
  #  i.stream.register_message_callback(aioxmpp.MessageType.CHAT, None, msg_in)

  presence_dispatcher = client.summon(
     #  aioxmpp.dispatcher.SimpleMessageDispatcher
     dispatcher.SimplePresenceDispatcher
  )
  presence_dispatcher.register_callback(
      None,
      None,
      msgxp,
  )

#  client.stream.register_iq_request_handler(
#      aioxmpp.IQType.GET,
#      aioxmpp.disco.xso.InfoQuery,
#      request_handler,
#  )

  #  async def request_handler(request):
  #      print("request_handler: %s" % request)
  #
  #  client.stream.register_iq_request_handler(
  #      aioxmpp.IQType.GET,
  #      aioxmpp.disco.xso.InfoQuery,
  #      request_handler,
  #  )

  #  from aioxmpp.version.xso import Query

  @exceptions_handler
  async def cb(iq):
      #  print("software version request from {!r}".format(iq.from_))
      warn("收到查看系统信息的请求: {!r}".format(iq.from_))
      result = aioxmpp.version.xso.Query()
      result.name = "xmppbot"
      result.version = f"xmpp:{main_group}?join"
      result.os = f"by {ME}"
      return result

  client.stream.register_iq_request_handler(
      aioxmpp.IQType.GET,
      aioxmpp.version.xso.Query,
      cb,
  )

  #  pprint(client.stream)
  #  pprint(client.stream.service_outbound_message_filter)
  #  return
  #  client.stream.service_outbound_messages_filter = stream.AppFilter()
  #  client.stream.service_outbound_message_filter.register(msg_out, 1)
  #  client.stream.app_outbound_message_filter.register(msg_out, 1)



#  @exceptions_handler
def send_typing(muc):
  if type(muc) is int:
    # telegram
    chat_id = muc
    # https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.chats.ChatMethods.action
    #  async def f():
    #    await TB.action(chat_id, "typing")
    #  asyncio.create_task(f())
    return TB.action(chat_id, "typing")
  ms = get_mucs(muc)
  if ms:
  #  if muc == "gateway1":
  #    return True
  #  if muc in my_groups:
    type_=MessageType.GROUPCHAT
  else:
    type_=MessageType.CHAT
    ms = [muc]

  for muc in ms:
    msg = aioxmpp.Message(
        to=JID.fromstr(muc),
        type_=type_,
    )
    msg.xep0085_chatstate = chatstates.ChatState.COMPOSING
    #  info(f"{msg.body=}") # ={}
    #  await send_xmpp(msg)
    asyncio.create_task( send_xmpp(msg) )


last_outmsg = {}

def get_msg_jid(msg):
  #  # for tg
  #  if hasattr(msg, "id"):
  #    return msg.chat_id

  # 下面是xmpp用的代码
  J = msg.to
  jid = str(J.bare())
  if jid == myjid:
    J = msg.from_
    jid = str(J.bare())
  if msg.type_ == MessageType.GROUPCHAT:
    pass
    #  jid = get_jid(msg.to)
    #  jid = str(J.bare())
  elif msg.type_ == MessageType.CHAT:
    #  jid = str(J.bare())
    if jid in my_groups:
      #  jid = get_jid(msg.to, True)
      jid = str(J)
  else:
    return
  return jid

def clear_msg_jid(msg):
  j = get_msg_jid(msg)
  if j in last_outmsg:
    last_outmsg.pop(j)
    info(f"已清除msg记录: {j}")
  else:
    info(f"没找到msg记录: {j}")


tmp_msg_chats = set()

def add_id_to_msg(msg, correct, tmp_msg):
  j = get_msg_jid(msg)
  msg.autoset_id()
  if j in last_outmsg:
    if correct or j in tmp_msg_chats:
      r = aioxmpp.misc.Replace()
      r.id_ = last_outmsg[j]
      msg.xep0308_replace = r
    else:
      last_outmsg[j] = msg.id_
  else:
    last_outmsg[j] = msg.id_
    if correct:
      info("not found old msg, can't correct")
  if tmp_msg is True:
    tmp_msg_chats.add(j)
  elif j in tmp_msg_chats:
    tmp_msg_chats.remove(j)




#  async def ___add_id_to_msg(msg, correct):
#    j = get_msg_jid(msg)
#    if correct:
#      if j in last_outmsg:
#        #  msg.xep0308_replace = aioxmpp.misc.Replace(last_outmsg[get_jid(msg.to, True)])
#        for _ in range(5):
#          if last_outmsg[j][1]:
#            last_outmsg[j][0] = msg
#            r = aioxmpp.misc.Replace()
#            r.id_ = last_outmsg[j][1]
#            msg.xep0308_replace = r
#            break
#          else:
#            info("msg id 不可用: {last_outmsg[j][1]}")
#            await sleep(1)
#        if last_outmsg[j][1] is None:
#          last_outmsg[j] = [msg, None]
#      else:
#        last_outmsg[j] = [msg, None]
#        info("已添加msg")
#    else:
#        #  last_outmsg.pop(j)
#      if j in last_outmsg:
#        #  msg.xep0308_replace = aioxmpp.misc.Replace(last_outmsg[get_jid(msg.to, True)])
#        for _ in range(5):
#          if last_outmsg[j][1]:
#            last_outmsg[j][0] = msg
#            r = aioxmpp.misc.Replace()
#            r.id_ = last_outmsg[j][1]
#            msg.xep0308_replace = r
#          else:
#            info("msg id 不可用: {last_outmsg[j][1]}")
#            await sleep(1)
#        if last_outmsg[j][1] is None:
#          last_outmsg[j] = [msg, None]
#        last_outmsg[j].append(0)

def get_mucs(muc):
  if muc == "gateway1":
    muc = main_group
  elif muc not in my_groups:
    return {muc}
    return
  for s in sync_groups_all:
    if muc in s:
      tmp = set()
      for m in s:
        if m not in rooms:
          tmp.add(m)
      return s - tmp
  return {muc}
  return [muc]
  return set([muc])

def wtf_str(s, for_what="nick"):
  if for_what == "nick":
    ok = []
    #  no = ('Cn', 'Cs', 'Co', 'Cf', 'So', 'Ll', 'Cc', 'Mn', 'Po', 'Lo', 'Sm', 'Ps', 'Lu')
    no = ('Cn', 'Cs', 'Co', 'Cf', 'So', 'Ll', 'Cc', 'Mn', 'Sm', 'Ps', 'Lu')
  #  elif for_what == "xmpp":
  #    ok = ['\n', '\t']
  #    no = ('Cc', )
  else:
    ok = ['\n', '\t']
    no = ('Cc', )
  tmp=[]
  for c in s:
    if c in ok:
      tmp.append(c)
    #  if ud.category(c) in ('Cn', 'Cs', 'Co'):
    elif unicodedata.category(c) in no:
    #  if ud.category(c) not in ('Cn', 'Cs', 'Co',  'So'):
      #  nick = repr(nick)
      #  break
      tmp.append(c.encode("unicode-escape").decode())
    else:
      tmp.append(c)
  return "".join(tmp)

#  @exceptions_handler
def msg_out(msg):
  #  pprint(msg)
  j = get_msg_jid(msg)
  if j in last_outmsg:
    if last_outmsg[j][0] == msg:
      if len(last_outmsg[j]) > 2 and last_outmsg[j][2] < 1:
        info(f"停止记录msg id: {msg.id_}")
        last_outmsg.pop(j)
      else:

        info(f"更新msgid: {last_outmsg[j][1]} -> {msg.id_}")
        last_outmsg[j][1] = msg.id_
    else:
      info(f"msg不匹配: {last_outmsg[j][0]=} != {msg=}")
      last_outmsg.pop(j)
  else:
    logger.debug(f"忽略: {msg=}")
  return msg



#  @exceptions_handler
#  def xmpp_msg_p(msg):
#    # 状态消息，在线离线等
#    asyncio.create_task(_xmpp_msg_p(msg))

@auto_task
@exceptions_handler
async def msgxp(msg):
  dbg(f"got a xmpp p msg: {msg}")
  muc = str(msg.from_.bare())
  if msg.type_ == PresenceType.AVAILABLE:
    if msg.xep0045_muc_user:
      if muc in my_groups:
        jids = users[muc]
        room = rooms[muc]
        #  item = msg.xep0045_muc_user.items[0]
        #  print("---")
        #  print(msg)
        #  print(f"---{len(msg.xep0045_muc_user.items)}")
        for item in msg.xep0045_muc_user.items:

          if item.jid is None:
            #  pprint(msg)
            #  pprint(msg.xep0045_muc_user.items)
            #  pprint(item)
            err(f"item.jid is None: {msg} {msg.xep0045_muc_user.items} {item}")
            continue

          jid = str(item.jid.bare())
          res = f"上线: {len(msg.xep0045_muc_user.items)} {msg.from_} {jid} {item.nick} {item.role} {item.affiliation} {msg.status}"
          #  print(res)
          info(res)
          if item.nick is None:
            rnick = msg.from_.resource
            #  info(f"空nick：{item.jid} {item.nick} -> {rnick} {msg}")
          else:
            rnick = item.nick
          if rnick is None:
            warn(f"没找到nick：{item.jid} {item.nick} -> {rnick} {msg}")
            continue

          nick = f".ban {muc}/{rnick}"

          if jid in jids:
            if jid == myjid:
              if jid not in jids:
                #  j = [room.me.nick, room.me.affiliation, room.me.role]
                jids[jid] = []

              j = jids[jid]
              j.clear()
              j.extend([rnick, item.affiliation, item.role])

              if item.role == 'moderator':
                pass
              elif room.me is not None and room.me.role == 'moderator':
                pass
              else:
                err(f"没有管理权限: {muc} {rnick} {item.affiliation} {item.role} {room.me}")
              #  else:
              #    info(f"已存在nick记录: {jids[jid]}")
              #  continue
            #  if jid == myjid:
            #    #  info(f"不记录bot: {jid}")
            #    continue
            #  nick = f".ban {muc}/{msg.from_.resource}"

            elif jid in me:
              #  j = [msg.from_.resource, item.affiliation, item.role]
              j = [rnick, item.affiliation, item.role]
              jids[jid] = j
              #  continue

            else:
              j = jids[jid]
              if j[0] is None:
                j[0] = rnick
              if type(j[2]) is int:
                reason = "重新进群没用哦"
                if j[2] > 99:
                  if j[2] < time.time():
                    if member_only_mode is False or item.affiliation == "member":
                      w = j[4]
                      w[0] = 0
                      j[2] = "participant"
                      res = await room.muc_set_role(rnick, "participant", reason="临时禁言结束")
                      return
                    else:
                      # 不用解除禁言
                      j[2] = 1
                      if item.role == "participant":
                        await room.muc_set_role(rnick, "visitor", reason=reason)
                        return
                  else:
                      #  if j[2] > 99:
                    if item.role == "participant":
                      if item.affiliation == "member":
                        await room.muc_set_affiliation(item.jid.bare(), "none", "被临时禁言了请保持在线")
                      await room.muc_set_role(rnick, "visitor", reason=reason)
                      return
                elif j[2] == 1:
                  if member_only_mode:
                    if item.affiliation == "member":
                      j[2] = "participant"
                      if item.role == "visitor":
                        reason = "成员允许发言"
                        res = await room.muc_set_role(rnick, "participant", reason=reason)
                        return
                    else:
                      reason = "非成员暂时禁止发言"
                      if item.role == "participant":
                        await room.muc_set_role(rnick, "visitor", reason=reason)
                        return
                  else:
                    j[2] = "participant"
                    if item.role == "visitor":
                      reason = "非成员允许发言"
                      res = await room.muc_set_role(rnick, "participant", reason=reason)
                      return
                elif j[2] == 0:
                  if item.role == "participant":
                    if item.affiliation == "member":
                      await room.muc_set_affiliation(item.jid.bare(), "none", "被临时禁言了请保持在线")
                    await room.muc_set_role(rnick, "visitor", reason=reason)
                    return
                  #  res = await room.muc_set_role(rnick, "participant", reason="禁言结束")
              else:
                j[2] = item.role
                if member_only_mode:
                  reason = "非成员暂时禁止发言"
                  if item.affiliation == "none":
                    if item.role == "participant":
                      j[2] = 1
                      await room.muc_set_role(rnick, "visitor", reason=reason)
                      return
                else:
                  if item.role == "visitor":
                    if muc in public_groups:
                      reason = "不限制新人发言"
                      #  j[2] = "participant"
                      res = await room.muc_set_role(rnick, "participant", reason=reason)
                      return

              #  if j[0] != msg.from_.resource:
              if j[0] != rnick:
                #  j[0] = msg.from_.resource
                if item.role == "participant":
                  #  res = f"改名通知: {hide_nick(j[0])} -> {hide_nick(msg)}"
                  res = f"改名通知: {hide_nick(j[0])} -> {hide_nick(rnick)}"
                  send(res, muc, nick=nick)
                res = f"改名通知: {j[0]} -> {rnick}"
                j[0] = rnick
                send(f"{res}\njid: {jid}\nmuc: {muc}", nick=nick)
              j[1] = item.affiliation
              #  j[3] = time.time()
          else:
            j = [rnick, item.affiliation, item.role]
            if member_only_mode:
              if item.affiliation == "none":
                if item.role == "participant":
                  reason = "非成员暂时禁止发言"
                  #  j = jids[jid]
                  await room.muc_set_role(rnick, "visitor", reason=reason)
                  return
                elif item.role == "visitor":
                  j[2] = 1
                  #  jids[jid] = j
                  #  set_default_value(j)
                  #  return
              jids[jid] = j
            else:
              if item.role == "visitor":
                if muc in public_groups:
                  reason = "该群不限制新人发言"
                  res = await room.muc_set_role(rnick, "participant", reason=reason)
                  return

              jids[jid] = j
              if muc in bot_groups:
                welcome = f"欢迎 {hide_nick(msg)} ,这里是bot频道，专门用来测试bot，避免干扰主群。如有任何问题，建议根据群介绍前往主群沟通。该消息来自机器人(bot)，可不予理会。"
              elif muc in rss_groups or muc == acg_group:
                welcome = f"欢迎 {hide_nick(msg)} ,这里是rss频道，机器人推送消息很频繁。如有任何问题，建议根据群介绍前往主群沟通。该消息来自机器人(bot)，可不予理会。"
              elif muc == "wtfipfs@salas.suchat.org":
                welcome = f"欢迎 {hide_nick(msg)} ,该群新人默认不能发言。\n如果没有发言权，建议使用gajim或cheogram客户端申请。conversations不支持xmpp原生的申请方式。也可以群内私信bot：“申请发言权”，然后等管理批准。也可以改群内名字，添加“申请发言权”。\n建议经常在该群保持在线，管理看到就会给成员身份和发言权。\n该消息来自机器人(bot)，可不予理会。"
              else:
                welcome = f"欢迎 {hide_nick(msg)} ,如需查看群介绍，请发送 “.help”。该消息来自机器人(bot)，可不予理会。"
              send(welcome, muc, nick=nick)

            #  await send(f"有新人入群: {j[0]}\n身份: {j[1]}\n角色: {j[2]}\njid: {jid}\nmuc: {muc}", nick=nick)
            send(f"有新人入群: {j[0]}\n身份: {j[1]}\n角色: {item.role}\njid: {jid}\nmuc: {muc}", nick=nick)

          set_default_value(j)
          #  if len(jids[jid]) > 3:
          #    jids[jid][3] = int(time.time())
          #  else:
          #    jids[jid].append(int(time.time()))
          break
      else:
        pprint(msg)
        send(f"未知群组消息: {msg}")
    else:
      #  print(f"上线: {msg.from_} {msg.status}")
      info0(f"上线: {msg.from_} {msg.status}")
      #  if muc != rssbot:
      #    send(f"上线: {msg.from_} {msg.status}")
    #  for i in msg.xep0045_muc_user.items:
    #    pprint(i)
  elif msg.type_ == PresenceType.SUBSCRIBE:
    #  pprint(msg)
    # https://docs.zombofant.net/aioxmpp/devel/api/public/roster.html#aioxmpp.RosterClient.approve
    rc = XB.summon(aioxmpp.RosterClient)
    #  if get_jid(msg.from_) in me:
    if muc in me:
      #  pprint(rc)
      res = rc.approve(msg.from_)
      #  print(f"结果：{res}")
      #  print(f"结果：{res}")
      send("ok", msg.from_)
      warn(f"已同意状态订阅请求：{msg.from_} {res}")
      res = rc.subscribe(msg.from_)
    else:
      # https://docs.zombofant.net/aioxmpp/devel/api/public/roster.html#aioxmpp.RosterClient.remove_entry
      send(f"非管理禁止订阅，但可以私聊。暂时只支持ping命令，别的私聊消息会转发给管理。不要开启加密，bot暂时不支持。管理的xmpp账号: xmpp:{ME} 群: xmpp:{main_group}?join", msg.from_)
      try:
        res = await rc.remove_entry(msg.from_, timeout=5)
      except errors.XMPPModifyError as e:
        res = "err"
        if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}item-not-found":
          info("多余的联系人删除，此段代码可以删掉")
        else:
          warn(f"未知错误，待修复的联系人删除: {msg.from_} {e=}")
      warn(f"已拒绝状态订阅请求：{msg.from_} {res=}")
  elif msg.type_ == PresenceType.UNAVAILABLE:
    #  print(f"离线: {msg.from_} {msg.status}")
    info0(f"离线: {msg.from_} {msg.status}")
    #  if muc in my_groups:
    #    pass
    #  else:
    #    await sendg(f"离线: {msg.from_} {msg.status}")
    #  if hasattr(msg, "xep0045_muc_user"):
    #    print(f"离线: {msg.from_} {msg.status} {msg.xep0046_muc_user}")
    #    if msg.xep0045_muc_user is None:
    #      #  if msg.xep0045_muc_user:
    #      #  pprint(msg.xep0045_muc_user)
    #      await sendg(f"离线: {msg.from_} {msg.status}")
    #  else:
    #    print(f"离线: {msg.from_} {msg.status}")
    #    #  pprint(msg)
    #    await sendg(f"离线n: {msg.from_} {msg.status}")
    #  if muc in me:
    #    await sendg(f"离线: {msg.from_} {msg.status} {msg.xep0045_muc_user}")
  else:
    #  pprint(msg)
    #  print(f"未知状态{msg.type_}: {msg.from_} {msg.status}")
    info(f"未知状态 {msg.type_}: {msg.from_} {msg.status}")
    #  if muc in me:
    #    await sendg(f"{msg.type_}: {msg.from_} {msg.status}")

def hide_nick(msg):
  if type(msg) is str:
    nick = msg
  elif msg.type_ == MessageType.CHAT:
    nick = msg.from_.localpart
  elif msg.type_ == MessageType.GROUPCHAT:
    nick = msg.from_.resource
  elif msg.type_ == PresenceType.AVAILABLE:
    if str(msg.from_.bare()) in my_groups:
      nick = msg.from_.resource
    else:
      nick = msg.from_.localpart
  else:
    return f"{msg.type_=}"
  if  re.match(r'^[a-zA-Z0-9_\.]+$', nick):
    pass
  elif len(nick) < 4:
    pass
  else:
    nick = f"{nick[:3]}..."
  return nick



def get_src(msg):
  if msg.type_ == MessageType.GROUPCHAT:
    return str(msg.from_.bare())
  if msg.from_.is_bare:
    return str(msg.from_)
  if str(msg.to.bare()) in my_groups:
    return str(msg.from_)
  return str(msg.from_.bare())


#  def gmsg(msg, member, source, **kwargs):
#  @exceptions_handler
#  def x_msg(msg):
#    #  if hasattr(msg, "xep0203_delay"):
#    #    pprint(msg.xep0203_delay)
#    #    info("skip msg: delayed: {msg.xep0203_delay}")
#    #  if hasattr(msg, "xep308_replace"):
#    #    pprint(msg.xep308_replace)
#    asyncio.create_task(_xmpp_msg(msg))
#    #  return
#    #  info("\n>>> msg: %s\n" % msg)



private_locks = {}

@auto_task
@exceptions_handler
async def msgx(msg):
  dbg(f"got a xmpp msg: {msg}")
  #  if str(msg.from_.bare()) == rssbot:
  #    pprint(msg)
  muc = str(msg.from_.bare())
  nick = msg.from_.resource
  if nick is None:
    if msg.type_ == MessageType.ERROR:
      warn(f"收到错误消息：{msg} {msg.error}")
      return
    pprint(msg)
    warn(f"收到系统消息: {muc} {msg.from_} {msg.body} {msg}")
    return
  #  if not hasattr(msg, "body"):
  #    #  print("%s %s" % (type(msg), msg.type_))
  #    return

  real_time = None
  if msg.xep0203_delay:
    delay = msg.xep0203_delay[0]
    #  pprint(delay)
    #  await sleep(1)
    real_time = delay.stamp.timestamp()
    if time.time() - real_time > 60:
      #  info("跳过旧消息: %s %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, short(msg.body), delay))
      info("跳过旧消息: %s %s %s" % (str(msg.from_), short(msg.body), delay))
      return
    else:
      info("旧消息: 延迟%ss %s %s %s %s %s" % (time.time() - delay.stamp.timestamp(), msg.type_, msg.id_,  str(msg.from_), msg.to, short(msg.body)))
  else:
    #  info(f"假定消息无延迟: {msg}")
    real_time = time.time()


  #  clear_msg_jid(msg)

  #  text = None
  #  for i in msg.body:
  #    text = msg.body[i]
  #    break
  if msg.body:
    text = msg.body.any()
    if len(msg.body) > 1:
      warn(f"收到多语言消息: {muc} {msg.from_} {msg.body}")
  else:
    return
  is_admin = False
  jid = None
  if muc in my_groups:

    room = rooms[muc]
    #  if str(msg.from_) == str(rooms[muc].me.conversation_jid.bare()):
    #  if msg.from_.resource == rooms[muc].me.nick:
    if room.me is not None and nick == room.me.nick:
      info("跳过1: %s %s" % (msg.from_, short(text)))
      return

    jids = users[muc]
    j = jids[myjid]
    if nick == j[0]:
      info("跳过2: %s %s" % (msg.from_, short(text)))
      return

    rejoin = False
    while True:
      existed = False
      for i in room.members:
        #  if i.direct_jid is None:
        #    err("没有权限查看jid: {muc}")
        #    return
        #  if i.nick == msg.from_.resource:
        if i.nick == nick:
          jid = str(i.direct_jid.bare())
          if jid == myjid:
            warn("跳过3: %s %s" % (msg.from_, short(text)))
            return
          existed = True

          if jid not in jids:
            err(f"{jid} not in jids of: {muc}")
            #  return
            j = [nick, i.affiliation, i.role]
            set_default_value(j)
            jids[jid] = j

          #  if str(i.direct_jid.bare()) == myjid:
          if member_only_mode:
            if i.affiliation == 'none':
              reason = "非成员暂时禁止发言"
              #  jids = users[muc]
              jids[jid][2] = 1
              await room.muc_set_role(i.nick, "visitor", reason=reason)
              return
          #  if str(i.direct_jid.bare()) in me:
          if jid in me:
            is_admin = True
            info(f"admin msg: {short(text)}")
          break

      if not existed:
        if rejoin is False:
          warn("leave muc: {muc}")
          await room.leave()
          rejoin = True
          rooms.pop(muc)
          warn("检测到幽灵发言: %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
          await sleep(5)
          if await join(muc):
            room = rooms[muc]
            warn("joined muc: {muc}")
            continue
        else:
          send_log("重新进群无效，忽略幽灵发言%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
          return
      break

    #  if msg.type_ == MessageType.CHAT:

    if is_admin is False:
      info(f"group msg: {short(text)}")

    if not is_admin:
      j = jids[jid]
      #  if len(j) < 4:
      #    err(f"缺少记录: {j}")
      #  else:

      #  j[4] = ( j[4] + (text.count('\n') + len(text)/wtf_line)*wtf_time/(time.time()-j[5]) ) / 2
      w = j[4]
      score = w[0]
      #  global wtf_limit
      #  if score > wtf_limit:
      if score > wtf_limit/(9/(w[1]+8) +0.1):
        if type(j[2]) is str:
          warn(f"fixme: 跳过已禁言用户的消息{int(j[2]-real_time)}: {muc} {nick} {short(text)}")
        else:
          info(f"跳过已禁言用户的消息{int(j[2]-real_time)}: {muc} {nick} {short(text)}")
          j[2] = int(j[2] + wtf_ban_time)
      else:
        if score < wtf_limit/2:
          need_warn = True
        else:
          need_warn = False

        #  last = time.time() - j[3]
        last = real_time - j[3]
        j[3] = time.time()

        if last > wtf_time_max:
          score -= 2*last/wtf_time
          if score < 0:
            score = 0
        #  tmp = min(last/wtf_time, w[1], wtf_limit)

        long = text.count('\n') + len(text)//wtf_line + 1
        w[0] = score + long*wtf_time/last
        w[1] += 1
        #  if is_admin:
        #    send(f"now: {w[0]} / {wtf_limit}", jid=muc)
        if w[1] > 1 and w[0] > wtf_limit/(9/(w[1]+8) +0.1):
          j[2] = int(time.time() + wtf_ban_time)
          role = "visitor"
          reason = "不要刷屏"
          res = await room.muc_set_role(nick, role, reason=reason)
          warn(f"有人刷屏: {nick}\njid: {jid}\nmuc: {muc}\nnow: {w[0]}/{wtf_limit}/{w[1]}\n{res}")
          send(f"检测到刷屏，禁言{wtf_ban_time}s: {nick} {w[0]}/{wtf_limit}", jid=muc)
        elif need_warn:
          if w[1] == 1 and w[0] > wtf_limit/2:
            send(f"{nick}, 不要刷屏 {w[0]}/{wtf_limit}", jid=muc)
            w[0] = wtf_limit/2
          elif w[0] > wtf_limit/2:
            send(f"{nick}, 不要刷屏（第一次警告） {w[0]}/{wtf_limit}", jid=muc)
        

  elif muc == myjid:
    info0("跳过自己发送的消息: %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
    return
  elif muc in me:
    is_admin = True
    info(f"admin pm msg: {short(text)}")
    if text.startswith("> "):
      ts = text.splitlines()
      if len(ts) > 1:
        for i in range(len(ts)):
          if not ts[i].startswith(">"):
            break
        ts = ts[i:]
        if len(ts) != 0:
          if ts[0] == "":
            ts = ts[:1]
        if len(ts) == 0:
          reply = msg.make_reply()
          reply.body[None] = "skip empty msg"
          send(reply)
          return
        if text.startswith("> id: "):
          tid = int(text.split(" ", 3)[2])

          send("\n".join(ts), tid, name="**X admin:** ")

          reply = msg.make_reply()
          reply.body[None] = "ok"
          send(reply)
          return
        if text.startswith("> xmpp: "):

          tt = text.split(" ", 3)[2]
          tjid = text.split(" ", 4)[3][:-1]

          tjidb = tjid.split("/")[0]
          #  tj = JID.fromstr(tjid)
          if tt == "MessageType.CHAT":
            if tjidb in my_groups:
              pass
            else:
              tjid = tjidb
            #  send(text, tjid)
            send("\n".join(ts), tjid, name="**X admin:** ")
            reply = msg.make_reply()
            reply.body[None] = "ok"
            send(reply)
            return
          else:
            pass


      reply = msg.make_reply()
      reply.body[None] = "?"
      send(reply)
      return
    nick = msg.from_.localpart
  elif muc == rssbot:
    #  if msg.type_ == None:
    send(text, acg_group, name="", delay=5)
    return
  else:
    info("未知来源的消息%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
    jid = str(msg.from_.bare())
    if jid not in private_locks:
      private_locks[jid] = asyncio.Lock()
    try:
      async with asyncio.timeout(60):
        async with private_locks[jid]:
          if text == "ping":
            reply = msg.make_reply()
            reply.body[None] = "pong"
            send(reply)
            await sleep(1)
            return
          if msg.type_ == MessageType.ERROR:
            send_log("未知来源的消息(wtf) %s %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), f"{msg.from_=}", msg.to, msg.body))
            await sleep(1)
            return
          send(f"暂时只支持ping命令，别的私聊消息会转发给管理。\n不要开启加密，bot暂时不支持。\n管理的xmpp账号: xmpp:{ME}\n群: xmpp:{main_group}?join", msg.from_)
          #  chat = await get_entity(CHAT_ID, True)
          #  await UB.send_message(chat, f"{msg.type_} {msg.from_}: {text}")
          #  send_log(f"{msg.type_} {msg.from_}: {text}")
          send(f"xmpp: {msg.type_} {msg.from_}: {text}", MY_ID)
          send(f"xmpp: {msg.type_} {msg.from_}: {text}", ME, name="")
          await sleep(1)
    except TimeoutError:
      pass
    return
    #  pprint(msg)

  info0("%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))

  j = get_msg_jid(msg)
  if j in last_outmsg:
    last_outmsg.pop(j)

  info(f"original text: {short(text)}")
  text0 = text
  if msg.type_ == MessageType.GROUPCHAT:
    if muc == acg_group:
      if is_admin:
        send(text, rssbot, name="")
      else:
        send("仅管理可用", muc)
      return

    username=f"**X {nick}:** "
    name=f"X {nick}"
    qt = None
    #  if text.startswith('> ') or text.startswith('>> '):
    if text.startswith('>'):
      qt=[]
      tmp= text.splitlines()
      exqt = False
      k = 0
      for i in tmp:
        if i.startswith('>> '):
          qt.append("%s" % i.split(' ', 1)[1])
          exqt = True
        elif i.startswith('> > '):
          qt.append("%s" % i.split(' ', 2)[2])
          exqt = True
        elif i.startswith('> '):
          if exqt:
            qt.append("")
            exqt = False
          qt.append("%s" % i.split(' ', 1)[1])
        elif i.startswith('>'):
          if exqt:
            qt.append("")
            exqt = False
          qt.append("%s" % i[1:])
        elif i == "":
          if len(qt) > 0:
            qt.append(i)
        else:
          if len(qt) > 0:
            #  tmp = tmp[len(qt):]
            text0='\n'.join(tmp[k:])
            #  tmp = qt
            #  tmp='\n'.join(qt)
            #  text = f"{text0}\n\n{tmp}"
            text = text0 + "\n\n" + "\n".join(qt)
            #  qt2 = '\n> '.join(tmp)
            #  username = f"> {qt2}\n{username}"
          break
        k += 1
        #  warn("fixme: {tmp} != {qt}")
      if text0 != text:
        info(f"delete qt: {short(text0)}")
      else:
        qt = None
    ms = get_mucs(muc)
    #  for m in ms - {muc}:
    for m in ms - {muc}:
      #  asyncio.create_task( send_xmpp(f"{username}{text0}", m, name=name) )
      asyncio.create_task( send_xmpp(f"{username}{text0}", m, name=name, qt=qt) )
    if main_group in ms:
      asyncio.create_task( mt_send_for_long_text(text0, name=name, qt=qt) )
      await send_tg(f"{username}{text0}", GROUP_ID, qt=qt)
      await send_tg(f"{username}{text0}", GROUP2_ID, topic=GROUP2_TOPIC, qt=qt)
    elif muc in bot_groups:
      await send_tg(f"{username}{text0}", CHAT_ID, qt=qt)
    #  text = text2
  #  if msg.type_ == MessageType.GROUPCHAT:
  #    pass
  elif msg.type_ == MessageType.NORMAL:
    warn(f"wtf: normal msg: {msg}")
    return
  elif msg.type_ == MessageType.CHAT:
    #  if get_jid(msg.to) in my_groups:
    #  if get_jid(msg.from_) in my_groups:
    if muc in my_groups:
      nick = msg.from_.resource
    else:
      nick = msg.from_.localpart
    if is_admin is False:
      info("群内私聊: %s: %s" % (msg.from_, short(text)))
      #  await sendme(f"群内私聊 {msg.type_} {msg.from_}: {text}")

      #  send_log(f"群内私聊: {msg.type_} {msg.from_}: {text}")

      #  tjid = str(msg.from_)
      if muc not in private_locks:
        private_locks[muc] = asyncio.Lock()
      try:
        async with asyncio.timeout(60):
          async with private_locks[jid]:
            if text == "ping":
              reply = msg.make_reply()
              reply.body[None] = "pong"
              send(reply)
              await sleep(1)
              return

            res = f"xmpp: {msg.type_} {msg.from_}: {text}\njid: xmpp:{jid}"
            send(res, MY_ID)
            send(res, ME, name="")
            reply = msg.make_reply()
            reply.body[None] = "ok"
            send(reply)
            await sleep(1)
      except TimeoutError:
        warn(f"转发超时 {msg.from_}: {short(text)}")
      return
  elif msg.type_ == MessageType.ERROR:
    warn(f"收到错误消息：{msg} {msg.error}")
    return
  else:
    pprint(msg)
    info(f"skip unknown type: {msg.type_} {msg}")
    return

  if text == "ping":
    reply = msg.make_reply()
    reply.body[None] = "pong"
    send(reply)
    return

  res = await run_cmd(text0, get_src(msg), f"X {nick}: ", is_admin, qt)
  if res is True:
    return
  if res:
    reply = msg.make_reply()
    reply.body[None] = res
    send(reply)
    return

  return
  if get_jid(msg.from_) not in me:
    return
  #  awai:t mt_send(text, 'me', get_jid(msg.from_))
  if text == "test":
    logger.setLevel(logging.DEBUG)
    reply = msg.make_reply()
    reply.body[None] = "ok"
    send(reply)
  elif text == "ok":
    info(f"got a msg: ok")
  elif text == "correct":
    reply = msg.make_reply()
    reply.body[None] = generand(3)
    send(reply, correct=True)
  #  elif text == "correct":
  #    pprint(msg.xep308_replace)

  #  pprint(msg)
  return
  print(">>>> %s << %s" % (msg.body, msg))
  src = msg.from_
  text = msg.body

def get_jid_room(cmds, src):
  if src in my_groups or '/' in cmds[1]:
    muc = cmds[1].split('/', 1)[0]
    if muc in my_groups:
      nick = cmds[1].split('/', 1)[1]
    else:
      muc = src
      nick = cmds[1]
    #  if muc not in rooms:
    #    return f"没找到room: {muc}"
    room = rooms[muc]
    jids = users[muc]
    #  jid = None
    #  for i in room.members:
    #    if i.direct_jid:
    #      if str(i.direct_jid.bare()) not in jids:
    #        jids[str(i.direct_jid.bare())] = [i.nick, i.affiliation, i.role]
    #      if i.nick == nick:
    #        jid = str(i.direct_jid.bare())
    for jid, j in jids.items():
      if j[0] == nick:
        jid = JID.fromstr(jid)
        return jid, room
    #  if jid is None:
    return f"没找到: {nick}\nmuc: {muc}"
  elif "@" in cmds[1] and src in my_groups:
    muc = src
    if muc not in rooms:
      return f"没找到room: {muc}"
    jid = cmds[1]
    room = rooms[muc]
    jids = users[muc]
    if jid in jids:
      jid = JID.fromstr(jid)
      return jid, room
    else:
      return f"没找到该jid: {jid}\nmuc: {muc}"

  #  elif cmds[1].startswith("X ") and src in my_groups:
  elif src in my_groups:

    muc = None
    nick = cmds[1]
    if cmds[1].startswith("X "):
      nick = nick[2:]
      if nick[-1] == ' ':
        nick = nick[:-1]

    for m in get_mucs(src):
      room = rooms[m]
      for i in room.members:
        if i.nick == nick:
          jid = str(i.direct_jid.bare())
          break
      if muc is not None:
        break
    if muc is None:
      for m in get_mucs(src):
        jids = users[m]
        for jid, j in jids.items():
          if j[0] == nick:
            room = rooms[m]
            break
        if muc is not None:
          break
    if muc is None:
      return f"没找到nick: {nick}"
    #  if jid in jids:
    #    pass
    #  else:
    #    for i in room.members:
    #      if i.direct_jid:
    #        if str(i.direct_jid.bare()) not in jids:
    #          jids[str(i.direct_jid.bare())] = [i.nick, i.affiliation, i.role]
    #    if jid not in jids:
    #      return f"没找到该jid对应的nick: {jid}\nmuc: {muc}"
    #    else:
    #      pass
  else:
    return "格式不正确"
  return jid, room

def get_nick_room(cmds, src):
  if src in my_groups or '/' in cmds[1]:
    muc = cmds[1].split('/', 1)[0]
    if muc in my_groups:
      nick = cmds[1].split('/', 1)[1]
      if nick.endswith(": "):
        nick = nick[:-2]
    else:
      muc = src
      nick = cmds[1]
    if muc not in rooms:
      return f"没找到room: {muc}"
    room = rooms[muc]
    #  is_ok = False
    #  for i in room.members:
    #    if i.nick == nick:
    #      is_ok = True
    #      break
    #  if is_ok is False:
    #    return f"没找到nick: {nick}\nmuc: {muc}"
  elif "@" in cmds[1] and src in my_groups:
    muc = src
    if muc not in rooms:
      return f"没找到room: {muc}"
    jid = cmds[1]
    room = rooms[muc]
    jids = users[muc]
    if jid in jids:
      nick = jids[jid][0]
    else:
      return f"没找到该jid对应的nick: {jid}\nmuc: {muc}"
      #  for i in room.members:
      #    if i.direct_jid:
      #      if str(i.direct_jid.bare()) not in jids:
      #        jids[str(i.direct_jid.bare())] = [i.nick, i.affiliation, i.role]
      #  if jid not in jids:
      #    return f"没找到该jid对应的nick: {jid}\nmuc: {muc}"
      #  else:
      #    nick = jids[jid][0]
  elif src in my_groups:
  #  elif cmds[1].startswith("X ") and src in my_groups:
    muc = None
    nick = cmds[1]
    if cmds[1].startswith("X "):
      nick = nick[2:]
      if nick[-1] == ' ':
        nick = nick[:-1]

    for m in get_mucs(src):
      room = rooms[m]
      for i in room.members:
        if i.nick == nick:
          muc = m
          break
      if muc is not None:
        break
    if muc is None:
      for m in get_mucs(src):
        jids = users[m]
        for jid, j in jids.items():
          if j[0] == nick:
            room = rooms[m]
            muc = m
            break
        if muc is not None:
          break
    if muc is None:
      return f"没找到nick: {nick}"
        
  else:
    return "格式不正确"
  return nick, room




def load_chat_id(s):
  if s.isnumeric():
    return int(s)
  if s.startswith('-'):
    if s[1:].isnumeric():
      s = s[1:]
      return -1*int(s)
  return s
  #  raise ValueError("需要数字")


def unban(muc, nick=None, jid=None):
  #  w = j[4]
  jids = users[muc]
  for jj in jids:
    if nick:
      j = jids[jj]
      if i[0] == nick:
        j[2] = "participant"
    elif jid:
      if jid == jj:
        j = jids[jj]
        j[2] = "participant"
    else:
      return





member_only_mode = False

cmd_funs = {}
cmd_for_admin = set()

async def init_cmd():

  #  async def _(cmds: list, src: str | int) -> str | bool | None:
  async def _(cmds: list, src: str | int) -> tuple:
    return 0, "pong"
  cmd_funs["ping"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    tmp = set()
    cmds_admin = set()
    cmds_all = set()
    for k, v in cmd_funs.items():
      if k == 'cmd':
        continue
      if k in cmds_all:
        continue

      cmds_all.add(k)
      k1 = k

      for k2, v2 in cmd_funs.items():
        if k2 == k:
          continue
        if k2 in cmds_all:
          continue
        if v is v2:
          k1 += ' / '
          k1 += k2
          cmds_all.add(k2)

      if k in cmd_for_admin:
        cmds_admin.add(k1)
      else:
        tmp.add(k1)

    res = '可用的命令:\n'
    #  res += '\n'.join(cmds)
    res += '\n'.join(sorted(tmp))
    if cmds_admin:
      res += '\n\n仅管理可用的命令:\n'
      #  res += '\n'.join(cmds_admin)
    res += '\n'.join(sorted(cmds_admin))
    return 0, res
  cmd_funs["cmd"] = _


  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"disco\n.{cmds[0]} $domain\nhttps://docs.zombofant.net/aioxmpp/devel/api/public/disco.html?highlight=disco#aioxmpp.DiscoClient"
    if len(cmds) == 3:
      ns = cmds[2]
    else:
      ns = None
    if cmds[1] == "me":
      res = await disco_info(JID.fromstr(src).domain, node=ns)
    elif cmds[1] == "you":
      res = await disco_info(node=ns)
    else:
      res = await disco_info(cmds[1], node=ns)
    if res:
      res = res.to_dict()
    return 0, res
  cmd_funs["disco"] = _
  cmd_for_admin.add('disco')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"discoi\n.{cmds[0]} $domain\nhttps://docs.zombofant.net/aioxmpp/devel/api/public/disco.html?highlight=disco#aioxmpp.DiscoClient"
    if len(cmds) == 3:
      ns = cmds[2]
    else:
      ns = None
    if cmds[1] == "me":
      res = await disco_item(JID.fromstr(src).domain, node=ns)
    elif cmds[1] == "you":
      res = await disco_item(node=ns)
    else:
      res = await disco_item(cmds[1], node=ns)
    if res:
      tmp = ""
      for i in res.items:
        tmp += "%s %s %s %s\n\n" % (i.name, i.node, i.jid, await get_server_name(i.jid))
      res = tmp
      
    return 0, res
  cmd_funs["discoi"] = _
  cmd_for_admin.add('discoi')



  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return f"download file by url\n.{cmds[0]} $url [raw/curl/tg/clear[2]] [direct] [timeout]"
    if cmds[1] == "clear":
      if src in tg_download_tasks:
        tg_download_tasks.remove(src)
      #  if src in music_bot_state:
      #    music_bot_state.pop(src)
      return 0, "ok"
    elif cmds[1] == "clear2":
      tg_download_tasks.clear()
      #  music_bot_state.clear()
      await sleep(interval+1)
      tg_download_tasks.clear()
      return 0, "ok"
    if len(cmds) == 3:
      if cmds[2] == "tg":
        try:
          #  if src == log_group_private:
          if len(cmds) == 3:
            if cmds[2] == "tg":
              res = await UB.send_file(CHAT_ID, file=cmds[1], caption=cmds[1])
              return 0, "sent in tg"
        except Exception as e:
          warn(f"通过tg远程下载失败: {e=}")
          return 0, "failed"
    opts = cmds[2:4]
    while True:
      if len(opts) < 2:
        opts.append("")
      else:
        break
    if len(cmds) == 5:
      max_time = cmds[4]
    else:
      #  opts.append("600")
      max_time = run_shell_time_max
    opts.append(str(max_time))
    res = await get_title(cmds[1], src, opts=opts, max_time=max_time)
    return 0, f"{res}"
  cmd_funs["down"] = _
  cmd_for_admin.add('down')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"get title\n.{cmds[0]} $url [raw/curl] [direct]"
    res = await get_title(cmds[1], opts=cmds[2:4], src=src)
    return 0, f"{res}"
  cmd_funs["tl"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"get title\n.{cmds[0]} $url [raw/curl] [direct]"
    res = await get_title(cmds[1], src=src, opts=cmds[2:4])
  cmd_funs["tl2"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"bash\n.{cmds[0]} $code"
    return 0, str(time.time())
  cmd_funs["now"] = _

  #  async def _(cmds: list, src: str | int) -> str | bool | None:
  #    if len(cmds) == 1:
  #      return f"bash\n.{cmds[0]} $code"
  #    cmds = cmds[0]
  #    cmds = list(f"{x}\n" for x in cmds.splitlines())
  #    await run_run( myshell(cmds, src=src) , False)
  #  cmd_funs["date"] = _

  for i in [
      "date",
      "free",
      "cal"
      ]:
    async def _(cmds: list, src: str | int) -> tuple:
      cmds = cmds[0]
      #  cmds = list(f"{x}\n" for x in cmds.splitlines())
      #  await run_run( myshell(cmds, src=src) , False)
      await myshell(cmds, src=src)
      return 512,
    cmd_funs[i] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"bash\n.{cmds[0]} $code"
    cmds.pop(0)
    #  res = await my_popen(cmds)
    #  res = await my_popen(' '.join(cmds), src=src, shell=True)
    #  res = await my_sexec(' '.join(cmds), src=src)
    res = await my_sshell(' '.join(cmds), src=src)
    return 0, format_out_of_shell(res)
  cmd_funs["sh3"] = _
  cmd_for_admin.add('sh3')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"bash -l\n.{cmds[0]} $code"
    #  cmds[0] = "bash"
    cmds.pop(0)
    text = ' '.join(cmds)
    cmds = ["bash", "-c", text]
    res = await my_sexec(cmds, src=src)
    return 0, format_out_of_shell(res)
  cmd_funs["sh2"] = _
  cmd_for_admin.add('sh2')

  async def _(cmds: list, src: str | int) -> tuple:
    global myshell_p
    if len(cmds) == 1:
      return 0, f"bash -i\n.{cmds[0]} $code/stop/restart/err/kill\n'\\ '会翻译成空格再执行"
    elif len(cmds) == 2:
      if cmds[1] == "restart":
        if await stop_sub(myshell_p):
          #  myshell_p = await asyncio.create_subprocess_shell("bash -i", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
          if await init_myshell():
            return 0, "ok"
        return 0, "failed"
      elif cmds[1] == "stop":
        if await stop_sub(myshell_p):
          return 0, "ok"
        else:
          return 0, "failed"
      elif cmds[1] == "kill":
        myshell_p.kill()
        return 0, "ok"
      elif cmds[1] == "err":
        #  raise OSError("stop by sh3")
        raise SystemExit("stop by me, restart...")
        return 0, "ok"
    cmds.pop(0)
    cmds = ' '.join(cmds)
    #  cmds = list(f"{x}\n" for x in cmds.splitlines())
    #  res = await my_sshell("bash -i", ext=' '.join(cmds), src=src)
    #  res = await myshell(cmds, src=src)
    #  res = await run_run( myshell(cmds, src=src) , False)
    await myshell(cmds, src=src)
    return 512,
    #  if res:
    #    res = f"```\n{res}```"
    #  return format_out_of_shell(res)
  cmd_funs["sh"] = _
  cmd_for_admin.add('sh')

  async def _(cmds: list, src: str | int) -> tuple:
    global myshell_p
    if len(cmds) == 1:
      return 0, f"bash -i\n不显示临时结果，只显示最终结果\n.{cmds[0]} $code"
    cmds.pop(0)
    cmds = ' '.join(cmds)
    res = await myshell(cmds)
    return 0, format_out_of_shell(res)
  cmd_funs["sh5"] = _
  cmd_for_admin.add('sh5')

  async def _(cmds: list, src: str | int) -> tuple:
    cmds = f'''
    if [[ -e "{SH_PATH}/STOP" ]]; then
      rm "{SH_PATH}/STOP"
      echo running
    else
      touch "{SH_PATH}/STOP"
      echo stoped
    fi
    '''
    res = await myshell(cmds)
    return 0, format_out_of_shell(res)
  cmd_funs["stop"] = _
  cmd_for_admin.add('stop')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"python\n.{cmds[0]} $code"
    cmds.pop(0)
    res = await my_py(' '.join(cmds), src)
    return 0, f"{res}"
  cmd_funs["py"] = _
  cmd_for_admin.add('py')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"exec\n.{cmds[0]} $code"
    cmds.pop(0)
    #  res = await my_exec2(' '.join(cmds), src)
    #  if res is 0:
    #    return "end"
    return 0, await my_exec2(' '.join(cmds), src)
  cmd_funs["exec"] = _
  cmd_for_admin.add('exec')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"exec in main thread\n.{cmds[0]} $code"
    cmds.pop(0)
    return 0, await my_exec(' '.join(cmds), src)
  cmd_funs["exec0"] = _
  cmd_for_admin.add('exec0')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"python eval()\n.{cmds[0]} $code"
    cmds.pop(0)
    res = await my_eval(' '.join(cmds))
    return 0, f"{res}"
  cmd_funs["eval"] = _
  cmd_for_admin.add('eval')

  async def _(cmds: list, src: str | int) -> tuple:
    #  if len(cmds) == 1:
    #    return f"{cmds[0]}\n.{cmds[0]}"
    global member_only_mode
    if member_only_mode is False:
      member_only_mode = True
      reason = "非成员暂时禁止发言"
      role = "visitor"
      i = 0
      k = 0
      for muc in rooms:
        if muc not in public_groups:
          continue
        #  muc = str(room.jid.bare())
        room = rooms[muc]
        jids = users[muc]
        for m in room.members:
          jid = str(m.direct_jid.bare())
          if jid not in jids:
            info(f"{jid} not in jids({muc})")
            continue
          if m.affiliation == "none":
            jids[jid][2] = 1
            if m.role == "participant":
              res = await room.muc_set_role(m.nick, role, reason=reason)
              info(res)
              i += 1
              if muc == src:
                k += 1
      return 0, "%s, 禁言账户：%s/%s" % (reason, k, i)
    else:
      member_only_mode = False
      reason = "非成员允许发言"
      role = "participant"
      i = 0
      k = 0
      for muc in rooms:
        if muc not in public_groups:
          continue
        #  muc = str(room.jid.bare())
        room = rooms[muc]
        jids = users[muc]
        for m in room.members:
          jid = str(m.direct_jid.bare())
          #  if jids[jid][2] == 1 or ( m.affiliation == "none" and m.role == "visitor" ):
          if jid not in jids:
            info(f"{jid} not in jids({muc})")
            continue

          j = jids[jid]
          #  if j[2] == "visitor":
          if m.role == "visitor":
            j[2] = "participant"
            res = await room.muc_set_role(m.nick, role, reason=reason)
            info(res)
            i += 1
            if muc == src:
              k += 1

          elif j[2] == 1:
            j[2] = "participant"

      return 0, "%s, 解除账户：%s/%s" % (reason, k, i)
  cmd_funs["mo"] = _
  cmd_for_admin.add('mo')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"{cmds[0]}\n.{cmds[0]} $jid/$nick"
    res = get_nick_room(cmds, src)
    if type(res) is str:
      return 0, res
    nick = res[0]
    room = res[1]
    reason = "cmds[0]命令"

    for i in room.members:
      if i.nick == nick:
        res = await room.ban(i, reason)
        return 0, f"ok: {res}"

    res = get_jid_room(cmds, src)
    if type(res) is str:
      warn(res)
      role = "visitor"
      try:
        res = await room.muc_set_role(nick, role, reason=reason)
      except Exception as e:
        muc = str(room.jid.bare())
        return 0, f"failed: {muc}"
      return 0, f"ok2: {res}"
    jid = res[0]
    room = res[1]
    #  muc = str(room.jid)
    #  unban(muc, jid=jid)
    affiliation = "outcast"
    res = await room.muc_set_affiliation(jid, affiliation, reason=reason)
    return 0, f"ok3: {res}"

    return 0, "not found"
  cmd_funs["ban"] = _
  cmd_for_admin.add('ban')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"{cmds[0]}\n.{cmds[0]} $jid/$nick"

    if '/' in cmds[1]:
      #  muc = cmds[1].split('/', 1)[0]
      #  if muc in my_groups:
      #    nick = cmds[1].split('/', 1)[1]
      res = get_nick_room(cmds, src)
      if type(res) is str:
        if src == log_group_private:
          nick = cmds[1]
          muc = cmds[1].split('/', 1)[0]
          if muc in my_groups:
            nick = cmds[1].split('/', 1)[1]
        else:
          return 0, res
      else:
        nick = res[0]
    else:
      nick = cmds[1]

    reason = "cmds[0]命令"
    res2 = ""
    for room in rooms.values():
      muc = str(room.jid.bare())
      for i in room.members:
        if i.nick == nick:
          res = await room.ban(i, reason)
          res2 += f"\nok: {muc} {res}"

    if res2:
      return 0, f"ok: {nick}{res2}"

    res2 = ""
    res3 = ""
    for room in rooms.values():
      muc = str(room.jid.bare())
      #  for i in room.members:
      try:
        role = "visitor"
        res = await room.muc_set_role(nick, role, reason=reason)
        res2 += f"\nok: {muc} {res}"
      except Exception as e:
        res3 += f"\nfailed: {muc}"
    if res2:
      res = f"ok2: {nick}{res2}\n{res3}"
      err(res)
      return 0, res

    res = get_jid_room(cmds, src)
    if type(res) is str:
      if src == log_group_private:
        nick = cmds[1]
        muc = cmds[1].split('/', 1)[0]
        if muc in my_groups:
          nick = cmds[1].split('/', 1)[1]

        jid = None
        for room in rooms.values():
          room = rooms[muc]
          jids = users[muc]
          for jid, j in jids.items():
            if j[0] == nick:
              jid = JID.fromstr(jid)
              break
          if jid is not None:
            break

        if jid is None:
          warn(f"没找到: {nick}")
          return 0, f"没找到: {nick}"
      else:
        return 0, res
    #    else:
    #      warn(res)
    else:
      jid = res[0]

    res2 = ""
    res3 = ""
    affiliation = "outcast"
    for room in rooms.values():
      muc = str(room.jid.bare())
      try:
        res = await room.muc_set_affiliation(jid, affiliation, reason=reason)
        res2 += f"\nok: {muc} {res}"
      except Exception as e:
        res3 += f"\nfailed: {muc}"

    if res2:
      res = f"ok3: {nick} {jid}{res2}\n{res3}"
    else:
      res = f"failed3: {nick} {jid}"
    return 0, res
  cmd_funs["banall"] = _
  cmd_for_admin.add('banall')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"临时踢出\n.{cmds[0]} $jid/$nick"

    #  option = False
    #  if len(cmds) == 3:
    #    option = cmds[1]
    #    cmds.pop(1)

    res = get_nick_room(cmds, src)
    if type(res) is str:
      return 0, res
    nick = res[0]
    room = res[1]
    reason = "cmds[0]命令"
    #  if option == "-f":
    #    res = await room.kick(cmds[1], reason)
    #    return f"ok: {res}"
    #  else:
    for i in room.members:
      if i.nick == nick:
        res = await room.kick(i, reason)
        return 0, f"ok: {res}"
    return 0, "not found"
  cmd_funs["kick"] = _
  cmd_for_admin.add('kick')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"禁言\n.{cmds[0]} $jid/$nick [时间(默认300)]"

    option = 300
    if len(cmds) == 3:
      option = int(cmds[2])
      cmds.pop(2)

    res = get_nick_room(cmds, src)
    if type(res) is str:
      return 0, res
    nick = res[0]
    room = res[1]
    reason = "cmds[0]命令"
    #  if len(cmds) == 2 or cmds[2] == "v":
    #    role = "visitor"
    #  #  elif cmds[2] == "a":
    #  #    role = "moderator"
    #  else:
    #    role = "participant"
    role = "visitor"

    muc = str(room.jid)
    jids = users[muc]
    for jid, j in jids.items():
      if j[0] == nick:
        #  j = jids[jid]
        w = j[4]
        w[0] = time.time() + option
        break

    res = await room.muc_set_role(nick, role, reason=reason)
    return 0, f"ok: {res}"
  cmd_funs["wtf"] = _
  cmd_for_admin.add('wtf')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"禁言\n.{cmds[0]} $jid/$nick"
    res = get_nick_room(cmds, src)
    if type(res) is str:
      return 0, res
    nick = res[0]
    room = res[1]

    muc = str(room.jid)
    unban(muc, nick)

    reason = "cmds[0]命令"
    #  if len(cmds) == 2 or cmds[2] == "v":
    #    role = "visitor"
    #  #  elif cmds[2] == "a":
    #  #    role = "moderator"
    #  else:
    #    role = "participant"
    role = "participant"
    res = await room.muc_set_role(nick, role, reason=reason)
    return 0, f"ok: {res}"
  cmd_funs["unban"] = _
  cmd_for_admin.add('unban')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"解除驱逐（添加成员身份）\n.{cmds[0]} $jid/$nick"
    reason = "cmds[0]命令"
    res = get_jid_room(cmds, src)
    if type(res) is str:
      return 0, res
    jid = res[0]
    room = res[1]
    #  muc = str(room.jid)
    #  unban(muc, jid=jid)
    affiliation = "member"
    res = await room.muc_set_affiliation(jid, affiliation, reason=reason)

    res = get_nick_room(cmds, src)
    if type(res) is str:
      return 0, res
    nick = res[0]
    room = res[1]

    muc = str(room.jid)
    unban(muc, nick)

    reason = "cmds[0]命令"
    role = "participant"
    res2 = await room.muc_set_role(nick, role, reason=reason)

    return 0, f"ok: {res} {res2}"
  cmd_funs["op"] = _
  cmd_for_admin.add('op')
  cmd_funs["ub"] = _
  cmd_for_admin.add('ub')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"驱逐\n.{cmds[0]} $jid/$nick"

    res = get_jid_room(cmds, src)
    if type(res) is str:
      return 0, res
    jid = res[0]
    room = res[1]

    reason = "cmds[0]命令"
    affiliation = "outcast"
    res = await room.muc_set_affiliation(jid, affiliation, reason=reason)
    return 0, f"ok: {res}"
  cmd_funs["sb"] = _
  cmd_for_admin.add('sb')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"join all\n.{cmds[0]} all\n.{cmds[0]} $muc"
    if cmds[1] == "all":
      for tmuc in rooms:
        room =  rooms[tmuc]
        await room.leave()
      rooms.clear()
      await join_all()
    else:
      tmuc = cmds[1]
      if tmuc in rooms:
        room =  rooms[tmuc]
        await room.leave()
      res = await join(tmuc)
      return 0, "res: %s" % res
    return 0, "ok"
  cmd_funs["join"] = _
  cmd_for_admin.add('join')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"search\n.{cmds[0]} [clear/se/wtf/fix] $jid/$nick"

    if cmds[1] == "fix":
      res = ""
      i = 0
      for muc in rooms:
        room = rooms[muc]
        jids = users[muc]
        for m in room.members:
          jid = str(m.direct_jid.bare())
          if jid not in jids:
            j = set_default_value(m)
            jids[jid] = j
            res += f"\nW: {jid} not in jids({muc})"
            continue
          j = jids[jid]
          if type(j[2]) is str and j[2] != m.role:
            i += 1
            j[2] = m.role
            j[1] = m.affiliation
            j[0] = m.nick
            res += f"\nfix: {muc} {m.nick}"
      if res:
        pass
      else:
        res = "no error"
    else:
      option = False
      if len(cmds) == 3:
        option = cmds[1]
        cmds.pop(1)

      res = get_jid_room(cmds, src)
      if type(res) is str:
        if src in my_groups:
          info(res)
          muc = src
          jids = users[muc]
          tmp = []
          for jid, j in jids.items():
            if j is None:
              info(f"{jid} log is None")
              continue
            if j[0] is None:
              info(f"{jid} log: {j}")
              continue
            if cmds[1] in j[0]:
              tmp.append(str(j))
          if tmp:
            res += "\n\n模糊查找结果\n" + "\n".join(tmp)
        return 0, res
      jid = res[0]
      room = res[1]

      if option == "clear":
        muc = str(room.jid)
        jids = users[muc]
        j = jids[jid]
        w = j[4]
        tmp = w[0]
        w[0] = 0
        res = f"{tmp} -> {w[0]}"
      elif option == "se":
        muc = str(room.jid)
        jids = users[muc]
        j = jids[jid]
        w = j[4]
        res = f"{j}\n\n{w}"
      elif option == "wtf":
        muc = str(room.jid)
        jids = users[muc]
        j = jids[jid]
        w = j[4]
        res = f"{w}"
      else:
        muc = str(room.jid)
        jids = users[muc]
        if jid in jids:
          j = jids[jid]
          res = "%s" % j
        else:
          res = "not found"
    return 0, res
  cmd_funs["se"] = _
  cmd_for_admin.add('se')

  async def _(cmds: list, src: str | int) -> tuple:
    res = None
    if len(cmds) == 1:
      res = f"管理桥接\n.{cmds[0]} add $from $dst\n.{cmds[0]} del $id/$jid\n.{cmds[0]} se $id/$jid"
      res += "\n\n%s" % json.dumps(bridges, indent='  ')
    elif cmds[1] == "add":
      if len(cmds) != 4:
        res = "参数数量不对"
      else:
        #  if cmds[2].isnumeric():
        addr = cmds[2]
        if addr not in bridges:
          addr = load_chat_id(addr)
        #  bridges[get_addr(cmds[2])] = get_addr(cmds[3])
        if addr in bridges:
          res = "existed"
        else:
          bridges[addr] = load_chat_id(cmds[3])
          res = f"added: {addr} -> {bridges[addr]}"
    elif cmds[1] == "del":
      if len(cmds) != 3:
        res = "参数数量不对"
      else:
        addr = cmds[2]
        if addr not in bridges:
          addr = load_chat_id(addr)
        if addr in bridges:
          res = f"delete: {addr} -> {bridges[addr]}"
          bridges.pop(addr)
        else:
          res = "没找到"
    elif cmds[1] == "se":
      res = ''
      addr = cmds[2]
      if addr not in bridges:
        addr = load_chat_id(addr)
      if addr in bridges:
        res += f"existed: {addr} -> {bridges[addr]}"
      peer = await get_entity(addr)
      if peer:
        res += "\npeer id: %s" % await UB.get_peer_id(peer)
        res += "\n%s: %s\n\n%s" % (type(peer), peer.stringify(), peer)
    send(f"{res}", src)
    return 512,
  cmd_funs["br"] = _
  cmd_for_admin.add('br')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"添加好友\n.{cmds[0]} $jid"
    rc = XB.summon(aioxmpp.RosterClient)
    #  pprint(rc)
    res = rc.subscribe(JID.fromstr(cmds[1]))
    #  print(f"结果：{res}")
    send(f"结果：{res}", src)
    await sleep(1)
    res = rc.approve(JID.fromstr(cmds[1]))
    #  print(f"结果：{res}")
    send(f"结果：{res}", src)
    return 512,
  cmd_funs["connect"] = _
  cmd_for_admin.add('connect')

  async def _(cmds: list, src: str | int) -> tuple:
    global print_msg
    print_msg = not print_msg
    if print_msg:
      return 0, "ok"
    else:
      return 0, "hide"
    #  send(f"结果：{res}", src)
  cmd_funs["printmsg"] = _
  cmd_for_admin.add('printmsg')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      if src in my_groups:
        muc = src
        if muc not in rooms:
          return 0, f"没找到room: {muc}"
        room = rooms[muc]
        jids = users[muc]
        tmp = []
        for i in room.members:
          if i.direct_jid:
            if str(i.direct_jid.bare()) not in jids:
              jids[str(i.direct_jid.bare())] = [i.nick, i.affiliation, i.role]
          tmp.append(i.nick)
        return 0, "列表(%s)\n%s" % (len(tmp), '\n'.join(tmp))
      else:
        return 0, "need muc"
      #  rc = XB.summon(aioxmpp.RosterClient)
      #  return "items: %s" % rc.items
    elif cmds[1] == "json":
      rc = XB.summon(aioxmpp.RosterClient)
      return 0, "json:\n%s" % rc.export_as_json()
    else:
      return 0, "fixme"
    #    #  pc = XB.summon(aioxmpp.PresenceClient)
    #    #  res = XB.get_most_available_stanza(cmds[1])
    #    return res
  cmd_funs["list"] = _
  cmd_for_admin.add('list')

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"查询xmpp端口\n.{cmds[0]} $domain\n\n.xmppi\n.xmpps"
    res = await node.discover_connectors(cmds[1])
    o = [f"可用的xmpp端口: {cmds[1]}"]
    o += (str(x) for x in res)
    res = await disco_item(cmds[1])
    if res.items:
      o += ["服务列表", "name\tnode\tjid"]
    for i in res.items:
      o.append("%s\t%s\t%s" % (i.name, i.node, i.jid))
    return 0, "\n".join(o)
  cmd_funs["xmpp"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"xmpp服务列表\n.{cmds[0]} $domain"
    res = await disco_item(cmds[1])
    if len(cmds) == 3:
      if cmds[2] == "raw":
        return 0, f"{cmds[1]}\n{res}"
    o = [cmds[1]]
    if res.items:
      o += ["name\tnode\tjid"]
    for i in res.items:
      o.append("%s\t%s\t%s" % (i.name, i.node, i.jid))
    if len(cmds) == 3:
      if cmds[2] == "full":
        send("\n".join(o), src)
        for i in res.items:
          o = f"{str(i.jid)}"
          await sleep(1)
          res2 = await disco_info(i.jid)
          o += f"\n{res2.to_dict()}"
          send(o, src)
        return 512,
        return True
    return 0, "\n".join(o)
  cmd_funs["xmpps"] = _
  
  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"xmpp服务器信息\n.{cmds[0]} $domain"
    res = await disco_info(cmds[1])
    if len(cmds) == 3:
      if cmds[2] == "raw":
        return 0, f"{cmds[1]}\n{res.to_dict()}"
    return 0, f"{cmds[1]}\n%s" % "\n".join(res.features)
  cmd_funs["xmppi"] = _


  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"pastebin\n.{cmds[0]} text\n\nhttps://fars.ee/"
    text = ' '.join(cmds[1:])
    return 0, await pastebin(text)
  cmd_funs["pb"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"PrivateBin\n.{cmds[0]} text\n\nhttps://github.com/r4sas/PBinCLI\nhttps://github.com/PrivateBin/PrivateBin\nhttps://privatebin.info/directory/"
    elif cmds[1] == "init":
      pvb_init()
    text = ' '.join(cmds[1:])
    return 0, await pvb(text)
  cmd_funs["pvb"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"PrivateBin\n.{cmds[0]} text\n\nhttps://github.com/r4sas/PBinCLI\nhttps://github.com/PrivateBin/PrivateBin\nhttps://paste.ononoki.org/\nhttps://paste.i2pd.xyz/"
    #  fu = pvb_init(server="https://0.0g.gg/")
    #  await fu
    text = ' '.join(cmds[1:])
    return 0, await pvb(text, server="https://0.0g.gg/")
  cmd_funs["pvb2"] = _



  #  async def _(cmds: list, src: str | int) -> tuple:
  #    if len(cmds) == 1:
  #      return 0, f"gpt(telegram bot) translate\n.{cmds[0]} $text\n\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
  #    text = ' '.join(cmds[1:])
  #    text = f'{PROMPT_TR_MY}“{text}”'
  #    return 1, gpt_bot
  #  cmd_funs["gtr"] = _
  #
  #  async def _(cmds: list, src: str | int) -> tuple:
  #    if len(cmds) == 1:
  #      return 0, f"gpt(telegram bot) translate 中文专用翻译\n.{cmds[0]} $text\n\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
  #    text = ' '.join(cmds[1:])
  #    text = f'{PROMPT_TR_ZH}“{text}”'
  #    return 1, gpt_bot
  #  cmd_funs["gtz"] = _


  #  async def _(cmds, src):
  #    if len(cmds) == 1:
  #      return f"gpt bot\n.{cmds[0]} $text\n\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
  #    text = ' '.join(cmds[1:])
  #    mid = await send_to_tg_bot(text, gpt_bot, src)
  #    return 1, mid
  #  cmd_funs["gtg"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"音乐下载(.163命令的简化版)\n.{cmds[0]} $text\n.{cmds[0]} clear\n\ntelegram bot: https://t.me/{music_bot_name}"
    if cmds[1] == "clear":
      await clear_history()
      return 0, "ok"
    text = ' '.join(cmds[1:])
    #  music_bot_state[src] = 1
    text="/search "+text
    #  mid = await send_to_tg_bot(text, music_bot, src)
    #  return 1, mid
    return 1, music_bot, text
  cmd_funs["music"] = _

  short_cmds = {
      "s": "/start",
      "h": "/help",
      "a": "/about",
      "r": "/reset",
      }
  async def get_commands2(bot_name, cmd):
    if bot_name not in bot_cmds:
      peer = await get_entity(bot_name)
      chat_id = await UB.get_peer_id(peer)
      s = await get_commands(chat_id)
      if s:
        bot_cmds[bot_name] = "\n\n" + "\n".join(f".{cmd} {x}" for x in s.splitlines())
      else:
        bot_cmds[bot_name] = ""
        #  return ""
    return bot_cmds[bot_name]
  
  all_bots = set()

  def add_tg_bot(bot_name, cmd, cmd2=None, cmd1=None, no_file=False):
    all_bots.add(cmd)
    #  peer = await get_entity(bot_name)
    #  pid = await UB.get_peer_id(peer)
    #  bridges[pid] = src
    #  mtmsgsg[src] = {}
    #  @exceptions_handler
    async def _(cmds: list, src: str | int) -> tuple:
      if cmd2 is not None:
        if len(cmds) == 1:
          return 0, f"{cmds[0]} 是 {cmd1} {cmds2} 的快捷方式，要查看用法，请发送 {cmd1} {cmds2}"
        cmds.insert(1, cmd2)
      if len(cmds) == 1:
        deleted_tg_msg_ids.clear()
        cmds2 = await get_commands2(bot_name, cmds[0])
        name = await get_name(username=bot_name)
        res = f"{name}\n.{cmds[0]} $text"
        if bot_name == "OPENAl_ChatGPT_bot":
          res += f"\n.{cmds[0]} /start: 更换ai模型(\"/start\"可以简写为\"s\")"
        res += f"\n\nhttps://t.me/{bot_name}{cmds2}\n\n.{cmds[0]} /start: 某些bot通过该命令找到额外选项\n.{cmds[0]} /help: 某些bot通过该命令找到额外选项\n.{cmds[0]} /reset: 某些bot通过该命令清空bot记住的上下文\n.{cmds[0]} /about\n.{cmds[0]} $file_url: 转发文件给bot\n.{cmds[0]} $text $file_url: 转发文件并针对文件回复指定内容\n\n其他ai接口命令: ." + "/.".join(all_bots)
        return 0, res
      elif not no_file and urlre.fullmatch(cmds[-1]):
        cmds2 = [f"{SH_PATH}/title.sh", cmds[-1]]
        cmds2.extend(["", "", "", "just_path"])
        #  r, o, e = await myshell(cmds, src=src, max_time=60)
        r, o, e = await myshell(cmds2)
        if r == 0:
          if o:
            s = o.splitlines()
            if len(s) > 0:
              path = s[-1]
              if os.path.exists(path):
                try:
                  t = asyncio.create_task(backup(path))
                  peer = await get_entity(bot_name)
                  chat_id = await UB.get_peer_id(peer)
                  msg = await tg_upload_media(path, chat_id=chat_id)
                  if msg:
                    send("已发送", src=src, tmp_msg=True)
                    if len(cmds) > 2:
                      r =await msg.reply(' '.join(cmds[1:-1]))
                    await t
                    return 512,
                  else:
                    info("上传失败")
                finally:
                  asyncio.create_task(backup(path, delete=True))
              else:
                info(f"file of path not found")
            else:
              info(f"empty out of shell")
          else:
            info(f"empty out of shell")
        else:
          info(f"下载失败")
        return 0, "发送失败"
      text = ' '.join(cmds[1:])
      if text in short_cmds:
        text = short_cmds[text]
      return 3, bot_name, text
    #  cmd_funs["ai4"] = _
    cmd_funs[cmd] = _
  add_tg_bot("Music163bot", "163")
  add_tg_bot("OPENAl_ChatGPT_bot", "ai")
  add_tg_bot("chatGPT_studentBot", "pl")
  add_tg_bot("BabayChatBot", "gg")
  add_tg_bot("chatGPTwrapperbot", "gm")
  add_tg_bot("Tech_GPT_Bot", "gm1")
  add_tg_bot("GPT4Telegrambot", "gm2")
  add_tg_bot("repostermodsapk_bot", "ds")
  add_tg_bot("RussiaChatGPTBot", "ds1")
  add_tg_bot("DeepSeekBot", "ds2")
  add_tg_bot("chat_gpt_robot", "gpt")
  add_tg_bot("ChatGPTechBot", "gpt2")
  add_tg_bot("GPT3_Chat_Bot", "gpt3")
  add_tg_bot("Chat_GPT4_rubot", "gpt4")
  #  add_tg_bot("GPT_TechSupport", "ai2")
  add_tg_bot("ChatGPT_General_Bot", "ai3")
  add_tg_bot("martii_chat_bot", "ai4")
  add_tg_bot("gpt3_unlim_chatbot", "ai5")
  add_tg_bot("stable_diffusion_bot", "sd")
  add_tg_bot("MishkaAI_bot", "mk")
  add_tg_bot("GLBetabot", "gl")
  add_tg_bot("GLBetabot", "glai", "/gpt", ".gl")
  add_tg_bot("GLBetabot", "glimg", "/img", ".gl")
  add_tg_bot("littleb_gptBOT", "bai")
  add_tg_bot("chatgpt_tfrbot", "gk")
  add_tg_bot("UltraYTBot", "ytd", no_file=True)
  add_tg_bot("YTsavebot", "ytd2", no_file=True)
  add_tg_bot("CopilotOfficialBot", "cp")




  async def _(cmds: list, src: str | int) -> tuple:
    i = 0
    for g in mtmsgsg:
      i += 1
      for j in mtmsgsg[g]:
        i += 1
    #  for g in gid_src:
    #    i += 1
    ii = i

    if len(cmds) > 1:
      if cmds[1] == "all":
        await clear_history()
      else:
        return 0, "?"
    else:
      await clear_history(src)
    i = 0
    for g in mtmsgsg:
      i += 1
      for j in mtmsgsg[g]:
        i += 1
    #  for g in gid_src:
    #    i += 1
    #  return "ok {ii} -> {i}"
    return 0, f"清除状态\n.{cmds[0]} all\n\n{ii} -> {i}"
  cmd_funs["clear"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"unicode encode\n.{cmds[0]} [f/r] $text"
    elif cmds[1] == "f":
      if len(cmds) == 2:
        return 0, "缺少参数"
      s = ' '.join(cmds[2:])
      return 0, ascii(s)[1:-1]
    elif cmds[1] == "r":
      if len(cmds) == 2:
        return 0, "缺少参数"
      s = ' '.join(cmds[2:])
      return 0, s.encode("unicode-escape").decode()
    s = ' '.join(cmds[1:])
    #  s = "\n".join(s)
    #  return 0, ascii(s)[1:-1].replace("\\n", "\n")
    res = f"[ {len(s)} ]\n"
    k = 1
    for i in s:
      res += f"{k}: "
      if i == "\n":
        res += "\\n: skip" + "\n"
      else:
        res += f"{i}: " + ascii(i)[1:-1] + "\n"
      k += 1
    return 0, res
  cmd_funs["u"] = _
  cmd_funs["ue"] = _
  
  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"unicode decode\n.{cmds[0]} $text"
    s = ' '.join(cmds[1:])
    return 0, s.encode().decode("unicode-escape")
  cmd_funs["ud"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"utf-8 encode\n.{cmds[0]} $text"
    # return ''.join(format(ord(c), '02X') for c in ' '.join(cmds[1:]))
    # https://docs.python.org/zh-cn/3.11/library/stdtypes.html
    return 0, (' '.join(cmds[1:])).encode().hex().upper()
  cmd_funs["he"] = _

  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"utf-8 decode\n.{cmds[0]} $text"
    s = ' '.join(cmds[1:])
    if s.startswith("0x"):
      s = s[2:]
    elif s.startswith("0X"):
      s = s[2:]
    #  s = s.replace(" ", "")
    #  res = ""
    #  for i in range(s)/2:
    #    res += chr(int(s[:2], 16))
    try:
      return 0, bytes.fromhex(s).decode()
    except UnicodeDecodeError as e:
      return 0, "E: {!r}\n{}".format(e, bytes.fromhex(s).decode(errors="ignore"))
  cmd_funs["hd"] = _

  def my_bin(s: str) -> str:
    #  tmp = ""
    tmp = []
    l = len(s)
    #  ss = ""
    for i in range(l//4):
      #  tmp = "{}{}{}".format(s[l-i*4-4:l-i*4], ss, tmp)
      #  tmp = "{}{}{}".format(s[-4:], ss, tmp)
      #  tmp = s[-4:] + tmp
      #  tmp.append(s[-4:])
      #  s = s[:-4]
      k = l-i*4-4
      tmp.append(s[k:k+4])
      if i%8  == 7:
        #  ss = "\n\n"
        #  tmp = "\n\n" + tmp
        tmp.append("\n\n")
      elif i%2  == 1:
        #  ss = "\n"
        #  tmp = "\n" + tmp
        tmp.append("\n")
      else:
        #  ss = " "
        #  tmp = " " + tmp
        tmp.append(" ")
    k = l%4
    if k != 0:
      #  tmp = "{}{}".format(s[:k], tmp)
      tmp.append(s[:k])
    else:
      tmp.pop()

    #  return tmp.strip()
    tmp.reverse()
    return "".join(tmp)
  async def _(cmds: list, src: str | int) -> tuple:
    if len(cmds) == 1:
      return 0, f"hex or int to bin\n.{cmds[0]} $text"
    s = ' '.join(cmds[1:])
    s = s.replace(" ", "")
    #  s= s.replace(":", "")
    if src == CHAT_ID:
      try:
        s = eval(s)
      except NameError as e:
        info(f"eval error: {e=}")
      except Exception as e:
        warn(f"eval error", e=e)
    tmp = []
    if type(s) is int:
      s = bin(s)
      s = str(s)
      s = s[2:]
      tmp.append(my_bin(s))
    else:
      is_16 = False
      if ":" in s:
        sp = ":"
        is_16 = True
      else:
        sp="."
        for i in s.split(sp):
          if not i.isnumeric():
            is_16 = True
            break
      for s in s.split(sp):
        if len(s) == 0:
          tmp.append("\n")
        else:
          if is_16 is True:
            s = bin(int(s, 16))
          else:
            s = bin(int(s))
          s = str(s)
          s = s[2:]
          tmp.append(my_bin(s))
    return 0, "\n\n".join(tmp)
  cmd_funs["bin"] = _




bridges_tmp = {}

@exceptions_handler
async def run_cmd(*args, **kwargs):
  res = await _run_cmd(*args, **kwargs)
  if type(res) is str:
    res = wtf_str(res, "xmpp")
  return res

async def _run_cmd(text, src, name="X test: ", is_admin=False, qt=None) -> bool | str:
  text0 = text
  if qt is not None:
    text = "{}\n\n{}".format(text, "\n".join(qt))
  if text == "ping":
    return "pong"
  if text[0:1] == ".":
    if text[1:2] == " ":
      return True
    if text[1:2] == ".":
      return True
    cmds = get_cmd(text[1:])
    if cmds:
      pass
    else:
      return True
    #  print(f"> I: {cmds}")
    info("got cmds: {}".format(cmds))
    st = send_typing(src)
    if st is not None:
      await st.__aenter__()

    try:
      cmd = cmds[0]
      res = False
      if cmd in cmd_for_admin:
        if is_admin is False:
          return "仅管理可用"
        res = True
      elif cmd in cmd_funs:
        res = True
      if res is True:
        try:
        #    res = await cmd_funs[cmd](cmds, src)
          f = cmd_funs[cmd]
          res = await f(cmds, src)
        except Exception as e:
          return _exceptions_handler(e, no_send=True)
          #  return True
          res = 512,
        #    print("run_cmd error:", e)
        #    res = get_lineno(e)
        #    res = f"run_cmd error: {res} {e=}"
        #    info(res, exc_info=e)
        #  f = exceptions_handler(send_to=src)(cmd_funs[cmd])
        #  f = exceptions_handler(no_send=True)(cmd_funs[cmd])
        #  if asyncio.iscoroutinefunction(f):
        #    res = await f(cmds, src)
        #  else:
        #    warn(f"wtf: {f=}")
        #    return True
        #  res = await (exceptions_handler(no_send=True)(cmd_funs[cmd])(cmds, src))
        info(f"res: {res}")
        #  if type(res) is tuple:
        r = res[0]
        if r == 512:
          return True
        if r == 0:
          res = res[1]
          if type(res) is str:
            return res
          warn(f"fixme: res is not str: {res=}")
          return str(res)
        if r == 1 or r == 3:
          bot_name = res[1]
          text = res[2]
          #  mtmsgs, pid = await change_bridge(res[1], src, res[0])
          #  #  gid = await send_to_tg_bot(text, pid)
          #  #  gid = await send_to_tg_bot(text, bot_name)
          #  gid = await send_tg(text, pid, return_id=True)
          #  mtmsgs, pid = await change_bridge(res[1], src, res[2])
          peer = await get_entity(bot_name)
          pid = await UB.get_peer_id(peer)
          if src not in mtmsgsg:
            mtmsgsg[src] = {}
          mtmsgs = mtmsgsg[src]
          mtmsgs[pid] = [name]

          if pid in bridges:
            bridges.pop(pid)
          if pid not in bridges_tmp:
            bridges_tmp[pid] = src
          else:
            osrc = bridges_tmp[pid]

            if osrc != src:
              if type(osrc) is dict:
                bridges_tmp[pid] = src
              else:
                #  await send("coming", src, tmp_msg=True)
                #  await send("...", src, tmp_msg=True)
                #  if mtmsgs:
                #    await sleep(3)
                info(f"stop link to {osrc}")
                send("bye", osrc, tmp_msg=True)
                bridges_tmp[pid] = src
                info(f"link to {src}")
                #  send("typing", src, tmp_msg=True)

                if osrc in mtmsgsg:
                  #  mtmsgsg.pop(osrc)
                  mtmsgsg[osrc].clear()

          await send_tg2(text, pid)
          for i in bridges_tmp.copy():
            if i != pid:
              if bridges_tmp[i] == src:
                bridges_tmp.pop(i)
                if i in mtmsgs:
                  mtmsgs.pop(i)
                warn(f"stop link for {src}: {i} -> {pid}")
            else:
              l = mtmsgs[i]
              if len(l) > 1:
                l[1].clear()
                if len(l) > 2:
                  l[2].clear()

        else:
          warn(f"unknown res: {res}")
          # 加name是为了处理tg in消息时可以知道该消息是回复谁的
          #  mtmsgs[src] = [name]
        #  send_typing(src)
        return True
        #  if res:
        #    return res
        #  else:
        #    return True
        #  reply = msg.make_reply()
        #  reply.body[None] = "%s" % res
        #  send(reply)
        #  return True
      else:
        #  res = await send_cmd_to_bash(src, name, text)
        res = await send_cmd_to_bash(None, name, text)
        if res:
          return res
    finally:
      #  info("finally")
      try:
        if st is not None:
          await st.__aexit__()
      except asyncio.CancelledError as e:
        info("该任务被要求中止，无法清除输入状态: {!r}".format(e))
        raise
      except GeneratorExit as e:
        warn("fixme: 无法清除输入状态: {!r})".format(e))

    return True
  #  elif text.isnumeric() and bridges[music_bot] != src:
  elif text.isnumeric():

    #  src_o = src
    pid = None
    if src in mtmsgsg:
      mtmsgs = mtmsgsg[src]
      for pid,l in mtmsgs.items():
        if len(l) > 1:
          if l[1]:
            if pid in bridges_tmp:
              if bridges_tmp[pid] == src:
                break
        pid = None

    if pid is None:
      for src in get_mucs(src):
        if src in mtmsgsg:
          mtmsgs = mtmsgsg[src]
        else:
          info(f"not founc {src} in mtmsgsg")
          #  return
          continue
        for pid,l in mtmsgs.items():
          if len(l) > 1:
            if l[1]:
              if pid in bridges_tmp:
                if bridges_tmp[pid] == src:
                  break
          pid = None

        if pid is not None:
          break

    #  src = src_o
    if pid is None:
      return False

    s = int(text)
    k = 0
    #  for _, v in mtmsgs.items():
      #  v = mtmsgs[gid]
      #  if len(v) > 1:
      #    info(f"mtmsgs buttons: {v[1]}")
      #    #  k += len(get_buttons(v))
    #  if k is None:
    #    break

    for i in get_buttons(l[1]):
      k += 1
      if k == s:
        send(f"命中：{text} {i.text}", src, tmp_msg=True)
        info(f"已找到：{text} {i.text}")
        mtmsgs[pid] = [name]
        k = None
        await sleep(0.5)
        await i.click()
        break

    if k is not None:
      info(f"没找到：{text}")
    #  mtmsgs.clear()
      #  ids = list(mtmsgs.keys())
      #  m = None
      #  if len(ids) > 5:
      #    while True:
      #      m = min(ids)
      #      mtmsgs.pop(m)
      #      ids.remove(m)
      #      if len(ids) < 5:
      #        break
      #  if m is None:
      text = ""
      k = 0
      for pid in mtmsgs:
        l = mtmsgs[pid]
        if len(l) > 1:
          bs = l[1]
          text += print_buttons(bs)
      send(f"没找到，请重新发送指令{text}", src)

    return True
  else:
    # tilebot
    tmp=""
    info(f"check url in: {text0}")
    for i in text0.splitlines():
      if not i.startswith("> ") and  i != ">":
        tmp += i+"\n"

    urls=urlre.findall(qre.sub("", tmp))
    res = None
    #  M=' 🔗 '
    #  M='- '
    #  M=' ⤷ '
    k = 1
    for url in urls:
      #  url=url[0]
      url=url[1]
      if url.startswith("https://t.me/"):
        return False
      if url.startswith("https://conversations.im/j/"):
        return False
      if url.startswith("https://icq.im"):
        return False
      elif url.startswith("https://x.com/"):
        res = await get_twitter(url, max_time=8)
        return res
      elif url.startswith("https://twitter.com/"):
        res = await get_twitter(url, max_time=8)
        return res

      #  tmp = "%s" % await get_title(url, max_time=15)
      tmp = await get_title(url, max_time=15)
      if len(urls) == 1:
        if tmp is None:
          return True
        res = f"[URL]({url}): {tmp}"
      else:
        if res is None:
          res=" %s urls" % len(urls)
        #  res+="\n\n> %s\n%s" % (url, tmp)
        res += "\n\n%s. %s\n%s" % (k, url, tmp)
      k += 1

    #  if res:
    if res is not None:
      res = f"{name}{res}"
      #  res2 = await send_cmd_to_bash(src, "", text)
      #  if res2:
      #    res += f"\n{res2}"
      return res
    else:
      res = await send_cmd_to_bash(None, name, text)
      return res
      #  await mt_send(res, gateway=gateway, name="titlebot")

  return False

@exceptions_handler
async def set_presence(client=None):
  if client is None:
    client = XB
  ps = XB.summon(aioxmpp.PresenceServer)
  # https://stackoverflow.com/a/24773021
  st = ps.set_presence(
      aioxmpp.PresenceState(available=True, show="chat"),
      f"xmpp:{main_group}?join",
      )
  res = await st
  if res is not None:
    warn(f"error StanzaToken: {res}")
  else:
    info("update presence ok")
    #  st = ps.resend_presence()
    #  res = await st
    #  if res is None:
    #    info("update presence ok")
    #  else:
    #    warn(f"error StanzaToken: {res}")
@exceptions_handler
async def set_vcard(client=None):
  if client is None:
    client = XB
  jid = get_jid(client.local_jid)
  vs = client.summon(aioxmpp.vcard.VCardService)
  vc = await vs.get_vcard(None)
  if vc.get_photo_mime_type() is None:
  #  if True:
    #  fn = WORK_DIR / "photo.png"
    fn = WORK_DIR / "w.png"
    fn = fn.as_posix()
    #  fn = 'tx.jpg'
    data = await read_file(fn, 'rb')
    #  vc.set_photo_data('image/jpeg', data)
    vc.set_photo_data('image/png', data)
    await vs.set_vcard(vc)
    await sleep(1)
    vc = await vs.get_vcard(None)
    if vc.get_photo_mime_type() is not None:
      info(f"头像设置成功: {jid} {fn}")
      #  warn(f"修改头像需要重新登录才能生效：{jid}")
      #  await stop(client)
      #  if await login(client, True):
      #    #  n = fn.split("@", 1)[1].split('_', 1)[1].rsplit('.', 1)[0]
      #    #  mynicks.add((jid, n))
      #    info(f"头像设置成功: {jid} {fn}")
      #    return True
      #  else:
      #    return False
    else:
      warn(f"头像设置失败：{jid}")
  else:
    info(f"无需设置头像：{jid}")


@exceptions_handler
async def login(client=None):
  if client is None:
    client = XB
  jid = get_jid(client.local_jid)
  info(f"登录中: {jid}")
  try:
    #  steam = await i.connected().__aenter__()
    steam = await asyncio.wait_for(client.connected().__aenter__(), timeout=30)
    info(f"登录成功：{jid}")
    asyncio.create_task(set_presence(client))
    asyncio.create_task(set_vcard(client))

  except TimeoutError as e:
    warn(f"登录失败(超时)：{jid}, {e=}")
    await stop(client)
    return False
  except Exception as e:
    warn(f"登录失败：{jid}, {e=}")
    await stop(client)
    return False

  return True


ocr_ok = None

def ocr_init():
  global ocr_ok
  ocr_ok = []
  info("开始初始化ocr")
  #  if 'liqsliu' not in HOME:
  if os.path.exists("%s/ddddocr" % HOME):
    sys.path.append("%s/ddddocr" % HOME)
    import ddddocr
    ocr = ddddocr.DdddOcr()
    def f(img):
      info("正在运行识别程序：ddddocr")
      return ocr.classification(img)
    ocr_ok.append(f)
  if os.path.exists("%s/ddddocr" % HOME):
    sys.path.append("%s/muggle/muggle-ocr-1.0.3" % HOME)
    import muggle_ocr
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    def f(img):
      info("正在运行识别程序：muggle_ocr")
      return sdk.predict(image_bytes=img)
    ocr_ok.append(f)
  if ocr_ok is None:
    info("没找到orc程序，将会无法识别验证码")
    return False

def run_ocr(img):
  if ocr_ok is None:
    if ocr_init() is False:
      return
  elif ocr_ok == []:
    for _ in range(5):
      info("等待orc初始化")
      time.sleep(5)
      if ocr_ok:
        break
    if ocr_ok == []:
      info("等待orc初始化超时")
      return
  f = None
  try:
    while True:
      f = random.choice(ocr_ok)
    #  for f in ocr_ok:
      s = f(img)
      if s:
        info(f" 识别结果: {s}")
        return s
      else:
        info(f" 识别失败: {s}")
  except Exception as e:
    warn(f"识别程序出现错误 {f=} {e=}")



def jbypass(msg):
  #  warn(f"无法进群: {msg}")
  asyncio.create_task(_bypass(msg))

async def _bypass(msg):
  """
  body: <class 'aioxmpp.structs.LanguageMap'>: {<aioxmpp.structs.LanguageTag.fromstr('en')>: 'Your subscription request and/or messages to kvpxdg0u68wq4tae@conference.conversations.im have been blocked. To unblock your subscription request, visit https://xmpp.conversations.im/captcha/8977672564368233645'}

  https://xmpp.conversations.im/captcha/12941499225798303289/image
  --
	curl 'https://suchat.org:5443/captcha/7412684044252318043/image' \
		-H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
		-H 'Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6' \
		-H 'Connection: keep-alive' \
		-H 'Referer: https://suchat.org:5443/captcha/7412684044252318043' \
		-H 'Sec-Fetch-Dest: image' \
		-H 'Sec-Fetch-Mode: no-cors' \
		-H 'Sec-Fetch-Site: same-origin' \
		-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
		-H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
		-H 'sec-ch-ua-mobile: ?0' \
		-H 'sec-ch-ua-platform: "Windows"'
  ==

	curl 'https://suchat.org:5443/captcha/13773455620261259216' \
		-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
		-H 'Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6' \
		-H 'Cache-Control: max-age=0' \
		-H 'Connection: keep-alive' \
		-H 'Content-Type: application/x-www-form-urlencoded' \
		-H 'Origin: https://suchat.org:5443' \
		-H 'Referer: https://suchat.org:5443/captcha/13773455620261259216' \
		-H 'Sec-Fetch-Dest: document' \
		-H 'Sec-Fetch-Mode: navigate' \
		-H 'Sec-Fetch-Site: same-origin' \
		-H 'Sec-Fetch-User: ?1' \
		-H 'Upgrade-Insecure-Requests: 1' \
		-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
		-H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
		-H 'sec-ch-ua-mobile: ?0' \
		-H 'sec-ch-ua-platform: "Windows"' \
		--data-raw 'id=13773455620261259216&key=427617&enter=OK'

	--
	<?xml
	version='1.0'?>
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
			<head>
					<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
			</head>
			<body>
					<p>验证码有效。</p>
			</body>
	</html>

  --
  e=XMPPAuthError("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')")

  """
  #  pprint(request)
  #  pprint(request.xep0004_data)
  #  pprint(request.xso_serialise_to_sax())
  #  pprint(request.body)
  #  pprint(request.body.get(aioxmpp.structs.LanguageTag.fromstr('en')))
  #  pprint(request.body.get(aioxmpp.structs.LanguageTag.fromstr('zh')))

  #  pprint(msg.body.any())
  #  return
  if msg.body.get(aioxmpp.structs.LanguageTag.fromstr('zh')):
    text = msg.body.get(aioxmpp.structs.LanguageTag.fromstr('zh'))
  elif msg.body.get(aioxmpp.structs.LanguageTag.fromstr('en')):
    text = msg.body.get(aioxmpp.structs.LanguageTag.fromstr('en'))
  else:
    text = msg.body.any()

  jid = get_jid(msg.from_)
  myid = get_jid(msg.to)

  if text:
    tmp = []
    for u in urlre.findall(text):
      tmp.append(u[1])
    if tmp == []:
      warn("需要验证才能入群，但无法输入验证码，没找到URL: {myid} {jid} {text}")
      return
    else:
      info(f"需要验证才能入群: {myid} {jid} {text} {tmp}")
  else:
    info(f"fixme: 这个群需要验证才能进吗？那就程序有bug: {myid} {jid} {text}")
    return

  u = None
  for u in tmp:
    #  if jid.split('@', 1)[1] in u:
    if msg.from_.domain in u:
      break
    u = None
  if u is None:
    info(f"没找到合适的，随便选第一个作为验证码地址: {jid} {tmp}")
    u = tmp[0]
  info(f"验证码地址: {u}")
  #  info(f"验证码地址: {u=}")
  headers = {
      #  'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
      'Accept': 'image/jpeg,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
      'Connection': 'keep-alive',
    }

  #  res = await http(f"{u}")
  res = await http(f"{u}", headers=headers, proxy="http://127.0.0.1:6080")
  print(res)
  headers['Referer'] = u
  iu = f"{u}/image"
  res = await http(f"{iu}", headers=headers, proxy="http://127.0.0.1:6080")
  #  res = await http("https://fars.ee/eUVh.jpg")
  info(f"image size: {len(res)} {iu}")
  #  print("===")
  #  s = ocr.classification(res)
  s = await asyncio.to_thread(run_ocr, img=res)
  if s:
    await sleep(3)
		#  -H 'Origin: https://suchat.org:5443' \
		#  --data-raw 'id=13773455620261259216&key=427617&enter=OK'
    data = {
        "id": "%s" % u.rsplit('/', 1)[1],
        "key": f"{s}",
        "enter": "OK",
        }
    headers.pop('Referer')
    headers['Origin'] = "%s//%s" % (u.split('//', 1)[0], u.split('//', 1)[1].split('/', 1)[0])
    headers['Accept'] = 'application/json,application/xhtml+xml,application/xml,text/html;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    info(f"headers: {headers}")
    info(f"data: {data}")
    res = await http(f"{u}", "POST", headers=headers, data=data, proxy="http://127.0.0.1:6080")
    info(res)
    #  while True:
    #    ogger.info(f"等待进群结果: {myid} {jid}")
    #    await sleep(3)
    #    if jid in muc_now:
    #      if myid in muc_now[jid]:
    #        break
  else:
    #  pprint(s)
    info(f"识别验证码失败: {myid} {jid} {s}")



@exceptions_handler
def on_muc_role_request(form, submission_future):
  # https://docs.zombofant.net/aioxmpp/0.13/api/public/muc.html#aioxmpp.muc.Room.on_muc_role_request
  print(form)
  print(submission_future)
  print(f"发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")

  #  send(f"发言申请: {form}")
  #  if submission_future.done():
  #    send_log(f"skip: 发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")
  #    return
  #  send_log(f"发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")
  #默认拒绝
  if not submission_future.done():
    while True:
      try:
        form.request_allow.field.value=False
        break
      except Exception as e:
        err("2无法设置request_allow", e=e)
      try:
        form.request_allow.field=False
        break
      except Exception as e:
        warn("3无法设置request_allow", e=e)
      try:
        form.request_allow.value=False
        break
      except Exception as e:
        warn("4无法设置request_allow", e=e)
      try:
        form.request_allow=False
        break
      except Exception as e:
        warn("无法设置request_allow", e=e)
      return
    submission_future.set_result(form)
    send_log(f"已拒绝发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")
  else:
    send_log(f"skip: 发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")


#  test_group = 'ipfs@salas.suchat.org'
rooms = {}
auto_input = False

async def join_all():
  info(f"join all groups...\n%s" % my_groups)
  tasks = set()
  groups = my_groups.copy()
  tmp = []
  while True:
    #  await join(test_group)
    #  break
    #  tmp = []
    #  for i in ms:
    #    if await join(i):
    #      continue
    #    tmp.append(i)
    #  if tmp:
    #    info(f"无法进入的群组: {tmp}")
    #    #  await mt_send_for_long_text(f"无法进入的群组: {tmp}")
    #    ms = tmp
    #    await sleep(5)
    #  else:
    #    break

    how_long = int(time.time()-start_time)
    #  if len(tasks) < (how_long-1)*4 if how_long > 2 else 4:
    if len(tasks) < 4:
      if groups:
        muc = groups.pop()
        t = asyncio.create_task(join(muc), name=muc)
        tasks.add(t)
        continue
      if len(tasks) == 0:
        info(f"join all ok: {len(tasks)}/{len(groups)}")
        break
    info(f"等待任务队列: {len(tasks)}/{len(groups)}")
    done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    for i in done:
      #  if i.result() is False:
      if i.result():
        pass
      else:
        #  groups.add(i.get_name())
        tmp.append(i.get_name())
        warn(f"进群失败一次: {i.result()} {i.get_name()} {len(tasks)}/{len(groups)}")
  if tmp:
    async def f():
      warn("进群失败，会继续尝试：\n%s" % "\n".join(tmp))
      await sleep(300)
      asyncio.create_task(join_all())
    asyncio.create_task(f())
  return True


@exceptions_handler
async def join(jid=None, nick=None, client=None):
  if jid is None:
    jid = test_group

  if jid not in send_locks:
    send_locks[jid] = asyncio.Lock()
  async with send_locks[jid]:

    if nick is None:
      #  if "wtf" in myjid:
      #    nick = 'bot'
      #  else:
      #    nick = 'liqsliu_bot'
      nick = 'bot'
    if client == None:
      client = XB

    global mucsv
    if "mucsv" not in globals():
      mucsv = client.summon(aioxmpp.MUCClient)
    J = JID.fromstr(jid)

    #  client.stream.register_iq_request_handler(
    #  try:
    #    client.stream.unregister_message_callback(
    #        aioxmpp.MessageType.NORMAL,
    #        None,
    #    )
    #  except KeyError as e:
    #    pass

    if auto_input:
      client.stream.register_message_callback(
      #  stream.message_handler(client.stream,
          aioxmpp.MessageType.NORMAL,
          J,
      #      #  None,
          jbypass,
      )

    myid = get_jid(client.local_jid)
    #  client.stream.on_message_received.connect(bypass)
    try:
      sum_try = 0
      while True:
        try:
          room, fut = mucsv.join(J, nick=nick, autorejoin=True)
          #  if fut is not None and room.muc_joined is False:
          if room.muc_joined is False:
            info(f"等待进群: {get_jid(client.local_jid)} {jid}")

            #  await fut
            await asyncio.wait_for(fut, timeout=15)
            info(f"进群成功: {myid} {jid}")


          if room is not None:
            rooms[jid] = room
            room.on_muc_role_request.connect(on_muc_role_request)
            room.on_nick_changed.connect(on_nick_changed)

            jids = users[jid]
            if myjid in jids:
              j = jids[myjid]
            #    j[0] = nick
            else:
              j = []
              jids[myjid] = j
            set_default_value(j, m=room.me)

            return room
          else:
            warn(f"failed to join: room is None {jid}")
        
        except TimeoutError as e:
          #  warn(f"进群超时(废弃): {jid} {muc} {e=}")
          warn(f"进群超时{sum_try}: {myid} {jid} {nick} {e=}")
        except errors.XMPPCancelError as e:
          # XMPPCancelError("{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: No route to host')")
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: connection refused')":
            info(f"进群失败, 网络问题，拒绝连接: {myid} {jid} {e=}")
            return False
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: No route to host')":
            info(f"进群失败, 网络问题，找不到主机: {myid} {jid} {e=}")
            return False
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: connection timeout')":
            info(f"进群失败, 网络问题，连接超时: {myid} {jid} {e=}")
            return False
          if e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found"):
            info(f"进群失败, 网络问题，找不到地址: {myid} {jid} {e=}")
            return False

          elif e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}conflict ('That nickname is already in use by another occupant')" or e.args[0] == '{urn:ietf:params:xml:ns:xmpp-stanzas}conflict' or '{urn:ietf:params:xml:ns:xmpp-stanzas}conflict' in e.args[0]:
            onick = nick
            if '_' in nick:
              nick = f"{nick}%s" % generand(1)
            else:
              nick = f"{nick}_%s" % generand(1)
            info(f"群名字冲突{sum_try}: {myid} {jid} {onick}->{nick} {e=}")

          else:
            info(f"进群失败{e.args}: {myid} {jid} {e=}")
            return False
        except errors.XMPPAuthError as e:
          #  pprint(e.args)
          #  if e.args == ("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')", ):
          if e.args:
            if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized"):
              if auto_input is False:
                return False
              info(f"进群失败, 验证码不正确，准备重试: {myid} {jid} {e=}")
            else:
              if e.args[0] == '{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden':
                info(f"进群失败，被ban了(forbiden): {myid} {jid} {e=}")
              elif e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden ('You have been banned from this room')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden"):
                info(f"进群失败，被ban了: {myid} {jid} {e=}")
              else:
                info(f"进群失败{e.args}: {myid} {jid} {e=}")
              return False
          else:
            info(f"进群失败(无权限): {myid} {jid} {e=}")
            return False
        except Exception as e:
          err(f"进群失败: {myid} {jid} {e=}")
          return False
        sum_try += 1
        if sum_try > 3:
          warn(f"进群失败(重试次数达到最大值): {myid} {jid}")
          return False
        await sleep(0.1)

    finally:
      if auto_input:
        client.stream.unregister_message_callback(
            aioxmpp.MessageType.NORMAL,
            J,
        )
    return False


@exceptions_handler
async def msgb(event):
  # msg to TB

  chat_id = event.chat_id
  sender_id = event.sender_id
  msg = event.message
  #  text = msg.text
  text = event.text
  info(f"{chat_id} {sender_id}: {short(text) if text is not None and len(text) > 0 else type(msg.media)}_{msg.id}")

  if event.fwd_from:
    return
  need_forward = False
  if chat_id == GROUP_ID:
    need_forward = True
  #    info("ignore msg from GROUP_ID")
  #    return
  elif chat_id == GROUP2_ID:
    if msg.reply_to is None:
      info("fixme: unknown msg: %s" % msg.stringify())
    elif msg.reply_to.reply_to_top_id == GROUP2_TOPIC or msg.reply_to.reply_to_msg_id == GROUP2_TOPIC:
      need_forward = True

  #  if chat_id == GROUP2_ID:
  if need_forward is True:
    #  text = msg.text
    #  peer = await event.get_sender()
    #  #  nick = "G [%s %s]" % (peer.first_name, peer.last_name)
    #  name = "G %s" % peer.first_name
    #  name2 = "**G %s:** " % peer.first_name

    text, name, _ = await print_tg_msg(msg, True)
    name2 = f"**{name}:** "

    qt = None
    if msg.is_reply:
      if chat_id == GROUP_ID or msg.reply_to.reply_to_msg_id != GROUP2_TOPIC:
        msgr = await msg.get_reply_message()
        #  peer = await msgr.get_sender()
        #  qto = "**G %s%s:** %s" % (peer.first_name, " " + peer.last_name if peer.last_name is not None else "", msgr.text)
        qto, namer, _ = await print_tg_msg(msgr, True)
        qto = f"**{namer}:** {qto}"
        qt = qto.splitlines()

    if chat_id == GROUP_ID:
      asyncio.create_task( send_tg(f"{name2}{text}", GROUP2_ID, qt=qt, topic=GROUP2_TOPIC) )
    elif chat_id == GROUP2_ID:
      asyncio.create_task( send_tg(f"{name2}{text}", GROUP_ID, qt=qt) )
    asyncio.create_task( mt_send_for_long_text(text, name=name, qt=qt) )
    ms = get_mucs(main_group)
    for m in ms:
      asyncio.create_task( send_xmpp(f"{name2}{text}", m, name=name) )
    #  res = await run_cmd(f"{text}\n\n{qt}", get_src(msg), f"X {name}: ", is_admin=False, text)
    if qt is not None:
      res = await run_cmd(f"{text}\n\n{qto}", chat_id, f"X {name}: ", False, text)
    else:
      res = await run_cmd(text, chat_id, f"X {name}: ", False)
    if res is True:
      return
    if res:
      send(res, main_group)
    return

  if event.is_private or chat_id == CHAT_ID:
    # my private group
    #  text = msg.text
    text = msg.raw_text
    sender_id = event.sender_id
    if text:
      info(f"bot got msg: {chat_id} {sender_id}: {text}")
    if text == "ping":
      #  await TB.send_message(chat_id, "pong")
      await msg.reply("pong")
      return
    if text == "raw sender":
      sender = await event.get_sender()
      await msg.reply(sender.stringify())
      return
    if text == "raw chat":
      peer = await event.get_chat()
      #  await msg.reply(peer.stringify())
      await send_tg(peer.stringify(), chat_id, topic=msg.id)
      return
    if text == "dc":
      try:
        sender = await event.get_sender()
        if sender.photo:
          await msg.reply("dc_id: %d" % sender.photo.dc_id)
        else:
          await msg.reply("没设置头像")
          #  info(sender.stringify())
      except Exception as e:
        await msg.reply("error")
        raise
      return
    #  res = await run_cmd(text, CHAT_ID, "G me")
    if chat_id == CHAT_ID:
      if text == "id":
        await msg.reply(f"id [f] @name https://t.me/name\nchat_id: {chat_id}")
        return
      if text == "msg":
        await msg.reply("msg url raw/fast/xmpp/direct/vps")
        return
      if text.startswith("id "):
        full = False
        if text.startswith("id f "):
          full = True
        url = text.split(' ')[-1]
        #  url = text.split(' ')[1]
        #  if url.startswith("https://t.me/"):
        #    username = url.split('/')[3]
        #  elif url.startswith("@"):
        #    username = url[1:]
        #  else:
        #    await UB.send_message(chat_id, "error url")
        #    return
        #
        #  e = await UB.get_entity(username)

        e, gid = await get_entity(url, False, return_gid=True)
        #  if type(e) is tuple:
        #    peer = e[0]
        #    gid = e[1]
        #    e = await UB.get_messages(peer, ids=gid)
        #    #  await UB.send_message(chat_id, f"{e.stringify()}")
        #    if full:
        #      #  await msg.reply(f"{e.stringify()}")
        #      await send_tg(e.stringify(), chat_id, topic=msg.id)
        #    await msg.reply("peer id: %s %s" % (await UB.get_peer_id(peer), type(e)))
        if e:
          res = ""
          if gid is not None:
            if msg.is_group:
              res += "chat:\n"
              res += print_entity(e)
              res += "\n\nsender:\n"

              info(f"get msg: {e} {gid}")
              msg = await UB.get_messages(e, ids=gid)
              if msg is None:
                info(f"get msg(TB): {e} {gid}")
                msg = await get_msg(url, TB)
              if msg is not None:
                if full:
                  await send_tg(msg.stringify(), chat_id, topic=msg.id)
                ee = await msg.get_sender()
                if ee is None:
                  res += "E: sender: None"
                else:
                  e = ee

          if full:
            #  await msg.reply(f"{e.stringify()}")
            await send_tg(e.stringify(), chat_id, topic=msg.id)
          #  pid = await UB.get_peer_id(e)
          res += print_entity(e)

          #  await msg.reply(res)
          await send_tg(res, chat_id, topic=msg.id)

          #  if pid > 0:
          #    await msg.reply("peer id: [%s](tg://openmessage?user_id=%s)" % (pid, pid))
          #  else:
          #    await msg.reply("peer id: %s" % pid)
        else:
          e = await get_entity(url, False, client=TB)
          if type(e) is tuple:
            peer = e[0]
            gid = e[1]
            e = await TB.get_messages(peer, ids=gid)
            if e:
              #  if len(e) > 1:
              if hasattr(e, "__len__"):
                await msg.reply(f"found {len(e)} msgs")
                e = e[0]
              #  await UB.send_message(chat_id, f"{e.stringify()}")
              if full:
                await msg.reply(f"{e.stringify()}")
              await msg.reply("using TB, peer id: %s" % await UB.get_peer_id(peer))
            else:
              await msg.reply("not fount entity")
          elif e:
            if full:
              await msg.reply(f"{e.stringify()}")
            pid = await TB.get_peer_id(e)
            #  res = "peer id: %s" % pid
            res = "using TB, peer id: %s %s %s" % (pid, e.first_name, e.last_name)
            if e.username:
              res += " @%s" % e.username
            else:
              if pid > 0:
                res += " [%s](tg://openmessage?user_id=%s) " % (pid, pid)
            await msg.reply(res)
            #  if pid > 0:
            #    await msg.reply("using TB, peer id: [%s](tg://openmessage?user_id=%s)" % (pid, pid))
            #  else:
            #    await msg.reply("using TB, peer id: %s" % pid)
          else:
            await msg.reply("not fount entity")
        return
      elif text.startswith("msg "):
        cmds = get_cmd(text)
        full = False
        if text.startswith("msg f "):
          full = True
        #  url = cmds[1]
        url = text.split(' ')[-1]
        if url:
          opts = 0
          peer, gid = await get_entity(url, return_gid=True)
          if peer:
            #  send(peer.stringify(), chat_id)
            #  ss = url.split('/')
            #  if len(ss) > 4:
            #    gid = int(ss[-1])
            if gid:
              tmsg = await UB.get_messages(peer, ids=gid)
              if tmsg:
                if full:
                  #  await msg.reply(f"{e.stringify()}")
                  await send_tg(tmsg.stringify(), chat_id)
                opts = 0
                if len(cmds) == 3:
                  opts = cmds[2]
                await save_tg_msg(tmsg, chat_id, opts, url)
              else:
                await msg.reply(f"error id: {gid}\nres: {msg}")
            return
          else:
            await msg.reply(f"error url: {url}\nres: {peer}")
            return
        await msg.reply("error")
        return


      if msg.file:
        return
      #  res = await run_cmd(text, log_group_private, f"G {MY_NAME}: ", is_admin=True)
      res = await run_cmd(text, chat_id, f"G {MY_NAME}: ", is_admin=True)
      #  info("end")
      if res is True:
        pass
      elif res:
        #  res = f"```\n{res}```"
        #  await UB.send_message(CHAT_ID, res)
        #  send(res, chat_id)
        #  await msg.reply(res)
        await send_tg(res, chat_id, topic=msg.id)

    elif chat_id == MY_ID:
      if msg.is_reply:
        msg2 = await msg.get_reply_message()
        if msg2.raw_text:
          text2 = msg2.raw_text
          if text2.startswith("id: "):
            tid = int(text2.split(" ", 2)[1])
            msg3 = await msg.forward_to(tid)
            await msg.reply("ok")
            return
          if text2.startswith("xmpp: "):
            text2 = msg2.raw_text
            tt = text2.split(" ", 2)[1]
            tjid = text2.split(" ", 3)[2][:-1]

            tjidb = tjid.split("/")[0]
            #  tj = JID.fromstr(tjid)
            if tt == "MessageType.CHAT":
              if tjidb in my_groups:
                pass
              else:
                tjid = tjidb
              send(text, tjid, name="**T admin:** ")
              await msg.reply("ok")
              return
            else:
              pass
      await msg.reply("?")
    elif event.is_private:
      try:
        async with asyncio.timeout(60):
          if chat_id not in private_locks:
            private_locks[chat_id] = asyncio.Lock()
          async with private_locks[chat_id]:
            if text == 'id':
              await msg.reply(f"{chat_id}")
              return
            msg2 = await msg.forward_to(MY_ID)
            send(msg.text, ME)
            if sender_id:
              #  await TB.send_message(MY_ID, f"id: [{sender_id}](tg://user?id={sender_id})")
              #  await TB.send_message(MY_ID, f"id: [{sender_id}](tg://user?id={sender_id})")
              #  await msg2.reply(f"id: [{sender_id}](tg://user?id={sender_id})", parse_mode="md")
              #  await msg2.reply(f"chat_id: [{chat_id}](tg://openmessage?user_id={chat_id})")
              res = f"id: [{sender_id}](tg://openmessage?user_id={sender_id})"
            else:
              res = f"chat_id: [{chat_id}](tg://openmessage?user_id={chat_id})"
            await msg2.reply(res)
            send(res, ME)
            await msg.reply("ok")
            await sleep(1)
      except TimeoutError:
        pass

    #  info("return")
    return

@exceptions_handler
async def msgbo(event):
  # msg from TB
  msg = event.message
  chat_id = event.chat_id
  text = msg.text
  if text:
    sender_id = event.sender_id
    info(f"bot out msg: {chat_id} {sender_id}: {short(text)}")

@exceptions_handler
async def tg_start():
  global UB, MY_NAME, MY_ID
  info("telegram user bot login...")

  #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, proxy=("socks5", '127.0.0.1', 6080))
  api_id = int(get_my_key("TELEGRAM_API_ID"))
  api_hash = get_my_key("TELEGRAM_API_HASH")
  #  client = TelegramClient('anon', api_id, api_hash)
  #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, proxy=("socks5", '172.23.176.1', 6084), loop=loop)
  #  global loop
  #  loop = asyncio.get_event_loop()
  #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, loop=loop)
  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash)
  #  async with UB:
  await UB.__aenter__()

  UB.parse_mode = 'md'
  #  UB.parse_mode = None

  me = await UB.get_me()
  #  print(me.stringify())
  MY_ID = me.id
  MY_NAME = me.username
  print(f"tg account: {MY_NAME}: {MY_ID}")

  @UB.on(events.MessageDeleted())
  async def _(event):
    global parse_message_deleted_task
    parse_message_deleted_task = asyncio.create_task(msgtd(event))
  global parse_message_deleted_task
  parse_message_deleted_task = None

  @UB.on(events.NewMessage(incoming=True))
  @UB.on(events.MessageEdited(incoming=True))
  async def _(event):
    asyncio.create_task(msgt(event))

  @UB.on(events.NewMessage(outgoing=True))
  async def _(event):
    asyncio.create_task(msgtout(event))

  #  @UB.on(events.UserUpdate)
  @UB.on(events.UserUpdate())
  async def _(event):
    asyncio.create_task(msgtp(event))

    #  await UB.run_until_disconnected()

@exceptions_handler
async def bot_start():
  global TB
  info("telegram bot login...")

  api_id = int(get_my_key("TELEGRAM_API_ID"))
  api_hash = get_my_key("TELEGRAM_API_HASH")
  #  TB = await TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_bot"), api_id, api_hash).start(bot_token=bot_token)
  TB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_bot"), api_id, api_hash)

  bot_token = get_my_key("TELEGRAM_BOT_TOKEN")
  await TB.start(bot_token=bot_token)
  info("telegram bot 登陆成功")
  #  async with TB:
  await TB.__aenter__()

  info("telegram bot 登陆成功2")
  #  TB.parse_mode = 'md'
  TB.parse_mode = None

  @TB.on(events.NewMessage(incoming=True))
  @TB.on(events.MessageEdited(incoming=True))
  async def _(event):
    asyncio.create_task(msgb(event))

  @TB.on(events.NewMessage(outgoing=True))
  async def _(event):
    asyncio.create_task(msgbo(event))

    #  await TB.run_until_disconnected()


@exceptions_handler
async def xmpp_start():
  global XB, myjid, UPLOAD, UPLOAD_MAX
  info("开始登录xmpp")

  myjid = get_my_key("JID")
  password = get_my_key("JID_PASS")
  info(f"xmpp: {myjid} {password[:3]}...")
  #  jid = aioxmpp.JID.fromstr(jid)
  XB = aioxmpp.PresenceManagedClient(
      JID.fromstr(myjid),
      aioxmpp.make_security_layer(password)
  )
  info(f"已导入新账户: {myjid} password: {password[:4]}...")
  t = asyncio.create_task(load_config())
  await t
  if await login():
    pass
    #  info(f"join all groups...\n%s" % my_groups)
    #  await join()
    #  global mucsv
    #  mucsv = client.summon(aioxmpp.MUCClient)
    #  for coro in asyncio.as_completed(map(join, my_groups),
    #  await join_all()
  else:
    err(f"登陆失败：{myjid}")
    return


  #    #  asyncio.create_task(xmpp_daemon(), name="xmpp")
  #  else:
  #    await sendg("已重新启动xmppbot")
    
  UPLOAD = None
  UPLOAD_MAX = 0
  res = await disco_item()
  if res:
    for i in res.items:
      r = await disco_info(i.jid)
      if r:
        if "urn:xmpp:http:upload:0" in r.features:
          UPLOAD = i.jid
          info(f"上传文件用的服务器地址：{UPLOAD}")
          for j in r.to_dict()["forms"]:
            if j["FORM_TYPE"]:
              if j["FORM_TYPE"][0] == "urn:xmpp:http:upload:0":
                if j["max-file-size"]:
                  UPLOAD_MAX = int(j["max-file-size"][0])
                  info(f"上传文件大小限制：{UPLOAD_MAX}")
          break
  if UPLOAD is None:
    warn(f"没找到上传文件用的服务器地址：{myjid}")
  if UPLOAD_MAX == 0:
    warn(f"没找到文件大小限制：{myjid}")

  #  await upload()

#  @exceptions_handler
#  async def xmpp_daemon():
#    while True:
#      if XB.running:
#        await sleep(60)
#        continue
#      info("xmppbot is not running")
#      #  try:
#      #  # RuntimeError: write() called (invalid in state _State.CLOSED, closing=False)
#      #  except RuntimeError as e:
#      #    if e.args[0] == 'write() called (invalid in state _State.CLOSED, closing=False)':
#      #      warn(f"fixme: xmpp error {e=}")
#      #    else:
#      #      warn(f"fixme: unknown xmpp error {e=}")
#      await stop()
#      await save_data()
#      sys.exit(2)
#      await sleep(5)
#      t = asyncio.create_task(xmppbot(), name="xmppbot")
#      await t



async def stop_sub(p=None):
  if p is None:
    if "myshell_p" in globals():
      p = myshell_p
    else:
      warn("没找到需要停止的进程")
      return True
  if p.returncode is not None:
    info(f"已经停止: {p}")
    return
  try:
    #  if p is myshell_p:
    #    info("clean out of myshell")
    #    async with myshell_lock:
    #      while not myshell_queue.empty():
    #        res = await myshell_queue.get()
    #        info(f"clean out from myshell: {short(res)}")
    #        await sleep(0.2)
    if p.returncode is None:
      if p.stdin is not None:
        info(f"尝试关闭stream stdin: {p.stdin}")
        p.stdin.close()
        await p.stdin.wait_closed()
        #  await sleep(0.5)
    if p.returncode is None:
      p.terminate()
      info(f"尝试停止: {p}")
      try:
        await asyncio.wait_for(p.wait(), timeout=2)
        return
      except Exception as e:
        info(f"timeout {e=}")
    if p.returncode is None:
      p.kill()
      info(f"强制停止: {p}")
      try:
        await asyncio.wait_for(p.wait(), timeout=5)
      except Exception as e:
        info(f"timeout {e=}")
  finally:
    if p.returncode is None:
      info(f"停止成功: {p} {p.returncode=}")
      return True
    else:
      warn(f"停止失败: {p}")


async def after_init():
  info("run after init...")

  global loop2_thread, loop2, main_thread
  main_thread =  threading.main_thread()
  loop2_thread = threading.Thread(target=thread2_daemon, daemon=True)
  loop2_thread.start()
  while True:
    if "loop2" in globals() and loop2.is_running():
      info("子线程事件循环正在运行")
      break
    else:
      info("等待子线程事件循环启动")
      await sleep(2)
  #  info("判断是否在主线程，应该是True: %s" % str(main_thread.native_id == threading.get_native_id()))
  #  info("判断是否在副线程，应该是False: %s" % str(loop2_thread.native_id == threading.get_native_id()))
  #  info(f"ids: {main_thread.native_id} {loop2_thread.native_id} {threading.get_native_id()}")

  if await init_myshell():
    info("启动常驻shell成功")
  else:
    warn("启动常驻shell失败")
  #  global myshell_p
  #  myshell_p = await asyncio.create_subprocess_shell("bash -i", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  #  start_time = time.time()
  #  def wrap_read(func):
  #    k = len(ress)
  #    @wraps(func)
  #    async def wrapper(*args, **kwargs):
  #      data = await func(*args, **kwargs)
  #      if data and data[-1] == "\n":
  #        ress[k] += data
  #        now = time.time()
  #        if now - ress[0] > interval/2:
  #          ress[0] = now
  #          if src:
  #            asyncio.create_task(send( "执行中，临时输出{k}: \n%s" % ress[k].decode("utf-8", errors="ignore"), src, correct=True) )
  #          ress[k] = b""
  #        #  print(f"{len(data)}")
  #      return data
  #    return wrapper
  #  ress = [start_time, b""]
  #  p.stdout.readline = wrap_read(p.stdout.readline)
  #  ress.append(b"")
  #  p.stderr.readline = wrap_read(p.stderr.readline)
  pvb_init()


async def loop_task():
  #  while True:
  #    if XB.running:
  while XB.running:
    await sleep(60)
    #  info0(f"XB is running {TB.parse_mode} {UB.parse_mode}")
    info0(f"XB is running")

  warn("xmppbot is not running, restart...", no_send=False)
  await sleep(15)
  await send_tg("xmpp bot 已断开，准备重启...")
  await sleep(1)
  sys.exit(2)
  
  await UB.run_until_disconnected()


async def init():
  global loop
  loop = asyncio.get_event_loop()

  #

  #  LOGGER.addFilter(NoParsingFilter())
  # https://stackoverflow.com/questions/17275334/what-is-a-correct-way-to-filter-different-loggers-using-python-logging
  #  for handler in logging.root.handlers:
  #    #  handler.addFilter(logging.Filter('foo'))
  #    #  handler.addFilter(NoParsingFilter())
  #    f = NoParsingFilter()
  #    handler.addFilter(f)
  #    info(f"added filter to: {handler}")

  #  await init_aiohttp_session()
  #  global session
  #  session = aiohttp.ClientSession()

  global SH_PATH, DOMAIN
  SH_PATH = await read_file()
  if SH_PATH:
    SH_PATH = SH_PATH.rstrip('\n')
  DOMAIN = await read_file("DOMAIN")
  if DOMAIN:
    DOMAIN = DOMAIN.rstrip('\n')
  print(f"SH_PATH: {SH_PATH}")
  print(f"DOMAIN: {DOMAIN}")

  return True


#  @exceptions_handler
async def amain():
  try:

    if await init() is not True:
      err("初始化失败")
      return

    if len(sys.argv) > 1:
      #  if sys.argv[1] == '1':
      if sys.argv[1].isnumeric():
        pass
      elif sys.argv[1] == 'cmd':
        #  res = await my_popen(' '.join(sys.argv[2:]))
        res = await my_sshell(' '.join(sys.argv[2:]))
        print(res)
      elif sys.argv[1] == 'cmd2':
        res = await send_cmd_to_bash("gateway1", "X test", ' '.join(sys.argv[2:]))
        print(res)
      return



    xmpp = asyncio.create_task(xmpp_start(), name="xmpp")
    #  asyncio.create_task(wtf_loop())
    tg = asyncio.create_task(tg_start(), name="tg")
    bot = asyncio.create_task(bot_start(), name="bot")

    #  del api_id
    #  del api_hash
    #  #  del bot_token

    #  asyncio.create_task(other_init())

    # with UB:
    #  loop.run_until_complete(run())

    #  await UB.start()
    #  async with UB:

    k = 0b000
    while True:
      #  if allright_task > 0:
        #  info(f"等待初始化完成，剩余任务数：{allright_task}")
      if k & 0b100 == 0:
        if not xmpp.done():
          info(f"等待xmpp")
        else:
          xmpp = asyncio.create_task(join_all())
          mt_read_task = asyncio.create_task(mt_read(), name="mt_read")
          k = k | 0b100
      if not tg.done():
        info(f"等待tg user bot")
      else:
        k = k | 0b010
      if not bot.done():
        info(f"等待tg bot")
      else:
        k = k | 0b001
      if k != 0b111:
        await sleep(1)
      else:
        break

    #  await mt_send("gpt start")

    #  await join_all()

    await after_init()

    info(f"测试通过副线程发信息")
    #  fu = t
    #  res = await t
    t = loop2.create_task(send_tg("通过副线程发信息成功(loop2)", CHAT_ID)) # 测试结果: 必须放在下面这行代码上面，不然就无法执行task

    fu = asyncio.run_coroutine_threadsafe(send_tg("通过副线程发信息成功"), loop2)
    while not fu.done():
      info(f"等待发送消息的任务结束: not done, loop is_running: {loop2.is_running()}")
      await sleep(1)
    info(f"副线程发信息结果: {fu.result()}")

    #  while not t.done():
    #    info(f"通过副线程发信息(loop2): not done, loop is_running: {loop2.is_running()}")
    #    await sleep(1)
    #  info(f"副线程发信息结果(loop2): {t.result()}")

    await init_cmd()
    await xmpp
    await regisger_handler(XB)

    info(f"初始化完成")
    sendme(f"启动成功，用时: {int(time.time()-start_time)}s", to=0)
    #  send(f"启动成功，用时: {int(time.time()-start_time)}s", jid=main_group)
    try:
      #  await loop_task()
      while XB.running:
        await sleep(60)
        #  info0(f"XB is running {TB.parse_mode} {UB.parse_mode}")
        info0(f"XB is running")

      warn("xmppbot is not running, restart...", no_send=False)
      await sleep(15)
      await send_tg("xmpp bot 已断开，准备重启...")
      await sleep(1)
      sys.exit(2)
    finally:
      info("断开bot连接前需要清理")
      await stop()
      await stop_sub()
      info("清理完成")


    info("主程序结束")
  finally:
    info("开始关闭")
    #  for j in asyncio.all_tasks(loop):
    #    if not j.done():
    #      if "@" in j.get_name():
    #        j.cancel()
    #  for j in asyncio.all_tasks(loop):
    #    if not j.done():
    #      if "@" in j.get_name():
    #        info(f"正在关闭task, {j}")
    #        #  loop.run_until_complete(j)
    #        await j
    #  mt_read_task.cancel()
    await save_data()
    #  try:
    #    await mt_send("正在停止")
    #    await sendg("正在停止")
    #    await sendg("正在停止", jid=main_group)
    #  except Exception as e:
    #    pass
    #  await save_data()
    #  loop.run_until_complete(stop())
    #  loop.run_until_complete(loop.shutdown_asyncgens())
    #  loop.close()
    info("bye")


start_time=time.time()

def main():
  try:

    #  with UB:
    #    UB.loop.run_until_complete(amain())
    asyncio.run(amain())
  except KeyboardInterrupt as e:
    info("停止原因：用户手动终止")
    sys.exit(1)
  except SystemExit as e:
    if "restart" in str(e.args[0]):
      info(f"捕获到systemexit: {e=} {e.args=}")
      sys.exit(1)
    else:
      warn(f"捕获到systemexit: {e=} {e.args=}", exc_info=True, stack_info=True)
      sys.exit(2)
  except Exception as e:
    err(f"出现未知异常: 正在停止运行...{e=}", exc_info=True, stack_info=True)
    sys.exit(5)
    raise e


if __name__ == '__main__':
  print('{} 作为主程序运行'.format(__file__))
#  print(data2url("test"))
  #  asyncio.run(test())
elif 0:
  with open("test.jpg", "rb") as file:
    data = file.read()
    asyncio.run(ipfs_add(data, filename="test.jpg"))
elif __package__ == "":
  print('{} 运行, empty package'.format(__file__))
  #  from .html_to_telegraph_format import convert_html_to_telegraph_format
  # from ..telegram import put
  SH_PATH = asyncio.run(read_file()).rstrip('\n')
  DOMAIN = asyncio.run(read_file("DOMAIN")).rstrip('\n')
else:
  print('{} 运行, package: {}'.format(__file__, __package__))
# /tmp/run/user/1000/bot
  #  asyncio.create_task(_init())

