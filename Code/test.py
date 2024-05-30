import requests
from bs4 import BeautifulSoup
import time

current_BTC = 0

def scrape_value():
    url = "https://finance.yahoo.com/quote/BTC-USD"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    value = soup.find('fin-streamer',{"class":"livePrice svelte-mgkamr"}).text
    if value:
        return value
    else:
        print("Not Found")
        return None
    
while True:
    t1 = time.time()
    BTC_Current = scrape_value()
    if BTC_Current == current_BTC:
        time.sleep(5)
    else: 
        t2 = time.time() - t1
        current_BTC = BTC_Current
        print(f"Price:{BTC_Current} Frequency:{t2} seconds")
