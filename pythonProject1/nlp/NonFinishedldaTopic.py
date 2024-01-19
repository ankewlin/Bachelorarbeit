import pandas as pd
import jieba
from gensim import corpora, models
from multiprocessing import freeze_support
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt

# 定义停用词
stopwords_path = r'/Users/ankew/Desktop/stopwords.txt'
stopwords = [line.strip() for line in open(stopwords_path, 'r', encoding='utf-8').readlines()]

# 读取数据
df = pd.read_csv(r"/Users/ankew/Desktop/manynews.csv")

# 对新闻内容概述进行分词处理
def cut_words(text):
    return [word for word in jieba.cut(text) if word not in stopwords]

df['新闻分词'] = df['新闻内容概述'].apply(cut_words)

# 构建词典和语料库
dictionary = corpora.Dictionary(df['新闻分词'])
corpus = [dictionary.doc2bow(words) for words in df['新闻分词']]

# 训练LDA模型
def train_lda(num_topics):
    lda_model = models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics, workers=3, passes=10)
    return lda_model

if __name__ == '__main__':
    freeze_support()
    # 设置主题数范围
    topic_range = range(2, 20)
    perplexity_list = []
    coherence_scores = []

    # 计算不同主题数下的困惑度
    for num_topics in topic_range:
        lda_model = train_lda(num_topics)
        perplexity = lda_model.log_perplexity(corpus)
        perplexity_list.append(perplexity)
        coherence_lda = lda_model.get_coherence(corpus)
        coherence_scores.append(coherence_lda)
        print(f"Num Topics: {num_topics}, Perplexity Score: {perplexity}, Coherence Score{coherence_lda}")

    # 绘制困惑度曲线
    plt.plot(topic_range, perplexity_list)
    plt.xlabel("Num Topics")
    plt.ylabel("Perplexity Score")
    plt.show()

    # 绘制主题一致性曲线
    plt.plot(topic_range, coherence_scores)
    plt.xlabel('Number of Topics')
    plt.ylabel('Coherence Score')
    plt.show()

    # 选择合适的主题数量
    optimal_num_topics = coherence_scores.index(max(coherence_scores)) + 2
    print("Optimal Number of Topics:", optimal_num_topics)


    # 训练最终的LDA模型
    final_lda_model = train_lda(optimal_num_topics)

    # 可视化结果
    vis = pyLDAvis.gensim_models.prepare(final_lda_model, corpus, dictionary)
    pyLDAvis.display(vis)
    pyLDAvis.save_html(vis, 'lda_1.html')  # 将结果保存为该html文件



