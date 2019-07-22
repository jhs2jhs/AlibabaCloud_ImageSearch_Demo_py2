# pip install scrapy
# pip install requests

import scrapy
from scrapy.crawler import CrawlerProcess

import requests
from pprint import pprint
import datetime

import hashlib
import os
import json
import shutil
import time

import argparse

###################################################################################################
###################################################################################################
###################################################################################################

def get_md5(txt):
    return str(hashlib.sha224(txt).hexdigest())

def img_download(img_url):
    resp = requests.session().get(img_url, stream = True)
    img_body = b""
    if resp.status_code == 200:
        for chunk in resp.iter_content(1024):
            #print(chunk)
            img_body += chunk
            #print("---")
    return img_body

def img_save(img_url, img_fn, img_body):
    f = open(img_fn, "wb")
    f.write(img_body)

def json_save(js_fn, js):
    with open(js_fn, "w") as f:
        json.dump(js, f, indent=4, sort_keys=True)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except:
        pass

def drop_folder(fd):
    try:
        shutil.rmtree(fd)
    except:
        pass

###################################################################################################
###################################################################################################
###################################################################################################

def parse_ae_for_product_list(response, dt, limit=10):
    #pprint(response)
    count = 0
    for prod in response.css("li.list-item"):
        prod_cateid = prod.css("::attr(pub-catid)").get()
        #print(prod_cateid)
        img_url = "http:" + str(prod.css("img.picCore::attr(image-src)").get())
        prod_url = "http:" + str(prod.css("a.product::attr(href)").get())
        prod_price = prod.css("span.value[itemprop='price']::text").get()

        if img_url == 'http:None':
            continue

        count += 1
        if count > limit:
            print('++++ ignore as reach limitation: ', count, limit, img_url)
            continue

        print(count, limit)
        print(img_url)
        print(prod_url)
        print(prod_cateid)
        print(prod_price)

        img_body = img_download(img_url)
        img_id = get_md5(img_body)

        img_fn = './image_auto_scraped/img/img_' + img_id + '.png'
        js_fn = './image_auto_scraped/obj/js_' + img_id + '.json'

        js = {'img_url': img_url, 'prod_url': prod_url, 'prod_price': prod_price, 'prod_cateid': prod_cateid, 'dt': dt, 'parent_url': response.url}
        json_save(js_fn, js)

        img_save(img_url, img_fn, img_body)

        print(img_id)
        print("-------")
        #time.sleep(1) # by default not to setup time limitation

    print("== complete parsing ==")
    return count

class AESpider(scrapy.Spider):
    name = 'AliExpress Scrape'
    #start_urls = ['https://www.aliexpress.com/premium/category/100003109.html']
    #start_urls = ['https://www.aliexpress.com/']
    #url_to_start = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=bottle'
    #start_urls = [url_to_start]
    limit = 10

    def start_requests(self):
        drop_folder('./image_auto_scraped/img')
        drop_folder('./image_auto_scraped/obj')

        mkdir_p('./image_auto_scraped/img')
        mkdir_p('./image_auto_scraped/obj')
        mkdir_p('./image_auto_scraped/htm')

        #urls = ['https://www.aliexpress.com/premium/category/100003109.html']
        #urls = ['https://www.aliexpress.com/']
        #urls = ['https://sale.aliexpress.com/__pc/XZL7sThtbD.htm']
        #urls = ['https://www.aliexpress.com/wholesale?catId=0&SearchText=bottle']
        url_to_start = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=bottle'
        urls = [url_to_start]
        #print('***************', limit)
        #return 
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print(response.body)
        #print("====================================")
        filename = './image_auto_scraped/htm/html_ae.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        dt = str(datetime.datetime.now())

        print('***************', limit)
        count = parse_ae_for_product_list(response, dt, limit)
        #if count <= 1:
        #    url_to_start = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=bottle'
        #    yield scrapy.Request(url=url_to_start, callback=self.parse)
        #    time.sleep(10)

def run_scraper_ae(limit=10):
    # https://docs.scrapy.org/en/latest/topics/practices.html 
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(AESpider, limit=limit)
    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', help='limit the number of images to be downloaded. example: --limit 10')
    args = parser.parse_args()
    try:
        if args.limit:
            if int(args.limit):
                if int(args.limit) > 1:
                    limit = int(args.limit)
                    print('== set limit:', limit)
                    run_scraper_ae(limit)
                else:
                    print("== please input a positive number ==")
    except Exception as e:
        print(e)