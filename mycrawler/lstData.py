class lstData:

    @staticmethod
    def get_urllist():
        all_urls = [
        "http://www.dianping.com/shop/17971182/review_more", #yulin
        "http://www.dianping.com/shop/11549926/review_more", #yankoushi
        "http://www.dianping.com/shop/9067814/review_more", #kehua
        "http://www.dianping.com/shop/26954362/review_more", #ludao
        "http://www.dianping.com/shop/6560134/review_more", #babao
        "http://www.dianping.com/shop/6019933/review_more", #shuangnan
        "http://www.dianping.com/shop/15907260/review_more" #zijing
                 ]
        for u in all_urls:
            yield u