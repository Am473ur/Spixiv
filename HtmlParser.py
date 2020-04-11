from bs4 import BeautifulSoup
import re
import json
class htmlparser():
    def __init__(self):
        self.img_qulity=self.get_img_quality()
    
    def get_img_quality(self):
        f = open("Settings.json", encoding='utf-8')
        setting = json.load(f)
        img_quality=setting[0]["img_quality"]
        return img_quality

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
        pattern = re.compile('\"'+self.img_qulity+'\":"(.*?)"',re.I)
        img_url = re.findall(pattern,str_soup)[0]
        return img_url
