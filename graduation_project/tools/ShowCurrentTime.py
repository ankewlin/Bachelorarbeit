# -*- coding:utf-8 -*-
import datetime

start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("开始的时间是{}".format(start_time))

numsum = 0
for i in range(0,10000000):
    numsum = numsum + i
print(numsum)

end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("结束的时间是{}".format(end_time))
