import matplotlib.pyplot as plt
# 设置中文字体
from matplotlib.font_manager import FontProperties
# 一系列横坐标显示中文
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

font = FontProperties(fname=r'/Users/ankew/Desktop/SimHei.ttf',size=10)

phone_list_one = [1+0.06,1+0.05,1+0.04,1+0.02]
phone_list_two = [1+0.12,1+0.08,1+0.05,1+0.04,1+0.02]
phone_list_three =[1+0.06,1+0.05]

pc_list_one = [1+0.06,1+0.03,1+0.02,1+0.01]
pc_list_two = [1+0.09,1+0.08,1+0.05,1+0.03,1+0.01]
pc_list_three =[1+0.12,1+0.14,1+0.03,1+0.02,1+0.01]

screen_list_one = [1+0.12,1+0.11,1+0.10,1+0.08]
screen_list_two = [1+0.12,1+0.10,1+0.01]

sum_one =[0,0,0]
sum_two = [0,0,0]
sum_three =[0,0]
for i in range (0,len(phone_list_one)):
    sum_one[0] = sum_one[0] + phone_list_one[i]
for i in range (0,len(phone_list_two)):
    sum_one[1] = sum_one[1]+ phone_list_two[i]
for i in range (0,len(phone_list_three)):
    sum_one[2] = sum_one[2]+ phone_list_three[i]
print(sum_one)
for i in range (0,len(pc_list_one)):
    sum_two[0] = sum_two[0] + pc_list_one[i]
for i in range (0,len(pc_list_two)):
    sum_two[1] = sum_two[1]+ pc_list_two[i]
for i in range (0,len(pc_list_three)):
    sum_two[2] = sum_two[2]+ pc_list_three[i]
print(sum_two)
for i in range (0,len(screen_list_one)):
    sum_three[0] = sum_three[0] + screen_list_one[i]
for i in range (0,len(screen_list_two)):
    sum_three[1] = sum_three[1]+ screen_list_two[i]
print(sum_three)

fig = plt.figure(figsize=(10, 8))


plt.figure( dpi=100)
x_label = ['手机外观与体验','购物物流与质量','性能与媒体体验']
plt.plot(x_label, sum_one,color='black')
plt.scatter(x_label, sum_one, c='red',label="人工结果")
y_ticks = range(6)
plt.yticks(y_ticks[::1])
plt.xlabel("主题", fontproperties=font)
plt.ylabel("情感分数", fontproperties=font)
plt.title("评分", fontproperties=font)

new_model_res = [4.483,5.787,2.893]
plt.plot(x_label,new_model_res,color='black')
plt.scatter(x_label,new_model_res,c='green',label=r"模型结果")
plt.legend()
plt.show()

plt.figure( dpi=100)
pc_x_label = ['性能与设计体验','购买与使用体验','购物物流与质量']
plt.plot(pc_x_label, sum_two,color='black')
plt.scatter(pc_x_label, sum_two, c='red',label="人工结果")
y_ticks = range(6)
plt.yticks(y_ticks[::1])
plt.xlabel("主题", fontproperties=font)
plt.ylabel("情感分数", fontproperties=font)
plt.title("评分", fontproperties=font)

pc_new_model_res = [4.483,5.978,5.977]
plt.plot(x_label,pc_new_model_res,color='black')
plt.scatter(x_label,pc_new_model_res,c='green',label=r"模型结果")
plt.legend()
plt.show()