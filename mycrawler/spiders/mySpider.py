import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse


class DZDPSpider(scrapy.Spider):
    name = "dazhongdianping"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "www.google.com", #fake address
    ]
    
    def __init__(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.real_urls = ["http://www.dianping.com/shop/9067814/review_more"]
        self.logger.info("Start Firfox browser")
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
    
    def parse(self, response):
        sefl.logger.info("Start Selenium process")
        self.driver.get(self.real_urls[0])
        real_response = HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=None)
        
        for a in response.xpath('//div[@class="J_brief-cont"]/text()'):
            print a.extract() #print all reviews in this page