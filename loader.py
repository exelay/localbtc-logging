import pygsheets


google_client = pygsheets.authorize()
sheet = google_client.sheet('Local Bitcoins Stat')
worksheet = sheet.sheet1
