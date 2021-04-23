import redis
import pygsheets
from localbitcoins_sdk import LBClient
from loguru import logger

from config import LB_HMAC_KEY, LB_HMAC_SECRET


logger.info('Initializing clients...')
# Local Bitcoins client
lb_client = LBClient(LB_HMAC_KEY, LB_HMAC_SECRET)

# Google Sheets client
google_client = pygsheets.authorize(service_file='localbitcoinsstat-a63a7a6949b0.json')
spreadsheet = google_client.open('Local Bitcoins Stat')
worksheet = spreadsheet.sheet1

# Storage
storage = redis.Redis()


