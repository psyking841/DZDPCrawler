import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse
import logging
from mycrawler.items import MSStoreAppItem
from mycrawler.lstData import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re,time

class MSStoreSpider(scrapy.Spider):
    name = "MSStoreSpider"
    allowed_domains = ["microsoft.com"]
    start_urls = [
        "http://www.dmoz.org/",
    ]
    
    def __init__(self):
        logging.info("Initiating...")
        #self.home_url = "http://www.dianping.com/shop/9067814/review_more"
        self.next_page = None
        service_args = ['--load-images=false', '--disk-cache=true']
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.PhantomJS(executable_path = '/Users/SPan/Source/phantomjs-2.1.1/bin/phantomjs', service_args = service_args)
        self.driver.get("https://www.microsoft.com/en-us/store/apps/fotor/9wzdncrfhw5q")
        self.fake_url = "http://www.dmoz.org/"
    
    def parse(self, response):
        next_page = self.driver.find_element_by_xpath('//li[@id="reviewsPageNext"]')
        next_page_butt = self.driver.find_element_by_xpath('//li[@id="reviewsPageNext"]/a')
        #next_page_butt.click()
        logging.info("crawling the first page of reviews")
        body = self.driver.page_source
        response_msstore = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=None)
        all_review = response_msstore.xpath('//div[@id="reviewsPagingSection"]/div[2]/div[1]/div[1]/div')
        
        for rvw in all_review:
            user_name = rvw.xpath('./div[@class="panel-heading"]/span[1]/text()').extract_first()
            comment_rating = rvw.xpath('./div[@class="panel-heading"]//div[@class="rating"]/div[@class="sr-only"]/text()').extract()
            
            
            comment_timestamp = rvw.xpath('./div[@class="panel-heading"]/meta/@content').extract_first()
            comment_title = rvw.xpath('./div[@class="panel-heading"]/h5/span/text()').extract_first()
            user_comment = rvw.xpath('./div[2]/p/text()').extract_first()         
            comment_helpful_num = rvw.xpath('./div[3]/ul/li[2]/span/span/text()').extract_first()
            comment_not_helpful_num = rvw.xpath('./div[3]/ul/li[3]/span/span/text()').extract_first()
            
            item = MSStoreAppItem()
            item["comment_rating"] = comment_rating
            item["user_name"] = user_name
            item["comment_timestamp"] = comment_timestamp
            item["comment_title"] = comment_title
            item["user_comment"] = user_comment
            item["comment_helpful_num"] = comment_helpful_num
            item["comment_not_helpful_num"] = comment_not_helpful_num
            logging.info("FINISH scrapying one item")
            
            yield item
        if next_page.get_attribute("class") != u'disabled':
            logging.info("crawling next page")
            yield scrapy.Request(url=self.fake_url, callback=self.parse1, dont_filter=True)
        
    def parse1(self, response):
        #self.check_element_exists(10, '//li[@id="reviewsPageNext"]/a')
        next_page = self.driver.find_element_by_xpath('//li[@id="reviewsPageNext"]')
#         while not self.check_element_exists(5, '//li[@id="reviewsPageNext"]/a'):
#             next_page_butt = self.driver.find_element_by_xpath('//li[@id="reviewsPageNext"]/a')
#             next_page_butt.click()
        next_page_butt = self.driver.find_element_by_xpath('//li[@id="reviewsPageNext"]/a')
        next_page_butt.click()
        body = self.driver.page_source
        response_msstore = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=None)
        #all_review = response_msstore.xpath('//div[@id="reviewsPagingSection"]//div[@itemprop="review"]')
        all_review = response_msstore.xpath('//div[@id="reviewsPagingSection"]/div[2]/div[1]/div[1]/div')
        
        for rvw in all_review:
            user_name = rvw.xpath('./div[@class="panel-heading"]/span[1]/text()').extract_first()
            comment_rating = rvw.xpath('./div[@class="panel-heading"]//div[@class="rating"]/div[@class="sr-only"]/text()').extract()
            comment_timestamp = rvw.xpath('./div[@class="panel-heading"]/span[2]/text()').extract_first()
#             if not comment_timestamp:
#                 comment_timestamp = rvw.xpath('./div[@class="panel-heading"]/meta/@content').extract()
#             else:
#                 comment_timestamp = comment_timestamp
            comment_title = rvw.xpath('./div[@class="panel-heading"]/h5/text()').extract_first()
                        
            #comment_rating = rvw.xpath('div[@class="panel-heading"]/div[@itemprop="reviewRating"]/div[@aria-label="Ratings"]/div[@class="sr-only"]/text()').extract()[0]
            #user_name = rvw.xpath('div[@class="panel-heading"]/span[@itemprop="author"]/text()').extract()[0]
            #comment_timestamp = rvw.xpath('div[@class="panel-heading"]/meta/@content').extract()[0]
            #comment_title = rvw.xpath('div[@class="panel-heading"]/h5/span/text()').extract()[0]
            user_comment = rvw.xpath('./div[2]/p/text()').extract_first()
            comment_helpful_num = rvw.xpath('./div[3]/ul/li[2]/span/span/text()').extract_first()
            comment_not_helpful_num = rvw.xpath('./div[3]/ul/li[3]/span/span/text()').extract_first()
            
            item = MSStoreAppItem()
            item["comment_rating"] = comment_rating
            item["user_name"] = user_name
            item["comment_timestamp"] = comment_timestamp
            item["comment_title"] = comment_title
            item["user_comment"] = user_comment
            item["comment_helpful_num"] = comment_helpful_num
            item["comment_not_helpful_num"] = comment_not_helpful_num
            logging.info("FINISH scrapying one item")
            
            yield item
        
        if next_page.get_attribute("class") != u'disabled':
            #time.sleep(5)
            logging.info("crawling next page")
            yield scrapy.Request(url=self.fake_url, callback=self.parse1, dont_filter=True)
        
    def check_element_exists(self, time_out, xpath):
        try:
            self.logger.info("Checking xpath: %s exists" % xpath)
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #time.sleep(5)
            #self.driver.find_element_by_xpath(xpath)
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False
        return True