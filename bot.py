import requests

TOKEN = "8543827401:AAHUeV3MTIApnJ4qkNQnOeLY-gbnqBUtH0U"
CHAT_ID =  "8360061605"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": "Test warga siaga"
})