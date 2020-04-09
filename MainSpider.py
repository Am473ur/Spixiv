from bs4 import BeautifulSoup
import UrlManager, HtmlDownloader, HtmlParser, ImgDownloader
import json
#from SignIn import login

class Spider():
    def __init__(self):
        #self.login = login()
        self.urls = UrlManager.url_manager()
        self.downloader = HtmlDownloader.htmldownloader()
        self.parser = HtmlParser.htmlparser()
        self.imgdownloader = ImgDownloader.imgdownloader()

        self.url_list=self.get_url_list()
        self.url_list_num=len(self.url_list)
        self.url_list_cnt=0

        self.img_list=None
        self.img_list_num=0
        self.img_list_cnt=0

    def craw_one(self):
        if self.img_list_num<=self.img_list_cnt:#当前页面图片总数小于等于正在爬取的图片序号，就会换一页爬
            if self.url_list_cnt==self.url_list_num:#没有新的页面可爬了 :)
                return None
            base_url=self.url_list[self.url_list_cnt]
            self.url_list_cnt+=1
            html_text = self.downloader.download(base_url)
            urls = self.parser.get_img_urls(base_url, html_text)
            self.urls.add_new_urls(urls)
            self.img_list_num=self.urls.unvisited_url_num()
            print("num=", self.img_list_num)
            self.img_list_cnt=0
        if self.urls.unvisited_url_num()==0:
            self.craw_one()
        url = self.urls.get_url()
        if url == None:
            self.craw_one()
        img_html_text = self.downloader.download(url)
        img_url = self.parser.get_img_url(url, img_html_text)
        self.imgdownloader.imgdownload(img_url)
        print("本页第{}张图片下载完成".format(self.img_list_cnt))
        self.img_list_cnt+=1

    def get_url_list(self):
        f = open("Settings.json", encoding='utf-8')
        setting = json.load(f)
        url_list=setting[0]["url_list"]
        return url_list

'''
    def craw_base_urls(self):
        for base_url in self.url_list:
            html_text = self.downloader.download(base_url)
            urls = self.parser.get_img_urls(base_url, html_text)
            self.urls.add_new_urls(urls)
            print("num=", self.urls.unvisited_url_num())
            if self.urls.unvisited_url_num()==0:
                continue
            num = 1
            while self.urls.unvisited_url_num() != 0:
                url = self.urls.get_url()
                if url == None:
                    break
                img_html_text = self.downloader.download(url)
                img_url = self.parser.get_img_url(url, img_html_text)
                self.imgdownloader.imgdownload(img_url)
                print("本页第{}张图片下载完成".format(num))
                num += 1
'''