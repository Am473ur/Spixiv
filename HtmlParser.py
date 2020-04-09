import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random
class htmlparser():
    def get_img_urls(self,page_url,html_text):# 从图片列表页面获取多个进入图片详情页面的 url
        urls=[]
        if page_url is None or html_text is None:
            return
        soup=BeautifulSoup(html_text,'html.parser')
        links=soup.find_all('a',href=re.compile(r"/artworks/"))
        for link in links:
            link_url='https://www.pixiv.net'+link['href']
            if link_url in urls:
                continue
            urls.append(link_url)
        return urls
    def get_img_url(self,page_url,html_text):# 从单个图片详情页面提取单个高清原图 url
        if page_url is None or html_text is None:
            return
        soup=BeautifulSoup(html_text, 'lxml')
        str_soup=str(soup)
        pattern = re.compile('"regular":"(.*?)"',re.I)
        img_url = re.findall(pattern,str_soup)[0]
        return img_url
'''
审查元素发现 Pixiv 对每一个图片给出了以下五种尺寸的图片:
"urls":{
    "mini":"https://i.pximg.net/c/48x48/custom-thumb/img/2020/04/05/00/37/23/80569169_p0_custom1200.jpg",
    "thumb":"https://i.pximg.net/c/250x250_80_a2/custom-thumb/img/2020/04/05/00/37/23/80569169_p0_custom1200.jpg",
    "small":"https://i.pximg.net/c/540x540_70/img-master/img/2020/04/05/00/37/23/80569169_p0_master1200.jpg",
    "regular":"https://i.pximg.net/img-master/img/2020/04/05/00/37/23/80569169_p0_master1200.jpg",
    "original":"https://i.pximg.net/img-original/img/2020/04/05/00/37/23/80569169_p0.jpg"
}

'''