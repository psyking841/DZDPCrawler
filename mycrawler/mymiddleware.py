import logging
from scrapy.http import HtmlResponse
from selenium import webdriver
# class TestMiddleware1(object):  
#     # overwrite process request  
#     def process_request(self, request, spider):  
#         print 'TestMiddleware1:process_request'  
#   
#     def process_response(self, request, response, spider):  
#         print 'TestMiddleware1:process_response' 
#         return response  
#     
# class TestMiddleware2(object):  
#     # overwrite process request  
#     def process_request(self, request, spider):  
#         print 'TestMiddleware2:process_request'  
#   
#     def process_response(self, request, response, spider):  
#         print 'TestMiddleware2:process_response' 
#         return response  

class PhantomJSMiddleware(object):  
    # overwrite process request  
    def process_request(self, request, spider):  
        pass
#         if request.meta.has_key('PhantomJS'):# If you set PhantomJS parameter
#             logging.info('PhantomJS Requesting: '+request.url, level=log.WARNING)  
#             service_args = ['--load-images=false', '--disk-cache=true']  
#             if request.meta.has_key('proxy'): #if using proxy  
#                 logging.info('PhantomJS proxy:'+request.meta['proxy'][7:], level=log.WARNING)  
#                 service_args.append('--proxy='+request.meta['proxy'][7:])  
#             try:  
#                 driver = webdriver.PhantomJS(executable_path = '/Users/SPan/Source/phantomjs-2.1.1/bin/phantomjs', service_args = service_args)  
#                 driver.get(request.url)  
#                 content = driver.page_source.encode('utf-8')  
#                 url = driver.current_url.encode('utf-8')  
#                 driver.quit()  
#                 if content == '<html><head></head><body></body></html>':#if content is empty  
#                     return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')  
#                 else: #  
#                     return HtmlResponse(url, encoding = 'utf-8', status = 200, body = content)  
#                     
#             except Exception, e: #
#                 logging.warn('PhantomJS Exception!')  
#                 return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')  
#         else:  
#             logging.warn('Common Requesting: '+request.url)