import os
from dotenv import load_dotenv


load_dotenv()

# Local Bitcoins Keys
LB_HMAC_KEY = os.getenv('LB_HMAC_KEY')
LB_HMAC_SECRET = os.getenv('LB_HMAC_SECRET')
