import pandas as pd
import jieba
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# 读取csv文件
df = pd.read_csv(r"/Users/ankew/Desktop/DataAna/data.csv")

# 将评论拼接成一个字符串
text = ' '.join(df['comments'].tolist())

# 中文分词
seg_list = jieba.cut(text)

# 去除停用词
stopwords = set(STOPWORDS)
with open(r"/Users/ankew/Desktop/stopwords.txt", 'r', encoding='utf-8') as f:
    for word in f.readlines():
        stopwords.add(word.strip())

seg_list = [i for i in seg_list if i not in stopwords and i != ' ']

# 统计词频
word_counts = {}
for word in seg_list:
    word_counts[word] = word_counts.get(word, 0) + 1

# 全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 生成词云
wc = WordCloud(background_color="white", max_words=2000,
               font_path='/Users/ankew/opt/anaconda3/pkgs/matplotlib-base-3.5.1-py39hfb0c5b7_1'+
                         '/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimHei.ttf',
               width=400,height=400,scale=2)
wc.generate_from_frequencies(word_counts)

# 显示词云图
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
