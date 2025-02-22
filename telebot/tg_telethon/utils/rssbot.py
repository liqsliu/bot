from .tools import SH_PATH

from .telegram import MSG_QUEUE
from .telegram import MAX_MSG_LEN
from .telegram import MAX_MSG_LINE

from .telegram import tg_exceptions_handler

from .config import cid_wtfipfs, cid_ipfsrss, cid_tw, cid_ipfsrss, cid_btrss, cid_fw

#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from ..bot import *
#from ..utils.telegram import tg_exceptions_handler

#import logging
logger = logging.getLogger(__name__)
mp = logger.info

import asyncio

#from urllib.parse import urlencode
import feedparser

import threading
import os
from datetime import timedelta
import time
#from time import time
#from time import strftime
#from time import strptime

import datetime
import traceback

from .tools import get_my_key, SH_PATH
from ..utils.config import save_config


feed_list = CONFIG[2]

#time_format="%Y%m%d_%H%M%S%z" #strptime() can not identify %z , zoneinfo will be -1(unknown)
#time_format="%Y%m%d_%H%M%S%Z" #zoneinfo is not correct, always is HKT
time_format = "%Y%m%d_%H%M%S"


#https://www.codenong.com/13297077/
async def max_entry_date(feed):
    #  if 'published', 'updated' ]:
    #  entry_pub_dates = (e.get('published_parsed') for e in feed.entries)
    #  entry_pub_dates = (e.get('updated_parsed', e.get('published_parsed',time.localtime())) for e in feed.entries)
    entry_pub_dates = (e.get('updated_parsed',
                             e.get('published_parsed', time.gmtime()))
                       for e in feed.entries)
    #  entry_pub_dates = tuple(e for e in entry_pub_dates if e is not None)
    entry_pub_dates = tuple(e for e in entry_pub_dates if e != None)
    if len(entry_pub_dates) > 0:
        return max(entry_pub_dates)
#  return None
#  return time.localtime()
    return time.gmtime()


#async def send_entry_task(cid=0):
#  t=threading.Thread(target=send_entry_task_1, kwargs={"cid":cid})
#  t.start()
#  t.join()
#  while t.is_alive():
#    await asyncio.sleep(5)

#def send_entry_task_1(cid=0):
#  asyncio.run(send_entry_task_2(cid))
MAX_AUTO_MSG_TASK_TIME = 300

entry_task = []
feeds = []
t_1_tasks = []
#[cid,info,False,"htm",files]

#need_wait=False
need_wait = 0


async def send_entry_task(cid=cid_btrss):
    global entry_task
    global need_wait

    #  while True:
    #    for msg in entry_task.copy():
    #  for i in range(0,MAX_AUTO_MSG_TASK_TIME,3):
    i = 0
    await asyncio.sleep(1)
    while i < MAX_AUTO_MSG_TASK_TIME:
        if len(entry_task) > 512:
            entry_task = []
            await NB.send_message(MY_ID,
                                  "E: waiting entry num > 512, cleared!")

        msg = None
        for msg in entry_task:
            if msg[0] == MY_ID:
                entry_task.remove(msg)
#        elif msg[0] == cid_btrss and cid == cid_btrss:
            elif msg[0] != cid:
                msg = None
                continue
            else:
                entry_task.remove(msg)
            break

        if msg:
            logger.info("I: task got a msg")
            try:
                i = 0
                while need_wait:
                    await asyncio.sleep(5)
                    i += 1
                    if i > 512:
                        await NB.send_message(
                            MY_ID, "E: send_entry_task wait too long, wtf?")
                        break

                if len(msg) == 2:
                    #          await bot.send_message(msg[0], msg[1],parse_mode="htm")
                    await NB.send_message(msg[0], msg[1], parse_mode="htm")
                elif len(msg) == 3:
                    await NB.send_message(msg[0],
                                          msg[1],
                                          parse_mode="htm",
                                          link_preview=msg[2])
                elif len(msg) == 4:
                    await NB.send_message(msg[0],
                                          msg[1],
                                          parse_mode=msg[3],
                                          link_preview=msg[2])
                elif len(msg) == 5:
                    # tw_fav with files
                    #      msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md')
                    if len(msg[4]) == 1:
                        await MB.send_file(msg[0],
                                           file=msg[4][0],
                                           caption=msg[1],
                                           parse_mode=msg[3],
                                           link_preview=msg[2])
                    else:
                        await NB.send_file(msg[0],
                                           file=msg[4],
                                           caption=msg[1],
                                           parse_mode=msg[3],
                                           link_preview=msg[2])
                else:
                    await NB.send_message(MY_ID,
                                          "E: wtf entry_task msg:" + str(msg))


#        except telethon.errors.rpcerrorlist.FloodWaitError as e:
            except FloodWaitError as e:
                #        need_wait=True
                need_wait += 1

                #          entry_task.append(msg)
                entry_task.insert(0, msg)

                info = "E: " + str(sys.exc_info(
                )[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
                    sys.exc_info())
                print(info)

                await asyncio.sleep(e.seconds)
                await asyncio.sleep(5)

                #        need_wait=False
                need_wait -= 1
                if need_wait < 0:
                    need_wait = 0
            except:
                info = "E: " + str(sys.exc_info(
                )[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
                    sys.exc_info())
                await NB.send_message(
                    MY_ID, "E: entry_task: msg: " + str(msg) + "\n==\n" + info)
            i = 0  # for loop
        else:
            i += 3
        await asyncio.sleep(3)


async def send_entry(entry, url):
    #      threading.Thread(target=send_entry_task).start()
    global entry_task
#    info = entry.link + "\n<b>" + entry.title + "</b>"
    info = "<b><a href=\""+entry.link + "\">" + entry.title + "</a></b>"

    info += "\n" + entry.get(
        "updated", entry.get("published", "E: wtf!"))
    info2 = entry.get("description",
                      entry.get("content", entry.get("summary", "")))
    info = info + "\n" + info2
    if len(info) > 4096:
        info = info[0:4090] + "..."


#    await bot.send_message(MY_ID, info,parse_mode="htm")
    if len(feed_list[url]) == 3:
        #      await bot.send_message(cid_btrss, info,parse_mode="htm")
        #    entry_task.append([cid_btrss,info])
        msg = [0, cid_btrss, info, {"parse_mode": "htm"}]
        await MSG_QUEUE.put(msg)
    elif len(feed_list[url]) < 3:
        return
    else:
        for cid in feed_list[url][3:]:
            if info2:
                #          await bot.send_message(cid, info,parse_mode="htm",link_preview=False)
                #        entry_task.append([cid,info,False])
                msg = [
                    2, cid, info, {
                        'link_preview': False,
                        "parse_mode": "htm"
                    }
                ]
            else:
                #          await bot.send_message(cid, info,parse_mode="htm")
                #        entry_task.append([cid,info])
                msg = [0, cid, info, {"parse_mode": "htm"}]

            await MSG_QUEUE.put(msg)


async def _get_one_feed(url, **kwargs):
    global feeds
    #    d=feedparser.parse(url,etag=status[0],modified=status[1],request_headers=request_headers)
    d = 0
    try:
        if "etag" in kwargs and "modified" in kwargs:
            d = feedparser.parse(url,
                                 etag=kwargs["etag"],
                                 modified=kwargs["modified"],
                                 request_headers=kwargs["request_headers"])
        elif "etag" in kwargs:
            d = feedparser.parse(url,
                                 etag=kwargs["etag"],
                                 request_headers=kwargs["request_headers"])
        elif "modified" in kwargs:
            d = feedparser.parse(url,
                                 modified=kwargs["modified"],
                                 request_headers=kwargs["request_headers"])
        else:
            d = feedparser.parse(url,
                                 request_headers=kwargs["request_headers"])
    except:
        return False
    if d:
        if hasattr(d, 'status'):
            if d.status != 304:
                #        feeds.append(dict(d).copy())
                if hasattr(d.feed, 'link'):
                    feeds.append(d)
                    mp("I: got " + url)
                    return True
    return False


async def get_feed():
    mp("I: new update_feed lood")
    #  for url in feed_list:
    for url in feed_list.copy():
        global t_1_tasks
        t_1_tasks = []
        for j in asyncio.all_tasks():
            if t_1.is_alive():
                t_1_tasks.append(j.get_name())
        if url not in feed_list:
            continue
        status = feed_list[url]
        d = {}
        for j in asyncio.all_tasks():
            #        tasks.append(j.get_name())
            if j.get_name() == url:
                print("E: rss timeout: " + url)
                j.cancel()
                await asyncio.sleep(5)
                if j.done():
                    print("E: rss stoped: " + url)
                    break
                else:
                    print("E: can't stop rss:  " + url)
                    j.cancel()
                    break
        if status[0] == "disable" or status[0] == 1:
            continue
        mp("I: get " + url)
        #    if status[0] == "updated" or status[0] == "published":
        #      if status[0] == 0 or status[1] == 0:
        #      continue
        request_headers = {'Cache-control': 'max-age=600'}
        if status[0] and status[1]:
            #  t.start()
            #  t.join()
            #  while t.is_alive():
            #        d=feedparser.parse(url,etag=status[0],modified=status[1],request_headers=request_headers)
            asyncio.create_task(get_one_feed(url,
                                             etag=status[0],
                                             modified=status[1],
                                             request_headers=request_headers),
                                name=url)
        elif status[0]:
            #        d=feedparser.parse(url,etag=status[0],request_headers=request_headers)
            asyncio.create_task(get_one_feed(url,
                                             etag=status[0],
                                             request_headers=request_headers),
                                name=url)
        elif status[1]:
            #        d=feedparser.parse(url,modified=status[1],request_headers=request_headers)
            asyncio.create_task(get_one_feed(url,
                                             modified=status[1],
                                             request_headers=request_headers),
                                name=url)
        else:
            #        d=feedparser.parse(url)
            asyncio.create_task(get_one_feed(url,
                                             request_headers=request_headers),
                                name=url)


#      await asyncio.sleep(1)
#      await asyncio.sleep(len(asyncio.all_tasks())/5+len(entry_task)/2+1)
#        time.sleep(3)
#  await save_config()
        await asyncio.sleep(len(asyncio.all_tasks()) / 2)


def get_feed_t1():
    logger.debug("I: new update_feed lood")
    for url in feed_list.copy():
        global t_1_tasks
        if url not in feed_list:
            continue
        status = feed_list[url]
        d = {}
        if status[0] == "disable" or status[0] == 1:
            continue
        logger.debug("fetch: " + url)
        request_headers = {'Cache-control': 'max-age=600'}
        try:
            if status[0] and status[1]:
                d = feedparser.parse(url,
                                     etag=status[0],
                                     modified=status[1],
                                     request_headers=request_headers)
            elif status[0]:
                d = feedparser.parse(url,
                                     etag=status[0],
                                     request_headers=request_headers)
            elif status[1]:
                d = feedparser.parse(url,
                                     modified=status[1],
                                     request_headers=request_headers)
            else:
                d = feedparser.parse(url, request_headers=request_headers)
        except:
            info = "E: " + str(sys.exc_info(
            )[0]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
                sys.exc_info())
            logger.info(info)
            #      asuncio.run(bot.send_message(MY_ID, info))
            info = "E: get_feed_t1 url: " + url + "\n==\n" + str(
                sys.exc_info())
            logger.warning(info)
            from .telegram import put
            put(info)
            continue
        if d:
            if hasattr(d, 'status'):
                if d.status != 304:
                    #        feeds.append(dict(d).copy())
                    if hasattr(d.feed, 'link'):
                        global feeds
                        feeds.append(d)
                        logger.info("I: got " + url)


# not use
async def ___get_feed_loop_bu():
    while True:
        mp("I: new loop: get_feed")
        await get_feed()
        await save_config()
        mp("I: loop end: get_feed")


#    await asyncio.sleep(60)
#    await asyncio.sleep(30/len(feed_list)+len(feeds)+len(entry_task)+1)


#def get_feed(status,url):
def get_feed_loop():
    global entry_task
    entry_task.append([MY_ID, "get_feed_loop start", False, None])
    #  await start_send_entry_task(cid=MY_ID)

    #https://stackoverflow.com/questions/9772691/feedparser-with-timeout
    import socket
    socket.setdefaulttimeout(300)

    from .telegram import put
    while True:
        logger.info("I: new loop: get_feed")
        put("new loop, get_feed")
        try:
            get_feed_t1()
        except:
            logger.error("E: get_feed_t1 raise an Exception")
            info = "E: " + str(sys.exc_info(
            )[0]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
                sys.exc_info())
            print(info)
            #      asuncio.run(bot.send_message(MY_ID, info))
            entry_task.append([MY_ID, info, False, None])


#    if not t_1.is_alive():
#      print("I: thraed 1 is dead")
#      await save_config()
#      await asyncio.sleep(5)
#https://stackoverflow.com/questions/46992496/runtimeerror-threads-can-only-be-started-once
#      t_1=threading.Thread(target=thread_1,daemon=True)
#      t_1.start()

        logger.debug("I: loop end: get_feed")
        #    time.sleep(60)
        time.sleep(60 / len(feed_list) + len(tasks) + len(feeds) +
                   len(entry_task) + 30)

tasks = []


@tg_exceptions_handler
async def parse_feed_loop():
    global feed_list
    global feeds
    #  t=threading.Thread(target=get_feed, kwargs={"status":status,"url":url})
    #  task_name="get_feed"
    #  asyncio.create_task(get_feed(),name=task_name)
    global tasks
    while True:
        tasks = []
        for t in asyncio.all_tasks():
            if t.get_name()[0] == "-":
                tasks.append(t.get_name())
        mp("parse start")
        await asyncio.sleep(5)
        await save_config()
        while True:
            await asyncio.sleep(1)
            #      if threading.active_count() == 1:
            #        if len(feeds) == 0:
            #          break
            if len(feeds) == 0:
                break
            d = feeds[0]
            feeds.pop(0)
            #      feeds.remove(d)
            #    elif status[0] == "published" or status[0] == "updated":

            #      url=d.feed.link
            url = d.feed.title_detail.base
            if url not in feed_list:
                #        url=d.feed.link
                for link in d.feed.links:
                    if link.rel == "self":
                        url = link.href
                        break
                if url not in feed_list:
                    continue
            status = feed_list[url]
            if d.get('etag', 0) or d.get('modified', 0):
                status[0] = d.get('etag', 0)
                status[1] = d.get('modified', 0)

            url_count = 0
            url_max = int(720 / (20 + len(d.entries)) + 2)
            #      url_max=len(d.entries)
            if type(status[2]) != str:
                await NB.send_message(MY_ID, "E: rss url data error: " + url)
                continue
            old_max_date = (
                datetime.datetime.strptime(status[2], time_format) -
                datetime.timedelta(hours=8)).utctimetuple()
            new_max_date = ()
            for entry in d.entries:
                if entry.get("updated_parsed",
                             entry.get("published_parsed",
                                       old_max_date)) > old_max_date:
                    await send_entry(entry, url)
                    if new_max_date:
                        new_max_date = max(
                            (new_max_date,
                             entry.get(
                                 "updated_parsed",
                                 entry.get("published_parsed", old_max_date))))
                    else:
                        new_max_date = entry.get(
                            "updated_parsed",
                            entry.get("published_parsed", old_max_date))
                    url_count += 1
                    #          if url_count > url_max:
                    if False:
                        await NB.send_message(
                            cid_btrss, "W: too many rss : " + url + "\n" +
                            str(len(d.entries)) + " > " + str(url_max))
                        break
                else:
                    continue
            if new_max_date and new_max_date != old_max_date:
                if url not in feed_list:
                    continue
                feed_list[url][2] = (
                    datetime.datetime(*(new_max_date[0:6])) +
                    datetime.timedelta(hours=8)).strftime(time_format)
        #      await save_config() # no need save too early, or will be telethon.errors.rpcerrorlist.FloodWaitError:
        #  if config_save_buffer != [auto_forward_list,auto_msg_list,feed_list]:


#    await save_config()
    mp("parse stop")


def thread_2():
    try:
        asyncio.run(mt_read())


#    mt_read()
    except:
        info = "E: thraed 2 raise an Exception: " + str(sys.exc_info(
        )[0]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
            sys.exc_info())
        print(info)
        #    await bot.send_message(MY_ID, info)
        global entry_task
        entry_task.append([MY_ID, info, False])


def thread_1():
    try:
        #  asyncio.run(parse_feed())
        #    asyncio.run(get_feed_loop())
        #    get_feed_t1()
        get_feed_loop()
    except:
        info = "E: thraed 1 raise an Exception: " + str(sys.exc_info(
        )[0]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
            sys.exc_info())
        #    await bot.send_message(MY_ID, info)
        print(info)
    print("thraed 1 is over")
    global entry_task
    entry_task.append([MY_ID, "thread 1 is over", False])


async def start_send_entry_task(cid=cid_btrss):
    global tasks
    tasks = []
    for j in asyncio.all_tasks():
        tasks.append(j.get_name())
    if cid == cid_btrss:
        task_name = "send_entry_task"
    else:
        task_name = "send_entry_task_" + str(cid)
    if task_name not in tasks:
        asyncio.create_task(send_entry_task(cid), name=task_name)


def get_one_feed(url):
    global feed_list
    if url not in feed_list:
        return
    status = feed_list[url]
    d = {}
    if status[0] == "disable" or status[0] == 1:
        return
    logger.debug("fetch: " + url)
    #  print("fetch: "+url)
    request_headers = {'Cache-control': 'max-age=600'}
    try:
        if status[0] and status[1]:
            d = feedparser.parse(url,
                                 etag=status[0],
                                 modified=status[1],
                                 request_headers=request_headers)
        elif status[0]:
            d = feedparser.parse(url,
                                 etag=status[0],
                                 request_headers=request_headers)
        elif status[1]:
            d = feedparser.parse(url,
                                 modified=status[1],
                                 request_headers=request_headers)
        else:
            d = feedparser.parse(url, request_headers=request_headers)
    except:
        info = "E: " + str(sys.exc_info(
        )[0]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(
            sys.exc_info())
        logger.info(info)
        #      asuncio.run(bot.send_message(MY_ID, info))
        info = "E: get_feed_t1 url: " + url + "\n==\n" + str(sys.exc_info())
        logger.warning(info)
        from .telegram import put
        put(info)
        return
    if d:
        if hasattr(d, 'status'):
            if d.status != 304:
                #        feeds.append(dict(d).copy())
                if hasattr(d.feed, 'link'):
                    global feeds
                    logger.debug("I: got " + url)
                    #          feeds.append(d)
                    return d


def get_headers(url):
    global feed_list
    if url not in feed_list:
        return
    status = feed_list[url]
    if status[0] == "disable" or status[0] == 1:
        return
    headers = {'Cache-control': 'max-age=600'}
    if status[0]:
        headers["ETags"] = status[0]
    if status[1]:
        headers["Last-Modified"] = status[1]
    return headers

def save_headers(url, headers):
    global feed_list
    if url not in feed_list:
        return
    status = feed_list[url]
    if status[0] == "disable" or status[0] == 1:
        return
    if "ETags" in headers:
        status[0] = headers["ETags"]
    if "Last-Modified" in headers:
        status[1] = headers["Last-Modified"]
    return True

def parse_xml(xml):
    global feed_list
    d = feedparser.parse(xml)
    if d:
        if hasattr(d.feed, 'link'):
            return d

@tg_exceptions_handler
async def feed_loop():
    """get and send"""
    global feed_list
    mp("rss bot start")
    await NB.send_message(MY_ID, "rss bot start")
#    last = time.time()
    wait = 60*5

    #  t=threading.Thread(target=get_feed, kwargs={"status":status,"url":url})
    #  task_name="get_feed"
    #  asyncio.create_task(get_feed(),name=task_name)
    #  async def gf(url):
    #    return await asyncio.to_thread(get_one_feed, url)
    def gf(url):
        return asyncio.to_thread(get_one_feed, url)

    from .tools import http
    async def gf(url):
        headers = get_headers(url)
        if not headers:
            return
        res = await http(url, headers=headers, timeout=wait-15, return_headers=True)
        if res is not None:
            xml, headers = res
            if headers is not None:
                save_headers(url, headers)
            logger.debug("got " + url)
            if xml is not None:
                return await asyncio.to_thread(parse_xml, xml)

    while True:
        feed_list = CONFIG[2]
        tasks = []
        for t in asyncio.all_tasks():
            if t.get_name()[0] == "-":
                tasks.append(t.get_name())
        await asyncio.sleep(wait + len(tasks))
        #    await asyncio.sleep(last+wait - time.time())
        #    put("new loop, get_feed all")
        mp("parse loop start")
        #    await NB.send_message(MY_ID, "I: feed: new loop, wait: {}s".format(time.time()-last))
        try:
            await save_config()
        except Exception as e:
            logger.error(f"can not save condig: {e=}")
            await asyncio.sleep(wait)

        for coro in asyncio.as_completed(map(gf, feed_list.keys()),
                                         timeout=wait - 5):
            try:
                result = await coro
            except asyncio.TimeoutError:
                logger.error("timeout")
                from .telegram import put
                put("rssbot: timeout")
                break
            logger.debug("result: {}".format(result))
            if result:
                d = result

                url = d.feed.title_detail.base
                logger.debug("parse res: {}".format(url))

                if url not in feed_list:
                    #        url=d.feed.link
                    for link in d.feed.links:
                        if link.rel == "self":
                            url = link.href
                            break
                    if url not in feed_list:
                        continue
                status = feed_list[url]
                if 0:
                    if d.get('etag', 0) or d.get('modified', 0):
                        status[0] = d.get('etag', 0)
                        status[1] = d.get('modified', 0)

                url_count = 0
                url_max = int(720 / (20 + len(d.entries)) + 2)
                #      url_max=len(d.entries)
                if type(status[2]) != str:
                    await NB.send_message(MY_ID,
                                          "E: rss url data error: " + url)
                    continue
                old_max_date = (
                    datetime.datetime.strptime(status[2], time_format) -
                    datetime.timedelta(hours=8)).utctimetuple()
                new_max_date = ()
                for entry in d.entries:
                    if entry.get("updated_parsed",
                                 entry.get("published_parsed",
                                           old_max_date)) > old_max_date:
                        await send_entry(entry, url)
                        if new_max_date:
                            new_max_date = max(
                                (new_max_date,
                                 entry.get(
                                     "updated_parsed",
                                     entry.get("published_parsed",
                                               old_max_date))))
                        else:
                            new_max_date = entry.get(
                                "updated_parsed",
                                entry.get("published_parsed", old_max_date))
                        url_count += 1
                        #          if url_count > url_max:
                        if False:
                            await NB.send_message(
                                cid_btrss, "W: too many rss : " + url + "\n" +
                                str(len(d.entries)) + " > " + str(url_max))
                            break
                    else:
                        continue
                if new_max_date and new_max_date != old_max_date:
                    if url not in feed_list:
                        continue
                    feed_list[url][2] = (
                        datetime.datetime(*(new_max_date[0:6])) +
                        datetime.timedelta(hours=8)).strftime(time_format)


def __main(queue):

    global MSG_QUEUE
    MSG_QUEUE = queue

    t_1 = threading.Thread(target=thread_1, daemon=True)
    #t_2=threading.Thread(target=thread_2,daemon=True)
    t_1.start()
    #  await get_feed_loop()
    task_name = "parse_feed"
    asyncio.create_task(parse_feed_loop(), name=task_name)


#  t_2.start()


def main(queue):

    global MSG_QUEUE
    MSG_QUEUE = queue

    task_name = "feed_loop"
    asyncio.create_task(feed_loop(), name=task_name)


#  t_2.start()
