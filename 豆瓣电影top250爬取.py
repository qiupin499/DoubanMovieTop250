
#任务一：爬取豆瓣电影top250的所有网址
import urllib.request
import lxml.html
import cssselect #电脑需要提前安装cssselect模块，lxml.html.fromstring函数会使用这个模块
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} #网址防爬，需要加上这个headers来模拟浏览器
all_web = [] #all_web记录豆瓣电影top250的所有网址
#一、爬取top250首页
req = urllib.request.Request(url='https://movie.douban.com/top250', headers=headers) #爬取首页https://movie.douban.com/top250
con = urllib.request.urlopen(req).read() #获得网址内容
tree = lxml.html.fromstring(con) #对网址内容进行字符串解析
fixed_html = lxml.html.tostring(tree,pretty_print=True)
for i in range(25): #由于首页有25部电影，所以这里是25
    movie_com = tree.cssselect('div.info>div.hd>a')[i].get('href') #遍历所有css为div.info>div.hd>a的内容，这里的href是这些电影的网址
    all_web.append(movie_com)
#二、爬取top250的其它页
for loop in [25,50,75,100,125,150,175,200,225]:
    req = urllib.request.Request(url='https://movie.douban.com/top250?start='+str(loop)+'&filter=', headers=headers) #爬取其它页
    con = urllib.request.urlopen(req).read() #获得网址内容
    tree = lxml.html.fromstring(con) #对网址内容进行字符串解析
    fixed_html = lxml.html.tostring(tree,pretty_print=True)
    for i in range(25): #由于每页有25部电影，所以这里是25
        movie_com = tree.cssselect('div.info>div.hd>a')[i].get('href') #遍历所有css为div.info>div.hd>a的内容，这里的href是这些电影的网址
        all_web.append(movie_com)
print('豆瓣电影Top250的网址是：',all_web)


#任务二：爬取所有电影的具体信息
from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
title_list = []
score_list = []
date_list = []
director_list = []
actor_list = []
runtime_list = []

#遍历每一个网址
for i in all_web:
    url = i
    sesh = Session()  #创建Session类的默认对象
    result = sesh.get(url, headers=headers)  #获取网页内容
    soup = BeautifulSoup(result.text, 'html.parser') #解析
    title_css = "h1>span[property='v:itemreviewed']"  #电影名字css
    score_css = 'strong.ll.rating_num'  #评分css
    date_css = "span[property='v:initialReleaseDate']" #上映日期css
    director_css = "span>a[rel='v:directedBy']" #导演css
    actor_css = "span>a[rel='v:starring']" #主演css
    runtime_css = "span[property='v:runtime']" #片长css

    title_select = soup.select(title_css)
    score_select = soup.select(score_css)
    date_select = soup.select_one(date_css)
    director_select = soup.select_one(director_css)
    actor_select = soup.select_one(actor_css)
    runtime_select = soup.select_one(runtime_css)

    title_list.append(title_select[0].get_text())  #soup.select获取的对象以列表形式储存,所以要切片第一个
    score_list.append(score_select[0].get_text())
    date_list.append(date_select.get_text())  #soup.select_one获取的对象是第一个，所以无需切片
    director_list.append(director_select.get_text())
    if actor_select is None: #由于有些电影没有主演，比如《二十二》，所以这里要进行判断
        actor_list.append('无')
    else:
        actor_list.append(actor_select.get_text())
    runtime_list.append(runtime_select.get_text())

#储存成csv表格
all_info = pd.DataFrame({'电影名':title_list,'评分':score_list,'上映日期':date_list,'导演':director_list,'主演':actor_list,'片长':runtime_list,'网址':all_web}) #储存成pandas的数据框格式
print('所有豆瓣电影Top250信息：',all_info)
all_info.to_csv('DoubanMovie_Top250.csv',header=True)

