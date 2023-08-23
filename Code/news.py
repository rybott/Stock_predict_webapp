from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

ticker = 'TSLA'  

n = 6
url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
fin_viz_req = Request(url=url, headers={'user-agent': 'app'})
fin_viz_response = urlopen(fin_viz_req)
html = soup(fin_viz_response,'html')
news_tbl = html.find(id='news-table')
rows = news_tbl.findAll('tr')
headlines = []
urls=[]
for index, row in enumerate(rows):
    try:
        title = row.a.text
        title1 = row.a['href']
        headlines.append([title])
        urls.append([title1])
    except:
        pass
print(len(urls))
print(len(headlines))
headlines = [item[0] for item in headlines if item]
urls = [item[0] for item in urls if item]
print(headlines[:n])
print(urls[:n])