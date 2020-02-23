import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
from selenium import webdriver
from urllib.request import urlopen
import time

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')


time.sleep(2)
title = soup.find('div', class_='content_title').text.strip()
paragraph = soup.find('div', class_='article_teaser_body').text.strip()


jpl_url = "https://www.jpl.nasa.gov"
jpl_search = "/spaceimages/?search=&category=Mars"
jpl_query = (jpl_url+jpl_search)

browser.visit(jpl_query)
jpl_html = browser.html

time.sleep(2)
jpl_soup = bs(jpl_html, 'html.parser')
featured_image = jpl_soup.find('a', class_="button fancybox")['data-fancybox-href']
img_url = jpl_url + featured_image

fact_url = "https://space-facts.com/mars/"
table = pd.read_html(fact_url)
facts = table[0]
facts.columns = ['Measure','Tidbit']
facts.set_index('Measure', inplace=True)
fact_table = facts.to_html().replace('\n', '')
fact_table

twitter_weather = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitter_weather)

time.sleep(1)
weather = bs(browser.html, 'html.parser')
weather_tweet_text = weather.findAll('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
mars_weather = weather_tweet_text[23].text.strip()

hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemis_url)
hemis_soup = bs(browser.html, 'html.parser')

time.sleep(2)
results = hemis_soup.find_all('div', class_ = 'item')
base = 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/'
image_urls = []

for result in results:
    title = result.find('div', class_ = 'description').find('a', class_ = 'product-item').find('h3').text
    thumbnail = result.find('a', class_ = 'product-item').find('img', class_ = 'thumb')
    thumbstring = str(thumbnail)
    splitthumb = thumbstring.split('_', 1)
    splitAGAIN = splitthumb[1].split('_thumb.png"/>')
    full_url = base + splitAGAIN[0] + '/full.jpeg'
    
    dict_of_these = {'title':title, 'urls': full_url}
    image_urls.append(dict_of_these)

    browser.close()