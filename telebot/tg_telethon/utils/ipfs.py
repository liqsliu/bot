import logging

logger = logging.getLogger(__name__)
mp = logger.warning

from .. import *

from .tools import SH_PATH, tw_re, pic_re, url_only_re, my_host_re


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))

else:
    print('{} 运行'.format(__file__))
