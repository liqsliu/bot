#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)
mp = logger.info

from ..utils.config import save_config


import feedparser
import datetime

from ..utils.rssbot import max_entry_date, time_format


async def _(event):
    mp("cmd {}: {}: {}".format(
        __name__.split(".")[-1], event.sender_id, event.raw_text))
    pass
    #  await UB.send_message(MY_ID, "ok")
    client = event.client
    cmd = await get_cmd(event)
    feed_list = CONFIG[2]
    news_list = CONFIG[3]
    if cmd[0] == "rss":
        if len(cmd) == 1:
            #          await client.send_message(event.chat_id, "hi")
            #      await client.send_message(event.chat_id, str(feed_list))
            info = (i for i in feed_list)
            info = "\n".join(list(info))
            await client.send_message(event.chat_id, info)
        elif cmd[1] == "save":
            await save_config()
        elif cmd[1] == "tg":
            if len(cmd) == 2:
                await client.send_message(event.chat_id, str(news_list))
            elif cmd[2] == "del":
                if int(cmd[3]) in news_list:
                    news_list.remove(int(cmd[3]))
                    await client.send_message(event.chat_id, str(news_list))
                else:
                    await client.send_message(event.chat_id, "no")
            elif cmd[2] == "add":
                if not int(cmd[3]) in news_list:
                    news_list.append(int(cmd[3]))
                    await save_config()
                    await client.send_message(event.chat_id, str(news_list))
                else:
                    await client.send_message(event.chat_id, "exist")
            elif cmd[2] == "load":
                import ast
                news_list.clear()
                news_list.extend(
                    ast.literal_eval(event.raw_text.split(' ', 3)[3]))
                await save_config()
                await client.send_message(event.chat_id, str(news_list))
        elif cmd[1] == "cid":
            global cid_btrss
            cid_btrss = int(cmd[2])
            await client.send_message(event.chat_id,
                                      "rss to: " + str(cid_btrss))
        elif cmd[1] == "stop" or cmd[1] == "disable":
            if len(cmd) > 2:
                if cmd[2] in feed_list:
                    feed_list[cmd[2]][0] = "disable"
                    if len(cmd) > 3:
                        feed_list[cmd[2]][1] = cmd[3]
                    else:
                        feed_list[cmd[2]][1] = 0
                    await client.send_message(event.chat_id,
                                              str(feed_list[cmd[2]]))
                else:
                    await client.send_message(event.chat_id, "need a rss url")
        elif cmd[1] == "add":
            if len(cmd) == 2:
                await client.send_message(event.chat_id, "rss add url [cid]")

            else:
                if not cmd[2] in feed_list:
                    url = cmd[2]
                    request_headers = {'Cache-control': 'max-age=600'}
                    #              d=feedparser.parse(url,extra_headers={'Cache-control': 'max-age=600'})
                    #              d=feedparser.parse(url,request_headers={'Cache-control': 'max-age=600'})
                    d = feedparser.parse(url, request_headers=request_headers)

                    feed_list.update({cmd[2]: []})
                    if hasattr(d, 'etag'):
                        feed_list[cmd[2]].append(d.etag)
                    else:
                        feed_list[cmd[2]].append(0)
                    if hasattr(d, 'modified'):
                        feed_list[cmd[2]].append(d.modified)
                    else:
                        feed_list[cmd[2]].append(0)
                    if d.entries:
                        if feed_list[cmd[2]][0] and feed_list[cmd[2]][1]:
                            d = feedparser.parse(
                                url,
                                etag=feed_list[cmd[2]][0],
                                modified=feed_list[cmd[2]][1],
                                request_headers=request_headers)
                            if d.status != 304:
                                d = feedparser.parse(
                                    url,
                                    etag=d.etag,
                                    modified=d.modified,
                                    request_headers=request_headers)
                        elif feed_list[cmd[2]][0]:
                            d = feedparser.parse(
                                url,
                                etag=feed_list[cmd[2]][0],
                                request_headers=request_headers)
                            if d.status != 304:
                                d = feedparser.parse(
                                    url,
                                    etag=d.etag,
                                    request_headers=request_headers)
                        elif feed_list[cmd[2]][1]:
                            d = feedparser.parse(
                                url,
                                modified=feed_list[cmd[2]][1],
                                request_headers=request_headers)
                            if d.status != 304:
                                d = feedparser.parse(
                                    url,
                                    modified=d.modified,
                                    request_headers=request_headers)
                        if d.status != 304:
                            await client.send_message(
                                event.chat_id,
                                "W: etag or ctime is not efficient, deleted!")
                            feed_list[cmd[2]][0] = 0
                            feed_list[cmd[2]][1] = 0
                        max_date = await max_entry_date(d)
                        feed_list[cmd[2]].append((
                            datetime.datetime(*(max_date[0:6])) +
                            datetime.timedelta(hours=8)).strftime(time_format))

                    else:
                        feed_list.pop(cmd[2])
                        await client.send_message(event.chat_id,
                                                  "no entry,deleted")
                if len(cmd) == 4:
                    feed_list[cmd[2]].append(int(cmd[3]))
#            await client.send_message(event.chat_id, str(feed_list))
                await client.send_message(event.chat_id,
                                          str(feed_list[cmd[2]]))
        elif cmd[1] == "update" or cmd[1] == "up":
            if len(cmd) == 2:
                await client.send_message(event.chat_id, "rss up|update url")
            else:
                if not cmd[2] in feed_list:
                    await client.send_message(event.chat_id, "no url")
                else:
                    url = cmd[2]
                    request_headers = {'Cache-control': 'max-age=600'}
                    d = feedparser.parse(url, request_headers=request_headers)
                    #              feed_list.update({cmd[2]: []})
                    feed_list[cmd[2]][0] = d.get("etag", 0)
                    feed_list[cmd[2]][1] = d.get("modified", 0)

                    info = "feed url : " + d.feed.get("link", None)
                    info = info + "\nentry num: " + str(len(d.entries))
                    if d.entries:
                        max_date = await max_entry_date(d)
                        feed_list[cmd[2]][2] = (
                            datetime.datetime(*(max_date[0:6])) +
                            datetime.timedelta(hours=8)).strftime(time_format)

                        info = info + "\nstatus: " + str(d.get("status", None))
                        if feed_list[cmd[2]][0] and feed_list[cmd[2]][1]:
                            d = feedparser.parse(
                                url,
                                etag=feed_list[cmd[2]][0],
                                modified=feed_list[cmd[2]][1],
                                request_headers=request_headers)
                            if d.status != 304:
                                d = feedparser.parse(
                                    url,
                                    etag=d.etag,
                                    modified=d.modified,
                                    request_headers=request_headers)
                        elif feed_list[cmd[2]][0]:
                            d = feedparser.parse(
                                url,
                                etag=feed_list[cmd[2]][0],
                                request_headers=request_headers)
                            if d.status != 304:
                                d = feedparser.parse(
                                    url,
                                    etag=d.etag,
                                    request_headers=request_headers)
                        elif feed_list[cmd[2]][1]:
                            d = feedparser.parse(
                                url,
                                modified=feed_list[cmd[2]][1],
                                request_headers=request_headers)
                            if d.status != 304:
                                d = feedparser.parse(
                                    url,
                                    modified=d.modified,
                                    request_headers=request_headers)
                        info = info + "\nstatus new: " + str(
                            d.get("status", None))
                        info = info + "\nentry num new: " + str(len(d.entries))
                        if d.status != 304:
                            info = info + "\nW: etag or ctime is not efficient, deleted?"
                            info = info + "\nkeys:" + str(d.keys())
                        await client.send_message(event.chat_id, info)
                    else:
                        await client.send_message(event.chat_id,
                                                  "no entry,delete?")
                await client.send_message(event.chat_id,
                                          str(feed_list[cmd[2]]))
        elif cmd[1] == "load":
            import ast
            feed_list = ast.literal_eval(event.raw_text.split(' ', 2)[2])
            await client.send_message(event.chat_id, str(feed_list))
        elif cmd[1] == "del":
            #          feed_list.pop(int(cmd[1]))
            res = None
            if cmd[2] in feed_list:
                if len(cmd) == 3:
                    res = feed_list.pop(cmd[2])
                elif len(cmd) == 4:
                    if int(cmd[3]) in feed_list[cmd[2]]:
                        res = feed_list[cmd[2]].pop(feed_list[cmd[2]].index(int(cmd[3])))
#                        res=feed_list[cmd[2]].remove(int(cmd[3]))
#            if cmd[2] in feed_list:
#                await client.send_message(event.chat_id, "E: fail")
            await client.send_message(event.chat_id, "deleted: {}".format(res))

        elif cmd[1] == "clear":
            feed_list = {}
            await client.send_message(event.chat_id, str(feed_list))
        elif cmd[1] == "se" or cmd[1] == "search":
            found = 0
            info = ""
            for url in feed_list:
                if cmd[2] in url:
                    found += 1
                    if found > 5:
                        info = info + "\n\n..."
                        break
                    else:
                        info = info + "\n" + url + " : " + str(feed_list[url])

            if not found:
                #          if not info:
                await client.send_message(event.chat_id, "None")
            else:
                await client.send_message(event.chat_id, info)
        else:
            await client.send_message(event.chat_id, "wtf cmd")


#asyncio.create_task(main(),name=__name__)
from ..utils.telegram import MSG_QUEUE

from ..utils.rssbot import main
main(MSG_QUEUE)



cmd = __name__.split(".")[-1]
CMD.add(_, cmd=cmd, need=need, forbid=forbid)
