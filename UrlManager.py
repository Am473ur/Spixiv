import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random
session = requests.session()
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64503210'
}
class url_manager():
    def __init__(self):
        self.old_url=[]
        self.new_url=[]
    def add_new_url(self,url):
        if url is None:
            return
        if url not in self.old_url and url not in self.new_url:
            self.new_url.append(url)
    def add_new_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_url(url)
    def get_url(self):
        if len(self.new_url)>0:
            url=self.new_url.pop()
            self.old_url.append(url)
            return url
        else:
            return None
    def unvisited_url_num(self):
        return len(self.new_url)
