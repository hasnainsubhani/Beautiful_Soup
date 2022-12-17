from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os

html_doc = urlopen("https://www.flipkart.com/search?q=laptops&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_9_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_9_0_na_na_na&as-pos=9&as-type=TRENDING&suggestionId=laptops&requestId=6b3f209a-f81d-4f6e-9fe0-158134b4d5b8")



soup = BeautifulSoup(html_doc, 'html.parser')
_data = soup.find_all('div','_2kHMtA')
_data_1 = soup.find_all('div',{'class':'_1YokD2 _3Mn1Gg','class':'_2MImiq'})
pages = int(_data_1[0].find('span').text.split(' ')[3])

f = open("laptop_data.csv",'w+')
f.write("productname,specification,star,ratings,Reviews,price,MRP,processor,ram,storage,warranty\n")
f.close()

f = open("laptop_data.csv",'a')
for page in range(1,pages):
    print(page)
    print('\n')
    if page == 1:
        _doc = urlopen("https://www.flipkart.com/search?q=laptops&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_9_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_9_0_na_na_na&as-pos=9&as-type=TRENDING&suggestionId=laptops&requestId=6b3f209a-f81d-4f6e-9fe0-158134b4d5b8")
    else:
        _doc = urlopen(f"https://www.flipkart.com/search?q=laptops&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_9_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_9_0_na_na_na&as-pos=9&as-type=TRENDING&suggestionId=laptops&requestId=6b3f209a-f81d-4f6e-9fe0-158134b4d5b8&page={page}")
    
    soup = BeautifulSoup(_doc, 'html.parser')
    _data = soup.find_all('div','_2kHMtA')
    for item in _data:
        
        products = item.find('div',{'class':'_4rR01T'})
        productname = products.text.split('-')[0].replace(',','')
        specification = products.text.split('-')[1].replace(',','')
        stars = item.find('div',{'class':'_3LWZlK'})
        try:
            star = stars.text
        except:
            star =  0
        
        rate_review = item.find('span',{'class':'_2_R_DZ'})

        try:
            rateReview = re.findall('\d+,?\d*',rate_review.text)
            ratings = rateReview[0].replace(',','')
            Reviews = rateReview[1].replace(',','')
        except:
            ratings = 0
            Reviews = 0
        
        
        current_price = item.find('div',{'class':'col col-5-12 nlI3QM','class':'_30jeq3 _1_WHN1'})
        price = current_price.text.replace(',','').replace('₹','')

        mrp = item.find('div',{'class':'col col-5-12 nlI3QM','class':'_3I9_wc _27UcVY'})
        MRP = current_price.text.replace(',','').replace('₹','')

        

        info = item.find_all('li',{'class':'rgWa7D'})


        information = [0,0,0,0]
        for i in range(0,len(info)):
            if info[i].text.lower().find('processor')>0:
                information[0]=(info[i].text)
            elif info[i].text.lower().find('ram')>0:
                information[1]=(info[i].text)
            elif info[i].text.lower().find('ssd')>0:
                information[2]=(info[i].text)
            elif info[i].text.lower().find('hdd')>0:
                information[2]=(info[i].text)
            elif info[i].text.lower().find('warranty')>0:
                    information[3]=(re.findall('\d',info[i].text)[0])
            
            processor = information[0]
            ram = information[1]
            storage = information[2]
            warranty = information[3]

        f.write(f"{productname},{specification},{star},{ratings},{Reviews},{price},{MRP},{processor},{ram},{storage},{warranty}\n")    
        print(f"{productname},{specification},{star},{ratings},{Reviews},{price},{MRP},{processor},{ram},{storage},{warranty}")

f.close()   