#_*_ coding:utf-8 _*_
from bs4 import BeautifulSoup   #BeautifulSoup用于解析HTML或者xml文件
from urlparse import urljoin
import  requests
import csv
import time

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

#已完成的页数序号，初值为0
page = 0
csv_file = open("rent.csv","wb")
csv_writer = csv.writer(csv_file,delimiter = ',')

while True:
    page +=1
    print "fetch: ",url.format(page=page)
    # if page % 60 == 0:
    #     time.sleep(3)
    response = requests.get(url.format(page=page))  #抓取目标页面
    html = BeautifulSoup(response.text,"html.parser")
    #print(html.prettify())
    house_list = html.select(".list > li")  #获取class=list的元素下的所有li元素

    #分析页面，以页面有无.list元素来判断是否已读取完所有房源

    #循环在读不到新的房源时结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf8") #得到标签包裹着的文本
        house_url   = urljoin(url,house.select("a")[0]["href"]) #得到标签内属性的值，href得到相对路径，urljoin得到完整路径
        house_info_list = house_title.split()

        #如果第二列是公寓名则去第一列作为地址
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location =house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
        csv_writer.writerow([house_title,house_location,house_money,house_url])

csv_file.close()

