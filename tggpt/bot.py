
#!/usr/bin/python
# -*- coding: UTF-8 -*-


#  from . import *  # noqa: F403
#  from enum import auto
from typing import Type
from . import debug, WORK_DIR, PARENT_DIR, LOG_FILE, get_my_key, HOME, LOGGER



#  from tg.telegram import DOWNLOAD_PATH
from telethon.tl.types import KeyboardButton, KeyboardButtonUrl, PeerUser, PeerChannel, PeerChat, User, Channel, Chat
from telethon import events, utils
import telethon.errors
from telethon.errors import rpcerrorlist

#  import aioxmpp
from aioxmpp import stream, ibr, protocol, node, dispatcher, connector, JID, im, errors, MessageType, PresenceType, misc, chatstates

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



from inspect import isawaitable, currentframe

from functools import wraps
import pickle
from pathlib import Path

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


from collections import deque
from os.path import isdir


import time
#  from time import time, sleep
#  from time import time
#  from asyncio import sleep
import asyncio

#  HOME = os.environ.get("HOME")

import logging
logger = logging.getLogger(__name__)

class NoParsingFilter(logging.Filter):
  def filter(self, record):
    #  if record.name == 'tornado.access' and record.levelno == 20:
    if record.levelno == 20:
      if record.name == 'httpx':
        #  pprint(record)
        msg = record.getMessage()
        if msg.startswith('HTTP Request: GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/') and msg.endswith(' "HTTP/1.1 404 Not Found"'):
          return False
        elif '404 Not Found' in msg and 'GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/' in msg:
           #  logger.info(f"根据关键词找到了文本: {msg=}")
           return False
        elif '404 Not Found' in msg:
           logger.info(f"根据关键词找到了文本: {msg=}")
           return False
        #  else:
        #    logger.info(f"文本不对: {msg=}")
    return True


interval = 5
download_media_time_max = 300

wtf_time = 5
wtf_time_max = 1800

wtf_line = 20
wtf_line_max = 300

wtf_limit = 512
wtf_ban_time = 300

async def wtf_loop():
  while True:
    await asyncio.sleep(wtf_time)
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


def info0(s):
  print("%s\r" % s.replace("\n", " "), end='')

def info1(s):
  print("%s" % s.replace("\n", " "), end='')

def info2(s):
  print("%s" % s.replace("\n", " "))

def send_log(text):
  #  asyncio.create_task(mt_send_for_long_text(text))
  #  asyncio.create_task(send(text))
  asyncio.create_task(sendg(text))

def err(text):
  if type(text) is not str:
    text = f"{text=}"
  #  lineno = currentframe().f_back.f_lineno
  #  lineno = sys._getframe(1).f_lineno
  tb = sys._getframe()
  lineno = get_lineno(tb)
  text = f"E: {lineno}: {text}"
  logger.error(text, exc_info=True, stack_info=True)
  #  raise ValueError
  send_log(text)


def warn(text, more=False):
  if type(text) is not str:
    text = f"{text=}"
  #  lineno = currentframe().f_back.f_lineno
  #  lineno = sys._getframe(1).f_lineno
  tb = sys._getframe()
  lineno = get_lineno(tb)
  text = f"W: {lineno}: {text}"
  if more:
    logger.warning(text, exc_info=True, stack_info=True)
  else:
    logger.warning(text)
  send_log(text)

def info(text):
  if type(text) is not str:
    text = f"{text=}"
  #  lineno = sys._getframe(1).f_lineno
  tb = sys._getframe()
  lineno = get_lineno(tb)
  text = f"{lineno}: {text}"
  logger.info(text)


def log(text):
  if type(text) is not str:
    text = f"{text=}"
  #  lineno = currentframe().f_back.f_lineno
  #  lineno = sys._getframe(1).f_lineno
  tb = sys._getframe()
  lineno = get_lineno(tb)
  text = f"{lineno}: {text}"
  send_log(text)
  logger.warning(text)

def dbg(text):
  logger.debug(text)

def get_cmd(text):
  if text.endswith(": "):
    text = text[:-2]
  cmd = text.split(' ')
  tmp = []
  for i in cmd:
    if tmp:
      ii = tmp[-1].split("\\\\")[-1]
      if ii and ii[-1] == "\\":
        tmp[-1] = tmp[-1][:-1] + " " + i
      else:
        #  if i:
        tmp.append(i)
    else:
      if i:
        tmp.append(i)
  if tmp:
    cmd = tmp
    logger.info(f"return cmd {len(cmd)}: {cmd=}")
  return cmd

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


async def split_long_text(text, msg_max_length=500):
  if len(text.encode()) / msg_max_length > 3:
    url =await pastebin(text)
    return [f"文本过长，请打开链接查看: {url}"]
  texts = []
  if len(text.encode()) > msg_max_length:
    ls = text.splitlines()
    tmp = None
    last = None
    for l in ls:
      if tmp:
        if len((tmp+l).encode()) > msg_max_length:
          #  break
          texts.append(tmp)
          tmp = l
        else:
          tmp += '\n'+l
      else:
        if last:
          if len((last+l).encode()) > msg_max_length:
            texts.append(last)
            last = None
          else:
            texts.append(last+'\n'+l)
            last = None
            continue
        if len(l.encode()) > msg_max_length:
          tmp = l[:1300]
          while True:
            if len(tmp.encode()) > msg_max_length:
              tmp = tmp[:-1]
            else:
              texts.append(tmp)
              l = l[len(tmp):]
              if len(l.encode()) > msg_max_length:
                tmp = l[:1300]
              else:
                last = l
                break
        else:
          tmp = l

    if tmp:
      texts.append(tmp)
  else:
    texts = [text]
  return texts


#  api_id = int(get_my_key("TELEGRAM_API_ID"))

MY_ID = int(get_my_key("TELEGRAM_MY_ID"))

CHAT_ID = int(get_my_key("TELEGRAM_GROUP_LIQS"))
#  GROUP_ID = int(get_my_key("TELEGRAM_GROUP_WTFIPFS"))

#  gpt_bot = int(get_my_key("TELEGRAM_GPT_ID"))
gpt_bot = 6226014461
gpt_bot_name = 'littleb_gptBOT'

#  rss_id = int(get_my_key("TELEGRAM_RSS_ID"))
rss_bot = 284403259
music_bot = 1404457467
music_bot_name = 'Music163bot'



MAX_MSG_BYTES = 8000
MAX_MSG_BYTES_TG = 4000

HTTP_RES_MAX_BYTES = 15*2**20
HTTP_FILE_MAX_BYTES = 50*2**20

FILE_DOWNLOAD_MAX_BYTES = 64*2**20
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
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
#  urlre=re.compile(r'((^|https?://|\s+)((([\dA-Za-z0-9.]+-?)+\.)+[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s]+)*/?)')
#  urlre=re.compile(r'((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s"]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[0-9a-zA-Z$\-_\.\+\!\*\'\(\)\,]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)(https?://((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[0-9a-zA-Z$\-_\.\+\!\*\'\(\)\,\?\=%]+)*/?)')
#  urlre = re.compile(r'(^|\n|\s+)(https?://((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^\s\\\"\',?!，。？！“”‘’、【】…]+)*/?)')
urlre = re.compile(r'(^|\n|\s+)(https?://((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|\[[\da-fA-F:]{4,}\])(:\d+)?(/[^\s]+)*/?)')
url_md_left=re.compile(r'\[[^\]]+\]\([^\)]+')
shell_color_re=re.compile(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')

qre = re.compile(r'^(>( .+)?)$', re.M)


#  gptmode=[]
CLEAN = "/new_chat"

#  queue = asyncio.Queue(512)

#  queue = {}
#  stuck= {}
queues = {}
nids = {}
mt_send_lock = asyncio.Lock()
mt_send_lock2 = asyncio.Lock()
downlaod_lock = asyncio.Lock()
bash_lock = asyncio.Lock()
tg_send_lock = asyncio.Lock()

rss_lock = asyncio.Lock()


gid_src = {}
mtmsgsg={}





allright = asyncio.Event()
#  allright.set()

allright_task = 0

LOADING="思考你发送的内容..."
LOADING2="Thinking about what you sent..."
LOADINGS="\n\n"+LOADING
LOADINGS2="\n\n"+LOADING2
  #  elif text == "处理图片请求并获得响应可能需要最多5分钟，请耐心等待。" or text == "It may take up to 5 minutes to process image request and give a response, please wait patiently.":

loadings = (
    LOADING,
    LOADING2,
    """思考你发送的内容...
If the bot doesn't respond, please /new_chat before asking.""",
    "Thinking about what you sent...\nIf the bot doesn't respond, please /new_chat before asking.",
"处理图片请求并获得响应可能需要最多5分钟，请耐心等待。",
"It may take up to 5 minutes to process image request and give a response, please wait patiently.",
)

#  UB.parse_mode = None
#  UB.parse_mode = 'html'






# https://xtxian.com/ChatGPT/prompt/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98.html#%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98
PROMPT_TR_ZH = '''我想让你充当中文翻译员、拼写纠正员和改进员我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答我希望你用更优美优雅的高级中文描述保持相同的意思，但使它们更文艺。

你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。

我要你只回复更正、改进，不要写任何解释我的第一句话是'''

PROMPT_TR_MY_S = '请翻译引号中的内容，你要检测其原始语言，如果是中文就翻译成英文，否则就翻译为中文:'

PROMPT_TR_MY = '请翻译引号中的内容，你要检测其原始语言是不是中文，如果原始语言是中文就翻译成英文，否则就翻译为中文。你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。 我要你只回复更正、改进，不要写任何解释我的第一句话是：\n'



def exceptions_handler(func):
  if asyncio.iscoroutinefunction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      try:
        return await func(*args, **kwargs)
      #  except Exception as e:
      except BaseException as e:
        return  _exceptions_handler(e, *args, **kwargs)
  else:
    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      #  except Exception as e:
      except BaseException as e:
         return  _exceptions_handler(e, *args, **kwargs)
  return wrapper



def get_lineno(tb):
  lineno = "%s" % tb.f_lineno
  while tb.f_back is not None:
    if tb.f_code.co_filename == __file__:
      lineno += " %s" % tb.f_back.f_lineno
      tb = tb.f_back
    else:
      break
  return lineno

def _exceptions_handler(e, *args, **kwargs):
  more = True
  #  res = f'内部错误: {e=} line: {e.__traceback__.tb_next.tb_lineno}'
  tb = e.__traceback__
  #  lineno = get_lineno2(tb)
  lineno = "%s" % tb.tb_lineno
  while tb.tb_next is not None:
    lineno += " %s" % tb.tb_next.tb_lineno
    tb = tb.tb_next
  res = f'内部错误: {e=} line: {lineno}'
  try:
    #  res = f'{e=} line: {e.__traceback__.tb_next.tb_next.tb_lineno}'
    raise e
  except KeyboardInterrupt:
    logger.info("W: 手动终止")
    raise
  except SystemExit:
    logger.error(res, exc_info=True, stack_info=True)
    raise
  except RuntimeError:
    pass
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
  except ConnectionError as e:
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
    pass
  except rpcerrorlist.FloodWaitError:
    pass
  except Exception:
    pass
    #  logger.error(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    #  print(f"W: {repr(e)} line: {e.__traceback__.tb_next.tb_next.tb_lineno}")

  res = f"已忽略{res}"
  #  log(res)
  #  logger.warning(res)
  #  asyncio.create_task(mt_send(res))
  #  asyncio.create_task(send(res, ME))
  if more:
    logger.error(res, exc_info=True, stack_info=True)
    send_log(res)
  else:
    logger.warning(res)
  #  logger.warning(res)
  return res


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



def num2byte(num):
    return bytes.fromhex(hex(num)[2:])

def byte2num(b):
    return int(b.hex(), 16)


# def int_to_bytes(x: int) -> bytes:
def num2byte(x):
    if type(x) == int:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    else:
        logger.warning("type error")
    
# def int_from_bytes(xbytes: bytes) -> int:
def byte2num(b):
    if isinstance(b, bytes):
        return int.from_bytes(b, 'big')
    else:
        logger.warning("type error")



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
        logger.error(f"wtf: {data=}")
        logger.error(f"wtf: {type(data)}")
        return
    data = bytes(data)
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    try:
        return base64.b64decode(data, altchars)
    except binascii.Error as e:
        logger.error(e)


def encode_base64(data, altchars=b'+/'):
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data, altchars=altchars).decode().rstrip("=")


def compress(data, m="zst"):
    if isinstance(data, str):
        data = data.encode()
    if m == "zst":
        return zstandard.compress(data, level=22)
    if m == "br":
        return brotli.compress(data)
    if m == "gzip":
        return gzip.compress(data)
    if m == "deflate":
        return zlib.compress(data)


#  return zlib.compress(data,level=9)


def decompress(data):
    if isinstance(data, str):
        data = data.encode()
    return zstandard.decompress(data)



pb_list = {
    "anon": ["https://api.anonfiles.com/upload", "file"],
    "0x0": ["https://0x0.st/", "file"],
    "fars": ["https://fars.ee/?u=1", "c"]
    }
#async def pastebin(data="test", filename=None, url="https://fars.ee/?u=1", fieldname="c", extra={}, **kwargs):
@exceptions_handler
async def pastebin(data="test", filename=None, url=pb_list["fars"][0], fieldname="c", extra={}, ce=None, use=None, **kwargs):
  if not data:
    return
  if use:
    if use not in pb_list:
      use = "fars"
    url = pb_list[use][0]
    fieldname = pb_list[use][1]
  if not ce:
    if url == pb_list["fars"][0]:
      ce = "br"

  headers = {}
  #  if type(data) == str:
  if isinstance(data, str):
#  data = {"content": data}
#    data = zlib.compress(data)
#    headers = {'Content-Encoding': 'deflate'}
#    data = gzip.compress(data.encode())
#    headers = {'Content-Encoding': 'gzip'}
    if ce:
      data = compress(data.encode(), ce)
      headers = {'Content-Encoding': ce}
    data = {fieldname: data}
    data.update(extra)
  elif isinstance(data, bytes) or type(data) == BufferedReader or type(data) == TextIOWrapper or type(data) == BytesIO:
    if filename:
      data = file_for_post(data, filename=filename, fieldname=fieldname, **extra)
    else:
      data = {fieldname: data}
      data.update(extra)
  elif isinstance(data, dict):
    pass
#  elif type(data) == aiohttp.formdata.FormData:
  elif type(data) == FormData:
    pass
  else:
    return
  res = await http(url=url, method="POST", data=data, headers=headers,  **kwargs)
#    res = res + "." + filename.split(".")[-1]
  res = res.strip()
  if url == pb_list["fars"][0]:
    if not url.startswith("https://fars.ee/"):
      res = await pastebin(data=data, filename=filename, extra=extra, use="0x0", **kwargs)
  return res

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

async def my_split(path, is_str=False):
  if is_str:
    text = path
  else:
    if os.path.exists(path):
      text = await read_file(path)
      logger.info(f"{path}: {text[:64]}...")
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
    logger.error("E: fail to ipfs")
    return

  url = res.strip()
  logger.info(res)
#  url = json.loads(url)
  try:
    url = load_str(url)
  except SyntaxError as e:
    info = f"{e=}\n\n{url}"
    print(info)
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
  if filename and not mimetype:
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
  if not filename and filename.split(".")[-1] not in allowed:
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
    logger.error("need bytes")
    return
  data = bytes(data)
  with open(name, "wb") as file:
    file.write(data)
  return name

def load_str(msg, no_ast=False):
  """str to dict"""
  msg = msg.strip()
  if no_ast:
    import json
    return json.loads(msg)
  try:
    return ast.literal_eval(msg)
  except ValueError:
    logger.warning(msg)
    import json
    try:
      return json.loads(msg)
    except Exception as e:
      err(f"json: error str: {msg} line: {e.__traceback__.tb_lineno}")
      #  raise e




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





async def update_stdouterr(data):
  while data[2].poll() == None:
    try:
      data[0], data[1] = data[2].communicate(timeout=0.6)
    except subprocess.TimeoutExpired as e:
      if e.stdout:
        data[0] = e.stdout.decode("utf-8")
      if e.stderr:
        data[1] = e.stderr.decode("utf-8")
    await asyncio.sleep(0.3)


async def update_stdout(data):
  while True:
    print(1)
    await asyncio.sleep(0.4)
    tmp = await data[2].stdout.readline()
    if tmp:
      data[0] = data[0] + tmp.decode("utf-8")
    else:
      break
  logger.info(11)


async def update_stderr(data):
  while True:
    print(2)
    await asyncio.sleep(0.2)
    tmp = await data[2].stderr.readline()
    if tmp:
      data[1] = data[1] + tmp.decode("utf-8")
    else:
      break
  logger.info(22)


async def my_popen(cmd,
           shell=True,
           max_time=60,
           client=None,
           src=None,
           combine=True,
           return_msg=False,
           executable='/bin/bash',
           **args):
  
  async with bash_lock:
    #  logger.info(cmd)
    #    args=shlex.split(message.text.split(' ',1)[1])

    #    p=subprocess.Popen(message.text.split(' '))
    #    p=subprocess.Popen(message.text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #    p=subprocess.Popen(shlex.split(message.text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)

    #    p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #    p=Popen(args,text=True,universal_newlines=True,bufsize=1,stdout=PIPE, stderr=PIPE)
    #    p=Popen(args,text=True,stdout=PIPE, stderr=PIPE)
    #    p=await asyncio.create_subprocess_shell(message.text.split(' ',1)[1],stdout=PIPE, stderr=PIPE)#limit=None
    #    p=Popen(args,stdout=PIPE, stderr=PIPE,bufsize=8000000)
    #    p=Popen(args,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    #  p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    p = Popen(cmd,
          shell=shell,
          stdout=PIPE,
          stderr=PIPE,
          text=True,
          encoding="utf-8",
          errors="ignore",
          executable=executable)

    start_time = time.time()
    res = ""
    errs = ""
    data = ["", "", p]
    asyncio.create_task(update_stdouterr(data))
    await asyncio.sleep(2)
    logger.info(f"popen cmd: {p.args}")
    if type(cmd) == list:
      if len(cmd) == 6 and "bcmd.sh" in cmd[1]:
        cmd_str = cmd[4]
      else:
        cmd_str = " ".join(cmd)
    else:
      cmd_str = cmd
    if len(str(cmd_str)) > 512:
      cmd_str = "%s..." % cmd_str[:512]
    tmp_last = None
    while True:
      #  if p.poll() == None and p.returncode == None:
      if p.poll() == None:
        pass
      else:
        break
      #  await asyncio.sleep(0.5)
      res = data[0]
      errs = data[1]

      #  if msg:
      #    if tmp != msg.text:
      if src:
        if res:
          if len(res) > 512:
            res = "%s..." % res[:512]
        else:
          res = '...'
        #  tmp = "...\n" + res + "\n==\nE: \n" + errs
        tmp = "正在执行(%ss): %s\n%s\nE: ?\n%s" % (int(time.time()-start_time), cmd_str, res, errs)
        tmp = tmp.strip()
        if tmp != tmp_last:
          try:
            tmp = re.sub(shell_color_re,  "", tmp)
            logger.info(f"临时输出: {tmp}")
            #  msg = await cmd_answer(tmp, client, msg, **args)
            #  logger.info(f"临时输出: {tmp}")
            await send(tmp, src, xmpp_only=True, correct=True)
            tmp_last = tmp
          except Exception as e:
            #  logger.error(f"can not send tmp: {e=}")
            #  msg = await client.send_message(MY_ID, tmp)
            warn(f"无法发送临时输出: {tmp} {e=}")
      await asyncio.sleep(interval)
      if time.time() - start_time > max_time:
        p.kill()
        res = "my_popen: timeout, killed, cmd: {}\nres: {}".format(cmd, res)
        warn(res)
        if src:
          await send(f"E: killed(timeout): {cmd_str}", src)
        #  await cmd_answer(res, client, msg)
        #  logger.info(f"最终输出: {res}")
        break

    try:
      res, errs = p.communicate(timeout=5)
    except subprocess.TimeoutExpired as e:
      logger.error("timeout")
      res = e.stdout
      if res:
        res = res.decode("utf-8")
      errs = e.stderr
      if errs:
        errs = errs.decode("utf-8")

    logger.info(f"popen exit: {p.returncode} {res=} {errs=}")
    if res:
      res = res.strip()
    if errs:
      errs = errs.strip()
    #  if res:
    #    if isinstance(res, bytes):
    #      res = res.decode("utf-8")
    #  if errs:
    #    if isinstance(errs, bytes):
    #      errs = errs.decode("utf-8")
    #  if not res:
    #    return False

    #  if msg:
    #    #  msg = await cmd_answer(res, client, msg, **args)
    #    logger.info(f"发送: {res}")
    #    if return_msg:
    #      return msg
    if combine:
      if errs:
        res = "%s\n--\nE: %s\n%s" % (res, p.returncode, errs)
      elif p.returncode:
        res = "%s\n--\nE: %s" % (res, p.returncode)
      if res:
        if len(res) > MAX_MSG_BYTES:
          res = await pastebin(res)
        return res
      else:
        return
        return "None"
    else:
      return p.returncode, res, errs


async def run_my_bash(cmd, shell=True, max_time=120):
  p = Popen(cmd,
        shell=shell,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore")

  start_time = time.time()
  res = ""
  errs = ""
  await asyncio.sleep(0.5)
  if p.poll() == None and p.returncode == None:
    while p.poll() == None and p.returncode == None:
      if time.time() - start_time > max_time:
        p.kill()
        break
      await asyncio.sleep(1)

  try:
    res, errs = p.communicate(timeout=3)
  except subprocess.TimeoutExpired as e:
    res = e.stdout
    errs = e.stderr
  if not res:
    res = "null"
  #  res = str(res)
  if p.returncode:
    #  res = res + "\n==\nE: " + str(p.returncode)
    res = "%s\n==\nE: %s" % (res, p.returncode)
    if errs:
      res = res + "\n" + errs
    #await msg.delete()
  if len(res) > MAX_MSG_BYTES:
    res = await pastebin(res)
  return res


async def my_exec(cmd, src=None, client=None, **args):
  #  exec(cmd) #return always is None
  #  p=Popen("my_exec.py "+message.text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
  #  await my_popen(["python3", "my_exec.py", cmd], shell=False, msg=msg)
  #  await my_popen([ SH_PATH + "/my_exec.py", cmd], shell=False, msg=msg, executable="/usr/bin/python3")
  res = await my_popen(cmd,
             shell=True,
             client=client, 
             src=src,
             executable="/usr/bin/python3",
             **args)
  return res


async def my_eval(cmd):
  res = eval(cmd)
  logger.info("%s %s" % (res, type(res)))
  #  res = await cmd_answer(str(res), client=client, msg=msg, **args)
  return res

async def send_cmd_to_bash(gateway, name, text):
  #  if not text:
  #    logger.warning("skip bash cmd, text is empty: {}".format(msg))
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
  #  logger.info("msg_mt: {}".format(msg))
  #  shell_cmd="{} {} {} {}"
  #  shell_cmd = ["bash -l", SH_PATH + "/bcmd.sh"]
  shell_cmd = ["bash", SH_PATH + "/bcmd.sh"]
  #  shell_cmd = [SH_PATH + "/bcmd.sh"]
  shell_cmd.append(gateway)
  shell_cmd.append(name)
  shell_cmd.append(text)
  shell_cmd.append(repr(msg))

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
  #  logger.warning("bash cmd: {}".format(shell_cmd))
  #  await run_my_bash(shell_cmd, shell=False)
  #  await my_popen(shell_cmd, shell=False)
  #  await my_popen(" ".join(shell_cmd))
  res = await my_popen(shell_cmd, shell=False, src=gateway)
  if res:
    return re.sub(shell_color_re,  "", res)
  #  logger.info(res)
  return res

#  @exceptions_handler
#  async def send2mt(client, message):
#      "get msg for matterbridge api"
#      chat_id = get_chat_id(message)
#      if chat_id in MT_GATEWAY_LIST_for_tg:
#          sender_id = get_sender_id(message)
#  #        logger.warning(f"send 2 mt: {message.raw_text}")
#          logger.debug("start to mt")
#  #        if message.fwd_from:
#          if is_forward(message):
#              if sender_id == cid_tw:
#                  logger.info("I: ignore a msg from tw")
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
#                                  logger.info("use bash")
#                                  asyncio.create_task(send_cmd_to_bash(msg))
#                                  raise StopPropagation
#  #        if message.out:
#  #            raise StopPropagation




async def load_config():
  path = PARENT_DIR / "config.json"
  config = await read_file(path.as_posix())
  config = load_str(config)

  #  logger.info("config\n%s" % json.dumps(config, indent='  '))
  
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

    logger.info("loaded config\n%s" % json.dumps(config, indent='  '))

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
        #  logger.info(f"loaded gd: {gd}")
      else:
        gd = {}
    except Exception as e:
      err(e)
      gd = {}

    if "users" not in gd:
      gd["users"] = {}

    if "bridges" not in gd:
      gd["bridges"] = {
          -1001577701755: acg_group,
          rss_bot: rss_group,
          #  gpt_bot: "gateway1",
          }

    #  logger.info("loaded gd\n%s" % json.dumps(gd, indent='  '))
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

    for chat_id in bridges:
      target = bridges[chat_id]
      if type(target) is dict:
        target.clear()


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
    warn("保存失败")






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
#      #  logger.info(res)
#      warn(res)
#      #  prof.cons_show(res)
#    #  except urltitle.urltitle.URLTitleError as e:
#    except URLTitleError as e:
#      res=f"URLTitleError: {e=}"
#      #  prof.cons_show(res)
#      warn(res)
#    except Exception as e:
#      #  logger.warning(f"E: {e=}", exc_info=True, stack_info=True)
#      res=f"{e=}"
#      #  prof.cons_show(res)
#      warn(res)
#    return res

async def backup(path, src=None):
  info(f"backup: {path}")
  url = "https://%s%s/%s" % (DOMAIN, URL_PATH, (urllib.parse.urlencode({1: path[len(DOWNLOAD_PATH):]})).replace('+', '%20')[5:])
  info(f"url: {url}")
  shell_cmd=["/usr/bin/mv", path, DOWNLOAD_PATH0+"/"]
  res = await run_my_bash(shell_cmd, shell=False)
  if res:
    info(f"backup res: {res}")
    if src:
      await send(url, src)
  return url



async def get_title(url, src=None, opts=[]):
  shell_cmd = ["bash", f"{SH_PATH}/title.sh"]
  shell_cmd.append(url)
  #  while opts:
  #    shell_cmd.append(opts.pop(0))
  shell_cmd.extend(opts)
  #  if down:
  #    #  shell_cmd.append("%s" % (2**20*1000))
  #    while True:
  #      if len(shell_cmd) < 5:
  #        shell_cmd.append("")
  #      else:
  #        break
  #    shell_cmd.append("down")
  if len(shell_cmd) == 6:
    max_time = 600
  else:
    max_time = 60
  r, out, err = await my_popen(shell_cmd, shell=False, src=src, combine=False, max_time=max_time)
  if r == 0:
    s = out.splitlines()
    if len(s) > 1:
      path = s[-1]
      if os.path.exists(path):
        url = await upload(path)
        asyncio.create_task(backup(path, url))
        if url:
          s[-1] = f"\n- {url}"
        else:
          s.pop(-1)
      else:
        s.pop(-1)
      return "\n".join(s)
    else:
      return out
  else:
    #  if err:
    warn("%s\n--\nE: %s\n%s" % (out, r, err))
    return "%s\n--\nE: %s\n%s" % (out, r, err)



#  async def other_init():
#    logger.info("开始初始化其他组件")
#    res = await asyncio.to_thread(_other_init)
#    logger.info(res)
#  #  allright.set()
#    if res is True:
#      global allright_task
#      allright_task -= 1
#
#  @exceptions_handler
#  def _other_init():
#    return True


#  global G1PSID
#  BING_U = get_my_key("BING_U")
G1PSID = get_my_key('BARD_COOKIE_KEY')

from g4f.cookies import set_cookies

#  set_cookies(".bing.com", {
#    "_U": "%s" % BING_U
#  })
set_cookies(".google.com", {
  "__Secure-1PSID": G1PSID
})


from g4f import models, Provider
from g4f.client import Client as Client_g4f

#  def ai_img(prompt, model="gemini", proxy=None):
async def ai_img(prompt, model="gemini"):
  try:
    global g4fclient
    if "g4fclient" not in globals():
      g4fclient = Client_g4f()
    #  response = client.images.generate(
      #  response = await client.images.generate(
    response = await asyncio.to_thread(g4fclient.images.generate,
      model=model,
      #  prompt="a white siamese cat",
      prompt=prompt,
    )
  except Exception as e:
    image_url = f"{e=}"
  else:
    image_url = response.data[0].url
  #  print(image_url)
  return image_url

async def ai(prompt, provider=Provider.You, model=models.default, proxy=None):
  try:
    global g4fclient
    if "g4fclient" not in globals():
      g4fclient = Client_g4f()
    #  response = client.chat.completions.create(
      #  response = await client.chat.completions.create(
      #  s = await asyncio.to_thread(run_ocr, img=res)
    response = await asyncio.to_thread(g4fclient.chat.completions.create,
      model=model,
      messages=[{"role": "user", "content": prompt}],
      provider=provider,
      proxy=proxy,
    )
  except Exception as e:
    image_url = f"{e=}"
  else:
    image_url  = response.choices[0].message.content
  #  print(image_url)
  return image_url



from gradio_client import Client as Client_hg

HF_TOKEN = get_my_key('HF_TOKEN')


async def hg(prompt, provider=Provider.You, model=models.default, proxy=None):
  try:
    global hgclient
    if "hgclient" not in globals():
      hgclient = Client_hg(api_key=HF_TOKEN)
    #  response = client.chat.completions.create(
    response = await hgclient.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": prompt}],
      provider=provider,
      proxy=proxy,
    )
  except Exception as e:
    image_url = f"{e=}"
  else:
    image_url  = response.choices[0].message.content
  #  print(image_url)
  return image_url


async def qw(text):
  try:
    global qw_client
    if "qw_client" not in globals():
      qw_client = Client_hg("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/")
    #  result = qw_client.predict(
    result = await asyncio.to_thread(qw_client.predict,
        #  sys.argv[1],	# str  in 'Input' Textbox component
        text,	# str  in 'Input' Textbox component
        #  [[sys.argv[1], sys.argv[1]]],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
        [],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
        "You are a helpful assistant.",	# str  in 'parameter_9' Textbox component
        api_name="/model_chat"
    )
    #  print(result)
    #  print(result[1][1][1])
    #  print(result[1][0][1])
    res = result[1][0][1]
  except Exception as e:
    res = f"{e=}"
  return res

async def qw2(text):
  try:
    global qw2_client
    if "qw2_client" not in globals():
      qw2_client = Client_hg("Qwen/Qwen1.5-110B-Chat-demo")
    #  result = qw2_client.predict(
    result = await asyncio.to_thread(qw2_client.predict,
        #  query=sys.argv[1],
        query=text,
        history=[],
        system="You are a helpful assistant.",
        api_name="/model_chat"
    )
    #  print(result)
    #  print(result[1][1][1])
    #  print(result[1][0][1])
    res = result[1][0][1]
  except Exception as e:
    res = f"{e=}"
  return res

def get_src(msg):
  if msg.type_ == MessageType.GROUPCHAT:
    return str(msg.from_.bare())
  if msg.from_.is_bare:
    return str(msg.from_)
  if str(msg.to.bare()) in my_groups:
    return str(msg.from_)
  return str(msg.from_.bare())

#  async def set_nick(room, nick):
  #  if msg.type_ == MessageType.GROUPCHAT:

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
  #  logger.info(f"nick changed: {jid} {muc} {old_nick} -> {new_nick}")

send_locks = {}

async def _send(*args, **kwargs):
  #  info(f"{args=} {kwargs=}")
  asyncio.create_task(__send(*args, **kwargs))
  return True

@exceptions_handler
async def __send(msg, client=None, room=None, name=None, correct=False, fromname=None, nick=None, delay=None, xmpp_only=False):
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
        if myjid in jids:
          nick_old = jids[myjid][0]
        else:
          nick_old = room.me.nick
          jids[myjid] = [nick_old, room.me.affiliation, room.me.role]
          err(f"不存在nick记录，已添加: {muc} {myjid} {msg} {jids[myjid]}")
        if nick_old != nick:
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
              await asyncio.wait_for(fu, timeout=5)
            #  except Exception as e:
            except TimeoutError as e:
              on_nick_changed_futures.pop(muc)
              jids[myjid][0] = nick
              info(f"改名失败(超时)：{muc} {nick_old} -> {nick} {e=}")
            else:
              on_nick_changed_futures.pop(muc)
              jids[myjid][0] = fu.result()
              if fu.result() != nick:
                info(f"改名结果有问题: {muc} {fu.result()=} != {nick=}")
              #  else:
              #    logger.info(f"set nick: {muc} {nick_old} -> {nick}")
            #  else:
            #    logger.info(f"same nick: {str(msg.to.bare())} {room.me.nick} = {nick}")
            #  else:
            #    logger.info(f"not found room: {msg.to}")

    text = None
    for i in msg.body:
      text = msg.body[i]
      if text:
        break

    if text:
      if jid == log_group_private:
        sendme(text)
      msgs = []
      for text in await split_long_text(text, MAX_MSG_BYTES):
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

    for msg in msgs:
      if text:
        add_id_to_msg(msg, correct)
        msg.xep0085_chatstate = chatstates.ChatState.ACTIVE
      if msg.to.is_bare or msg.type_ == MessageType.GROUPCHAT or str(msg.to.bare()) not in my_groups:
      #  if gpm is False:
        if client is not None:
          # https://docs.zombofant.net/aioxmpp/devel/api/public/node.html?highlight=client#aioxmpp.Client.send
          res = client.send(msg)
        elif room:
          # https://docs.zombofant.net/aioxmpp/devel/api/public/muc.html?highlight=room#aioxmpp.muc.Room.send_message
          res = room.send_message(msg)
        else:
          client = XB
          res = client.send(msg)
      else:
        # https://docs.zombofant.net/aioxmpp/devel/api/public/im.html#aioxmpp.im.conversation.AbstractConversation.send_message
        if client is None:
          client = XB
        p2ps = client.summon(im.p2p.Service)
        c = p2ps.get_conversation(msg.to)
        #  stanza = c.send_message(msg)
        res = c.send_message(msg)
        #  return False
      #  if isawaitable(res):
      #  logger.info(f"{type(res)}: {res} {msg}")
      if asyncio.iscoroutine(res) or type(res) is stream.StanzaToken:
        #  dbg(f"client send: {res=}")
        res2 = await res
        if res2 is None:
          dbg(f"send msg: finally: {res=}")
        #  elif hasattr(res, "stanza") and res.stanza and res.stanza.error is None:
        #    # 群内私聊
        #    logger.info(f"send gpm msg: finally: {res=}")
        #    return True
          if delay:
            #  info(f"delay: {delay}s")
            await asyncio.sleep(delay)
          return True
        else:
          logger.info(f"send msg: finally: {res=} {res2=}")
          return False
      else:
        warn(f"send msg: res is not coroutine: {res=} {client=} {room=} {msg=}")
      return False


@exceptions_handler
async def send(text, jid=None, *args, **kwargs):
  muc = None
  if 'name' in kwargs:
    name = kwargs["name"]
    #  kwargs.pop("name")
  else:
    name = "**C bot:** "
  if name:
    kwargs["name"] = name[2:-4]
    nick = name[2:-4]
  else:
    kwargs["name"] = None
    nick = name
  #  if 'correct' in kwargs:
  #    correct = kwargs["correct"]
  #  else:
  #    correct = False

  if 'xmpp_only' in kwargs:
    xmpp_only = kwargs["xmpp_only"]
  else:
    xmpp_only = False

  if jid is None:
    if isinstance(text, aioxmpp.Message):
      if text.type_ == MessageType.GROUPCHAT:
        muc = str(text.to.bare())
      else:
        pass
    else:
      #  err(f"需要jid")
      #  return False
      jid = log_group_private
  #  elif jid == "gateway1":
  #    jid = main_group
  else:
    muc = jid

  if isinstance(text, aioxmpp.Message):
    text0 = text.body[None]
    text.body[None] = f"{name}{text0}"
  else:
    text0 = text
    text = f"{name}{text}"


  ms = get_mucs(muc)
  if ms:
  #  if muc in my_groups:
    #  info(f"准备发送同步消息到: {ms} {text=}")
    if main_group in ms:
      if xmpp_only:
        for m in ms:
          await send_typing(m)
        await send1(text, jid=log_group_private, *args, **kwargs)
        return True
        ms = set()
      else:
        await mt_send_for_long_text(text0, name=nick)

    for m in ms:
      if await send1(text, jid=m, *args, **kwargs):
        if isinstance(text, aioxmpp.Message):
          text = text.body[None]

    #  if main_group in ms and xmpp_only:
    #    for m in ms:
    #      await send_typing(m)
    #  else:
    #    for m in ms:
    #      if await send1(text, jid=m, *args, **kwargs):
    #        if isinstance(text, aioxmpp.Message):
    #          text = text.body[None]
    #          #  #  text.body[None] = text0
    #          #  body = text.body
    #          #  text = aioxmpp.Message(
    #          #      to=JID.fromstr(text.to),  # recipient_jid must be an aioxmpp.JID
    #          #      type_=text.type_,
    #          #  )
    #          #  text.body = body
    #        continue
    #      return False
    #  if xmpp_only is False:
    #    if main_group in ms:
    #      await mt_send_for_long_text(text0, name=nick)
    return True
  else:
    #  info(f"准备发送到: {muc=} {jid=}")
    return await send1(text, jid=jid, *args, **kwargs)

async def send1(text, jid=None, *args, **kwargs):

  if type(text) is str:
    #  if name:
    #    text = f"{name}{text}"
    if jid is None:
      jid = ME
    else:
      if type(jid) is JID:
        jid = get_jid(jid, True)

      #  if gpm and '/' not in jid:
      #    err(f"无法群私聊，地址错误: {jid}")
      #    return False
    texts = await split_long_text(text, 4096)
    #  for i in texts:
    if jid in my_groups:
      msg = aioxmpp.Message(
          to=JID.fromstr(jid),  # recipient_jid must be an aioxmpp.JID
          type_=MessageType.GROUPCHAT,
      )
    else:
      #  if '/' in jid and jid.split('/', 1)[0] in my_groups:
      msg = aioxmpp.Message(
          to=JID.fromstr(jid),  # recipient_jid must be an aioxmpp.JID
          type_=MessageType.CHAT,
      )
    #  j = get_msg_jid(msg)
    #  if correct:
    #    if j in last_outmsg:
    #      #  msg.xep0308_replace = misc.Replace(last_outmsg[get_jid(msg.to, True)])
    #      r = misc.Replace()
    #      r.id_ = last_outmsg[j]
    #      msg.xep0308_replace = r
    #  else:
    #    if j in last_outmsg:
    #      last_outmsg.pop(j)
    #  if len(texts) > 1:
    #    await add_id_to_msg(msg, False)
    #  else:
    msg.body[None] = text
    if await _send(msg, *args, **kwargs) is not True:
      return False
    #  if correct:
    #  if msg.xep0308_replace:
    #  if "correct" in kwargs and kwargs["correct"]:
    #    break

    return True
  elif isinstance(text, aioxmpp.Message):
    #  logger.info(f"send1: {jid=} {text=}")
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
        logger.info(f"已修正地址错误: {orig} -> {msg=}")
    #  elif gpm and msg.to.resource is None:
    #    err(f"无法群私聊，地址错误: {msg.to}")
    #    return False


    return await _send(msg, *args, **kwargs)
  else:
    err(f"text类型不对: {type(text)}")
    return False
    #  elif isinstance(text, aioxmpp.stanza.Message):
    #    #  logger.info(f"send2: {jid=} {text=}")
    #    msg = text

#  async def __send(msg, jid=None, client=None, gpm=False):
#    #  if type(text) is str:
#      #  logger.info(f"send: {jid=} {text=}")
#      # None is for "default language"
#    #  logger.info(f"send: {type(msg)} {msg=}")
#    if client is None:
#      client = XB
#    #  return await client.send(msg)
#    return await _send(msg, client, gpm=gpm)

def sendme(text):
  asyncio.create_task(_sendme(text))



async def _sendme(text, chat_id=CHAT_ID):
  async with tg_send_lock:
    for t in await split_long_text(text, MAX_MSG_BYTES_TG):
      await UB.send_message(chat_id, t)
      await asyncio.sleep(len(t.encode())/MAX_MSG_BYTES_TG+0.2)
  return True
  chat = await get_entity(CHAT_ID, True)
  await UB.send_message(chat, text)

async def sendg(text, jid=None, room=None, client=None, name="**C bot:** ", **kwargs):
  if name:
    text = f"{name}{text}"
  #  sendme(text)
  logger.info(f"send group msg: {jid} {text}")
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
    #      logger.info(f"room send: finally: {res=}")
    #      return False
    #  else:
    #    logger.info(f"room send res is not coroutine: {res=}")
    #    return False
  #  else:
  #    warn(f"need client or room")
  #    return False


#  @exceptions_handler
async def mt_read():
  # api.xmpp
  MT_API = "127.0.0.1:4247"
  url = "http://" + MT_API + "/api/stream"
  #  session = await init_aiohttp_session()
  logger.info("start read msg from mt api...")
  while True:
    try:
      async with aiohttp.ClientSession() as session:
        #  async with session.get(url, timeout=0, read_bufsize=2**20) as resp:
          #  print("N: mt api init ok")
          #  resp.content.read()
          #  async for line in resp.content:
          #    #  logger.info("I: got a msg from mt api: %s", len(line))
          #    #  print(f"I: original msg: %s" % line)
          #    await mt2tg(line)

        async with session.get(url, timeout=0, read_bufsize=2**18*4, chunked=True) as resp:
          send_log("N: mt api init ok")
          #  await mt_send("N: tggpt: mt read: init ok")
          line = b""
          async for data, end_of_http_chunk in resp.content.iter_chunks():
            line += data
            #  logger.info(f"read bytes: {len(data)}")
            if end_of_http_chunk:
              #  logger.info(f"read end: {len(line)}")
              # # print(buffer)
              # await send_mt_msg_to_queue(buffer, queue)
              #  await mt2tg(line)
              #  asyncio.create_task(mt2tg(line))
              asyncio.create_task(parse_mt(line))
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
    await asyncio.sleep(3)


#  @exceptions_handler
#  async def titlebot(msgd):
#
#    await asyncio.sleep(5)
#    text = msgd['text']


@exceptions_handler
async def parse_mt(msg):
  '''
  #       Data sent: 'GET /api/stream HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
  #      Data received: 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nDate: Wed, 19 Jan 2022 02:03:29 GMT\r\nTransfer-Encoding: chunked\r\n\r\nd5\r\n{"text":"","channel":"","username":"","userid":"","avatar":"","account":"","event":"api_connected","protocol":"","gateway":"","parent_id":"","timestamp":"2022-01-19T10:03:29.666861315+08:00","id":"","Extra":null}\n\r\n'
  2024-05-07 17:26:25,343 [INFO] tggpt.bot [bot.info:157]: msg of mt_read: {'text': 'ping', 'channel': 'bebat', 'username': 'X liqsliu_: ', 'userid': 'bebat@muc.pimux.de/liqsliu_', 'avatar': 'https://wtfipfs.eu.org/0789fa8d/bebat_muc_pimux_de_liqsliu_.png', 'account': 'xmpp.pimux', 'event': '', 'protocol': 'xmpp', 'gateway': 'test', 'parent_id': '', 'timestamp': '2024-05-07T17:26:25.22885781+08:00', 'id': '', 'Extra': None}
  2024-05-07 17:26:25,778 [INFO] tggpt.bot [bot.mt_send:1806]: res of mt_send: {"text":"pong. now tasks: 0/0","channel":"api","username":"C bot","userid":"","avatar":"","account":"api.cmdres","event":"","protocol":"api","gateway":"test","parent_id":"","timestamp":"2024-05-07T17:26:25.367596549+08:00","id":"","Extra":null}
  '''
  try:
      msg = msg.decode()
      if not msg or msg.startswith("HTTP/1.1"):
        logger.info("I: ignore init msg")
        return

      msgd = json.loads(msg)
  except json.decoder.JSONDecodeError:
      logger.error("fail to decode msg from mt")
      print("################")
      print(msg)
      print("################")
      #  info = "E: {}\n==\n{}\n==\n{}".format(sys.exc_info()[1], traceback.format_exc(), sys.exc_info())
      #  logger.error(info)
      logger.error("E: failed to decode msg from mt...", exc_info=True, stack_info=True)
      return

  account = msgd["account"]
  #  if account == "api.cmdres":
  #    logger.info("I: ignore msg from cmdres")
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
    logger.debug("original msg of mt_read: %s" % msgd)
    # file
    #,"id":"","Extra":{"file":[{"Name":"proxy-image.jpg","Data":"/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAA ... 6P9ZgOT6tI33Ff5p/MAOfNnzPzQAN4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAGQAAYAkAAGTGAAAAAAAAwsAAHLAAAK//9k=","Comment":"","URL":"https://liuu.tk/ddb833ad/proxy_image.jpg","Size":0,"Avatar":false,"SHA":"ddb833ad"}]}}\n\r\n'
    files = msgd["Extra"]["file"]
    for file in fs:
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
    logger.warning("removed file info from mt api(saved)")
    msgd['text'] = text
  else:
      msgd.pop("Extra")
      logger.warning("removed file info from mt api")

  #  print(f"I: got msg: {name}: {text}")
  if not text:
    logger.info(f"I: ignore msg: no text {msgd=}")
    return
  if not name:
    logger.info(f"I: ignore msg: no name {msgd=}")
    return

  #  if name == "C twitter: ":
  #      return
  #  if name.startswith("C "):
  #    logger.info("I: ignore msg: C ")
  #    return
  #  if name.startswith("X "):
  #    logger.info("I: ignore msg: X ")
  #    return
  #  if name.startswith("**C "):
  #    logger.info("I: ignore msg: **C ")
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
  logger.info("msg of mt_read: %s" % msgd)

  #  logger.info("got msg from mt: {}".format(msgd))
  #      if name == "C Telegram: ":
  if gateway == "gateway1":

    text0 = text
    if '\n' in name:
      ls = name.splitlines()
      name = ls[-1]
      rname = name[:-2]
      qt = '\n'.join(ls[:-1])
      text = f"{text}\n\n{qt}"
      qt = '\n> '.join(ls[:-1])
      name2 = f"> {qt}\n**{rname}:** "
    else:
      rname = name[:-2]
      name2 = f"**{rname}:** "

    text2 = f"{name2}{text0}"

    for m in get_mucs(main_group):
      if await send1(text2, m, nick=rname) is False:
        return

    res = await run_cmd(text, gateway, name, textq=text0)
    if res is True:
      return
    if res:
      await mt_send_for_long_text(res, gateway)
      res = f"**C bot:** {res}"

      for m in get_mucs(main_group):
        if await send1(res, m, nick="C bot") is False:
          return
    #    if await send1(f"{name}{text}", m, name) is False:
    #      return
    #    if res:
    #      if await send1(f"{name}{res}", m, "C bot") is False:
    #        return


  #  except Exception as e:
  #    #  info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
  #    #  logger.error(info)
  #    logger.error("error: msg from mt to tg: ", exc_info=True, stack_info=True)
  #    #  await NB.send_message(MY_ID, info)
  #    await asyncio.sleep(5)



async def send_to_tg_bot(text, chat_id):
  chat = await get_entity(chat_id, True)
  msg = await UB.send_message(chat, text)
  #  if src:
  #    mtmsgsg[src][msg.id] = []
  #  info(f"res of send: {msg.stringify()}")
  #  gid_src[msg.id] = src
  #  if src not in mtmsgsg:
  #    mtmsgsg[src] = {}
  #  mtmsgsg[src][msg.id] = [msg]
  #  mtmsgsg[src][msg.id] = [None]
  return msg.id




async def clear_history(src=None):
  if not allright.is_set():
    warn("wait for allright...")
    await allright.wait()
    return
  music_bot_state.clear()
  allright.clear()
  #  await asyncio.sleep(1)
  #  for g in queues:
  if src:
    tmp = []
    for i in gid_src:
      if gid_src[i] == src:
        tmp.append(i)
    for i in tmp:
      gid_src.pop(i)

    if src in mtmsgsg:
      ms = mtmsgsg[src]
      ms.clear()
  else:
    for g in mtmsgsg:
      mtmsgs = mtmsgsg[g]
      mtmsgs.clear()
    #  await mt_send(f"cleaned: {mtmsgsg=}", gateway="test")
    gid_src.clear()
    #  await mt_send(f"cleaned: {gid_src=}", gateway="test"):w
  allright.set()
  logger.info("reset ok")


#  session = None
#  async def init_aiohttp_session():
#    global session
#    if session is None:
#      session = aiohttp.ClientSession()
#      logger.warning("a new session")

@exceptions_handler
async def http(url, method="GET", return_headers=False, *args, **kwargs):
  if "headers" in kwargs:
    headers = kwargs["headers"]
  else:
    headers = {}
    kwargs["headers"] = headers
  if "Accept-Encoding" not in headers:
    headers.update({
      "Accept-Encoding": "br;q=1.0, gzip;q=0.8, deflate;q=0.5"
      })
  if "User-agent" not in headers:
    headers.update({'User-agent': UA})
  res = None
  data = None
  html = None
  #  await init_aiohttp_session()
  async with aiohttp.ClientSession() as session:
    try:
      res = await session.request(url=url, method=method, *args, **kwargs)
    except asyncio.TimeoutError as e:
      #  raise
      err(f"{e=} {url=}")
    except Exception as e:
      err(f"{e=} {url=}")
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
              err(f"文件过大，终止下载({length}): {url}")
            elif 'Transfer-Encoding' in res.headers and res.headers['Transfer-Encoding'] == "chunked":
              #  async for data in res.content.iter_chunked(HTTP_RES_MAX_BYTES):
              #    break
              data = b""
              async for tmp, _ in res.content.iter_chunks():
                data += tmp
                if len(data) > HTTP_FILE_MAX_BYTES:
                  break
                info(f"http downlod({length})... {len(tmp)} > {len(data)}")
            else:
              info(f"http downlod({length})...")
            # if res.headers['content-type'] == "text/plain; charset=utf-8":
              #  data = await res.read()
              data = await res.content.read(HTTP_FILE_MAX_BYTES)
      except ClientPayloadError as e:
        err(f"http connect error: {e=} {url=}")
      except Exception as e:
        err(f"http connect error: {e=} {url=}")

      if data:
        try:
          if "Content-Encoding" in res.headers:
            if res.headers['Content-Encoding'] == "gzip":
              logger.info("use gzip")
              data = gzip.decompress(data)
            elif res.headers['Content-Encoding'] == "deflate":
              logger.info("use zlib")
              data = zlib.decompress(data)
            elif res.headers['Content-Encoding'] == "br":
              logger.info("use br")
              data = brotli.decompress(data)
            elif res.headers['Content-Encoding']:
              err("url: {}\nunknown encoding: {}".format(url, res.headers['Content-Encoding']))
              #  return data
        except Exception as e:
          warn(f"解压时出现错误: {e=}")
        try:
          # if "text/plain" in res.headers['content-type']:
          if "text" in res.headers['content-type']:
            # return await res.text()
            html = data.decode(errors='ignore')
          else:
            #  html = data.decode()
            html = data
          info(f"http res: {html} url: {url}")
        except UnicodeDecodeError as e:
          warn(f"{e=} res data: {data[:64]} 64/{len(data)}")
          html = data
  if return_headers:
    if res:
      return html, res.headers
    else:
      return html, None
  else:
    return html

async def mt_send(*args, **kwargs):
  asyncio.create_task(_mt_send(*args, **kwargs))
  return True

#  async def mt_send(text="null", name="bot", gateway="test", qt=None):
async def _mt_send(text="null", gateway="gateway1", name="C bot", qt=None):

  # api.xmpp
  MT_API_RES = "127.0.0.1:4247"
  #  if gateway == 'me':
  #    # api.xmpp
  #    MT_API_RES = "127.0.0.1:4247"
  #  else:
  #    # api.cmdres
  #    MT_API_RES = "127.0.0.1:4249"
  # send msg to matterbridge
  url = "http://" + MT_API_RES + "/api/message"

  #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
  #  url="http://127.0.0.1:5555/api/message"

#  if not username.startswith("C "):
#    username = "T " + username

  if qt:
    name = "{}\n\n{}".format("> " + "\n> ".join(qt.splitlines()), name)
#  gateway="gateway0"
  data = {
    "text": "{}".format(text),
    "username": "{}".format(name),
    "gateway": "{}".format(gateway)
  }
  async with mt_send_lock:
    res = await http(url, method="POST", json=data)
  #  logger.info("res of mt_send: {}".format(res))
  return True
  return res

#  async def mt_send_for_long_text(text, gateway='test'):
#    fn='gpt_res'
#    async with queue_lock:
#      async with aiofiles.open(f"{SH_PATH}/{fn}", mode='w') as file:
#        await file.write(text)
#      #  os.system(f"{SH_PATH}/sm4gpt.sh {fn} {gateway}")
#      return await asyncio.to_thread(os.system, f"{SH_PATH}/sm4gpt.sh {fn} {gateway}")

async def mt_send_for_long_text(text, gateway="gateway1", name="C bot", *args, **kwargs):
  if not isinstance(text, str):
    text = "%s" % text
  info(f"send to mt: {gateway} {text}")
  async with mt_send_lock:
    need_delete = False
    if os.path.exists(f"{SH_PATH}"):
      fn = f"{SH_PATH}/SM_LOCK_{gateway}"
      for _ in range(5):
        if os.path.exists(fn):
          logger.info(f"busy: {gateway} {fn}")
          await asyncio.sleep(2)
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


async def tg_upload_media(path=None, src=None, chat_id=CHAT_ID, caption=None, in_memory=False, max_wait_time=download_media_time_max):
  if path is None:
    err(f"need file path: {path}")
    return
  if path.endswith(".mp4"):
    force_document = False
    supports_streaming = True
  else:
    force_document = True
    supports_streaming = False
  cb = None
  length = os.path.getsize(path)
  if length > 5000000:
    last_time = [time.time(), 0]
    def cb(sent, total):
      last_time[1] = sent
      if len(last_time) == 2:
        last_time.append(total)
        asyncio.create_task(send("开始上传: {:.1f}MB".format(total/1024/1024), src))
    async def update_tmp_msg():
      while True:
        await asyncio.sleep(interval)
        if len(last_time) == 2:
          await send("准备中", src, correct=True)
          if time.time() - last_time[0] > 15:
            await send("准备超时，可能网络过慢或者文件太小", src, correct=True)
            break
        else:
          current = last_time[1]
          total = last_time[2]
          if current == total:
            break
          await send("{:.1f}M".format((total-current)/1024/1024), src)
        if time.time() - last_time[0] > download_media_time_max:
          await send("超时", src, correct=True)
          break
    if src:
      t = asyncio.create_task(update_tmp_msg())
  h = await UB.upload_file(path, progress_callback=cb)
  try:
    res = await UB.send_file(chat_id, file=h, caption=caption, force_document=force_document, supports_streaming=supports_streaming)
  except Exception as e:
    res = await UB.send_file(chat_id, file=h, caption=caption, force_document=force_document)
  return res




#  last_time = {}

async def tg_download_media(msg, src=None, path=f"{DOWNLOAD_PATH}/", in_memory=False, max_wait_time=download_media_time_max):
#  await client.download_media(message, progress_callback=callback)
  #  async with downlaod_lock:
  if msg.file and msg.file.name:
    res = f"{msg.file.name}"
  else:
    res = ''
  if msg.buttons:
    logger.info(msg.buttons)
    for i in get_buttons(msg.buttons):
      if isinstance(i.button, KeyboardButtonUrl):
        logger.info(f"add url from: {i}")
        res += f" {i.url}"
      else:
        logger.info(f"ignore button: {i}")
  #  await mt_send(f"{res} 下载中...", gateway=gateway)
  #  res = f"{res} 下载中..."
  if src and res:
    await send(res, src, xmpp_only=True, correct=True)
  #  last_time[src] = time.time()
  last_time = [time.time(), 0]

  # Printing download progress
  def download_media_callback(current, total):
    #  last_time[0] = time.time()
    last_time[1] = current
    if len(last_time) == 2:
      last_time.append(total)
      asyncio.create_task(send("开始下载：{} {:.1f}MB".format(res, total/1024/1024), src))
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
      await asyncio.sleep(interval)
      now = time.time()-start_time
      #  if music_bot_state[src] != 3:
      #    await send("取消：{}".format(now, res), src, correct=True)
      #    break
      if len(last_time) == 2:
        #  if now > 60:
        #    await send(f"等待超时: {res}", src, xmpp_only=True, correct=True)
        #    break
        #  await send("准备中({:.0f}s)：{}".format(now, res), src, xmpp_only=True, correct=True)
        await send("准备中({:.0f}s)：{}".format(now, res), src, correct=True)
      else:
        current = last_time[1]
        total = last_time[2]
        if current == total:
          break
        #  await send("执行中({:.0f}s)：{} {:.2%} {:.2f}/{:.2f}MB {:.1f}MB/s".format(now, res, current / total, current/1024/1024, total/1024/1024, (current-last_current)/(time.time()-last_time[0])/1024/1024), src, xmpp_only=True, correct=True)
        #  await send("({:.0f}s)：{} {:.2%} {:.2f}/{:.2f}MB {:.1f}MB/s".format(now, res, current / total, current/1024/1024, total/1024/1024, (current-last_current)/(time.time()-last_time[0])/1024/1024), src, correct=True)
        await send("-{:.1f}M".format((total-current)/1024/1024), src)
        last_time[0] = time.time()
        #  last_current = current


  async def _download_media(msg, path):
    try:
      path = await asyncio.wait_for(msg.download_media(path, progress_callback=download_media_callback), timeout=max_wait_time)
    except TimeoutError as e:
      path = None
    return path


  file_path = None
  try:
    if src:
      t = asyncio.create_task(update_tmp_msg())
    t1 = asyncio.create_task(_download_media(msg, path))
    now = time.time()
    while True:
      await asyncio.sleep(interval+1)
      #  if src:
      #    if src not in music_bot_state or music_bot_state[src] < 3:
      #      info(f"下载中止：{res}")
      #      path = None
      #      res = f"下载取消: {res}"
      #      break
      if t1.done():
        file_path = t1.result()
        if path is None:
          res = f"下载失败(下载速度太慢): {res}"
        break
      if len(last_time) == 2:
        #  if time.time() - now > 60:
        if time.time() - now > max_wait_time:
          t1.cancel()
          path = None
          res = f"下载失败(等待超时): {res}"
          break
        else:
          info(f"等待上游下载完成：{res}")
  except Exception as e:
    err(f"下载失败 {e=}")
  finally:
    if file_path is None:
      err(f"下载失败 file_path is None")
    else:
      if not file_path.startswith("/"):
        file_path = path + file_path
      info(f"下载完成：{res} {file_path}")
    if not t1.done():
      t1.cancel()
      #  return
    if src:
      if not t.done():
        t.cancel()

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
      #  await send(f"{res}\n{path}", src)
      #  await send(f"{res}", src)
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
      await send(res, src)
    warn(res)

def get_buttons(bs):
  tmp = []
  for i in bs:
    if type(i) is list:
      tmp += i
    else:
      tmp.append(i)
  return tmp


def parse_tg_url(url, wtf=1):
  peer = None
  ids = None
  url.rstrip("?single")
  if "?comment=" in url:
    #需要先获取频道绑定的群，然后再在群里根据消息id找，麻烦，先不搞
    url = url.split("?comment")[0]
  if url.startswith("https://t.me/"):
    url = url[13:]
    if url.startswith("c/"):
      url = url[2:]
    if url:
      peer = url.split('/',1)[0]
      if '/' in url:
        ids = url.rsplit('/', 1)[-1]
    #    if url:
    #      peer = url.rsplit('/',1)[0]
    #      if '/' in url:
    #        ids = url.rsplit('/')[-1]
    #      #    ids = url.rsplit('/',1)[1]
    #      #    if '/' in ids:
    #      #      err(f"fixme: tg url 格式错误")
    #  elif url:
    #    peer = url.rsplit('/',1)[0]
    #    #  url = url.rsplit('/',1)[1]
    #    if '/' in url:
    #      ids = url.rsplit('/')[-1]
    #    #    ids = url.rsplit('/',1)[1]
    #    #    if '/' in ids:
    #    #      ids = ids.rsplit('/',1)[1]
  if peer:
    #  if peer[0] != "-":
    if peer.isnumeric():
      if wtf == 1:
        # channel or super group
        peer = f"-100{peer}"
        peer = int(peer)
      elif wtf == 2:
        peer = f"-{peer}"
        peer = int(peer)
  if ids:
    ids = int(ids)
  return peer, ids


async def get_entity(chat_id, id_only=True):
  #  if isinstance(peer, PeerUser):
  #    #  logger.info(f"PeerUser: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, PeerChat):
  #    #  logger.info(f"PeerChat: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, PeerChannel):
  #    #  logger.info(f"PeerChannel: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, str):
  #    peer = await UB.get_input_entity(peer)
  #  else:
  try:
    url = chat_id
    #  chat_id = get_addr(chat_id)
    if type(chat_id) is int:
      peer = await UB.get_input_entity(chat_id)
      if id_only:
        return peer
    elif type(chat_id) is str:
      peer, _ = parse_tg_url(url)
      if peer:
        pass
      elif url.startswith("@"):
        peer = url[1:]
      elif url.isnumeric():
        peer = int(url)
      elif url.startswith("-") and  url[1:].isnumeric():
        peer = int(url)
      else:
        peer = url
    else:
      return False
    if peer:
      entity = None
      info(f"search inputpeer: {peer}")
      try:
        peer = await UB.get_input_entity(peer)
        if id_only:
          return peer
      except TypeError as e:
        err(f"E: {e=}, not found input entity: {peer}")
        return
      except ValueError as e:
        info(f"search inputpeer(use get_peer_id): {peer}")
        try:
          peer = await UB.get_peer_id(peer)
          peer = await UB.get_input_entity(peer)
          if id_only:
            return peer
        except TypeError as e:
          err(f"E: {e=}, not found input entity(use get_peer_id): {peer}")
          return
        except ValueError as e:
          warn(f"not found input entity: {peer}")

      info(f"search peer: {peer}")
      try:
        entity = await UB.get_entity(peer)
      except TypeError as e:
        err(f"E: {e=}, not found entity: {peer}")
        return
      except ValueError as e:
        warn(f"not found entity: {peer}")
      return entity
  except Exception as e:
    err(f"E: {e=}")
    return
  raise ValueError(f"无法获取chat信息: {chat_id} {peer}")



async def print_tg_msg(event, to_xmpp=False):
  msg = event.message
  res = ''
  nick= "G None"
  if event.is_private:
    delay = None
    res += "@"
    #  peer = await get_entity(event.chat_id)
    peer = await event.get_chat()
    if peer is not None:
      res += " [%s %s]" % (peer.first_name, peer.last_name)
      nick = "G [%s %s]" % (peer.first_name, peer.last_name)
  else:
    if event.is_group:
      delay = 2
      res += "+"
    else:
      delay = 5
      #  if event.is_channel:
      res += "#"

    #  peer = await get_entity(event.chat_id)
    peer = await event.get_chat()
    if peer is not None:
      res += " %s" % peer.title
      nick = "G %s" % peer.title
    if event.from_id:
      #  peer = await get_entity(event.from_id)
      peer = await event.get_sender()
      if peer is not None:
        if isinstance(peer, User):
          res += " [%s %s]" % (peer.first_name, peer.last_name)
          nick = "G [%s %s]" % (peer.first_name, peer.last_name)
        else:
        #  if isinstance(peer, Channel):
          res += " %s" % peer.title
  #  res2 = None
  res1 = res
  if msg.text:
    #  if not event.is_private:
    #    res2 = f"{res}: {msg.text}"
    #  res += ": %s" % msg.text.splitlines()[0][:64]
    res = msg.text
  else:
    res = None
  if False and msg.file:
    path = await tg_download_media(msg)
    if path is not None:
      if res:
        res += "\n--\nfile: %s" % path
        #  text = f"{text} file: {path}"
      else:
        res = "file: %s" % path
        #  text = f"file: {path}"
        #  await send(text, jid=jid)
        #  return

    #  res += " %s" % msg.file
    #  if msg.file.name:
    #    res += " %s" % msg.file.name
    #    if res2:
    #      res2 += "\n%s" % msg.file.name
  #  if res2:
  #    #  await send(res2, jid=log_group, name="", nick=nick, delay=1)
  #    await send(res2, name="", nick=nick, delay=1)
  #  if not event.is_private:
  print(f"{res1}: {res[:64]}")
  #    return None, nick, delay
  return res, nick, delay



music_bot_state = {}


@exceptions_handler
async def parse_tg_msg(event):
  msg = event.message
  chat_id = event.chat_id
  
  #  if event.chat_id not in id2gateway:
  #    #  print("W: skip: got a unknown: chat_id: %s\nmsg: %s" % (event.chat_id, msg.stringify()))
  #    return
  #  if event.chat_id in id2gateway:
  #  if chat_id == gpt_bot:
  #    pass

  if chat_id == music_bot:
    #  print("I: music bot: chat_id: %s\nmsg: %s" % (event.chat_id, msg.stringify()))
    if msg.is_reply:
      pass
    else:
      return
    #  try:
    qid=msg.reply_to_msg_id
    if qid not in gid_src:
      logger.error(f"E: not found src for {qid=}, {gid_src=} {msg.text=}")
      return
    text = msg.text
    if not text:
      print(f"W: skip msg without text in chat with gpt bot, wtf: {msg.stringify()}")
      return
    
    if text == '搜索中...':
      #         message='搜索中...',
      logger.info(text)
      return

    if text == '正在获取歌曲信息...':
      #         message='正在获取歌曲信息...',
      logger.info(text)
      return

    src = gid_src[qid]

    if text == '等待下载中...':
      #   message='等待下载中...',
      #  logger.info(text)
      await send(text, src, correct=True)
      return
    if text.endswith('正在发送中...'):
      # message='大熊猫\n专辑: 火火兔儿歌\nflac 14.87MB\n命中缓存, 正在发送中...',
      #  logger.info(text)
      await send(text, src, correct=True)
      return
    if '中...' in text:
      #         message='搜索中...',
      #  warn(f"已忽略疑似临时消息: {text}", False)
      await send(text, src, correct=True)
      return

    mtmsgs = mtmsgsg[src]

    if music_bot_state[src] == 1:
      logger.info(msg.buttons)
      #  logger.info(f"找到了几个音乐:{len(msg.buttons)} {msg.text}")

      music_bot_state[src] += 1

      #  logger.info(f"{mtmsgs[qid]}搜索结果(回复序号)\n{text}")
      res = f"{mtmsgs[qid][0]}搜索结果(回复序号)\n{text}"
      #  await mt_send_for_long_text(res, src)
      await send(res, src)

      gid_src[msg.id] = src

      mtmsgs[qid].append(msg.buttons)
      mtmsgs[msg.id] = mtmsgs[qid]

      gid_src.pop(qid)
      mtmsgs.pop(qid)

    elif music_bot_state[src] == 2:
      warn(f"不应该出现: music bot: {gid_src=} {music_bot_state[src]}\nmsg:\n{msg.stringify()}")
      gid_src.pop(qid)
      mtmsgs.pop(qid)
      return
    elif music_bot_state[src] == 3:
      if '发送失败' in text:
        await send(text, src)
        music_bot_state[src] = 2
      elif msg.file:
        info(f"download... {text}")
        path = await tg_download_media(msg, src)
        if path is not None:
          await send("下载完成，正在上传到xmpp...", src, correct=True)
          url = await upload(path)
          t = asyncio.create_task(backup(path))
          await t
          url2 = None
          if t.done():
            url2 = t.result()
          if url and url2:
            res = f"{mtmsgs[qid][0]}{url}\n\n{url2}\n\n{text}"
            #  res = f"{url}\n\n{res}"
          else:
            if url:
              res = f"{mtmsgs[qid][0]}{url}\n{text}"
            else:
              res = f"{mtmsgs[qid][0]}{url2}\n{text}"

          if msg.buttons:
            for i in get_buttons(msg.buttons):
              #  if isinstance(i, KeyboardButtonUrl):
              if isinstance(i.button, KeyboardButtonUrl):
                res += f"\n原始链接: {i.url}"
          #  await mt_send_for_long_text(res, gateway)
          await send(res, src)
        if src in music_bot_state and music_bot_state[src] == 3:
          music_bot_state[src] = 2
      else:
        await send(text, src, correct=True)
        music_bot_state[src] = 2
    else:
      warn(f"未知状态，已忽略: music bot: {gid_src=} {music_bot_state[src]}\nmsg:\n{msg.stringify()}")
      return


    #  except Exception as e:
    #    err(f"fixme: music bot: {gid_src=} {e=} line: {e.__traceback__.tb_lineno}")

    return

  #  elif event.chat_id == rss_bot:
  #    async with rss_lock:
  #      #  await mt_send(msg.text, "C rss2tg_bot", id2gateway[rss_bot])
  #      #  await mt_send_for_long_text(msg.text, id2gateway[rss_bot])
  #      await send(msg.text, rss_group, name="")
  #      await asyncio.sleep(5)
  #    return
  #  elif event.chat_id in bridges:
  #    await send(msg.text, bridges[event.chat_id], name="")
  #    await asyncio.sleep(5)
  #    return
    #  print("N: skip: %s != %s" % (event.chat_id, gpt_bot))
  else:
    #  print("W: skip unknown chat_id: %s %s" % (event.chat_id, msg.text[:64]))
    if chat_id in bridges:
      target = bridges[chat_id]
      if type(target) is dict:
        gid = msg.id
        jid = None
        #  res, nick, delay = await print_tg_msg(event)
        #  if gid-1 in target or gid > mid_max:
        if len(target) == 0:
          return
        #  elif len(target) == 1:
        else:
          for mid, jid in target.items():
            break
        #  else:
        #    mid_min = min(target.keys())
        #    if msg.edit_date is None:
        #      mid_max = max(target.keys())
        #      if gid-1 > mid_max:
        #        target.pop(mid_min)
        #        mid_max = max(target.keys())
        #    jid = target[gid_min]
        #    mid = gid_min
          #  if msg.edit_date is None:
          #    target[gid] = target[gid-1]
          #    target.pop(gid-1)
          #  await send(msg.text, jid=target[gid-1], name=f"**{nick}:** ", nick=nick, correct=True)

        if jid is not None:
          text = msg.text
          if jid not in mtmsgsg:
            warn(f"{jid} not in {mtmsgsg}")
            return
          mtmsgs = mtmsgsg[jid]
          if mid not in mtmsgs:
            warn(f"{mid} not in {mtmsgs}")
            return
          l = mtmsgs[mid]
          text = f"{l[0]}{text}"
          now = msg.date.timestamp()

          if msg.file:
            path = await tg_download_media(msg)
            if path is not None:
              if text:
                text = f"{text} file: {path}"
              else:
                text = f"file: {path}"
                await send(text, jid=jid)
                return

          #  if msg.edit_date is None:
          if len(l) == 1:
            #  if type(l[0]) is str:
            #  l[0] = now
            l.append(now)
            l.append(gid)
            await send(text, jid=jid, correct=True)
          elif jid in bot_groups:
            l[1] = now
            l.append(gid)
            await send(text, jid=jid, correct=True)
          else:
            if now > l[1]:
              l[1] = now
              l.append(gid)
            await asyncio.sleep(5)
            if mid in mtmsgsg[jid] and now == l[1]:
              await send(text, jid=jid)
            else:
              info(f"忽略旧的临时消息: {text[:64]}")
        else:
          info(f"skip msg: {gid} {target} {msg.stringify()}")

      else:
        #  if msg.text:
        res, nick, delay = await print_tg_msg(event)
        #  logger.info(f"转发桥接消息: {chat_id} -> {bridges[chat_id]}: {msg.text[:64]}")
        if res:
          logger.info(f"转发桥接消息: {chat_id} -> {bridges[chat_id]}: {res[:16]}")
          #  await send(msg.text, jid=target, name=f"**{nick}:** ", nick=nick, delay=delay)
          await send(res, jid=target, name=f"**{nick}:** ", nick=nick, delay=delay)

      #  elif event.is_private:
      #    pass
    #  else:
    #    res, nick, delay = await print_tg_msg(event)
    #    if res:
    #      #  await send(res, jid=log_group, name="", nick=nick, delay=delay)
    #      await send(res, jid=log_group, name="", delay=delay)

    return

  #  if msg.is_reply:
  #    qid=msg.reply_to_msg_id
  #    print(f"tg msg id: {msg.id=} {event.id=} {qid=}")
  #    if qid not in gid_src:
  #      logger.error(f"E: not found src for {qid=}, {gid_src=} {msg.text=}")
  #      return
  #    #  await queues[gid_src[qid]].put( (id(msg), qid, msg) )
  #    #  await queues[gid_src[qid]].put( (msg.date, qid, msg) )
  #    #  await queues[gid_src[qid]].put( (msg.id, "test") )
  #    #  await queues[gid_src[qid]].put( (id(msg), qid, msg) )
  #    if msg.file:
  #      return
  #    text = msg.text
  #    if not text:
  #      print(f"W: skip msg without text in chat with gpt bot, wtf: {msg.stringify()}")
  #      return
  #    print(f"tg msg: {text}: {msg.id=} {event.id=} {qid=} {gid_src=} {mtmsgsg=}")
  #    l = text.splitlines()
  #    if l[-1] in loadings:
  #      return
  #    elif len(l) > 1 and f"{l[-2]}\n{l[-1]}" in loadings:
  #      return
  #    else:
  #      src = gid_src[qid]
  #      mtmsgs = mtmsgsg[src]
  #      res = f"{mtmsgs[qid][0]}{text}"
  #      #  await mt_send_for_long_text(res, src)
  #      await send(res, src)
  #      gid_src.pop(qid)
  #      mtmsgs.pop(qid)
  #
  #    #  except Exception as e:
  #    #    err(f"fixme: {qid=} {gid_src=} {queues=} {e=} line: {e.__traceback__.tb_lineno}")
  #      #  raise e
  #    return
  #    await queues[gid_src[qid]].put( (msg.id, msg, qid) )
  #    return
  #
  #  else:
  #    print("W: skip: got a msg without reply: is_reply: %s\nmsg: %s" % (msg.is_reply, msg.stringify()))
  #    return


@exceptions_handler
async def parse_tg_out_msg(event):
  #  info(event.stringify())
  msg = event.message
  text = msg.text
  chat_id = event.chat_id
  info(f"tg out msg: {chat_id}: {text}")
  if text.startswith("$"):
    if text == "$get id":
      #  await UB.send_message('me', f"{event.chat_id}")
      sendme(f"{event.chat_id}")
    elif text == "$get event":
      sendme(f"{event.stringify()}")
    elif text == "$get msg":
      sendme(f"{msg.stringify()}")
    elif text == "$get chat":
      e = await event.get_chat()
      sendme(f"{e.stringify()}")
    elif text == "$get reply":
      if event.is_reply:
        sendme(event.reply_to.stringify())
        e = await msg.get_reply_message()
        sendme(f"{e.stringify()}")
      else:
        sendme(f"not a reply: {msg.stringify()}")
    elif text == "$get sender":
      if event.is_reply:
        e = await msg.get_reply_message()
        e = await e.get_sender()
        sendme(f"{e.stringify()}")
      else:
        sendme(f"not a reply: {msg.stringify()}")
    return

  if chat_id == MY_ID or chat_id == CHAT_ID:
    if chat_id == CHAT_ID:
      if event.fwd_from:
        sendme(event.fwd_from.stringify())
        return
      #  elif event.is_reply:
      #    sendme(event.reply_to.stringify())
      #    return
    if not text:
      return
    #  res = await run_cmd(text, CHAT_ID, "G me")
    res = await run_cmd(text, log_group_private, f"G {MY_NAME}: ", is_admin=True)
    if res is True:
      return
    if res:
      #  await UB.send_message(CHAT_ID, res)
      await _sendme(res, chat_id)
      return

    if text == 'id':
      #  await UB.send_message('me', f"id @name https://t.me/name\nchat_id: {chat_id}")
      await UB.send_message(chat_id, f"id @name https://t.me/name\nchat_id: {chat_id}")
      return
    if text.startswith("id "):
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

      url = text.split(' ')[1]
      e = await get_entity(url, False)
      if e:
        await UB.send_message(chat_id, f"{e.stringify()}")
        await UB.send_message(chat_id, "peer id: %s" % await UB.get_peer_id(e))
      else:
        await UB.send_message(chat_id, "not fount entity")
    elif text.startswith("msg "):
      cmds = get_cmd(text)
      url = cmds[1]
      if url:
        if url == "h":
          await _sendme("msg url raw/fast/xmpp/direct/vps", chat_id)
          return
        opts = 0
        if len(cmds) == 3:
          if cmds[2] == "fast":
            opts = 1
          elif cmds[2] == "direct":
            opts = 2
          elif cmds[2] == "xmpp":
            opts = 3
          elif cmds[2] == "vps":
            opts = 4
        peer = await get_entity(url)
        if peer:
          #  await _sendme(peer.stringify(), chat_id)
          ss = url.split('/')
          if len(ss) > 4:
            ids = int(ss[-1])
            tmsg = await UB.get_messages(peer, ids=ids)
            if tmsg:
              if cmds[-1] == "raw":
                await _sendme(tmsg.stringify(), chat_id)
              elif tmsg.file:
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
                info(f"file type: {type(file)}")

                res = None
                #  if tmsg.text:
                # https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.uploads.UploadMethods.send_file
                # https://docs.telethon.dev/en/stable/modules/utils.html#telethon.utils.pack_bot_file_id
                try:
                  res = await UB.send_file(chat_id, file=file, caption=tmsg.text)
                  if opts == 1:
                    return
                except rpcerrorlist.ChatForwardsRestrictedError as e:
                  info(f"fixme: {e=}")
                  try:
                    file = utils.pack_bot_file_id(file)
                  except AttributeError as e:
                    err(f"fixme: {e=} {type(file)}")
                    try:
                      # AttributeError("'PhotoSize' object has no attribute 'location'")
                      file = utils.pack_bot_file_id(tmsg.file)
                      if file is None:
                        file = utils.pack_bot_file_id(tmsg.photo)
                      if file is None:
                        file = utils.pack_bot_file_id(tmsg.document)
                      if file is None:
                        file = utils.pack_bot_file_id(tmsg.media)
                      if file is None:
                        err(f"wtf: {tmsg.stringify()}")
                        return
                      res = await UB.send_file(chat_id, file=file, caption=tmsg.text)
                      if opts == 1:
                        return
                    except AttributeError as e:
                      err(f"fixme: {e=}")
                  except Exception as e:
                    err(f"fixme: {e=}")
                    
                src = log_group_private
                path = await tg_download_media(tmsg, src=log_group_private, max_wait_time=600)
                if path:

                  if opts == 2 or res is None:
                    try:
                      res = await tg_upload_media(path, src, chat_id=chat_id, caption=cmds[1])
                      if opts == 2:
                        return
                    except Exception as e:
                      err(f"上传失败 {e=}")
                  else:
                    await _sendme(cmds[1], chat_id)

                  url = None
                  if opts < 4:
                    await send("下载完成，正在上传到xmpp...", src, correct=True)
                    try:
                      url = await upload(path)
                      info(url)
                    except Exception as e:
                      err(f"上传失败 {e=}")
                  try:
                    if url:
                      res = await UB.send_file(chat_id, file=url, caption=url)
                      if opts == 3:
                        return
                  except rpcerrorlist.WebpageCurlFailedError as e:
                    err(f"文件url有问题: {e=} {url}")
                  except rpcerrorlist.WebpageMediaEmptyError as e:
                    err(f"文件url有问题: {e=} {url}")
                  except Exception as e:
                    err(f"{e=} {url}")

                  t = asyncio.create_task(backup(path))
                  try:
                    await t
                    if t.done():
                      url = t.result()
                      if url:
                       info(url)
                       await asyncio.sleep(2)
                       res = await UB.send_file(chat_id, file=url, caption=url)
                  except rpcerrorlist.WebpageCurlFailedError as e:
                    err(f"文件url有问题: {e=} {url}")
                  except rpcerrorlist.WebpageMediaEmptyError as e:
                    err(f"文件url有问题: {e=} {url}")
                  except Exception as e:
                    err(f"{e=} {url}")

              elif tmsg.text:
                res = await UB.send_message(chat_id, tmsg.text)
              else:
                await _sendme(tmsg.stringify(), chat_id)
            else:
              await _sendme(f"error id: {ids}\nres: {msg}", chat_id)
          return
        else:
          await _sendme(f"error url: {url}\nres: {peer}", chat_id)
          return
      await _sendme("error", chat_id)



#  @UB.on(events.NewMessage(incoming=True))
#  @UB.on(events.MessageEdited(incoming=True))
#  @exceptions_handler
#  async def read_res(event):
#
#    if not allright.is_set():
#      return
#    #  if event.chat_id in id2gateway:
#    if event.chat_id == gpt_bot:
#      pass
#    elif event.chat_id == rss_bot:
#      msg = event.message
#      await mt_send(msg.text, id2gateway[rss_bot], "rss2tg_bot")
#      return
#      #  print("N: skip: %s != %s" % (event.chat_id, gpt_bot))
#    else:
#      return
#    #  if not allright.is_set():
#    #    print("W: skiped the msg because of reset is waiting")
#    #    return
#    #  elif event.chat_id not in gid_src:
#    #    logger.error(f"E: not found gateway for {event.chat_id}, {gid_src=}")
#    #    return
#    msg = event.message
#
#    if msg.is_reply:
#      qid=msg.reply_to_msg_id
#      print(f"msg id: {msg.id=} {event.id=} {qid=} {gid_src=} {mtmsgsg=}")
#      if qid not in gid_src:
#        logger.error(f"E: not found gateway for {qid=}, {gid_src=} {msg.text=}")
#        return
#      try:
#        #  await queues[gid_src[qid]].put( (id(msg), qid, msg) )
#        #  await queues[gid_src[qid]].put( (msg.date, qid, msg) )
#        await queues[gid_src[qid]].put( (id(msg), qid, msg) )
#        #  await queues[gid_src[qid]].put( (msg.id, "test") )
#      except Exception as e:
#        logger.info(f"E: fixme: {qid=} {gid_src=} {queues=} {e=}")
#        #  raise e
#      return
#      await queues[gid_src[qid]].put( (msg.id, msg, qid) )
#      return



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
    if 'XB' in globals():
      client = XB
    else:
      return
  jid = get_jid(client.local_jid)
  if client.running:
    logger.info(f"开始断开账户: {jid}")
    client.stop()
    while True:
      if client.running:
        logger.info(f"等待断开账户: {jid}")
        await asyncio.sleep(0.5)
      else:
        logger.info(f"已断开: {jid}")
        break
  else:
    logger.info(f"已离线: {jid}")



async def disco_info(jid, node=None, client=None):
  if client is None:
    client = XB
  if jid is None:
    jid = XB.local_jid
  elif isinstance(jid, JID):
    pass
  else:
    jid = JID.fromstr(jid)
  #  for i in my_groups:
  #    jid = i
  #    break
  #  jid = test_group.rsplit('@', 1)[1]
  dc = client.summon(aioxmpp.DiscoClient)
  #  res = await dc.query_info(JID.fromstr(jid))
  try:
    res = await dc.query_info(jid, node=node, timeout=5)
    #  pprint(res)
    #  print(jid, res.to_dict())
    return res
  except TimeoutError as e:
    warn(f"失败(超时)：{jid}, {e=}")
    #  res = "失败(超时)"

async def disco_item(jid=None, node=None, client=None):
  if client is None:
    client = XB
  if jid is None:
    jid = JID.fromstr(XB.local_jid.domain)
  elif isinstance(jid, JID):
    pass
  else:
    jid = JID.fromstr(jid)
  #  for i in my_groups:
  #    jid = i
  #    break
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


async def get_server_name(jid):
  await asyncio.sleep(0.5)
  res = await disco_info(jid)
  if res:
    if res.identities:
      return res.identities[0]



async def upload(file_path=f"{HOME}/t/1.jpg", src=None):
  if UPLOAD is None:
    err(f"服务器不支持文件上传: {myjid}")
    return False

  if type(file_path) is str:
    fp = Path(file_path)
    #  file_path = Path(file_path)
  else:
    fp = file_path
  if not fp.is_file():
    err(f"仅支持文件: {file_path}")
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
  print(XB,UPLOAD, filename, os.path.getsize(fp), mimetypes.guess_type(fp)[0], file_path)
  slot = await aioxmpp.httpupload.request_slot(XB,UPLOAD, filename, length, mimetypes.guess_type(fp)[0])
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

  chunk_size = 512 * 1024
  if length / chunk_size > 2:
  #  if False:
    #  async with aiofiles.open(fp, "rb") as file:
    #    data = await file.read()
    #  res = await http(slot.put.url, method="PUT", headers=headers, data=data, chunked=chunk_size)
    #  info(f"res: {res}\nslot: {slot}")
    #  return slot.get.url
    #  headers['Transfer-Encoding'] = 'chunked'
    last_time = [time.time(), 0]
    total = length
    async def update_tmp_msg():
      while True:
        await asyncio.sleep(interval/2)
        if len(last_time) == 2:
          await send("准备中", src, correct=True)
          if time.time() - last_time[0] > 15:
            await send("准备超时，可能网络过慢或者文件太小", src, correct=True)
            break
        else:
          current = last_time[1]
          total = last_time[2]
          if current == total:
            break
          await send("{:.1f}M".format((total-current)/1024/1024), src)
        if time.time() - last_time[0] > download_media_time_max:
          await send("超时", src, correct=True)
          break
    if src:
      t = asyncio.create_task(update_tmp_msg())
    try:
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
      #  def d(func):
      #    @wraps(func)
      #    async def wrapper(*args, **kwargs):
      #      data = await func(*args, **kwargs)
      #      print(f"read: {len(data)}")
      #      return data
      #    return wrapper

      class MyFiles:
        def __init__(self, file_obj):
          self._file = file_obj

        async def read(self, *args, **kwargs):
          data = await self._file.read(*args, **kwargs)
          print(f"read: {len(data)}")
          return data

      headers["Content-Length"] = str(length)
      async with aiofiles.open(fp, "rb") as file:
        file = MyFiles(file)
        #  file.read = d(file.read)
        res = await http(slot.put.url, method="PUT", headers=headers, data=file)
        info(f"res: {res}\nslot: {slot}")

    except Exception as e:
      err(f"分块上传失败：{e=} {slot.put.url=}")
      return
    finally:
      if src:
        if not t.done():
          t.cancel()
  else:
    # 流式上传需要手动设置Length
    headers["Content-Length"] = str(length)
    info("headers: %s" % headers)
    try:
      async with aiofiles.open(fp, "rb") as file:
        res = await http(slot.put.url, method="PUT", headers=headers, data=file)
        info(f"res: {res}\nslot: {slot}")
    except Exception as e:
      err(f"上传失败：{e=} {slot.put.url=}")
      return
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
#    logger.info("\n>> group msg: %s\n" % msg)

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
      xmpp_msg_in,
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
      xmpp_msgp_in,
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

  from aioxmpp.version.xso import Query

  async def _(iq):
      print("software version request from {!r}".format(iq.from_))
      result = Query()
      result.name = "xmppbot"
      result.version = f"xmpp:{main_group}?join"
      result.os = f"by {ME}"
      return result

  client.stream.register_iq_request_handler(
      aioxmpp.IQType.GET,
      Query,
      _,
  )

  #  pprint(client.stream)
  #  pprint(client.stream.service_outbound_message_filter)
  #  return
  #  client.stream.service_outbound_messages_filter = stream.AppFilter()
  #  client.stream.service_outbound_message_filter.register(msg_out, 1)
  #  client.stream.app_outbound_message_filter.register(msg_out, 1)



async def send_typing(muc):
  if muc == "gateway1":
    return True
  if muc in my_groups:
    type_=MessageType.GROUPCHAT
  else:
    type_=MessageType.CHAT

  msg = aioxmpp.Message(
      to=JID.fromstr(muc),
      type_=type_,
  )
  msg.xep0085_chatstate = chatstates.ChatState.COMPOSING
  #  info(f"{msg.body=}") # ={}
  await _send(msg)


last_outmsg = {}

def get_msg_jid(msg):
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
    logger.info(f"已清除msg记录: {j}")
  else:
    logger.info(f"没找到msg记录: {j}")


def add_id_to_msg(msg, correct):
  j = get_msg_jid(msg)
  if j in last_outmsg:
    r = misc.Replace()
    r.id_ = last_outmsg[j][1]
    msg.xep0308_replace = r
    if not correct:
      last_outmsg.pop(j)
  if correct:
    msg.autoset_id()
    last_outmsg[j] = [msg, msg.id_]


async def ___add_id_to_msg(msg, correct):
  j = get_msg_jid(msg)
  if correct:
    if j in last_outmsg:
      #  msg.xep0308_replace = misc.Replace(last_outmsg[get_jid(msg.to, True)])
      for _ in range(5):
        if last_outmsg[j][1]:
          last_outmsg[j][0] = msg
          r = misc.Replace()
          r.id_ = last_outmsg[j][1]
          msg.xep0308_replace = r
          break
        else:
          logger.info("msg id 不可用: {last_outmsg[j][1]}")
          await asyncio.sleep(1)
      if last_outmsg[j][1] is None:
        last_outmsg[j] = [msg, None]
    else:
      last_outmsg[j] = [msg, None]
      logger.info("已添加msg")
  else:
      #  last_outmsg.pop(j)
    if j in last_outmsg:
      #  msg.xep0308_replace = misc.Replace(last_outmsg[get_jid(msg.to, True)])
      for _ in range(5):
        if last_outmsg[j][1]:
          last_outmsg[j][0] = msg
          r = misc.Replace()
          r.id_ = last_outmsg[j][1]
          msg.xep0308_replace = r
        else:
          logger.info("msg id 不可用: {last_outmsg[j][1]}")
          await asyncio.sleep(1)
      if last_outmsg[j][1] is None:
        last_outmsg[j] = [msg, None]
      last_outmsg[j].append(0)

def get_mucs(muc):
  if muc == "gateway1":
    muc = main_group
  elif muc not in my_groups:
    return
  for s in sync_groups_all:
    if muc in s:
      tmp = set()
      for m in s:
        if m not in rooms:
          tmp.add(m)
      return s - tmp
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

@exceptions_handler
def msg_out(msg):
  if not allright.is_set():
    #  logger.info("skip msg: allright is not ok: {msg.from_}: {msg.body}")
    return
  #  pprint(msg)
  j = get_msg_jid(msg)
  if j in last_outmsg:
    if last_outmsg[j][0] == msg:
      if len(last_outmsg[j]) > 2 and last_outmsg[j][2] < 1:
        logger.info(f"停止记录msg id: {msg.id_}")
        last_outmsg.pop(j)
      else:

        logger.info(f"更新msgid: {last_outmsg[j][1]} -> {msg.id_}")
        last_outmsg[j][1] = msg.id_
    else:
      logger.info(f"msg不匹配: {last_outmsg[j][0]=} != {msg=}")
      last_outmsg.pop(j)
  else:
    logger.debug(f"忽略: {msg=}")
  return msg



#  @exceptions_handler
def xmpp_msgp_in(msg):
  # 状态消息，在线离线等
  if not allright.is_set():
    return
  asyncio.create_task(xmpp_msgp(msg))

@exceptions_handler
async def xmpp_msgp(msg):
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
          res = f"上线{len(msg.xep0045_muc_user.items)}: {msg.from_} {jid} {item.nick} {item.role} {item.affiliation} {msg.status}"
          print(res)
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
            #    #  logger.info(f"不记录bot: {jid}")
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
                  await send(res, muc, nick=nick)
                res = f"改名通知: {j[0]} -> {rnick}"
                j[0] = rnick
                await send(f"{res}\njid: {jid}\nmuc: {muc}", nick=nick)
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
              await send(welcome, muc, nick=nick)

            #  await send(f"有新人入群: {j[0]}\n身份: {j[1]}\n角色: {j[2]}\njid: {jid}\nmuc: {muc}", nick=nick)
            await send(f"有新人入群: {j[0]}\n身份: {j[1]}\n角色: {item.role}\njid: {jid}\nmuc: {muc}", nick=nick)

          set_default_value(j)
          #  if len(jids[jid]) > 3:
          #    jids[jid][3] = int(time.time())
          #  else:
          #    jids[jid].append(int(time.time()))
          break
      else:
        pprint(msg)
        await send(f"未知群组消息: {msg}")
    else:
      print(f"上线: {msg.from_} {msg.status}")
      #  if muc != rssbot:
      #    await send(f"上线: {msg.from_} {msg.status}")
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
      await send("ok", msg.from_)
      log(f"已同意状态订阅请求：{msg.from_} {res}")
      res = rc.subscribe(msg.from_)
    else:
      # https://docs.zombofant.net/aioxmpp/devel/api/public/roster.html#aioxmpp.RosterClient.remove_entry
      await send(f"非管理禁止订阅，但可以私聊。暂时只支持ping命令，别的私聊消息会转发给管理。不要开启加密，bot暂时不支持。管理的xmpp账号: xmpp:{ME} 群: xmpp:{main_group}?join", msg.from_)
      try:
        res = await rc.remove_entry(msg.from_, timeout=5)
      except errors.XMPPModifyError as e:
        res = "err"
        if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}item-not-found":
          info("多余的联系人删除，此段代码可以删掉")
        else:
          warn(f"未知错误，待修复的联系人删除: {msg.from_} {e=}")
      log(f"已拒绝状态订阅请求：{msg.from_} {res=}")
  elif msg.type_ == PresenceType.UNAVAILABLE:
    print(f"离线: {msg.from_} {msg.status}")
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
    print(f"未知状态{msg.type_}: {msg.from_} {msg.status}")
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




#  def gmsg(msg, member, source, **kwargs):
#  @exceptions_handler
def xmpp_msg_in(msg):
  if not allright.is_set():
    #  logger.info("skip msg: allright is not ok")
    return
  #  if hasattr(msg, "xep0203_delay"):
  #    pprint(msg.xep0203_delay)
  #    logger.info("skip msg: delayed: {msg.xep0203_delay}")
  #  if hasattr(msg, "xep308_replace"):
  #    pprint(msg.xep308_replace)
  asyncio.create_task(xmpp_msg(msg))
  #  return
  #  logger.info("\n>>> msg: %s\n" % msg)

@exceptions_handler
async def xmpp_msg(msg):
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
    #  await asyncio.sleep(1)
    real_time = delay.stamp.timestamp()
    if time.time() - real_time > 60:
      print("跳过旧消息: %s %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body, delay))
      return
    else:
      print("旧消息: %s %s %s %s %s 延迟%ss" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body, time.time() - delay.stamp.timestamp()))
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
  #  if text is None:
  #    #  print("跳过空消息: %s %s %s %s" % (msg.type_, msg.from_, msg.to, msg.body))
  #    return

  #  if text == "ping":
  #    #  await send("pong", ME)
  #    if msg.type_ == MessageType.GROUPCHAT:
  #
  #      nick = msg.from_.resource
  #      ms = get_mucs(muc)
  #      for m in ms - {muc}:
  #        if await send1(f"**X {nick}:** {text}", m) is False:
  #          return
  #      if main_group in ms:
  #        if await mt_send(text, name=f"X {nick}") is False:
  #          return
  #
  #      #  pprint(msg.from_)
  #      #  await sendg("pong1")
  #      #  await sendg("pong2", get_jid(msg.from_))
  #      await send("pong", msg.from_, gpm=True)
  #      reply = msg.make_reply()
  #      reply.body[None] = "pong"
  #      await send(reply)
  #      #  await mt_send("pong")
  #    elif msg.type_ == MessageType.CHAT:
  #
  #      reply = msg.make_reply()
  #      reply.body[None] = "pong"
  #      await send(reply)
  #    return
  is_admin = False
  if muc in my_groups:

    #  if muc not in rooms:
    #    if muc != log_group_private:
    #      err(f"not found room: {muc}")
    #    else:
    #      logger.error(f"not found room: {muc}", exc_info=True, stack_info=True)
    #      await send(f"not found room: {muc}", jid=ME)
    #    return
    room = rooms[muc]
    #  if str(msg.from_) == str(rooms[muc].me.conversation_jid.bare()):
    #  if msg.from_.resource == rooms[muc].me.nick:
    if room.me is not None and nick == room.me.nick:
      print("跳过自己发送的消息1: %s %s %s" % (msg.from_, msg.to, text[:16]))
      return

    jids = users[muc]
    j = jids[myjid]
    if nick == j[0]:
      print("跳过自己发送的消息2: %s %s %s" % (msg.from_, msg.to, text[:16]))
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
            print("跳过自己发送的消息3: %s %s %s" % (msg.from_, msg.to, text[:16]))
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
            logger.info(f"admin msg: {text[:16]}")
          break

      if not existed:
        if rejoin is False:
          await room.leave()
          rejoin = True
          rooms.pop(muc)
          send_log("检测到幽灵发言%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
          if await join(muc):
            room = rooms[muc]
            continue
        else:
          send_log("忽略幽灵发言%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
          return
      break


    #  if msg.type_ == MessageType.CHAT:


    if is_admin is False:
      logger.info(f"group msg: {text[:16]}")

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
          info(f"fixme: 跳过已禁言用户的消息{int(j[2]-real_time)}: {muc} {nick} {text[:64]}")
        else:
          info(f"跳过已禁言用户的消息{int(j[2]-real_time)}: {muc} {nick} {text[:64]}")
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
        #    await send(f"now: {w[0]} / {wtf_limit}", jid=muc)
        if w[1] > 1 and w[0] > wtf_limit/(9/(w[1]+8) +0.1):
          j[2] = int(time.time() + wtf_ban_time)
          role = "visitor"
          reason = "不要刷屏"
          res = await room.muc_set_role(nick, role, reason=reason)
          warn(f"有人刷屏: {nick}\njid: {jid}\nmuc: {muc}\nnow: {w[0]}/{wtf_limit}/{w[1]}\n{res}")
          await send(f"检测到刷屏，禁言{wtf_ban_time}s: {nick} {w[0]}/{wtf_limit}", jid=muc)
        elif need_warn:
          if w[1] == 1 and w[0] > wtf_limit/2:
            await send(f"{nick}, 不要刷屏 {w[0]}/{wtf_limit}", jid=muc)
            w[0] = wtf_limit/2
          elif w[0] > wtf_limit/2:
            await send(f"{nick}, 不要刷屏（第一次警告） {w[0]}/{wtf_limit}", jid=muc)
        

  elif muc == myjid:
    #  print("跳过自己发送的消息%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
    return
  elif muc in me:
    is_admin = True
    logger.info(f"admin pm msg: {text[:16]}")
    nick = msg.from_.localpart
  elif muc == rssbot:
    #  if msg.type_ == None:
    await send(text, acg_group, name="", delay=5)
    return
  else:
    print("未知来源的消息%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
    if text == "ping":
      reply = msg.make_reply()
      reply.body[None] = "pong"
      await send(reply)
      return
    if msg.type_ == MessageType.ERROR:
      sendme("未知来源的消息(wtf) %s %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), f"{msg.from_=}", msg.to, msg.body))
      return
    await send(f"暂时只支持ping命令，别的私聊消息会转发给管理。不要开启加密，bot暂时不支持。管理的xmpp账号: xmpp:{ME} 群: xmpp:{main_group}?join", msg.from_)
    #  chat = await get_entity(CHAT_ID, True)
    #  await UB.send_message(chat, f"{msg.type_} {msg.from_}: {text}")
    #  await sendme(f"{msg.type_} {msg.from_}: {text}")
    send_log(f"{msg.type_} {msg.from_}: {text}")
    return
    #  pprint(msg)

  print("%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))





  j = get_msg_jid(msg)
  if j in last_outmsg:
    last_outmsg.pop(j)

  text0 = text
  if msg.type_ == MessageType.GROUPCHAT:
    if muc == acg_group:
      if is_admin:
        await send(text, rssbot, name="")
      else:
        await send("仅管理可用", src)
      return

    #  if nick == "bot":
    #    #  if muc not in check_bot_groups:
    #    #  if muc != "ipfs@salas.suchat.org":
    #    #  if muc != "wtfipfs@muc.pimux.de":
    #    #    return
    #    #  if send_by_me(text):
    #    #    return
    #    #  username=""
    #    username=f"**C bot:** "
    #    name=f"C bot"
    #    qt=None
    #  else:
    username=f"**X {nick}:** "
    name=f"X {nick}"
    qt = None
    #  if text.startswith('> ') or text.startswith('>> '):
    if text.startswith('>'):
      qt=[]
      tmp= text.splitlines()
      exqt = False
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
          qt.append(i)
        else:
          break
      if len(tmp) != len(qt):
        tmp = tmp[len(qt):]
        text0='\n'.join(tmp)
        tmp = qt
        qt='\n'.join(qt)
        text = f"{text0}\n\n{qt}"
        qt2 = '\n> '.join(tmp)
        username = f"> {qt2}\n{username}"
    #    else:
    #      info(f"{tmp=} {qt=}")
    #  info(f"{text=} {text2=}")
    ms = get_mucs(muc)
    for m in ms - {muc}:
      #  if await send1(f"**X {nick}:** {text}", m, name=f"X {nick}") is False:
      if await send1(f"{username}{text0}", m, name=name) is False:
        return
    if main_group in ms:
      #  if await mt_send_for_long_text(text, name=f"X {nick}") is False:
      if await mt_send_for_long_text(text0, name=name, qt=qt) is False:
        return
    #  text = text2
  #  if msg.type_ == MessageType.GROUPCHAT:
  #    pass
  elif msg.type_ == MessageType.NORMAL:
    warn(f"normal msg: {msg}")
    return
  elif msg.type_ == MessageType.CHAT:
    if text == "ping":
      reply = msg.make_reply()
      reply.body[None] = "pong"
      await send(reply)
      return
    if is_admin is False:
      logger.info("群内私聊: %s" % msg)
      #  await sendme(f"群内私聊 {msg.type_} {msg.from_}: {text}")
      send_log(f"{msg.type_} {msg.from_}: {text}")
      return
    #  if get_jid(msg.to) in my_groups:
    #  if get_jid(msg.from_) in my_groups:
    if muc in my_groups:
      nick = msg.from_.resource
    else:
      nick = msg.from_.localpart
  elif msg.type_ == MessageType.ERROR:
    warn(f"收到错误消息：{msg} {msg.error}")
    return
  else:
    pprint(msg)
    logger.info(f"skip unknown type: {msg.type_} {msg}")
    return

  if text == "ping":
    reply = msg.make_reply()
    reply.body[None] = "pong"
    await send(reply)
    return

  res = await run_cmd(text, get_src(msg), f"X {nick}: ", is_admin, text0)
  if res is True:
    return
  if res:
    reply = msg.make_reply()
    reply.body[None] = res
    await send(reply)
    return

  return
  if get_jid(msg.from_) not in me:
    return
  #  awai:t mt_send(text, 'me', get_jid(msg.from_))
  if text == "test":
    logger.setLevel(logging.DEBUG)
    reply = msg.make_reply()
    reply.body[None] = "ok"
    await send(reply)
  elif text == "ok":
    log(f"got a msg: ok")
  elif text == "correct":
    reply = msg.make_reply()
    reply.body[None] = generand(3)
    await send(reply, correct=True)
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




def get_addr(s):
  if s.startswith('-'):
    if s.isnumeric():
      s = s[1:]
      return -1*int(s)
  if s.isnumeric():
    return int(s)
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

async def add_cmd():

  async def _(cmds, src):
    return "pong"
  cmd_funs["ping"] = _

  async def _(cmds, src):
    cmds = set()
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
        cmds.add(k1)

    res = '可用的命令:\n'
    res += '\n'.join(cmds)
    if cmds_admin:
      res += '\n\n仅管理可用的命令:\n'
      res += '\n'.join(cmds_admin)
    return res
  cmd_funs["cmd"] = _


  async def _(cmds, src):
    if len(cmds) == 1:
      return f"disco\n.{cmds[0]} $domain\nhttps://docs.zombofant.net/aioxmpp/devel/api/public/disco.html?highlight=disco#aioxmpp.DiscoClient"
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
    return res
  cmd_funs["disco"] = _
  cmd_for_admin.add('disco')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"discoi\n.{cmds[0]} $domain\nhttps://docs.zombofant.net/aioxmpp/devel/api/public/disco.html?highlight=disco#aioxmpp.DiscoClient"
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
      
    return res
  cmd_funs["discoi"] = _
  cmd_for_admin.add('discoi')



  async def _(cmds, src):
    if len(cmds) == 1:
      return f"download file by url\n.{cmds[0]} $url [raw/curl/tg] [direct]"
    if len(cmds) == 3:
      if cmds[2] == "tg":
        try:
          #  if src == log_group_private:
          if len(cmds) == 3:
            if cmds[2] == "tg":
              res = await UB.send_file(CHAT_ID, file=cmds[1], caption=cmds[1])
              return "sent in tg"
        except Exception as e:
          warn(f"通过tg远程下载失败: {e=}")
          return "failed"
    opts = cmds[2:4]
    while True:
      if len(opts) < 2:
        opts.append("")
      else:
        break
    opts.append("down")
    res = await get_title(cmds[1], src, opts=opts)
    return f"{res}"
  cmd_funs["down"] = _
  cmd_for_admin.add('down')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"get title\n.{cmds[0]} $url [raw/curl] [direct]"
    res = await get_title(cmds[1], src=src, opts=cmds[2:4])
    return f"{res}"
  cmd_funs["tl"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"bash\n.{cmds[0]} $code"
    #  cmds[0] = "bash"
    cmds.pop(0)
    #  res = await my_popen(cmds)
    res = await my_popen(' '.join(cmds), src=src, shell=True)
    return f"{res}"
  cmd_funs["sh"] = _
  cmd_for_admin.add('sh')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"python\n.{cmds[0]} $code"
    cmds.pop(0)
    res = await my_exec(' '.join(cmds), src)
    return f"{res}"
  cmd_funs["py"] = _
  cmd_for_admin.add('py')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"python eval()\n.{cmds[0]} $code"
    cmds.pop(0)
    res = await my_eval(' '.join(cmds))
    return f"{res}"
  cmd_funs["eval"] = _
  cmd_for_admin.add('eval')

  async def _(cmds, src):
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
      return "%s, 禁言账户：%s/%s" % (reason, k, i)
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

      return "%s, 解除账户：%s/%s" % (reason, k, i)
  cmd_funs["mo"] = _
  cmd_for_admin.add('mo')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"{cmds[0]}\n.{cmds[0]} $jid/$nick"
    res = get_nick_room(cmds, src)
    if type(res) is str:
      return res
    nick = res[0]
    room = res[1]
    reason = "cmds[0]命令"

    for i in room.members:
      if i.nick == nick:
        res = await room.ban(i, reason)
        return f"ok: {res}"

    res = get_jid_room(cmds, src)
    if type(res) is str:
      warn(res)
      role = "visitor"
      try:
        res = await room.muc_set_role(nick, role, reason=reason)
      except Exception as e:
        muc = str(room.jid.bare())
        return f"failed: {muc}"
      return f"ok2: {res}"
    jid = res[0]
    room = res[1]
    #  muc = str(room.jid)
    #  unban(muc, jid=jid)
    affiliation = "outcast"
    res = await room.muc_set_affiliation(jid, affiliation, reason=reason)
    return f"ok3: {res}"

    return "not found"
  cmd_funs["ban"] = _
  cmd_for_admin.add('ban')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"{cmds[0]}\n.{cmds[0]} $jid/$nick"

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
          return res
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
      return f"ok: {nick}{res2}"

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
      res = f"ok2: {nick}{res2}\n--{res3}"
      err(res)
      return res

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
          return f"没找到: {nick}"
      else:
        return res
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
      res = f"ok3: {nick} {jid}{res2}\n--{res3}"
    else:
      res = f"failed3: {nick} {jid}"
    return res
  cmd_funs["banall"] = _
  cmd_for_admin.add('banall')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"临时踢出\n.{cmds[0]} $jid/$nick"

    #  option = False
    #  if len(cmds) == 3:
    #    option = cmds[1]
    #    cmds.pop(1)

    res = get_nick_room(cmds, src)
    if type(res) is str:
      return res
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
        return f"ok: {res}"
    return "not found"
  cmd_funs["kick"] = _
  cmd_for_admin.add('kick')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"禁言\n.{cmds[0]} $jid/$nick [时间(默认300)]"

    option = 300
    if len(cmds) == 3:
      option = int(cmds[2])
      cmds.pop(2)

    res = get_nick_room(cmds, src)
    if type(res) is str:
      return res
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
    return f"ok: {res}"
  cmd_funs["wtf"] = _
  cmd_for_admin.add('wtf')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"禁言\n.{cmds[0]} $jid/$nick"
    res = get_nick_room(cmds, src)
    if type(res) is str:
      return res
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
    return f"ok: {res}"
  cmd_funs["unban"] = _
  cmd_for_admin.add('unban')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"解除驱逐（添加成员身份）\n.{cmds[0]} $jid/$nick"
    reason = "cmds[0]命令"
    res = get_jid_room(cmds, src)
    if type(res) is str:
      return res
    jid = res[0]
    room = res[1]
    #  muc = str(room.jid)
    #  unban(muc, jid=jid)
    affiliation = "member"
    res = await room.muc_set_affiliation(jid, affiliation, reason=reason)

    res = get_nick_room(cmds, src)
    if type(res) is str:
      return res
    nick = res[0]
    room = res[1]

    muc = str(room.jid)
    unban(muc, nick)

    reason = "cmds[0]命令"
    role = "participant"
    res2 = await room.muc_set_role(nick, role, reason=reason)

    return f"ok: {res} {res2}"
  cmd_funs["op"] = _
  cmd_for_admin.add('op')
  cmd_funs["ub"] = _
  cmd_for_admin.add('ub')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"驱逐\n.{cmds[0]} $jid/$nick"

    res = get_jid_room(cmds, src)
    if type(res) is str:
      return res
    jid = res[0]
    room = res[1]

    reason = "cmds[0]命令"
    affiliation = "outcast"
    res = await room.muc_set_affiliation(jid, affiliation, reason=reason)
    return f"ok: {res}"
  cmd_funs["sb"] = _
  cmd_for_admin.add('sb')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"join all\n.{cmds[0]} all\n.{cmds[0]} $muc"
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
      return "res: %s" % res
    return "ok"
  cmd_funs["join"] = _
  cmd_for_admin.add('join')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"search\n.{cmds[0]} [clear/se/wtf/fix] $jid/$nick"

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
        return res
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
    return res
  cmd_funs["se"] = _
  cmd_for_admin.add('se')

  async def _(cmds, src):
    res = None
    if len(cmds) == 1:
      res = f"管理桥接\n.{cmds[0]} add $from $dst\n.{cmds[0]} del $id/$jid\n.{cmds[0]} se $id/$jid"
      res += "\n--\n%s" % json.dumps(bridges, indent='  ')
    elif cmds[1] == "add":
      if len(cmds) != 4:
        res = "参数数量不对"
      else:
        #  if cmds[2].isnumeric():
        addr = get_addr(cmds[2])
        #  bridges[get_addr(cmds[2])] = get_addr(cmds[3])
        if addr in bridges:
          res = "existed"
        else:
          bridges[addr] = get_addr(cmds[3])
          #  res = f"added: {get_addr(cmds[2])} -> {get_addr(cmds[3])}"
          res = f"added: {addr} -> {bridges[addr]}"
    elif cmds[1] == "del":
      if len(cmds) != 3:
        res = "参数数量不对"
      else:
        addr = get_addr(cmds[2])
        if addr in bridges:
          res = "没找到"
        else:
          res = f"delete: {addr} -> {bridges[addr]}"
          bridges.pop(get_addr(cmds[2]))
    elif cmds[1] == "se":
      res = ''
      addr = get_addr(cmds[2])
      if addr in bridges:
        res += f"existed: {addr} -> {bridges[addr]}"
      peer = await get_entity(addr)
      if peer:
        res += "\npeer id: %s" % await UB.get_peer_id(peer)
        res += "\n%s: %s\n--\n%s" % (type(peer), peer.stringify(), peer)
    await send(f"{res}", src)
  cmd_funs["br"] = _
  cmd_for_admin.add('br')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"添加好友\n.{cmds[0]} $jid"
    rc = XB.summon(aioxmpp.RosterClient)
    #  pprint(rc)
    res = rc.subscribe(JID.fromstr(cmds[1]))
    #  print(f"结果：{res}")
    await send(f"结果：{res}", src)
    await asyncio.sleep(1)
    res = rc.approve(JID.fromstr(cmds[1]))
    #  print(f"结果：{res}")
    await send(f"结果：{res}", src)
  cmd_funs["connect"] = _
  cmd_for_admin.add('connect')

  async def _(cmds, src):
    if len(cmds) == 1:
      if src in my_groups:
        muc = src
        if muc not in rooms:
          return f"没找到room: {muc}"
        room = rooms[muc]
        jids = users[muc]
        tmp = []
        for i in room.members:
          if i.direct_jid:
            if str(i.direct_jid.bare()) not in jids:
              jids[str(i.direct_jid.bare())] = [i.nick, i.affiliation, i.role]
          tmp.append(i.nick)
        return "列表(%s)\n%s" % (len(tmp), '\n'.join(tmp))
      else:
        return "need muc"
      #  rc = XB.summon(aioxmpp.RosterClient)
      #  return "items: %s" % rc.items
    elif cmds[1] == "json":
      rc = XB.summon(aioxmpp.RosterClient)
      return "json:\n%s" % rc.export_as_json()
    #  else:
    #    #  pc = XB.summon(aioxmpp.PresenceClient)
    #    #  res = XB.get_most_available_stanza(cmds[1])
    #    return res
  cmd_funs["list"] = _
  cmd_for_admin.add('list')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"查询xmpp端口\n.{cmds[0]} $domain"
    res = await node.discover_connectors(cmds[1])
    return f"可用的xmpp端口: {cmds[1]} {res}"
  cmd_funs["xmpp"] = _
  cmd_for_admin.add('xmpp')




  async def _(cmds, src):
    if len(cmds) == 1:
      return f"阿里千问\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await qw(text)
  cmd_funs["qw"] = _



  async def _(cmds, src):
    if len(cmds) == 1:
      return f"阿里千问\n{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await qw2(text)
  cmd_funs["qw2"] = _


  async def _(cmds, src):
    if len(cmds) == 1:
      return f"音乐下载\n.{cmds[0]} $text\n.{cmds[0]} clear\n--\ntelegram bot: https://t.me/{music_bot_name}"
    if cmds[1] == "clear":
      await clear_history()
      return "ok"
    text = ' '.join(cmds[1:])
    music_bot_state[src] = 1
    text="/search "+text
    #  mid = await send_to_tg_bot(text, music_bot, src)
    #  return 1, mid
    return 1, music_bot, text
  cmd_funs["music"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gpt(telegram bot) translate\n.{cmds[0]} $text\n--\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
    text = ' '.join(cmds[1:])
    text = f'{PROMPT_TR_MY}“{text}”'
    return 1, gpt_bot
  cmd_funs["gtr"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gpt(telegram bot) translate 中文专用翻译\n.{cmds[0]} $text\n--\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
    text = ' '.join(cmds[1:])
    text = f'{PROMPT_TR_ZH}“{text}”'
    return 1, gpt_bot
  cmd_funs["gtz"] = _


  #  async def _(cmds, src):
  #    if len(cmds) == 1:
  #      return f"gpt bot\n.{cmds[0]} $text\n--\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
  #    text = ' '.join(cmds[1:])
  #    mid = await send_to_tg_bot(text, gpt_bot, src)
  #    return 1, mid
  #  cmd_funs["gtg"] = _

  async def _(cmds, src):
    bot_name = "littleb_gptBOT"
    if len(cmds) == 1:
      return f"gpt bot\n.{cmds[0]} $text\n--\nhttps://t.me/{bot_name}"
    text = ' '.join(cmds[1:])
    return 3, bot_name, text
  cmd_funs["gtg"] = _

  async def _(cmds, src):
    bot_name = "MishkaAI_bot"
    if len(cmds) == 1:
      return f"Mishka\n.{cmds[0]} $text\n--\nhttps://t.me/{bot_name}"
    text = ' '.join(cmds[1:])
    return 3, bot_name, text
    #  mid = await send_to_tg_bot(text, await UB.get_input_entity(bot_name), src)
    #  e = await UB.get_entity(bot_name)
    e = await UB.get_input_entity(bot_name)
    pid = await UB.get_peer_id(e)
    mid = await send_to_tg_bot(text, pid, src)
    return 2, mid, pid
  cmd_funs["mk"] = _

  async def _(cmds, src):
    bot_name = "gpt3_unlim_chatbot"
    if len(cmds) == 1:
      return f"GPT-3.5-turbo\n.{cmds[0]} $text\n.{cmds[0]} reset: 清空上下文\n--\nhttps://t.me/{bot_name}"
    text = ' '.join(cmds[1:])
    if text == "reset":
      text = "/start"
    return 3, bot_name, text
  cmd_funs["gpt3"] = _

  async def _(cmds, src):
    bot_name = "OPENAl_ChatGPT_bot"
    if len(cmds) == 1:
      return f"模型不固定\n.{cmds[0]} $text\n--\nhttps://t.me/{bot_name}"
    text = ' '.join(cmds[1:])
    return 3, bot_name, text
  cmd_funs["gpt4"] = _

  async def _(cmds, src):
    bot_name = "chatGPTwrapperbot"
    if len(cmds) == 1:
      return f"Gemini\n.{cmds[0]} $text\n.{cmds[0]} reset: 清空上下文\n--\nhttps://t.me/{bot_name}"
    text = ' '.join(cmds[1:])
    if text == "reset":
      text = "/reset"
    return 3, bot_name, text
  cmd_funs["gm"] = _
  cmd_funs["ai"] = _
  cmd_funs["bd"] = _


  async def _(cmds, src):
    bot_name = "stable_diffusion_bot"
    if len(cmds) == 1:
      return f"stable diffusion\n.{cmds[0]} $text\n--\nhttps://t.me/{bot_name}"
    text = ' '.join(cmds[1:])
    return 3, bot_name, text
  cmd_funs["sd"] = _


  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gemini 图像生成(仅支持英文)\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await ai_img(text)
  cmd_funs["img"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"HuggingChat\n.{cmds[0]} $text\n\n--\nhttps://github.com/xtekky/gpt4free\n问答: hg/di/lb/kl/you/bd/ai"
    text = ' '.join(cmds[1:])
    return await hg(text, provider=Provider.HuggingChat)
  cmd_funs["hg"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"DeepInfra\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return  await ai(text, provider=Provider.DeepInfra)
  cmd_funs["di"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"Liaobots\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await ai(text, provider=Provider.Liaobots)
  cmd_funs["lb"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"Liaobots\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await ai(text, provider=Provider.Koala, proxy="http://127.0.0.1:6080")
  cmd_funs["kl"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"You\n.{cmds[0]} $text\n\n--\nhttps://github.com/xtekky/gpt4free\n问答: hg/di/lb/kl/you/bd/ai"
    text = ' '.join(cmds[1:])
    return await ai(text, provider=Provider.You, proxy="http://127.0.0.1:6080")
  cmd_funs["you"] = _

  async def _(cmds, src):
    i = 0
    for g in mtmsgsg:
      i += 1
      for j in mtmsgsg[g]:
        i += 1
    for g in gid_src:
      i += 1
    ii = i

    if cmds[1] == "all":
      await clear_history()
    else:
      await clear_history(src)
    i = 0
    for g in mtmsgsg:
      i += 1
      for j in mtmsgsg[g]:
        i += 1
    for g in gid_src:
      i += 1
    #  return "ok {ii} -> {i}"
    return f"清除状态\n.{cmds[0]} all\n--\n{ii} -> {i}"
  cmd_funs["clear"] = _


@exceptions_handler
async def run_cmd(*args, **kwargs):
  res = await _run_cmd(*args, **kwargs)
  if type(res) is str:
    res = wtf_str(res, "xmpp")
  return res

async def _run_cmd(text, src, name="X test: ", is_admin=False, textq=None):
  if text[0:1] == ".":
    if text[1:2] == " ":
      return
    if text[1:2] == ".":
      return
    cmds = get_cmd(text[1:])
    if cmds:
      pass
    else:
      return
    #  print(f"> I: {cmds}")
    logger.info("got cmds: {}".format(cmds))
    await send_typing(src)
    cmd = cmds[0]
    res = False
    if cmd in cmd_for_admin:
      if is_admin is False:
        return "仅管理可用"
      res = True
    elif cmd in cmd_funs:
      res = True
    if res is True:
      res = await cmd_funs[cmd](cmds, src)
      if type(res) is tuple:
        if res[0] == 1:
          #  mid = res[1]
          if src not in mtmsgsg:
            mtmsgsg[src] = {}
          mtmsgs = mtmsgsg[src]
          mtmsgs.clear()
          #  mtmsgs[mid][0] = name
          mid = await send_to_tg_bot(res[2], res[1])
          mtmsgs[mid] = [name]
          gid_src[mid] = src
        #  elif res[0] == 2:
        #    mid = res[1]
        #    mtmsgsg[src][mid][0] = name
        #    pid = res[2]
        #    if pid not in bridges:
        #      bridges[pid] = {}
        #    target = bridges[pid]
        #    need_delete = []
        #    for i, j in target.items():
        #      if j == src:
        #        need_delete.append(i)
        #    for i in need_delete:
        #      target.pop(i)
        #    target[mid] = src
        elif res[0] == 3:
          bot_name = res[1]
          text = res[2]
          e = await UB.get_input_entity(bot_name)
          pid = await UB.get_peer_id(e)

          if src not in mtmsgsg:
            mtmsgsg[src] = {}
          mtmsgs = mtmsgsg[src]

          if pid not in bridges:
            bridges[pid] = {}
          target = bridges[pid]

          i = 0
          while True:
            need_delete = []
            for i in target:
              if i in mtmsgs:
                #  if len(mtsmgs[i]) > 1:
                #  if type(mtmsgs[i][0]) is int:
                if len(mtmsgs[i]) > 1:
                  if time.time() - mtmsgs[i][1] > 6:
                    need_delete.append(i)
              else:
                need_delete.append(i)
            for i in need_delete:
              target.pop(i)
            if len(target) == 0:
              break
            i += 1
            if i > 5:
              warn(f"{bot_name} {src} {name}: bot太忙({len(target)}): {target}")
              #  return f"bot太忙({len(target)}), 请重试"
              target.clear()
              break
            await asyncio.sleep(4)

          mtmsgs.clear()

          mid = await send_to_tg_bot(text, pid)
          mtmsgs[mid] = [name]
          gid_src[mid] = src
          #  mid = res[1]
          #  pid = res[2]

          #  if pid not in bridges:
          #    bridges[pid] = {}
          #  target = bridges[pid]
          #  need_delete = []
          #  for i, j in target.items():
          #    if j == src:
          #      if i+1 < mid:
          #        need_delete.append(i)
          #  for i in need_delete:
          #    target.pop(i)

          target[mid] = src
        #  await send_typing(src)
        return True
      if res:
        return res
      else:
        return True
      #  reply = msg.make_reply()
      #  reply.body[None] = "%s" % res
      #  await send(reply)
      #  return True
    else:
      res = await send_cmd_to_bash(src, name, text)
      if res:
        return res
  elif text.isnumeric() and src in music_bot_state and music_bot_state[src] == 2:
    mtmsgs = mtmsgsg[src]
    tmp = []
    for i in gid_src:
      if gid_src[i] == src:
        tmp.append(i)
    qid = max(tmp)
    #  logger.info(f"尝试下载：{text} {qid}")
    bs = mtmsgs[qid][1]
    if bs is None:
      warn(f"fixme: bs is None, 尝试下载：{text} {qid} msg: {mtmsgs[qid]}")
      return
    if bs is float:
      warn(f"fixme: bs is float, 尝试下载：{text} {qid} msg: {mtmsgs[qid]}")
      return
    logger.info(f"尝试下载：{text} {qid} msg: {bs}")
    i = None
    for i in get_buttons(bs):
      #  if type(i) is list:
      #    for j in i:
      #      if j.text == text:
      #        logger.info(f"已找到：{text}")
      #        await j.click()
      #        i = True
      #        break
      #    if i is True:
      #      break
      #  else:
        if i.text == text:
          logger.info(f"已找到：{text}")
          music_bot_state[src] += 1
          await i.click()
          i = True
          await send(f"命中：{text}", src, correct=True)
          break

    if i is True:
      pass
    else:
      logger.info(f"没找到：{text}")
      await send(f"没找到：{text}", src)
    return
  else:
    # tilebot
    tmp=""
    if textq:
      tt = textq
    else:
      tt = text
    for i in tt.splitlines():
      if not i.startswith("> ") and  i != ">":
        tmp += i+"\n"

    urls=urlre.findall(qre.sub("", tmp))
    res=""
    #  M=' 🔗 '
    #  M='- '
    #  M=' ⤷ '
    for url in urls:
      #  url=url[0]
      url=url[1]
      if url.startswith("https://t.me/"):
        return
      if url.startswith("https://conversations.im/j/"):
        return
      if url.startswith("https://icq.im"):
        return
      if url.startswith("https://x.com/"):
        res = await send_cmd_to_bash(src, name, url)
        return res
      if url.startswith("https://twitter.com/"):
        res = await send_cmd_to_bash(src, name, url)
        return res
      if not res:
        if len(urls) == 1:
          res="%s" % await get_title(url)
          break
        res="[ %s urls ]" % len(urls)
      res+="\n\n> %s\n%s" % (url, await get_title(url, src))

    if res:
      res = f"{name}{res}"
      #  res2 = await send_cmd_to_bash(src, "", text)
      #  if res2:
      #    res += f"\n{res2}"
      return res
    else:
      res = await send_cmd_to_bash(src, name, text)
      return res
      #  await mt_send(res, gateway=gateway, name="titlebot")

  return False


@exceptions_handler
async def login(client=None):
  if client is None:
    client = XB
  jid = get_jid(client.local_jid)
  logger.info(f"登录中: {jid}")
  try:
    #  steam = await i.connected().__aenter__()
    steam = await asyncio.wait_for(client.connected().__aenter__(), timeout=30)
    logger.info(f"登录成功：{jid}")

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
      await asyncio.sleep(1)
      vc = await vs.get_vcard(None)
      if vc.get_photo_mime_type() is not None:
        logger.info(f"头像设置成功: {jid} {fn}")
        #  logger.warning(f"修改头像需要重新登录才能生效：{jid}")
        #  await stop(client)
        #  if await login(client, True):
        #    #  n = fn.split("@", 1)[1].split('_', 1)[1].rsplit('.', 1)[0]
        #    #  mynicks.add((jid, n))
        #    logger.info(f"头像设置成功: {jid} {fn}")
        #    return True
        #  else:
        #    return False
      else:
        logger.warning(f"头像设置失败：{jid}")
    else:
      logger.info(f"无需设置头像：{jid}")


    await regisger_handler(client)

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
  logger.info("开始初始化ocr")
  #  if 'liqsliu' not in HOME:
  if os.path.exists("%s/ddddocr" % HOME):
    sys.path.append("%s/ddddocr" % HOME)
    import ddddocr
    ocr = ddddocr.DdddOcr()
    def f(img):
      logger.info("正在运行识别程序：ddddocr")
      return ocr.classification(img)
    ocr_ok.append(f)
  if os.path.exists("%s/ddddocr" % HOME):
    sys.path.append("%s/muggle/muggle-ocr-1.0.3" % HOME)
    import muggle_ocr
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    def f(img):
      logger.info("正在运行识别程序：muggle_ocr")
      return sdk.predict(image_bytes=img)
    ocr_ok.append(f)
  if ocr_ok is None:
    logger.info("没找到orc程序，将会无法识别验证码")
    return False

def run_ocr(img):
  if ocr_ok is None:
    if ocr_init() is False:
      return
  elif ocr_ok == []:
    for _ in range(5):
      logger.info("等待orc初始化")
      time.sleep(5)
      if ocr_ok:
        break
    if ocr_ok == []:
      logger.info("等待orc初始化超时")
      return
  f = None
  try:
    while True:
      f = random.choice(ocr_ok)
    #  for f in ocr_ok:
      s = f(img)
      if s:
        logger.info(f" 识别结果: {s}")
        return s
      else:
        logger.info(f" 识别失败: {s}")
  except Exception as e:
    warn(f"识别程序出现错误 {f=} {e=}")



def jbypass(msg):
  #  logger.warn(f"无法进群: {msg}")
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
      logger.info(f"需要验证才能入群: {myid} {jid} {text} {tmp}")
  else:
    logger.info(f"fixme: 这个群需要验证才能进吗？那就程序有bug: {myid} {jid} {text}")
    return

  u = None
  for u in tmp:
    #  if jid.split('@', 1)[1] in u:
    if msg.from_.domain in u:
      break
    u = None
  if u is None:
    logger.info(f"没找到合适的，随便选第一个作为验证码地址: {jid} {tmp}")
    u = tmp[0]
  logger.info(f"验证码地址: {u}")
  #  logger.info(f"验证码地址: {u=}")
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
  logger.info(f"image size: {len(res)} {iu}")
  #  print("===")
  #  s = ocr.classification(res)
  s = await asyncio.to_thread(run_ocr, img=res)
  if s:
    await asyncio.sleep(3)
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
    logger.info(f"headers: {headers}")
    logger.info(f"data: {data}")
    res = await http(f"{u}", "POST", headers=headers, data=data, proxy="http://127.0.0.1:6080")
    logger.info(res)
    #  while True:
    #    logger.info(f"等待进群结果: {myid} {jid}")
    #    await asyncio.sleep(3)
    #    if jid in muc_now:
    #      if myid in muc_now[jid]:
    #        break
  else:
    #  pprint(s)
    logger.info(f"识别验证码失败: {myid} {jid} {s}")



def on_muc_role_request(form, submission_future):
  # https://docs.zombofant.net/aioxmpp/0.13/api/public/muc.html#aioxmpp.muc.Room.on_muc_role_request
  print(f"发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")
  print(form)
  print(submission_future)

  #  await send(f"发言申请: {form}")
  if submission_future.done():
    send_log(f"skip: 发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")
    return
  send_log(f"发言申请: {form.roomnick}\njid: {form.jid}\nrole: {form.role}\n{form}")
  #默认拒绝
  form.request_allow=False
  submission_future.set_result(form)


#  test_group = 'ipfs@salas.suchat.org'
rooms = {}
auto_input = False

async def join_all():
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
    #    logger.info(f"无法进入的群组: {tmp}")
    #    #  await mt_send_for_long_text(f"无法进入的群组: {tmp}")
    #    ms = tmp
    #    await asyncio.sleep(5)
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
        logger.info(f"join all ok: {len(tasks)}/{len(groups)}")
        break
    logger.info(f"等待任务队列: {len(tasks)}/{len(groups)}")
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
      send_log("进群失败，会继续尝试：\n%s" % "\n".join(tmp))
      await asyncio.sleep(300)
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
            logger.info(f"等待进群: {get_jid(client.local_jid)} {jid}")

            await fut
            logger.info(f"进群成功: {myid} {jid}")


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
          #  logger.warning(f"进群超时(废弃): {jid} {muc} {e=}")
          warn(f"进群超时(废弃){sum_try}: {myid} {jid} {nick} {e=}")
        except errors.XMPPCancelError as e:
          # XMPPCancelError("{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: No route to host')")
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: connection refused')":
            logger.info(f"进群失败, 网络问题，拒绝连接: {myid} {jid} {e=}")
            return False
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: No route to host')":
            logger.info(f"进群失败, 网络问题，找不到主机: {myid} {jid} {e=}")
            return False
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: connection timeout')":
            logger.info(f"进群失败, 网络问题，连接超时: {myid} {jid} {e=}")
            return False
          if e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found"):
            logger.info(f"进群失败, 网络问题，找不到地址: {myid} {jid} {e=}")
            return False

          elif e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}conflict ('That nickname is already in use by another occupant')" or e.args[0] == '{urn:ietf:params:xml:ns:xmpp-stanzas}conflict' or '{urn:ietf:params:xml:ns:xmpp-stanzas}conflict' in e.args[0]:
            if '_' in nick:
              nick = f"{nick}%s" % generand(1)
            else:
              nick = f"{nick}_%s" % generand(1)
            logger.warning(f"群名字冲突{sum_try}: {myid} {jid} {nick} {e=}")

          else:
            logger.info(f"进群失败{e.args}: {myid} {jid} {e=}")
            return False
        except errors.XMPPAuthError as e:
          #  pprint(e.args)
          #  if e.args == ("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')", ):
          if e.args:
            if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized"):
              if auto_input is False:
                return False
              logger.info(f"进群失败, 验证码不正确，准备重试: {myid} {jid} {e=}")
            else:
              if e.args[0] == '{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden':
                logger.info(f"进群失败，被ban了(forbiden): {myid} {jid} {e=}")
              elif e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden ('You have been banned from this room')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden"):
                logger.info(f"进群失败，被ban了: {myid} {jid} {e=}")
              else:
                logger.info(f"进群失败{e.args}: {myid} {jid} {e=}")
              return False
          else:
            logger.info(f"进群失败(无权限): {myid} {jid} {e=}")
            return False
        except Exception as e:
          err(f"进群失败: {myid} {jid} {e=}")
          return False
        sum_try += 1
        if sum_try > 3:
          warn(f"进群失败(重试次数达到最大值): {myid} {jid}")
          return False
        await asyncio.sleep(0.1)

    finally:
      if auto_input:
        client.stream.unregister_message_callback(
            aioxmpp.MessageType.NORMAL,
            J,
        )
    return False


@exceptions_handler
async def xmppbot():
  logger.info("开始登录xmpp")
  global XB, myjid, UPLOAD, UPLOAD_MAX
  myjid = get_my_key("JID")
  password = get_my_key("JID_PASS")
  logger.info(f"xmpp: {myjid} {password[:3]}...")
  #  jid = aioxmpp.JID.fromstr(jid)
  XB = aioxmpp.PresenceManagedClient(
      JID.fromstr(myjid),
      aioxmpp.make_security_layer(password)
  )
  logger.info(f"已导入新账户: {myjid} password: {password[:4]}...")
  t = asyncio.create_task(load_config())
  await t
  if await login():
    logger.info(f"join all groups...\n%s" % my_groups)
    #  await join()
    #  global mucsv
    #  mucsv = client.summon(aioxmpp.MUCClient)
    #  for coro in asyncio.as_completed(map(join, my_groups),
    await join_all()
  else:
    err(f"登陆失败：{myjid}")
    return


  global allright_task
  if allright_task > 0:
    allright_task -= 1
    await add_cmd()
    asyncio.create_task(xmppbot2(), name="xmppbot2")
  else:
    await sendg("已重新启动xmppbot")
    
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

@exceptions_handler
async def xmppbot2():
  while True:
    if XB.running:
      await asyncio.sleep(6)
      continue
    logger.info("需要重新启动xmppbot")
    #  try:
    #  # RuntimeError: write() called (invalid in state _State.CLOSED, closing=False)
    #  except RuntimeError as e:
    #    if e.args[0] == 'write() called (invalid in state _State.CLOSED, closing=False)':
    #      warn(f"fixme: xmpp error {e=}")
    #    else:
    #      warn(f"fixme: unknown xmpp error {e=}")
    await stop()
    await save_data()
    sys.exit(2)
    await asyncio.sleep(5)
    t = asyncio.create_task(xmppbot(), name="xmppbot")
    await t


async def init():
  #  LOGGER.addFilter(NoParsingFilter())
  # https://stackoverflow.com/questions/17275334/what-is-a-correct-way-to-filter-different-loggers-using-python-logging
  for handler in logging.root.handlers:
    #  handler.addFilter(logging.Filter('foo'))
    #  handler.addFilter(NoParsingFilter())
    f = NoParsingFilter()
    handler.addFilter(f)
    logger.info(f"added filter to: {handler}")

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

  global loop
  loop = asyncio.get_event_loop()
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
        res = await my_popen(' '.join(sys.argv[2:]))
        print(res)
      elif sys.argv[1] == 'cmd2':
        res = await send_cmd_to_bash("gateway1", "X test", ' '.join(sys.argv[2:]))
        print(res)
      return


    global allright_task

    allright_task += 1
    asyncio.create_task(xmppbot(), name="xmppbot")

    #  asyncio.create_task(wtf_loop())

    global UB
    from telethon import TelegramClient
    api_id = int(get_my_key("TELEGRAM_API_ID"))
    api_hash = get_my_key("TELEGRAM_API_HASH")
    #  client = TelegramClient('anon', api_id, api_hash)
    #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, proxy=("socks5", '172.23.176.1', 6084), loop=loop)
    #  global loop
    #  loop = asyncio.get_event_loop()
    #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, loop=loop)
    UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash)
    #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, proxy=("socks5", '127.0.0.1', 6080))

    #  del api_id
    #  del api_hash
    #  #  del bot_token

    #  allright_task += 1
    #  asyncio.create_task(other_init())

    # with UB:
    #  loop.run_until_complete(run())

    global MY_NAME, MY_ID
    #  await UB.start()
    async with UB:
      me = await UB.get_me()
      #  print(me.stringify())
      MY_ID = me.id
      MY_NAME = me.username
      print(f"{MY_NAME}: {MY_ID}")

      @UB.on(events.NewMessage(incoming=True))
      @UB.on(events.MessageEdited(incoming=True))
      async def _(event):
        if not allright.is_set():
          #  logger.info("skip msg: allright is not ok")
          return
        asyncio.create_task(parse_tg_msg(event))

      @UB.on(events.NewMessage(outgoing=True))
      async def _(event):
        if not allright.is_set():
          #  logger.info("skip msg: allright is not ok")
          return
        asyncio.create_task(parse_tg_out_msg(event))

      UB.parse_mode = 'md'

      #  await mt_send("gpt start")
      while True:
        if allright_task > 0:
          logger.info(f"等待初始化完成，剩余任务数：{allright_task}")
          await asyncio.sleep(1)
          continue
        allright.set()
        break

      mt_read_task = asyncio.create_task(mt_read(), name="mt_read")


      logger.info(f"初始化完成")
      send_log(f"启动成功，用时: {int(time.time()-start_time)}s")
      #  await send(f"启动成功，用时: {int(time.time()-start_time)}s", jid=main_group)

      await UB.run_until_disconnected()


    logger.info("主程序正常结束")
  #  except KeyboardInterrupt as e:
  #    logger.info("I: 手动终止")
  #    #  raise e
  #  except SystemExit as e:
  #    raise e
  #  except Exception as e:
  #    logger.error("error: stop...", exc_info=True, stack_info=True)
  #    raise e
  finally:
    logger.info("正在收尾...")
    #  for j in asyncio.all_tasks(loop):
    #    if not j.done():
    #      if "@" in j.get_name():
    #        j.cancel()
    #  for j in asyncio.all_tasks(loop):
    #    if not j.done():
    #      if "@" in j.get_name():
    #        logger.info(f"正在关闭task, {j}")
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
    await stop()
    #  loop.run_until_complete(stop())
    #  loop.run_until_complete(loop.shutdown_asyncgens())
    #  loop.close()
    logger.info("正在退出...")


start_time=time.time()

def main():
  try:

    #  with UB:
    #    UB.loop.run_until_complete(amain())
    asyncio.run(amain())
  except KeyboardInterrupt as e:
    logger.info("停止原因：用户手动终止")
    sys.exit(1)
  except SystemExit as e:
    logger.warning(f"捕获到systemexit: {e=}", exc_info=True, stack_info=True)
    sys.exit(2)
  except Exception as e:
    logger.error(f"出现未知异常: 正在停止运行...{e=}", exc_info=True, stack_info=True)
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

