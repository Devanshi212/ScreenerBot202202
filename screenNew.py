from bs4 import BeautifulSoup
from urllib.request import urlopen
# import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from time import sleep
import pandas as pd 

# to avoid the ERROR:chrome_browser_main_extra_parts_metrics
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#extracting names and links of automotive sector companies
# since the direct executable_path will be deprecated in the upcoming releases use service
ser=Service('V:\Programming\Python\chromedriver_new\chromedriver.exe')
wd=webdriver.Chrome(service=ser,options=options)

# to count the number of links retrieved 
count=0
companyLinks=[]
# extracting links from all the pages of screener.in
for x in range(1,10):
    page = urlopen(f'https://www.screener.in/company/compare/00000034/?page={x}')
    soup = BeautifulSoup(page, "lxml")
    
    for link in soup.find_all('a'):
        if(link.get('href')[0:8]=="/company"):
            # print(link.get('href'))
            companyLinks.append("https://www.screener.in/"+link.get('href'))
            count=count+1
# print(count)
# print(companyLinks)

# extracting links from a different website-moneycontrol.com
# page = urlopen("https://www.moneycontrol.com/india/stockmarket/sector-classification/marketstatistics/bse/banking-finance.html")
# soup = BeautifulSoup(page, "lxml")
# count=0
# for link in soup.find_all('a', attrs={'href': re.compile("/india/stockpricequote/finance")}):
#     print(link.get('href'))
#     count=count+1
# print(count)

df=pd.DataFrame(columns=['Company Name','PE Ratio','ROE','Net Profit','EPS','Cash Flow','Cash Conversion Cycle'])
for link in companyLinks:
    companyName=""
    pe=0
    roe=0
    netProfit=[]
    eps=[]
    cashflow=[]
    cashConversionCycle=[]
    
    wd.get(link)
    sleep(2)
    
    # get the name of the company
    companyName=wd.find_element(By .XPATH,'//*[@id="top"]/div[1]/div/h1').text
    # print(companyName)
    
    # P/E ratio 
    pe=wd.find_element(By .XPATH,'//*[@id="top-ratios"]/li[4]/span[2]/span').text
    # print(pe)
    
    # ROE percentage
    roe=wd.find_element(By .XPATH,'//*[@id="top-ratios"]/li[8]/span[2]/span').text
    # print(roe)
    
    # net profit 
    # wd.execute_script("window.scrollTo(0,2200)")
    for i in range(2,10):
        try:
            netProfit.append(wd.find_element(By .XPATH,f'//*[@id="quarters"]/div[3]/table/tbody/tr[10]/td[{i}]').text)
        except:
            try:
                # data is present in two different divs
                netProfit.append(wd.find_element(By .XPATH,f'//*[@id="quarters"]/div[2]/table/tbody/tr[10]/td[{i}]').text)
            except:
                break
    
    # eps 
    for i in range(2,10):
        try:
            eps.append(wd.find_element(By .XPATH,f'//*[@id="quarters"]/div[3]/table/tbody/tr[11]/td[{i}]').text)
        except:
            try:
                # data present in different divs
                eps.append(wd.find_element(By .XPATH,f'//*[@id="quarters"]/div[2]/table/tbody/tr[11]/td[{i}]').text)
            except:
                break
        
    # cashFlow
    #Range is 5 to account for companies that do not have data for 6-8 quarters 
    for i in range(2,7):
        try:
            cashflow.append(wd.find_element(By .XPATH,f'//*[@id="cash-flow"]/div[2]/table/tbody/tr[4]/td[{i}]').text)
        except:
            break
    
    # cashConversionCycle
    #Range is 5 to account for companies that do not have data for 6-8 quarters 
    for i in range(2,7):
        try:
            cashConversionCycle.append(wd.find_element(By .XPATH,f'//*[@id="ratios"]/div[2]/table/tbody/tr[4]/td[{i}]').text)
        except:
            break
    
    data={'Company Name':companyName,'PE Ratio':pe,'ROE':roe,'Net Profit':netProfit,'EPS':eps,'Cash Flow':cashflow,'Cash Conversion Cycle':cashConversionCycle}
    df=df.append(data,ignore_index=True)
    print(df)
df.to_csv('2_Technology.csv')

wd.close()