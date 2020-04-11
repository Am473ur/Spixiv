import requests,os,json

img_url="https://i.pximg.net/img-original/img/2020/04/05/23/08/58/80592880_p0.jpg"

session = requests.session()
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64503210'
}


class imgdownloader():
    def __init__(self):
        path = "data/images"
        current_path=os.getcwd()
        self.path=os.path.join(current_path, path)
        self.pic_name = 'data\\pic_name.json'
        f=open(self.pic_name,'w')
        json.dump([],f)
        f.close()
    def get_img_name(self,name):
        img_name=''
        for i in range(1,30):
            if name[-i]=='/':
                break
            img_name=name[-i]+img_name
        return img_name
    
    def imgdownload(self,img_url):
        #print(self.path)
        try:
            html = requests.get(img_url, headers=head)
            img = html.content
        except:
            print('获取该图片失败')
            return None
        img_name=self.get_img_name(img_url)
        with open(self.path+'\\'+img_name, 'ab') as f:
            f.write(img)
        f1=open(self.pic_name,encoding="utf-8")
        temp_list=json.load(f1)
        temp_list.append(img_name)
        with open(self.pic_name,"w") as f1:
            json.dump(temp_list,f1)
        
class img_manager():
    def __init__(self):
        self.local_img_url_list = []

    def get_local_img(self):#外部仅调用这一个函数
        if len(self.local_img_url_list) == 0:
            self.store_local_img()
        if len(self.local_img_url_list) == 0:
            return None
        local_img_url = self.local_img_url_list.pop()
        return local_img_url

    def store_local_img(self):#从data/pic_name.json获取未输出过的图片列表，并清空json
        local_img_urls=self.get_img_list()
        if len(local_img_urls) == 0:
            return
        for local_img_url in local_img_urls:
            self.local_img_url_list.append(local_img_url)

    def get_img_list(self):
        f1=open('data\\pic_name.json',encoding="utf-8")
        temp_list=json.load(f1)
        f1.close()
        f=open('data\\pic_name.json','w')
        json.dump([],f)
        f.close()
        return temp_list

