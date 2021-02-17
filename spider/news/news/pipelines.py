# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
# 存储所有数据
class NewsPipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        support = item['support']
        category = item['category']
        name ='{}.txt'.format(category)
        with open('./'+name, 'a+', encoding='utf-8') as f:
            f.write('       '+title+'       '+'点击数:'+support+'\n'+content+"--"*50)
        return item

# 获取分类与点击数，做数据分析
class New2Pipeline(object):
    coon = None
    cursor =None
    def open_spider(self,spider):
        self.coon =pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='mysql',db='news',charset='utf8')

    def process_item(self, item, spider):
        support = item['support']
        category = item['category']
        self.cursor =self.coon.cursor()
        try:
            self.cursor.execute('insert into wy_news values("%s","%s")'%(category,int(support)))
        except Exception as e:
            print(e)
            self.coon.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.coon.close()



