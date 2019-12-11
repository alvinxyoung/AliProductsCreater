from selenium import webdriver
import time
import requests
import re
import json

driver = webdriver.Chrome()
driver.get('https://www.aliexpress.com')


class AliDownloader():
    def __init__(self):
        self.url = None

    def set_product_url(self, url):
        pattern = r'http[s]?://www.aliexpress.com.+?\d+\.html'
        if re.match(pattern, url):
            self.url = url
        else:
            raise Exception("product url not match! exp: http[s]?://www.aliexpress.com.+?\d+\.html")

    def get_main_images(self):
        main_urls = []
        image_list=driver.find_element_by_class_name("images-view-list")
        lis = image_list.find_elements_by_tag_name("img")
        print("there are %d main pictures" % len(lis))
        for i in lis:
            image_raw_url=i.get_attribute("src")
            image_url=image_raw_url.split("_")
            image_url.pop(-1)
            image_url="_".join(image_url)
            main_urls.append(image_url)
        return main_urls

    def get_sku_images(self):
        sku_urls=[]
        sku_box = driver.find_element_by_class_name("sku-property-list")
        lis = sku_box.find_elements_by_tag_name("img")
        print("there are %d color pictures" % len(lis))
        for i in lis:
            image_raw_url=i.get_attribute("src")
            image_url=image_raw_url.split("_")
            image_url.pop(-1)
            image_url="_".join(image_url)
            sku_urls.append(image_url)
        return sku_urls

    def get_title(self):
        ele = driver.find_element_by_class_name('product-title')
        return ele

    def get_properties(self):
        pattern = '"props":(.+])'
        res = re.search(pattern, driver.page_source)
        if res:
            j = json.loads(res.groups()[0])
            return j

    def get_catalog_id(self):
        p = re.compile('"categoryId":(\d+)')
        page_source=driver.page_source
        res=p.search(page_source)
        if res :
            return int(res.groups()[0])

    def get_product_id(self):
        ptn = r'http[s]?://www.aliexpress.com.+?(\d+)\.html'
        res = re.search(ptn, self.url)
        if self.url != None:
            if res:
                product_id = res.groups()[0]
                return int(product_id)
            else:
                raise Exception("can not find product id, please check product url")
        else:
            raise Exception("url is not set")

    def get_propertyValueDisplayName(self):
        pass

def roll():
    js = "window.scrollBy(0,500)"
    for i in range(0,20000,500):
        driver.execute_script(js)
        time.sleep(0.2)

def download_image(urls, name,path):
    counter=0
    n=0
    for url in urls:
        if 'http' not in url:
            url = 'https:' + url
        while True:
            try:
                content=requests.get(url,timeout=5).content
                time.sleep(1)
                with open(path + "\\" +name + str(n)+".jpg",'wb') as f:
                    f.write(content)
                    print(str(n)+".jpg is downloaded")
                    n+=1
                    break
            except Exception as error:
                print("%s is not downloaded"%(url))
                counter += 1
                if counter ==5:
                    break