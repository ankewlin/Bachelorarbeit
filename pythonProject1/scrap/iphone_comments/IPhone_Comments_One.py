# -*- coding:utf-8 -*-
import requests
import re
import time
import csv

#读取csv文件
csv_header =['numbers','comments']
with open('/Users/ankew/Desktop/data.csv','w',encoding='utf-8',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

# 网址
prefix_url ="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100038004359&score=0&sortType=5&page="
suffix_url ="&pageSize=10&isShadowSku=0&rid=0&fold=1"


# 伪装
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

for i in range(0,100): # 最大页数100页
    url = prefix_url + str(i) + suffix_url

    # 发送请求
    response = requests.get(url=url, headers=headers)
    # print(response)# 打印响应状态 <Response [200]>：表示已经响应成功了

    # 获取数据
    if response.content:
        json_data = response.text

    # 解析数据 列表
    comments = json_data

    # 正则筛选
    res = r'"guid":"[a-zA-Z0-9]{32}"\s*,\s*"content":"(.*?)"'
    content = re.findall(res, comments)

    # 替换掉\n
    contents =[]
    for k in range(0,len(content)): # temp为临时变量
        temp = content[k].replace("\\n","").replace("&ldquo;","").replace("&rdquo;","") # cotent去掉\n变为contents
        contents.append(temp)

    # print(content)
    for index in range(0,len(contents)):
        csv_content =[index+1+i*10,contents[index]]
        with open('/Users/ankew/Desktop/data.csv','a',encoding='utf-8',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(csv_content)
        print("第{num1}条评论 {content}\n".format(num1=10 * i + index + 1,content=contents[index]) )

    # 休息20秒在进行
    time.sleep(3)











