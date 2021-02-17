import pymysql
import pandas as pd
from pylab import *
from matplotlib import font_manager
import random
plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签
plt.rcParams['axes.unicode_minus']=False
my_font=font_manager.FontProperties(fname="C:\Windows\Fonts\simsun.ttc")

plt.figure(figsize=(20,8),dpi=80)
# 连接配置信息
config = {
    'host': '127.0.0.1',
    'port': 3306,  # MySQL默认端口
    'user': 'root',  # mysql默认用户名
    'password': 'mysql',
    'db': 'news',  # 数据库
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 创建连接
con = pymysql.connect(**config)
# 执行sql语句
try:
    with con.cursor() as cursor:
        sql = "select category,sum(support) from wy_news group by category"
        cursor.execute(sql)
        result = cursor.fetchall()

finally:
    con.close();
df = pd.DataFrame(result)  # 转换成DataFrame格式

data = df['sum(support)']
name =df['category']

for a,b in zip(name,data):
    plt.text(a, float(b)+1, '%.0f' % float(b), ha='center',fontsize=15)

plt.bar(name, data,color =['#d867da','#7eccc1','#112374','#a761e9','#e9675d'])

# 设置横轴标签
plt.xlabel('分类')

# 设置纵轴标签
plt.ylabel('点击数')
plt.grid(alpha=0.4)
# 添加标题
plt.title('最受欢迎新闻类',fontsize=20)

plt.show()