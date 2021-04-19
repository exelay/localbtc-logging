import pygsheets
from localbitcoins_sdk import LBClient

from config import LB_HMAC_KEY, LB_HMAC_SECRET

# Local Bitcoins client
lb_client = LBClient(LB_HMAC_KEY, LB_HMAC_SECRET)

# Google Sheets client
google_client = pygsheets.authorize()
spreadsheet = google_client.open('Local Bitcoins Stat')
worksheet = spreadsheet.sheet1
