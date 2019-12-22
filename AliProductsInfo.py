from selenium import webdriver
import time
import requests
import re
import json

driver = webdriver.Chrome()
driver.get('https://www.aliexpress.com')


class AliDownloader():
    def __init__(self, driver):
        self.url = None
        self.driver = driver

    def set_product_url(self, url):
        pattern = r'http[s]?://www.aliexpress.com.+?\d+\.html'
        if re.match(pattern, url):
            self.url = url
        else:
            raise Exception("product url not match! exp: http[s]?://www.aliexpress.com.+?\d+\.html")

    def get_main_images(self):
        main_urls = []
        image_list = self.driver.find_element_by_class_name("images-view-list")
        lis = image_list.find_elements_by_tag_name("img")
        print("there are %d main pictures" % len(lis))
        for i in lis:
            image_raw_url = i.get_attribute("src")
            image_url = image_raw_url.split("_")
            image_url.pop(-1)
            image_url = "_".join(image_url)
            main_urls.append(image_url)
        return main_urls

    def get_sku_images(self):
        sku_urls = []
        sku_box = self.driver.find_element_by_class_name("sku-property-list")
        lis = sku_box.find_elements_by_tag_name("img")
        print("there are %d color pictures" % len(lis))
        for i in lis:
            image_raw_url = i.get_attribute("src")
            image_url = image_raw_url.split("_")
            image_url.pop(-1)
            image_url = "_".join(image_url)
            sku_urls.append(image_url)
        return sku_urls

    def get_title(self):
        ele = self.driver.find_element_by_class_name('product-title')
        return ele

    def get_properties(self):
        pattern = '"props":(.+])'
        res = re.search(pattern, self.driver.page_source)
        if res:
            j = json.loads(res.groups()[0])
            return j

    def get_catalog_id(self):
        p = re.compile('"categoryId":(\d+)')
        page_source = self.driver.page_source
        res = p.search(page_source)
        if res:
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
        '"productSKUPropertyList",   "skuPriceList",     "warrantyDetailJson"'
        properlist={
            "type":"",
            "color":[],
            "size":[],
            "sku":[]
        }
        page_source = self.driver.page_source
        productSKUPropertyList_re = re.compile('"productSKUPropertyList":(\[{.+?}\]),')
        skuPrice_re = re.compile('"skuPriceList":(\[{.+?}\])')
        res = productSKUPropertyList_re.search(page_source)
        if res:
            productSKUPropertyList = json.loads(res.groups()[0])
        res = skuPrice_re.search(page_source)
        if res:
            skuPriceList = json.loads(res.groups()[0])
        self._color_size(productSKUPropertyList)

    def _color_size(self,productlist=[]):
        length = len(productlist)
        if length==2:
            for i in productlist:
                property1 = i.get('skuPropertyName')
                



def roll():
    js = "window.scrollBy(0,500)"
    for i in range(0, 20000, 500):
        driver.execute_script(js)
        time.sleep(0.2)


def download_image(urls, name, path):
    counter = 0
    n = 0
    for url in urls:
        if 'http' not in url:
            url = 'https:' + url
        while True:
            try:
                content = requests.get(url, timeout=5).content
                time.sleep(1)
                with open(path + "\\" + name + str(n) + ".jpg", 'wb') as f:
                    f.write(content)
                    print(str(n) + ".jpg is downloaded")
                    n += 1
                    break
            except Exception as error:
                print("%s is not downloaded" % (url))
                counter += 1
                if counter == 5:
                    break
