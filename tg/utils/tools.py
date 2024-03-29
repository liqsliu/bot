import logging



from functools import wraps
import asyncio

import os
import re
import base64
import zstandard
import ast
#import json

import asyncio
import threading
from subprocess import Popen, PIPE

import socket
import sys
import io

import urllib
import urllib.request
import urllib.error

import binascii
import traceback

import zlib
import gzip
import brotli
import time

logger = logging.getLogger(__name__)
mp = logger.warning






from threading import Thread, Timer
from typing import Any, Callable, Optional, Union

HTTP_RES_MAX_BYTES = 15000000


def thread(target: Callable, args: tuple, kwargs: dict = None, daemon: bool = True) -> bool:
    # Call a function using thread
    result = False

    try:
        t = Thread(target=target, args=args, kwargs=kwargs, daemon=daemon)
        t.daemon = daemon
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Thread error: {e}", exc_info=True)

    return result


def threaded(daemon: bool = True):
    # Run with thread
    # https://github.com/scp-079/scp-079-tip/blob/b733fb68a93019916fa3865dcb2f04d67b33667c/plugins/functions/decorators.py#L49
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return thread(func, args, kwargs, daemon)
        return wrapper
    return decorator


from pyrogram.errors import FloodWait

def retry(func):
    # FloodWait retry
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        while True:
            try:
                result = func(*args, **kwargs)
            except FloodWait as e:
                wait_flood(e)
            except Exception as e:
                logger.warning(f"Retry error: {e}", exc_info=True)
                break
            else:
                break
        return result
    return wrapper


import inspect

def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


def test_varname():
    a=1
    t=varname(a)
    print(t)
    b=2
    c=3
    a=[b,c]
    t=list(varname(x) for x in a)
    print(t)
    print(t)


def get_ex(func, args, kwargs):
    allow = (str, int, bool, list, dict)
    if func.__name__ == "from_handler":
#        if type(args[0]) == function:
        func = args[0]
#        args.pop(0)
        args = args[1:]
    ex = f"""fail: {func.__name__}({", ".join(repr(x) if type(x) in allow else str(type(x)) for x in args)}, {", ".join(f"{x}={repr(kwargs[x]) if type(kwargs[x]) in allow else str(type(kwargs[x]))}" for x in kwargs)})"""
    return ex


#  def my_exceptions_handler(func, *, ex=None):
def my_exceptions_handler(func):

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                #  nonlocal ex
                #  if ex is None:
                ex = get_ex(func, args, kwargs)
                return await func(*args, **kwargs)
            #    if asyncio.iscoroutine(f):
            except Exception as e:
                # ex = f'fail: await {func.__name__}({", ".join(args)}, {", ".join(kwargs)})'
                # ex = f'fail: {func.__name__}({", ".join(varname(x) for x in args)}, {", ".join(f"{x}={varname(kwargs[x])}" for x in kwargs)})'
                # ex = f'fail: {func.__name__}({", ".join(str(x) for x in args)}, {", ".join(f"{x}={kwargs[x]}" for x in kwargs)})'
#                if args:
#                ex = None
                _my_exceptions_handler(e, ex=ex)
            # await asyncio.sleep(5)

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                ex = get_ex(func, args, kwargs)
                return func(*args, **kwargs)
            except Exception as e:
                _my_exceptions_handler(e, ex=ex)
            # if threading.current_thread().name != "MainThread":
                # time.sleep(5)

    return wrapper

def current_thread_is_main():
    if threading.current_thread().name == "MainThread":
        return True
    return False

def _my_exceptions_handler(e, *args, **kwargs):
    if type(e) == KeyboardInterrupt:
        if MY_NAME == "liqsliu":
            logger.warning("save config...")
            from .config import save_config
            LOOP.run_until_complete(save_config())
            logger.info("save config ok")
            from .utils.tools import session
            if session:
                LOOP.run_until_complete(session.close())
                logger.info("session closed")
            from .utils import db
            if db.conn:
                db.cur.close()
                db.conn.close()
        raise e
    elif type(e) == SystemExit:
        raise e
    elif type(e) == RuntimeError:
        raise e
    else:
        my_traceback(e, *args, **kwargs)




def my_traceback(exc, ex=None, put=True):
    # logger.error(f"error: {exc=}", exc_info=True, stack_info=True)
#    info = "E: {}\n==\n{}\n==\n{}".format(sys.exc_info()[1], traceback.format_exc(), sys.exc_info())
    info = "E: {}\n==\n{}\n==\n{}".format(sys.exc_info()[1], sys.exc_info(), "".join(traceback.format_exception(exc, value=exc, tb=exc.__traceback__)))
    if ex is not None:
        info = f"{ex}\n====\n" + info
    logger.error(info)
    if put is True:
        remind_me(info)
    return info


def remind_me(info):
    # from ..telegram import put
    put(info)


def put(text):
    "send text to me in telegram, don\'t call in init"

    from .. import MY_ID, LOOP
    from ..telegram import MAX_MSG_LEN, MAX_MSG_LINE, MSG_QUEUE
    if not isinstance(text, str):
        text = str(text)
    if len(text) > MAX_MSG_LEN:
        logger.warning("split long msg: {}".format(text[0:MAX_MSG_LINE]))
        text = text[-MAX_MSG_LEN:].splitlines()[-1]

    # msg = [5, MY_ID, text, {"link_preview": False}]
    #  msg = [5, MY_ID, text, {"disable_web_page_preview": True}]

    from ..config import cid_test
    msg = [5, cid_test, text, {}]

    from pyrogram import enums
    msg[3]["disable_web_page_preview"] = True
    msg[3]["parse_mode"] = enums.ParseMode.DISABLED

    if current_thread_is_main():
        logger.debug("current thread is main")
        asyncio.create_task(MSG_QUEUE.put(msg))
    else:
        try:
    #        loop = asyncio.get_event_loop()
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            loop = None
            logger.error(e, exc_info=True, stack_info=True)
        except Exception as e:
            loop = None
            logger.error(e, exc_info=True, stack_info=True)

        if loop == LOOP:
            logger.info("current thread is main")
            asyncio.create_task(MSG_QUEUE.put(msg))
        else:
            logger.info("current thread is not main")
            future = asyncio.run_coroutine_threadsafe(MSG_QUEUE.put(msg), LOOP)
#        result = future.result()
#        logger.info("put result: {}".format(result))

    #  await MSG_QUEUE.put(msg)
    #  loop = asyncio.get_running_loop()
    #  loop = asyncio.get_event_loop()
    #  loop.create_task(MSG_QUEUE.put(msg), name="put")
    #  loop.call_soon_threadsafe(MSG_QUEUE.put(msg))


def raise_error(error: str):
    error = "-" * 24 + f"\nerror:\n" + "-" * 24 + f"\n{error}" + "-" * 24
    #            logger.exception(info)
    logger.critical("\n" + error)
    raise SystemExit(error)


#  def my_raise(e, func, args, kwargs, ex=None):
def my_raise(e, ex=None):

    _my_exceptions_handler(e, ex=ex)
    return
    #  @my_exceptions_handler(ex=ex)
    @my_exceptions_handler
    def from_handler(*args, **kwargs):
        raise e

    if func.__name__ == "from_handler":
        return from_handler(*args, **kwargs)
    else:
        return from_handler(func, *args, **kwargs)



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
        return json.loads(msg)


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


#  def get_sh_path(path='SH_PATH'):
def read_file(path='SH_PATH'):
    # f = open(os.getcwd() + "/SH_PATH")
    # p = Path(__package__).absolute()
    # p = p.parent
    # f = p / "SH_PATH"
    #  p = "/".join(__file__.split("/")[:-2])
    p = "/".join(__file__.split("/")[:-3])
    #  f = p + "/SH_PATH"
    f = p + "/" + path

    with open(f) as f:
        line = f.readline()
        line = line.rstrip('\n')
    if line:
        return line
    else:
        raise_error("E: can't find SH_PATH")
        return None


SH_PATH = read_file()
DOMAIN = read_file("DOMAIN")

tw_re = re.compile(r"^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./?=&%-]+$")
#  my_host_re = re.compile(r"^https://wtfipfs\.tk/[a-zA-Z0-9_./?=%-]+$")
my_host_re = re.compile(r"^https://"+ DOMAIN.replace('.', '\\.') +"/[a-zA-Z0-9_./?=%-]+$")
pic_re = re.compile(r"^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(jpe?g|png|mp4|gif)$"
)
#url_re=re.compile(r"^(http(s)?|ftp|file)://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*$")
#url_re=re.compile(r"^(?=^.{3,255}$)http(s)?://(([0-9a-zA-Z][0-9a-zA-Z-]{0,62}\.)+\.[a-zA-Z]+|([0-9]+\.){4})(:[0-9]+)?/?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|$")

#URL_RE_TEXT=r"(?=^.{3,255}$)(http(s)?|ftp|file)://([0-9a-zA-Z][0-9a-zA-Z-]{0,62}(\.[0-9a-zA-Z][0-9a-zA-Z-]{0,62})+|([0-9]+\.){3}[0-9]+)(:[0-9]+)?(/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])?"
URL_RE_TEXT = r"(?P<url>(?=.{3,255})(http(s)?|ftp|file|tg|mailto)://([0-9a-zA-Z:.-]+@)?([0-9a-zA-Z][0-9a-zA-Z-]{0,62}(\.[0-9a-zA-Z][0-9a-zA-Z-]{0,62})+|([0-9]+\.){3}[0-9]+)(:[0-9]+)?(/([-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])?)?)"

url_re = re.compile(URL_RE_TEXT)
url_only_re = re.compile(r"^" + URL_RE_TEXT + r"$", re.M)

#url_md_re = re.compile(r"\[(?P<text>[^\n\]]+)\]\(\s*" + URL_RE_TEXT + r"(\s.+)?\)")
url_md_re = re.compile(r"\[(?P<text>(.|\n)+?)\]\(\s*" + URL_RE_TEXT + r"(\s.+)?\)", re.M)
#url1_md_re = re.compile(r"\[(?P<text>[^\n\]]+)\] ?\[(?P<mark>[^\n\]]+)\]")
url1_md_re = re.compile(r"\[(?P<text>(.|\n)+?)\] ?\[(?P<mark>(.|\n)+?)\]", re.M)
#url2_md_re = re.compile(r"^\[(?P<mark>[^\n\]]+)\]: " + URL_RE_TEXT + r"(\s['\”(].+['\”)])?", re.M)
url2_md_re = re.compile(r"^\[(?P<mark>(\n|.)+?)\]: " + URL_RE_TEXT + r"(\s['\”(].+['\”)])?", re.M)
#pic_md_re = re.compile(r"^\!\[[^\n\]]+\]\(\s*" + URL_RE_TEXT + r"(\s.+)?\)$", re.M)
pic_md_re = re.compile(r"^\!\[(.|\n)+?\]\(\s*" + URL_RE_TEXT + r"(\s.+)?\)$", re.M)

rgb_re = re.compile(r"#[0-9A-F]{6}")



BOT_MSG_TEXT = r"(?P<protocol>[A-Z0-9]) (?P<username>.*):( (?P<msg>(.|\r|\n)*))?"

bot_msg_re = re.compile(BOT_MSG_TEXT)
bot_msg_only_re = re.compile(r"^" + BOT_MSG_TEXT + r"$")
bot_msg_qt_re = re.compile(r"^> " + BOT_MSG_TEXT + r"$")

discord_id_end_re=re.compile(r"#[0-9]+$")


def text_has_md(text, url=None):
    i = 0
    while True:
        s = url_md_re.search(text, i)
        if s:
            if not url or url == s["url"]:
                return True
            i = s.span()[1]
        else:
            s = url1_md_re.search(text, i)
            if s:
                ss = url2_md_re.search(text)
                if ss and s["mark"] == ss["mark"]:
                    if not url or url == ss["url"]:
                        return True
                i = s.span()[1]
            else:
                s = pic_md_re.search(text, i)
                if s:
                    if not url or url == s["url"]:
                        return True
                    i = s.span()[1]
                else:
                    break
    return False



async def is_debug(text="auto_msg"):
    msg = 0
    while debug:
        tasks = ""
        for j in asyncio.all_tasks():
            tasks = tasks + "\n" + j.get_name()


#    msg=await myprint(text+" is running,but will not work in debug mode.\nrunning tasks: "+tasks)
#    msg=await myprint(text+"is running, now tasks: \n"+str(tasks))
#    msg=await myprint(text+"is running, now tasks: \n"+str(asyncio.all_tasks()))
        info = text + " is stopped, now tasks: \n" + str(tasks)
        info = info + "\nwaiting feed num: " + str(len(feeds))
        info = info + "\nwaiting entry num: " + str(len(entry_task))

        if t_1_tasks:
            info = info + "\n\nthread 1 tasks: " + "\n".join(t_1_tasks)
        info = info + "\n\nthread count: " + str(threading.active_count())
        info = info + "\nthread t_1 alive: " + str(t_1.is_alive())
        #    info=info+"\nthread current: "+str(threading.current_thread())
        #    info=info+"\nthread all: "+str(threading.enumerate())
        if msg:
            if msg.raw_text != info.strip():
                msg = await msg.edit(info)
        else:
            msg = await userbot.send_message(myid, info)
        await asyncio.sleep(5)
    if msg:
        await msg.delete()
    return True
    return False


def set_log_level(level=None):
    if logger.getEffectiveLevel():
        pass
    if level:
        #    logger.setLevel(logging.WARNING)
        logger.setLevel(level)

    mp("now log level: " % logger.getEffectiveLevel())
    mp("defined level: " + """CRITICAL 50
  ERROR 40
  WARNING 30
  INFO 20
  DEBUG 10
  NOTSET 0""")


def __my_execptions_handler(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
            logger.exception(info)
            await UB.send_message(MY_ID, info)

    return wrapper


def mdraw(text, type="text"):
    #  msg=msg.replace("\\","\\\\")
    chars = {
        "text": "\\_*[]()~`>#+-=|{}.!",
        "code": "\\`",
        "link": "\\)",
        "md": "\\_*[`"
    }
    if type in chars:
        type = chars[type]
    if text:
        for i in type:
            text = text.replace(i, "\\" + i)
    return text



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


def __ennum():
    # convert num to zero width spaces

    s=""
    for i in range(len(chr_list)):
        s+="{}{}".format(i, chr_list[i])
    print(s)
    print("ok")
    print(repr(s))
    print("ok")
    print(len(chr_list))

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

def _denum(s):
    s = s.replace('"', '')
    kk=0
    while s:
        try:
            k = chr_list.index(s[0])
            kk = kk*num_jz+k
            s = s[1:]
        except ValueError:
            return 0
    return kk


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



from urllib import request
from urllib import parse

import io
import mimetypes
import uuid


class MultiPartForm:
    """Accumulate the data to be used when posting a form."""
    # https://pymotw.com/3/urllib.request/#uploading-files

    def __init__(self):
        self.form_fields = []
        self.files = []
        # Use a large random byte string to separate
        # parts of the MIME data.
        self.boundary = uuid.uuid4().hex.encode('utf-8')
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary={}'.format(
            self.boundary.decode('utf-8'))

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))

    def add_file(self, fieldname, filename, fileHandle,
                 mimetype=None):
        """Add a file to be uploaded."""
#        body = fileHandle.read()
        body = fileHandle
        if mimetype is None:
            mimetype = (
                mimetypes.guess_type(filename)[0] or
                'application/octet-stream'
            )
        self.files.append((fieldname, filename, mimetype, body))
        return

    @staticmethod
    def _form_data(name):
        return ('Content-Disposition: form-data; '
                'name="{}"\r\n').format(name).encode('utf-8')

    @staticmethod
    def _attached_file(name, filename):
        return ('Content-Disposition: file; '
                'name="{}"; filename="{}"\r\n').format(
                    name, filename).encode('utf-8')

    @staticmethod
    def _content_type(ct):
        return 'Content-Type: {}\r\n'.format(ct).encode('utf-8')

    def __bytes__(self):
        """Return a byte-string representing the form data,
        including attached files.
        """
        buffer = io.BytesIO()
        boundary = b'--' + self.boundary + b'\r\n'

        # Add the form fields
        for name, value in self.form_fields:
            buffer.write(boundary)
            buffer.write(self._form_data(name))
            buffer.write(b'\r\n')
            buffer.write(value.encode('utf-8'))
            buffer.write(b'\r\n')

        # Add the files to upload
        for f_name, filename, f_content_type, body in self.files:
            buffer.write(boundary)
            buffer.write(self._attached_file(f_name, filename))
            buffer.write(self._content_type(f_content_type))
            buffer.write(b'\r\n')
            buffer.write(body)
            buffer.write(b'\r\n')

        buffer.write(b'--' + self.boundary + b'--\r\n')
        return buffer.getvalue()



def get_req(data):
    pass

def http_exceptions_handler(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except KeyboardInterrupt:
            raise
        except urllib.error.URLError as error:
            if isinstance(error.reason, socket.timeout):
#                logging.error('socket timed out - URL %s', url)
                logging.error('socket timed out')
                info = "E: {}".format(sys.exc_info())
    #            await NB.send_message(MY_ID, info)
                logger.error(info)
            else:
                logging.error('some other error happened')
                info = "E: {}".format(sys.exc_info())
                logger.error(info)
        except urllib.error.HTTPError as error:
            logging.error('Data not retrieved because %s\nURL: %s', error, url)
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except urllib.error.URLError:
            logger.warning("can not send")
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except socket.timeout:
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except UnicodeDecodeError as e:
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except Exception as e:
            info = "E: {}".format(sys.exc_info())
            info = f"http exception: {e=}"
            logger.error(info, exc_info=True)
            @my_exceptions_handler
            async def _():
                raise e
            return await _()

    return wrapper






def get_from_url(url):
    return data2url(data=None, url=url)




@http_exceptions_handler
def data2url(data="test", url="https://fars.ee/", filename="bin", fieldname="c"):
    # https://pymotw.com/3/urllib.request/#uploading-files
    if not data:
        req = request.Request(url=url)
    if isinstance(data, str):
#        data = {"content": data}
        data = {"c": data}
        req = request.Request(url=url, data=parse.urlencode(data).encode('utf-8'))
    elif isinstance(data, bytes):
        if not filename:
            filename = "None"
        form = MultiPartForm()
#            form.add_file("content", "test.jpg", data)
        form.add_file(fieldname, filename, data)
        data = bytes(form)
        req = request.Request(url=url, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))

    elif type(data) == dict:
        pass
        return
    else:
        # not support
        return

    req.add_header('User-agent', 'Chrome Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) Apple    WebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')

    #  data={"text":"test","username":"null", "gateway":"gateway0" }

    #  data=str(data)
    #  data=urlencode(data)#将字典类型的请求数据转变为url编码
    #  data=urllib.parse.quote(json.dumps(data), safe="{}:\\\"',+ ")
    #  data=urllib.parse.quote_plus(json.dumps(data))
    #  data=data.encode('ascii')#将url编码类型的请求数据转变为bytes类型
    #  with urllib.request.urlopen(url, data) as res:
    #  with urllib.request.urlopen(req_data) as res:
    #  mp("send headers: "+str(res.headers))

    with urllib.request.urlopen(req, timeout=30) as r:
        res = r.read().decode()
        return res



#def pastebin(data, url="https://fars.ee/", *args, **kwargs):
def __pastebin(data, url="https://fars.ee/?u=1", *args, **kwargs):
    res = data2url(data, url=url, *args, **kwargs)
    if not res:
        res = data2url(data, url=url, *args, **kwargs)
        if not res:
            return
    url = res.strip()
    return url



"""
local IPFS_GATEWAYS
https://ipfs.infura.io:5001 https://HASH_CID.ipfs.infura-ipfs.io/ 1 1
https://snap1.d.tube GATEWAY_URL/ipfs/HASH_CID 0 0

https://infura-ipfs.io GATEWAY_URL/ipfs/HASH_CID 0 1
https://ipfs.smartholdem.io GATEWAY_URL/ipfs/HASH_CID 0 0
https://ipfs1.pixura.io GATEWAY_URL/ipfs/HASH_CID 0 0

http://127.0.0.1:5001 http://127.0.0.1:8080/ipfs/HASH_CID 0 0
https://wtfipfs.tk GATEWAY_URL/ipfs/HASH_CID 0 0

"""
#        hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL/api/v0/add${cid_version}" | jq -r '.Hash' )

def ipfs_add(data, filename=None, url="https://ipfs.infura.io:5001/api/v0/add?cid-version=1", *args, **kwargs):
    res = data2url(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
    if not res:
        logger.error("fail to ipfs")
        return
    url = res.strip()
#    url = json.loads(url)
    try:
        url = load_str(url)
    except SyntaxError as e:
        put(e)
        return url
#    url = url["Hash"]
    url = "https://{}.ipfs.infura-ipfs.io/".format(url["Hash"])
    if filename:
    #    url += "?filename={}".format(parse.urlencode(filename))
        url += "?filename={}".format(parse.quote(filename))
    return url



def Jaccard(model, reference):  # terms_reference为源句子，terms_model为候选句子
    import jieba
    terms_reference = jieba.cut(reference)  # 默认精准模式
    terms_model = jieba.cut(model)
    grams_reference = set(terms_reference)  # 去重；如果不需要就改为list
    grams_model = set(terms_model)
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp = temp + 1
    fenmu = len(grams_model) + len(grams_reference) - temp  # 并集
    try:
        jaccard_coefficient = float(temp / fenmu)  # 交集
    except ZeroDivisionError:
        print(model, reference)
        return 0
    else:
      return jaccard_coefficient


def my_strip(text):
    tmp = ""
    for line in text.splitlines():
        if not line:
            break
        else:
            if line.startswith("> "):
                if tmp:
                    break
                else:
                    continue
            if not tmp and len(line) > 5:
                tmp = line
                break
            elif not tmp and url_only_re.match(line):
                tmp = line
                break
            elif url2_md_re.match(line):
                break
            elif pic_md_re.match(line):
                break
            else:
                tmp += "\n"+line
                break
    return tmp.strip()


def my_jaccard(new, ref, check_sub=False, *, need=0.8):
    if not ref:
        return False
    if not new:
        return False
    if new == ref:
        return True
    new = my_strip(new)
    ref = my_strip(ref)
    if not ref:
        return False
    if not new:
        return False
    if new == ref:
        return True
    new = list(new.lower())
    #  new = set(new)
    ref = list(ref.lower())
    #  ref = set(ref)

    if check_sub:
        ref = set(ref)
        tmp = 0
        for i in new:
            if i in ref:
                tmp += 1
        fenmu = len(new)
    else:
        tmps = []
        for j in range(len(new)):
            if j/len(new) > 1 - need:
                break
            tmp = 0
            it = iter(ref)
            try:
                #  for i in new[j:]:
                for i in new[j:]:
                    while next(it) != i:
                        pass
                    tmp += 1
            except StopIteration:
                pass
            #  print(tmp)
            tmps.append(tmp)
        tmp = max(tmps)
        fenmu = len(ref) + len(new) - tmp

    if fenmu <= 0:
        return 0
    s = float(tmp / fenmu)
    #  if s*(1-1/(10+len(ref))) >= need:
    if s >= need:
        #  print(f"check ok: {new}=={ref}>>{s}")
        return True
    #  print(f"check fail: {new}=={ref}>>{s}")
    return False




import aiohttp


QUEUE_FOR_HTTP = asyncio.Queue()

@my_exceptions_handler
async def yhttp():

    async with aiohttp.ClientSession() as session:
        while True:
            url = await QUEUE_FOR_HTTP.get()
            async with session.get(url) as response:

                print("All:", response)
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.text()
                print("Body:", html[:15], "...")
                yield html

#yhttp = yhttp()

session = None

async def init_aiohttp_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()
        logger.warning("a new session")
    else:
        logger.debug("session existed")
    return session



UA = 'Chrome Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) Apple    WebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'

@my_exceptions_handler
async def http(url, method="GET", return_headers=False, **kwargs):
    await init_aiohttp_session()

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

    try:
        res = await session.request(url=url, method=method, **kwargs)
    except asyncio.TimeoutError as e:
        raise
    async with res:
        # print("All:", res)
#        res.raise_for_status()
        if res.status == 304:
            logger.warning(f"http status: {res.status} {res.reason}\nurl: {res.url}")
            logger.warning("ignore: {}".format(await res.text()))
            if return_headers:
                return None, res.headers
            else:
                return
        if res.status != 200:
#            logger.error(res)
#            put(str(res))
            html = f"error http status: {res.status} {res.reason}\nurl: {res.url}\nheaders: {res.headers}"
            put(html)
            if return_headers:
                return html, res.headers
            else:
                return html
        # print(type(res))
        # print("Status:", res.status)
        # print("Content-type:", res.headers['content-type'])
        # print("Content-Encoding:", res.headers['Content-Encoding'])
        # print('Content-Length:', res.headers['Content-Length'])
        # print('Content-Length:', res.headers['Content-Length'])
            # print(res)
            # print("q: ", res.request_info)
            # print("a: ",  res.headers)

        try:
            data = None
            html = None
            if 'Content-Length' in res.headers and int(res.headers['Content-Length']) > HTTP_RES_MAX_BYTES:
                logger.warning(f"skip: too big: {url}")
            elif 'Transfer-Encoding' in res.headers and res.headers['Transfer-Encoding'] == "chunked":

                #  async for data in res.content.iter_chunked(HTTP_RES_MAX_BYTES):
                #      break
                data = b""
                async for tmp, _ in res.content.iter_chunks():
                    data += tmp
                    if len(data) > HTTP_RES_MAX_BYTES:
                        break
            else:
            # if res.headers['content-type'] == "text/plain; charset=utf-8":
                #  data = await res.read()
                data = await res.content.read(HTTP_RES_MAX_BYTES)

            if data is not None:
                #  try:
                #      if "Content-Encoding" in res.headers:
                #          if res.headers['Content-Encoding'] == "gzip":
                #              print("use gzip")
                #              data = gzip.decompress(data)
                #          elif res.headers['Content-Encoding'] == "deflate":
                #              print("use zlib")
                #              data = zlib.decompress(data)
                #          elif res.headers['Content-Encoding'] == "br":
                #              print("use br")
                #              data = brotli.decompress(data)
                #          elif res.headers['Content-Encoding']:
                #              logger.error("url: {}\nunknown encoding: {}".format(url, res.headers['Content-Encoding']))
                #              put("url: {}\nunknown encoding: {}".format(url, res.headers['Content-Encoding']))
                #              #  return data
                #  except Exception as e:
                #      logger.warning(e)
                #      put(e)

                # if "text/plain" in res.headers['content-type']:
                if "text" in res.headers['content-type']:
                    # return await res.text()
                    html = data.decode(errors='ignore')
                else:
                    # html = data.decode(errors='ignore')
                    html = data.decode()
        except ClientPayloadError as e:
            try:
                if "data" in locals():
                    html = data.decode(errors='ignore')
                else:
                    html = None
                my_traceback(e, put=True, ex=url)
            except UnicodeDecodeError as e:
                my_traceback(e, put=True, ex=url)
                html = None
        except UnicodeDecodeError as e:
            print("res.headers: ",  res.headers)
            print(f"res data: {data[:64]} 64/{len(data)}")
            logger.warning(f"decode failed: {url}\nerror: {e}")
            #  put(f"decode failed: {url}")
            if url.startswith("https://www.ptt.cc/"):
                my_traceback(e, put=True, ex=url)
            html = data
        if return_headers:
            return html, res.headers
        else:
            return html



async def nbnhhsh(text):
    #  res=$( curl -s -XPOST -H 'Content-Type: application/json' -d "$(get_text "$@")" https://lab.magiconch.com/api/nbnhhsh/guess )
    #  {"text":"${text}"}
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    data = {"text": text}
    headers = {}
    res = await http(url=url, method="POST", json=data, headers=headers)
    #  return res
    if res:
        #  return load_str(res)
        res = load_str(res)
        if res:
            res = res[0]
        else:
            return str(res)
        # [{'name': 'wtf', 'trans': ['what the fuck', '我头发', '五套房', ' 委托方']}]
        # [{"name":"200","inputting":[]}]
        info = f"**{res['name']}**: "
        if 'trans' in res:
            info += f"{','.join(res.get('trans'))}"
        else:
            info += f"None"
        return info
    else:
        return str(res)

async def wtf(text):
    "muxiaoguo api"
    #  res=$( curl -s -XPOST -H 'Content-Type: application/json' -d "$(get_text "$@")" https://lab.magiconch.com/api/nbnhhsh/guess )
    #  {"text":"${text}"}
    #  url = "https://api.muxiaoguo.cn/api/hybrid?word=wtf"
    url = "https://api.muxiaoguo.cn/api/hybrid"
    data = {"word": text}
    headers = {}
    res = await http(url=url, method="GET", params=data, headers=headers)
    #  return res
    #  return load_str(res)
    if res:
        res = load_str(res)
    # {"code":200,"msg":"success","data":[{"name":"swag","desc":"swag在 美式口语里面是 swagger的简写。 是一种自信，昂首阔步的心
        if res["code"] == 200:
            #  return res
            tmp = []
            for i in res["data"]:
                tmp.append("**{}**: {}".format(i['name'],i['desc']))
                if i["imgurl"] is not None:
                    tmp[-1] += f" {i['imgurl']}"
                if i["name"] == text:
                    return tmp[-1]
            info = "\n==\n".join(tmp)
            return info
        else:
            return str(res)
    else:
        return str(res)


pb_list = {
        "anon": ["https://api.anonfiles.com/upload", "file"],
        "0x0": ["https://0x0.st/", "file"],
        "fars": ["https://fars.ee/?u=1", "c"]
        }



from aiohttp import FormData
from aiohttp.client_exceptions import ClientPayloadError
from io import BufferedReader, TextIOWrapper, BytesIO

#async def pastebin(data="test", filename=None, url="https://fars.ee/?u=1", fieldname="c", extra={}, **kwargs):
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
#    data = {"content": data}
#        data = zlib.compress(data)
#        headers = {'Content-Encoding': 'deflate'}
#        data = gzip.compress(data.encode())
#        headers = {'Content-Encoding': 'gzip'}
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
#    elif type(data) == aiohttp.formdata.FormData:
    elif type(data) == FormData:
        pass
    else:
        return

    res = await http(url=url, method="POST", data=data, headers=headers,  **kwargs)
#        res = res + "." + filename.split(".")[-1]
    return res.strip()


def file_for_post(data, filename=None, fieldname="c", mimetype=None, **kwargs):
#    file = aiohttp.FormData()
    file = FormData(kwargs)
    if filename and not mimetype:
        mimetype = mimetypes.guess_type(filename)[0]
        if not mimetype:
            mimetype = 'application/octet-stream'
#    for i in kwargs:
#        file.add_fields((i, kwargs[i]))
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
        #      filename = "0.txt"
        #  data = compress(data, "zst")
        #  if not filename:
        #      filename = "bin_zst.zip"
        if not filename:
            filename = "txt_not_zip.zip"
    extra = {}
    if not filename and filename.split(".")[-1] not in allowed:
        #  extra = { "randomname": "on" }
        filename += "_not_zip.zip"
    fieldname = "file"
    res = await pastebin(data, url=url, filename=filename, fieldname=fieldname, extra=extra, *args, **kwargs)
    return res

async def transfer(data, filename=None, *args, **kwargs):
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
#    return load_str(res)["link"]
    try:
        d = load_str(res, no_ast=True)
    except SyntaxError as e:
        info = f"{e=}\n\n{url}"
        put(info)
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
#            "userhash": "",
            "reqtype": reqtype
            }
    if tmp:
        extra["time"] = "72h"
    res = await pastebin(data, url=url, filename=filename, fieldname=fieldname, extra=extra, *args, **kwargs)
    if res:
        if "https://files.catbox.moe/" in res:
            res = res.replace("https://files.catbox.moe/", "https://de.catbox.moe/")
        return res




async def ipfs_add(data, filename=None, url="https://ipfs.infura.io:5001/api/v0/add?cid-version=1", *args, **kwargs):
#    res = data2url(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
    if isinstance(data, str):
        data = data.encode()
    data = {"file": data}
    res = await http(url=url, method="POST", data=data, **kwargs)
    if not res:
        logger.error("fail to ipfs")
        return
    url = res.strip()
#    url = json.loads(url)
    try:
        url = load_str(url)
    except SyntaxError as e:
        info = f"{e=}\n\n{url}"
        put(info)
        return
#    url = url["Hash"]
    url = "https://{}.ipfs.infura-ipfs.io/".format(url["Hash"])
    if filename:
    #    url += "?filename={}".format(parse.urlencode(filename))
        url += "?filename={}".format(parse.quote(filename))
#    await session.close()
    return url





#from lxml.html.clean import clean_html
from lxml.html.clean import Cleaner
#cleaner = Cleaner(style=False, kill_tags=["style"], remove_tags=["div"], add_nofollow=True)
#cleaner = Cleaner(style=False, kill_tags=["style"], remove_tags=["div", "body", "span", "input"], add_nofollow=True, forms=False)
#cleaner = Cleaner(style=False, kill_tags=["style", "a"], remove_tags=["div", "body", "span", "input", "h1"], add_nofollow=True, safe_attrs_only=True)
cleaner = Cleaner(remove_unknown_tags=False, style=False, annoying_tags=False, allow_tags=["a", "blockquote", "br", "em", "figure", "h3", "h4", "img", "p", "strong"], add_nofollow=True)


def my_convert_for_html(html):
    html = cleaner.clean_html(html)[5:-6]

    tmp = html.splitlines()
    title = None
    for line in tmp.copy():
        line = line.strip()
        if line:
            if line.startswith("<"):
                if not title:
                    title = "no title"
                break
            else:
                if not title:
                    title = line
        tmp.pop(0)

    html = "\n".join(tmp)
    html = html.strip()
    return html, title



#import asyncio
from telegraph.aio import Telegraph

telegraph = None


async def save_to_telegraph(title, html=None):

    if html is None:
        text = title
        if url_only_re.match(text):
            title = "title"
            html = await http(url=text)
#            _, title = my_convert_for_html(html)
#            html = convert_html_to_telegraph_format(html, output_format="html_string")
            html, title = my_convert_for_html(html)
            if html.startswith("<body>"):
                html = html[6:-7]

    #        print(html)
            if html:
                if not title:
                    title = "no title"
                else:
                    title = title.strip()[:64]
                link = await save_to_telegraph(title, html)
            else:
                from ..modules.an import get_iv_from_bot
                link = await get_iv_from_bot(text)
                if link:
                    link = link.split(" ")[-1]
        else:
            title = "text"
            html = f'<p>{text}</p>'
            link = await save_to_telegraph(title, html)
        return link
    else:
        global telegraph
        from .. import BOT_NAME as NAME
        if telegraph is None:
            #  await init_telegraph()
            telegraph = Telegraph()
    #        from .. import MY_NAME
            #  from .. import MY_NAME as NAME
            print(await telegraph.create_account(short_name=NAME, author_name=NAME, author_url=f"https://t.me/{NAME}"))
    #    response = await telegraph.create_page( 'Hey', html_content='<p>Hello, world!</p>',)
        #  print(title, html)
        #  response = await telegraph.create_page(title, html_content=html)
        response = await telegraph.create_page(title, html_content=html, author_name=NAME, author_url=f"https://t.me/{NAME}")
    #    print(response)
    #    print(response['url'])
        if response:
            return response['url']




import aiofiles


async def file_read(path, *args, **kwargs):
    async with aiofiles.open(path, *args, **kwargs) as file:
        return await file.read()



#asyncio.run(main())


def tmp_save(data, ex=""):
    from ..config import SH_PATH
    name = "{}/{}{}".format(SH_PATH, time.time(), ex)
    if not isinstance(data, bytes):
        logger.error("need bytes")
        return
    data = bytes(data)
    with open(name, "wb") as file:
        file.write(data)
    return name


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



# https://dev.gajim.org/gajim/gajim-plugins/-/blob/master/omemo/backend/aes.py

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.backends import default_backend

def aes_decrypt(key, iv, tag, data):
    decryptor = Cipher(
        algorithms.AES(key),
        GCM(iv, tag=tag),
        backend=default_backend()).decryptor()
    return decryptor.update(data) + decryptor.finalize()

def aes_decrypt_file(key, iv, payload):
    data = payload[:-16]
    tag = payload[-16:]
    return aes_decrypt(key, iv, tag, data)





async def test():
    print(await nbnhhsh("wtf"))
    print(await wtf("wtf"))
    return
    test_varname()
    return
    print(await http("https://wtfismyip.com/json"))
    return
    t ='{"test": 1}'
    print(load_str(t))
    print(await http("https://wtfismyip.com/json"))
    print(await http("https://fars.ee/3cua"))
    with open("test.jpg", "rb") as file:
        data = file.read()
        print(await pb(data, filename="test.jpg"))
        await asyncio.sleep(5)
        print(await pb("test text"))
        await asyncio.sleep(5)
        print(await pb(data))

    await session.close()
    return
    with open("test.jpg", "rb") as file:
        data = file.read()
        print(await catbox(data, filename="test.jpg"))
        print(await put_0x0(data, filename="test.jpg"))
    print(await catbox("test text"))
    print(await put_0x0("test text"))

    return
    from lxml.html.clean import Cleaner
#    cleaner = Cleaner(style=False, kill_tags=["style"], remove_tags=["div", "body", "span", "input"], add_nofollow=True, forms=False)
    cleaner = Cleaner(style=False, kill_tags=["style"], remove_tags=["div", "body", "span", "input"], add_nofollow=True)


    title = "test"
    html = await http(url="https://www.v2ex.com/t/834962")
    html = cleaner.clean_html(html)[5:-6]
    link = await save_to_telegraph(title, html)
    return
    res = await http("https://bafkreiguywmpc4dftuaevita4mxokkatpshvp26bgxczu5vb4yi2yprutu.ipfs.infura-ipfs.io/?filename=photo_2022-02-18_11-19-17.jpg")
    res = await http("https://fars.ee/nxD2")
    print(res)



if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
#    print(data2url("test"))
    asyncio.run(test())
elif 0:
    with open("test.jpg", "rb") as file:
        data = file.read()
        asyncio.run(ipfs_add(data, filename="test.jpg"))
elif 0:
    asyncio.run(ipfs_add("12345"))
elif 0:
    asyncio.run(pb(data))
    asyncio.run(pb("test"))
    asyncio.run(http("http://python.org"))
    asyncio.run(save_to_tg())
    with open("test.jpg", "rb") as file:
        data = file.read()
        print(ipfs_add(data, filename="test.jpg"))
elif 0:
    print(pastebin("test"))
    with open("test.jpg", "rb") as file:
        data = file.read()
        print(data2url(data))

elif 0:
    print(__ennum())
    test = 252362411652008
    test = 25236241
    test = 1605913233762902549674297492922334083602989773277118769602277444770171056
    s = ennum(test)
    k = denum(s)
    print("{}: {} is {}".format(test, repr(s), k))
    print(denum_auto("'> T liqsliu\u200e\u206d\ufeff\u200b"))
elif __package__ != "":
    print('{} 运行'.format(__file__))
    from .html_to_telegraph_format import convert_html_to_telegraph_format
    # from ..telegram import put
else:
    print('{} 运行'.format(__file__))



