import pandas as pd
import jieba
from gensim import corpora, models
import pyLDAvis.gensim_models as gensimvis
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
import multiprocessing
import datetime

# 开始时间
start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("开始的时间是{}".format(start_time))

# 设置多进程启动方法
multiprocessing.set_start_method('fork')

# 读取数据集
df = pd.read_csv(r"/Users/ankew/Desktop/DataAna/data.csv")

# 中文分词
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

# 去除停用词和标点符号
stopwords = [line.strip() for line in open(r"/Users/ankew/Desktop/stopwords.txt", 'r', encoding='utf-8').readlines()]
df['content_cutted'] = df['comments'].apply(chinese_word_cut)
df['content_cutted'] = df['content_cutted'].apply(
    lambda x : ' '.join([word for word in x.split() if word not in stopwords]))

# 构建语料库
texts = [doc.split() for doc in df['content_cutted']]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 绘制困惑度曲线和主题一致性曲线
coherence_scores = []
perplexity_scores = []
for num_topics in range(2, 20):
    lda_model = models.ldamodel.LdaModel(corpus=corpus,
                                         id2word=dictionary,
                                         num_topics=num_topics,
                                         iterations=1000,
                                         passes=10,
                                         random_state=1)
    coherence_model_lda = models.CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    coherence_scores.append(coherence_lda)
    perplexity_scores.append(lda_model.log_perplexity(corpus))

# 绘制困惑度曲线
x = range(2, 20)
plt.plot(x, perplexity_scores)
plt.xlabel('Number of Topics')
plt.ylabel('Perplexity Score')
plt.show()

# 绘制主题一致性曲线
plt.plot(x, coherence_scores)
plt.xlabel('Number of Topics')
plt.ylabel('Coherence Score')
plt.show()

# 选择合适的主题数量
optimal_num_topics = coherence_scores.index(max(coherence_scores)) + 2
print("Optimal Number of Topics:", optimal_num_topics)

# 训练LDA模型
lda_model = models.ldamodel.LdaModel(corpus=corpus,
                                     id2word=dictionary,
                                     num_topics=optimal_num_topics,
                                     iterations=1000,
                                     passes=10,
                                     random_state=1)

# 可视化主题
vis = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis)
pyLDAvis.save_html(vis, 'IP14PM_LDA_Threetopics.html')  # 将结果保存为该html文件 #文件名字可以任意更改为你想要的名字

# pycharm单独设置显示所有列的结果
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行

# 用表格展示结果
all_topics = {}
num_terms = 10  # Adjust number of words to represent each topic
lambd = 0.6  # Adjust this accordingly based on tuning above lambda constant
for i in range(1, optimal_num_topics + 1):
    topic = vis.topic_info[vis.topic_info.Category == 'Topic' + str(i)].copy()
    topic['relevance'] = topic['loglift'] * (1 - lambd) + topic['logprob'] * lambd
    all_topics['Topic ' + str(i)] = topic.sort_values(by='relevance', ascending=False).Term[:num_terms].values
print(pd.DataFrame(all_topics).T + "\n")

# 结束时间
end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("结束的时间是{}".format(end_time))
