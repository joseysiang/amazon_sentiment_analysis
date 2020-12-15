# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:16:11 2020
@author: Administrator
"""

# %%%% Preliminaries and library loading
import datetime
import os
import pandas as pd
import re
import shelve
import time
import datetime

# libraries to crawl websites
from bs4 import BeautifulSoup
from selenium import webdriver
from pynput.mouse import Button, Controller


pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 5)
pd.set_option('display.width',800)
#path = 'C:\\Users\\Administrator\\Dropbox\\dropbox_mini_2'
#path = 'C:\\Users\\xvidalberastain\\Downloads'
#os.chdir(path)


path_to_driver ='/Users/jocelyn_x/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path=path_to_driver)

link_list = ['https://www.amazon.com/FOREO-Personalized-Cleansing-Anti-Aging-Sensitive/product-reviews/B01A61XUU4/ref=cm_cr_arp_d_show_all?ie=UTF8&reviewerType=all_reviews&pageNumber=1',
             'https://www.amazon.com/FOREO-Facial-Cleansing-Exfoliation-Sunflower/product-reviews/B018T7DI0Y/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews']
one_link = link_list[1]
driver.get(one_link)


# %%% 

# Finding all the reviews in the website and bringing them to python
reviews_one_store = []


# Finding all the reviews in the website and bringing them to python
condition = True

while (condition):  #inspect -> ctrl+f to copy path
    # dir(reviews[0] to check methods and )
    reviews           = driver.find_elements_by_xpath("//div[@class='a-section celwidget']")  
    #r                 = 0
    for r in range(len(reviews)):
        one_review                   = {}
        one_review['scrapping_date'] = datetime.datetime.now()
        one_review['url']     = driver.current_url
        soup                         = BeautifulSoup(reviews[r].get_attribute('innerHTML'))
        try: #try below first
            one_review_raw = reviews[r].get_attribute('innerHTML')
        except: #if shows an error, keep empty for this position
            one_review_raw = ""
        one_review['review_raw'] = one_review_raw
        
        # find rates
        try:
            one_review_stars = soup.find('span', attrs={'class':'a-icon-alt'}).get_text()
            one_review_stars = one_review_stars.split()[0]
        except:
            one_review_stars = ""
        one_review['one_review_stars'] = one_review_stars
        
        #find date
        try: #try below first
            one_review_raw_date = soup.find('span', attrs={'data-hook':'review-date', 'class':'a-size-base a-color-secondary review-date'}).get_text()
            #one_review_raw_date = re.search('Reviewed in the United States on (.*)$', one_review_raw_date).group(1)
        except: #if shows an error, keep empty for this position
            one_review_raw_date = ""
        one_review['review_raw_date'] = one_review_raw_date
        
        #find colors
        try:
            one_review_color = soup.find('a', attrs={'data-hook':'format-strip', 'class':'a-size-mini a-link-normal a-color-secondary'}).get_text()
            #one_review_color = re.search(' (.*)',one_review_color).group(1)
        except:
            one_review_color = ""
        one_review['one_review_color'] = one_review_color
        
        #find number of backer
        try:
            one_review_backer = soup.find('span', attrs={'data-hook':'helpful-vote-statement', 'class':'a-size-base a-color-tertiary cr-vote-text'}).get_text()
            one_review_bacer = one_review_backer.split()[0]
        except:
            one_review_text = ""
        one_review['one_review_text'] = one_review_text
        
        #find reviews ti
        try:
            one_review_text = soup.find('span', attrs={'data-hook':'review-body', 'class':'a-size-base review-text review-text-content'}).get_text()
        except:
            one_review_text = ""
        one_review['one_review_text'] = one_review_text
        
        reviews_one_store.append(one_review)
        
        #find reviews text
        try:
            one_review_text = soup.find('span', attrs={'data-hook':'review-body', 'class':'a-size-base review-text review-text-content'}).get_text()
        except:
            one_review_text = ""
        one_review['one_review_text'] = one_review_text
        
        reviews_one_store.append(one_review)


    a_last_check = driver.find_element_by_xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]").get_attribute('class')
    if a_last_check != 'a-last':
        break
    else: 
        # next page xpath
        next_page = driver.find_element_by_xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]/a")
        url = next_page.get_attribute('href')
        driver.get(url)
        time.sleep(1) #need to give python time to load; set it randomly, to avoid being recognized as robot



# %%%% More cleaning
a = pd.DataFrame.from_dict(reviews_one_store)
a.review_raw.iloc[0]
#a['review_raw'].map(lambda a: BeautifulSoup(a).text)
a.to_csv('amazon_luna2mini_review.csv')


'''
general expression: Go to Regex 101 to play
https://regex101.com/
https://cheatography.com/davechild/cheat-sheets/regular-expressions/
'''

# find reviewers' location
# 1. identify pattern
temp = []
# same as: a['review_raw'].map(lambda a: BeautifulSoup(a).text)
for i in range(a.shape[0]):
    temp.append(BeautifulSoup(a.review_raw.iloc[i]).text)
a['temp'] = temp.copy()


# %%%%
#concat: combine two df





# %%% 



