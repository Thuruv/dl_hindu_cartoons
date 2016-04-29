#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
import re
from bs4 import BeautifulSoup


br = mechanize.Browser()

#   setup the browser for action
br.set_all_readonly(False)
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders =  [('User-agent', 'Firefox')]

#   capture the base page
url = 'http://www.thehindu.com/opinion/cartoon/'
response = br.open(url)
html =  response.read()

dl_urls = dict()

soup = BeautifulSoup(html)
temp = []
#   get the PTO pages
for link in br.links(url_regex = 'http://www.thehindu.com/opinion/cartoon/+[?](.*)'):
    temp.append(str(link).split("'")[3])

#   workaround the each image section
for page_url in list(set(temp)):
    response = br.open(page_url)
    html =  response.read()
    soup = BeautifulSoup(html)
    for i in soup.find_all('div',{'class' : 'section-teaser'}):
        url,date  = re.sub('d.jpg', 'f.jpg', i.a.img['src']), ((i.h2.text).split('-')[-1]).strip()
        print url,date
        dl_urls[date] = re.sub('d.jpg', 'f.jpg', url)        
        image_response = br.open_novisit(url)
        with open(date + '.jpg', 'wb') as f:
            f.write(image_response.read())
