import os
from dotenv import load_dotenv


load_dotenv()

# Local Bitcoins Keys
LB_HMAC_KEY = os.getenv('LB_HMAC_KEY')
LB_HMAC_SECRET = os.getenv('LB_HMAC_SECRET')

spreadsheet_name = 'local'
service_file_name = 'localbitcoinsstat-a63a7a6949b0.json'
