import redis
import pygsheets
from localbitcoins_sdk import LBClient
from loguru import logger

from config import LB_HMAC_KEY, LB_HMAC_SECRET, spreadsheet_name, service_file_name


logger.info('Initializing clients...')
# Local Bitcoins client
lb_client = LBClient(LB_HMAC_KEY, LB_HMAC_SECRET)

# Google Sheets client
google_client = pygsheets.authorize(service_file=service_file_name)
spreadsheet = google_client.open(spreadsheet_name)
worksheet = spreadsheet.sheet1

# Storage
storage = redis.Redis()


