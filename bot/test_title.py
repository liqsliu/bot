#!/usr/bin/python
# -*- coding: UTF-8 -*-




from urltitle import URLTitleReader
from urltitle import config as urltitle_config
urltitle_config.REQUEST_TIMEOUT = 12
urltitle_config.MAX_REQUEST_ATTEMPTS = 2


urltitle_config.DEFAULT_REQUEST_SIZE = 1024 ** 2 * 16
reader = URLTitleReader(verify_ssl=True)

#  MiB = 1024 ** 2
#  urltitle_config.MAX_REQUEST_SIZES = {"html": MiB, "ipynb": 8 * MiB, "pdf": 8 * MiB}  # Title observed toward the bottom.
#  #  print(urltitle_config)
#  #  print(urltitle_config.MAX_REQUEST_SIZES)
urltitle_config.MAX_REQUEST_SIZES.update({ 'html': 1024 ** 2 * 16 })

# Titles for HTML content

EXTRA_HEADERS = {
    #  "Accept": "*/*",
    #  "Accept-Language": "en-US,en;q=0.5",
    "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
}

def r(url):
  netloc = reader.netloc(url)
  if netloc not in urltitle_config.NETLOC_OVERRIDES:
    urltitle_config.NETLOC_OVERRIDES[netloc] = {"extra_headers": {}}
  elif "extra_headers" not in urltitle_config.NETLOC_OVERRIDES[netloc]:
    urltitle_config.NETLOC_OVERRIDES[netloc]["extra_headers"] = {}
  EXTRA_CONFIG_HEADERS = urltitle_config.NETLOC_OVERRIDES[netloc]["extra_headers"]
  EXTRA_CONFIG_HEADERS.update(EXTRA_HEADERS)
  res = reader.title(url)
  print(res)
url = "https://www.youtube.com/watch?v=9GEPJEfM0I8"
r(url)
url = "https://youtu.be/NvVBYm4jeiQ"
r(url)
