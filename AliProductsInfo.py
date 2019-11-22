from selenium import webdriver
import time
import requests

driver = webdriver.Chrome()
driver.get('https://www.aliexpress.com')

class AliDownloader():
    def __init__(self):
        pass

    @staticmethod
    def get_main_images():
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

    @staticmethod
    def get_sku_images():
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