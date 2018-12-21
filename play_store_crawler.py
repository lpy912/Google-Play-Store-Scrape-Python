import time
from selenium import webdriver
import re
import sys
import requests
import json
from bs4 import BeautifulSoup as bs
import urllib2
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import pandas as pd

try:
    def improvize(rating,dummy_list,text):
        if dummy_list != []:
            name = dummy_list[0].split('\n')[0]
            #print name
            comment=text
            date = dummy_list[0].split('\n')[1]
            #print comment
            return {"name":name,"comments":comment,"ratings":rating,"date":date}
except:
    pass

def rating_conv(lis):
    c=0
    for i in lis:
        if i.startswith('v'):
            c=c+1
    return c

def get_rating(f):
    for i in f:
        ratting = []
        for j in i.find_elements_by_tag_name("div"):
            ratting.append(j.get_attribute("class"))
        #print ratting
        return rating_conv(ratting)
#Enter the path of the driver
browser = webdriver.Chrome("/home/soumitra/Downloads/chromedriver")

# Tell Selenium to get the URL you're interested in.

url = ""
browser.get(url)
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
new_height = 100
x = 50
y=100

to_break = 0
all_data = {}
try:
    while (True):
        try:
            flag = 0
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script("window.scrollTo({0},{1});".format(50+x,50+y))
            time.sleep(SCROLL_PAUSE_TIME)
            x=x+1500
            y=x+1500
            print y,last_height
            try:
                end = browser.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div')
            except:
                print "regular"
                flag = 2
                pass
            
            if flag == 2:
                
                pass
            else:
                  
                end = browser.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div').click()
            if y > 144000:# this value is calculate by trial and error, print the value and 
            #and checkapproximately at what value of y, the scroll reaches the bottom of page and change it
                break
        except:
            pass
                
    browser.execute_script("window.scrollTo(0, 0);")
    ele = browser.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div')
    try:
        dum = []
        for num,i in enumerate(ele.find_elements_by_xpath("./*")):
            
            dum = []
            if i.find_elements_by_class_name("cQj82c") != []:
                i.find_elements_by_class_name("cQj82c")[0].find_elements_by_xpath("./*")[0].click()
            else:
                pass
            e=i.find_elements_by_class_name('pf5lIe')[0]
            f=e.find_elements_by_xpath("./*")

            text = i.find_elements_by_class_name('UD7Dzf')[0].text
            l = get_rating(f)
            
            dum.append(i.text)
            
            try:
                all_data[num] = improvize(l,dum,text)
            except:
                pass
    except:
        pass
        
except:
    pass



df = pd.DataFrame(list(all_data.values()))


df['comments']=df['comments'].apply(lambda x : x.encode('utf-8'))
df['name']=df['name'].apply(lambda x : x.encode('utf-8'))


df = df[['date','name','comments','ratings']]
df.to_csv("results.csv",sep=",") #enter tha path of csv



