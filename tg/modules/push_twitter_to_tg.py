#from tgbots import UB, NB, MY_ID, BOT_ID, CONFIG
from . import *

logger = logging.getLogger(__name__)

#from ..utils.telegram import tg_exceptions_handler, get_pattern



from ..utils.tw_fav import main
# push my fav twitter to tg channel
main()
