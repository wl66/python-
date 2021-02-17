import scrapy
from xiaoyuan.items import XiaoyuanItem
import time
import json
import threading
class ZhaopinSpider(scrapy.Spider):
    # name:爬虫文件名称，爬虫源文件的唯一标识
    name = 'zhaopin'
    # 限制start_urls哪些url可以进行请求发送
    # allowed_domains = ['zhaopin.com']
    kw = input("请输入要查询的职位:")
    # scrapy自动进行请求发送
    start_urls = ['https://xiaoyuan.zhaopin.com/search/jn=2&pg=1&kw='+kw]
    # 用来控制进行全站数据爬取
    pg =2
    print('正在获取第一页')

    def parse(self, response):
        # xpath返回的是一个列表，列表里存储的是一个个Selector对象
        # extract()可以将列表中每一个selector对象中的data参数对应的字符串取出来

        # 获取总页数
        page_sum = response.xpath('//ul/li[@class="page-item page-btn"][last()]/text()').extract()

        # 获取所有的职位名称、所在城市、招聘人数、公司名称、职位类型

        #职位详情描述页url列表
        import_list = response.xpath('/html/body/script[3]/text()').extract()[0].lstrip('__INITIAL_STATE__=')
        import_list = json.loads(import_list)
        import_list = import_list['souresult']['Items']

        # 创建item类型的对象
        item = XiaoyuanItem()
        # 每条数据在一个div里
        div_list = response.xpath('//div[@class="el-tabs__content"]/div[1]/div/div')

        for index,div in enumerate(div_list):
            # 职位名称在父标签的div文本与子标签的div文本里
            position = div.xpath('./div/div[1]').xpath( 'string(.)').extract()
            city = div.xpath('./p/span[1]/text()').extract()
            num = div.xpath("./p/span[2]/text()").extract()
            corporation = div.xpath( "./div/div[last()]/text()").extract()
            industry = div.xpath("./p/span[last()]/text()").extract()
            # 存储到item类型的对象中
            item['position'] = position[0]
            item['city'] = city[0]
            item['num'] = num[0]
            item['corporation'] = corporation[0]
            # 三元运算符排除分类为空的情况
            item['industry'] = industry[0] if industry else '暂无分类'
            # 职位描述页url
            item['xq_url'] = 'https://xiaoyuan.zhaopin.com/job/' + import_list[index]['JobPositionNumber'] + '?' + import_list[index]['Traceurl']
            yield item

        time.sleep(1)
        # 获取所有数据
        if self.pg<=int(page_sum[0]):
            new_url = 'https://xiaoyuan.zhaopin.com/search/jn=2&pg={}&kw={}'.format(self.pg, self.kw)
            self.pg += 1
            print('正在获取' + str(self.pg-1) + "页")
            # 请求传参
            yield scrapy.Request(url=new_url,callback=self.parse)




