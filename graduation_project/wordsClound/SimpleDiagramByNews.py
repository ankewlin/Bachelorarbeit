import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from plotnine import *

# 读取CSV文件
df = pd.read_csv(r"/Users/ankew/Desktop/manynews.csv")

# 统计每个新闻机构的发文总数
news_count = df.groupby("新闻机构").size().reset_index(name="新闻数量")

# 全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 设置中文字体
font = FontProperties(fname=r'/Users/ankew/opt/anaconda3/pkgs/matplotlib-base-3.5.1-py39hfb0c5b7_1/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimHei.ttf')
theme_set(theme_minimal(base_family=font.get_name()))

# 绘制柱状图
p = (ggplot(news_count, aes(x="新闻机构", y="新闻数量", fill="新闻机构"))
     + geom_col()
     + xlab("新闻机构")
     + ylab("新闻数量")
     + ggtitle("新闻机构发文总数统计")
     + theme(axis_text_x=element_text(angle=90, hjust=1))
    )

# 显示图形
print(p)
