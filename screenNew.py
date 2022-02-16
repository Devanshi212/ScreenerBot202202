from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

# to count the number of links retrieved 
count=0
companyLinks=[]
# extracting links from all the pages of screener.in
for x in range(1,10):
    page = urlopen(f'https://www.screener.in/company/compare/00000034/?page={x}')
    soup = BeautifulSoup(page, "lxml")
    
    for link in soup.find_all('a'):
        if(link.get('href')[0:8]=="/company"):
            print(link.get('href'))
            companyLinks.append("https://www.screener.in/"+link.get('href'))
            count=count+1
print(count)
print(companyLinks)

# extracting links from a different website-moneycontrol.com
# page = urlopen("https://www.moneycontrol.com/india/stockmarket/sector-classification/marketstatistics/bse/banking-finance.html")
# soup = BeautifulSoup(page, "lxml")
# count=0
# for link in soup.find_all('a', attrs={'href': re.compile("/india/stockpricequote/finance")}):
#     print(link.get('href'))
#     count=count+1
# print(count)