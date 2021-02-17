# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XiaoyuanPipeline(object):
    def open_spider(self,spider):
        self.fp = open('./xioayuan.txt','w',encoding='utf-8')
    # 处理item
    def process_item(self, item, spider):
        position = item['position']
        city = item['city']
        num = item['num']
        corporation = item['corporation']
        industry = item['industry']
        xq_url = item['xq_url']
        self.fp.write(position+"\n"+city+"  "+num+"  "+corporation+"     "+industry+'\n'+'职位描述:'+xq_url+'\n')
        return item
    def close_spider(self,spider):
        self.fp.close()
