# url下载器
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64503210'
}
class htmldownloader():
    def download(self,url):
        if url is None :
            return None
        session = requests.session()
        html=session.get(url, headers=head)
        return html.text
