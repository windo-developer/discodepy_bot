import requests
from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=bitcoin'
reslut = requests.get(url)
soup = BeautifulSoup(reslut.text, "html.parser")
resluts = soup.find("div", {"class": "dDoNo vk_bk gsrt gzfeS"})

price = resluts.find("span", {"class": "DFlfde SwHCTb"})

print(price)

# https://futurum.tistory.com/353
