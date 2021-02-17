import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from news.items import NewsItem
import re
import time
class WyNewsSpider(CrawlSpider):
    name = 'wy_news'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/rank/']

    # 链接提取器
    link1 = LinkExtractor(allow=r'rank_(.*?).html')

    rules = (
        # 获取所有分类排行榜的url
        Rule(link1, callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        # 获取当前排行榜的点击数
        item = NewsItem()
        support_num =  response.xpath('//div[@class="area-half left"]/div/div[4]/table//tr/td[@class="cBlue"]/text()').extract()
        response_list =response.xpath('//div[@class="area-half left"]/div/div[4]/table//tr/td[1]/a/@href').extract()
        for index,url in enumerate(response_list):
            item['support']=support_num[index]
            yield  scrapy.Request(url=url,callback=self.parse_detail,meta={'item':item})
            time.sleep(1)


    def parse_detail(self, response):
        # 获取当前文章的内容、标题、类别
        item=response.meta['item']
        title = response.xpath('//h1[@class="post_title"]/text()|//div[@class="post_content_main"]/h1/text()|//*[@id="zajia_wrap"]/div[2]/div[2]/div[1]/h1').extract()
        content = response.xpath('//div[@class="post_body"]/p').extract()
        content = (''.join(content)).replace('</p>','\n')
        content = re.sub(r'<p(.*?)>',' ' ,content)
        content =re.sub(r'<style>(.*?)</style>',' ' ,content)
        content =re.sub(r'<!--(.*?)-->', ' ' ,content)
        category = response.xpath('//div[@class="post_crumb"]/a[2]/text()').extract()
        item['title'] = title[0] if title else response
        item['content'] =content
        item['category'] = category[0] if category else '暂无分类'
        print(title,category,item['support'])
        yield item
