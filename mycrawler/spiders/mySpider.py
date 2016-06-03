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
        real_response = HtmlResponse(drvr.current_url, body=body, encoding='utf-8', request=None)
        
        with open(filename, 'wb') as f:
            f.write(response.body)