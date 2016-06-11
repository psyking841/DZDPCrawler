import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse
import logging
from mycrawler.items import MycrawlerItem
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

class DZDPSpider(scrapy.Spider):
    name = "dazhongdianping"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://www.dmoz.org/", #fake address
    ]
    
    def __init__(self):
        #self.real_url = "http://www.dianping.com/shop/17971182/review_more" #yulin
        #self.real_url = "http://www.dianping.com/shop/11549926/review_more" #yankoushi
        #self.real_url = "http://www.dianping.com/shop/9067814/review_more" #kehua
        #self.real_url = "http://www.dianping.com/shop/26954362/review_more" #ludao
        #self.real_url = "http://www.dianping.com/shop/6560134/review_more" #babao
        #self.real_url = "http://www.dianping.com/shop/6019933/review_more" #shuangnan
        self.real_url = "http://www.dianping.com/shop/15907260/review_more" #zijing
        
        logging.info("Initiating...")
        #self.home_url = "http://www.dianping.com/shop/9067814/review_more"
        self.next_page = None
        service_args = ['--load-images=false', '--disk-cache=true']
        self.driver = webdriver.PhantomJS(executable_path = '/Users/SPan/Source/phantomjs-2.1.1/bin/phantomjs', service_args = service_args)
        self.response_home = None
        self.fake_url = "http://www.dmoz.org/"
    
    def parse(self, response):
        logging.info("response from fake url")
        if self.next_page:
            scrape_url = self.real_url + self.next_page
        else:
            scrape_url = self.real_url
        logging.info("scrape_url is " + scrape_url)
        self.driver.get(scrape_url)
        body = self.driver.page_source
        logging.info("get response")
        self.response_home = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=None)
        all_reviews = self.response_home.xpath('//div[@class="comment-list"]/ul/li') #includes all users and reviews
        logging.info("Got body of the page")
        #print(self.response_home.xpath('//h2/a/@href'))
        self.check_element_exists(1, '//h2/a/@href')
        shop_id = self.response_home.xpath('//h2/a/@href').extract()[0]
        shop_id = re.findall(r"\d+", shop_id)
        shop_name = self.response_home.xpath('//h2/a/text()').extract()[0]
        
        logging.info("scrape items")
        for rvw in all_reviews:
            #shop_id = rvw.xpath()
            #shop_name = rvw.xpath()
            user_id = rvw.xpath('div[@class="pic"]/a/@user-id').extract()[0]
            user_name = rvw.xpath('div[@class="pic"]/p[@class="name"]/a/text()').extract()[0]
            user_contribution = rvw.xpath('div[@class="pic"]/p[@class="contribution"]/span/@title').extract()[0]
            user_review_summary = rvw.xpath('div[@class="content"]/div[@class="user-info"]/span/@title').extract()[0]
            comment_ts = rvw.xpath('div[@class="content"]//div[@class="misc-info"]/span[@class="time"]/text()').extract()[0]
            user_review_tags = []
            user_review_tags_selector = rvw.xpath('div[@class="content"]/div[@class="user-info"]/div[@class="comment-rst"]/span/text()')
            for xx in user_review_tags_selector:
                user_review_tags.append(xx.extract())
            user_comment = rvw.xpath('div[@class="content"]//div[@class="J_brief-cont"]/text()').extract()[0]
            #i+=1
            
            item = MycrawlerItem()
            item["merchandise_name"] = shop_name
            item["merchandise_id"] = shop_id
            item["user_id"] = user_id
            item["user_name"] = user_name
            item["user_contribution"] = user_contribution
            item["user_review_summary"] = user_review_summary
            item["user_review_tags"] = user_review_tags
            item["user_comment"] = user_comment
            item["comment_timestamp"] = comment_ts
            logging.info("FINISH scrapying one item")
            yield item
        
        next_page_selector = self.response_home.xpath("//div[@class='Pages']/a[@class='NextPage']/@href")
        if next_page_selector:
            self.next_page = next_page_selector.extract()[0]
            next_page_url = self.real_url + self.next_page
            logging.info("Next page url will be: " + next_page_url)
            logging.info("Got next page info")
            yield scrapy.Request(url=self.fake_url, callback=self.parse, dont_filter=True)
        
    def check_element_exists(self, time_out, xpath):
        try:
            self.logger.info("Checking xpath: %s exists" % xpath)
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #time.sleep(5)
            self.driver.find_element_by_xpath(xpath)
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False
        return True