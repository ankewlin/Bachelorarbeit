import pandas as pd
import jieba
from gensim import corpora, models
import pyLDAvis.gensim_models as gensimvis
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
import multiprocessing
import datetime
import math as ma

# 开始时间
start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("开始的时间是{}".format(start_time))

# 设置多进程启动方法
multiprocessing.set_start_method('fork')

# 读取数据集
df = pd.read_csv(r"/Users/ankew/Desktop/DataAna/data.csv")

# 读取情感词典集合以及副词集合
pos_eval_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/pos_eval.csv")
neg_eval_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/neg_eval.csv")

pos_emo_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/pos_emo.csv")
neg_emo_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/neg_emo.csv")

most_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/most.csv")  # 2
very_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/very.csv")  # 1.5
more_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/more.csv")  # 1.25
ish_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/ish.csv")  # 0.5
insufficiently_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/insufficiently.csv")  # 0.25

# 获取正负评价文档列表并去除后缀r"\xa0"
pos_eval_list = pos_eval_data["contents"].tolist()
for i in range(0, len(pos_eval_list)):
    pos_eval_list[i] = "".join(pos_eval_list[i].split())
neg_eval_list = neg_eval_data["contents"].tolist()
for i in range(0, len(neg_eval_list)):
    neg_eval_list[i] = "".join(neg_eval_list[i].split())

# 获取正负情感文档列表并去除后缀r"\xa0"
pos_emo_list = pos_emo_data["contents"].tolist()
for i in range(0, len(pos_emo_list)):
    pos_emo_list[i] = "".join(pos_emo_list[i].split())
neg_emo_list = neg_emo_data["contents"].tolist()
for i in range(0, len(neg_emo_list)):
    neg_emo_list[i] = "".join(neg_emo_list[i].split())

# 获取程度副词文档列表并去除后缀r"\xa0"
most_list = most_data["contents"].tolist()
for i in range(0, len(most_list)):
    most_list[i] = "".join(most_list[i].split())
very_list = very_data["contents"].tolist()
for i in range(0, len(very_list)):
    very_list[i] = "".join(very_list[i].split())
more_list = more_data["contents"].tolist()
for i in range(0, len(more_list)):
    more_list[i] = "".join(more_list[i].split())
ish_list = ish_data["contents"].tolist()
for i in range(0, len(ish_list)):
    ish_list[i] = "".join(ish_list[i].split())
insufficiently_list = insufficiently_data["contents"].tolist()
for i in range(0, len(insufficiently_list)):
    insufficiently_list[i] = "".join(insufficiently_list[i].split())

# 中文分词
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

# 去除停用词和标点符号
stopwords = [line.strip() for line in open(r"/Users/ankew/Desktop/stopwords.txt", 'r', encoding='utf-8').readlines()]
df['content_cutted'] = df['comments'].apply(chinese_word_cut)
df['content_cutted'] = df['content_cutted'].apply(
    lambda x: ' '.join([word for word in x.split() if word not in stopwords]))

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
pyLDAvis.save_html(vis, 'screen_comments_result_random_two.html')  # 将结果保存为该html文件

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

# 提取每个主题下的前30个关键词
topics = lda_model.show_topics(num_topics=optimal_num_topics, num_words=30, formatted=False)

# 把关键词存进去
topics_words = []
for topic in range(0, optimal_num_topics):  # num_topics = optimal_num_topics
    topics_words.append([topic])
for each_topic_num in range(0, optimal_num_topics): # num_topics = optimal_num_topics
    for element_content in range(0, len(topics[each_topic_num][1])):
        topics_words[each_topic_num].append(topics[each_topic_num][1][element_content][0])

# 弹出首位数字
for num in range(0, len(topics_words)):
    topics_words[num].pop(0)  # 得到纯文本链表

# 运行算法

# 计算基础评价分数
pos_counter = 0
neg_counter = 0
basis_topics_scores = []

for i in range(0, optimal_num_topics):  # num_topics = optimal_num_topics

    # 把正负指针置零
    pos_counter = 0
    neg_counter = 0

    for content in topics_words[i]:

        # 统计正，负面评价词数
        if content in pos_eval_list:
            pos_counter = pos_counter + 1

        elif content in neg_eval_list:
            neg_counter = neg_counter + 1

    # 一共6轮，每轮正负评价词数统计完毕后进行比较赋值

    if pos_counter > neg_counter:
        # 如果pos_counter > neg_counter,该主题下的关键词是积极的,句子基本值设定为 +2
        basis_topics_scores.append(+2)

    elif pos_counter < neg_counter:
        # 如果pos_counter < neg_counter,该主题下的关键词是消极的,句子基本值设定为 -2
        basis_topics_scores.append(-2)
    else:
        # 如果pos_counter = neg_counter,该主题下的关键词是中性的,句子基本值设定为 0
        basis_topics_scores.append(0)

# print(basis_topics_scores) # 打印基本情感分数

# 在基础评价分数上计算临时情感分数
pos_emo_counter = 0
neg_emo_counter = 0
temp_topics_scores = []
log_temp_pos = 0
log_temp_neg = 0

for i in range(0, optimal_num_topics):  # num_topics = 6

    # 把正负指针置零
    pos_emo_counter = 0
    neg_emo_counter = 0

    # 统计正，负面情感词数
    for content in topics_words[i]:
        if content in pos_emo_list:
            pos_emo_counter = pos_emo_counter + 1
        elif content in neg_emo_list:
            neg_emo_counter = neg_emo_counter + 1

    #liyong
    if pos_emo_counter >= 1 :
        log_temp_pos = pos_emo_counter / ma.log(pos_emo_counter + 1)
    elif neg_emo_counter >= 1 :
        log_temp_neg = neg_emo_counter / ma.log(neg_emo_counter + 1)
    # elif pos_emo_counter == 1:
    #     log_temp_pos = 1
    # elif neg_emo_counter == 1:
    #     log_temp_neg = 1
    elif pos_emo_counter == 0:
        log_temp_pos = 0
    elif neg_emo_counter == 0:
        log_temp_neg = 0

    # 基本分数加上情感词分数
    if basis_topics_scores[i] > 0:
        temp_topics_scores.append(basis_topics_scores[i] + log_temp_pos * 0.5 - log_temp_neg * 0.5)
    elif basis_topics_scores[i] < 0:
        temp_topics_scores.append(basis_topics_scores[i] - log_temp_pos * 0.5 + log_temp_neg * 0.5)
    else:
        temp_topics_scores.append(basis_topics_scores[i])

# 在临时情感分数上计算最终得分
most_counter = 0
very_counter = 0
more_counter = 0
ish_counter = 0
insufficiently_counter = 0
final_topics_scores = []

for i in range(0, optimal_num_topics):  # num_topics = 6

    # 各类指针置零
    most_counter = 0
    very_counter = 0
    more_counter = 0
    ish_counter = 0
    insufficiently_counter = 0

    # 统计各类词的个数
    for content in topics_words[i]:
        if content in most_list:
            most_counter = most_counter + 1
        elif content in very_list:
            very_counter = very_counter + 1
        elif content in more_list:
            more_counter = more_counter + 1
        elif content in ish_list:
            ish_counter = ish_counter + 1
        elif content in insufficiently_list:
            insufficiently_counter = insufficiently_counter + 1
    # 防止程度副词为0个
    if most_counter+very_counter+more_counter+ish_counter+insufficiently_counter == 0:
        final_topics_scores.append(temp_topics_scores[i])
    else:
        final_topics_scores.append(temp_topics_scores[i] * (most_counter * 2 + very_counter * 1.5 +
                                                            more_counter * 1.25 + ish_counter * 0.5 +
                                                            insufficiently_counter * 0.25))
    # 最终结果
print(final_topics_scores)

# 结束时间
end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("结束的时间是{}".format(end_time))



# 0。75
#             0     1     2     3     4     5     6     7       8     9
# Topic 1  拍照\n  运行\n  屏幕\n  效果\n  速度\n  外观\n  音效\n  外形\n  待机时间\n  好看\n
# Topic 2  手机\n  京东\n   买\n  满意\n  质量\n  苹果\n  物流\n  不错\n    收到\n  购买\n
# Topic 3  效果\n  拍照\n  屏幕\n  外观\n  外形\n  运行\n  速度\n  音效\n  待机时间\n  特色\n
# [4.482798189170424, 5.786940292891443, 2.8934701464457215]

#             0     1     2     3      4     5     6     7     8      9
# Topic 1  运行\n  速度\n  外观\n  屏幕\n   轻薄\n  效果\n  散热\n  性能\n  外形\n   程度\n
# Topic 2  华为\n  电脑\n   买\n  办公\n  笔记本\n  手机\n  开机\n  系统\n  不错\n  第一次\n
# Topic 3  京东\n  质量\n  物流\n  满意\n   购物\n  值得\n  不错\n  包装\n  购买\n   收到\n
# [4.482798189170424, 5.9770642522272315, 5.9770642522272315]

#              0     1     2     3      4      5     6     7     8     9
# Topic 1   效果\n  游戏\n  外观\n  尺寸\n  刷新率\n   大小\n  外形\n  不错\n   寸\n  显色\n
# Topic 2  显示器\n   买\n  京东\n  质量\n   不错\n  性价比\n  满意\n  价格\n  物流\n   高\n
# [4.482798189170424, 2.8934701464457215]

# 0。5
#             0     1     2     3     4     5     6     7       8     9
# Topic 1  拍照\n  运行\n  屏幕\n  效果\n  速度\n  外观\n  音效\n  外形\n  待机时间\n  好看\n
# Topic 2  手机\n  京东\n   买\n  满意\n  质量\n  苹果\n  物流\n  不错\n    收到\n  购买\n
# Topic 3  效果\n  拍照\n  屏幕\n  外观\n  外形\n  运行\n  速度\n  音效\n  待机时间\n  特色\n
# [4.637035001905938, 6.466303462376432, 3.233151731188216]

# 1.0
#             0     1     2     3     4     5     6     7       8     9
# Topic 1  拍照\n  运行\n  屏幕\n  效果\n  速度\n  外观\n  音效\n  外形\n  待机时间\n  好看\n
# Topic 2  手机\n  京东\n   买\n  满意\n  质量\n  苹果\n  物流\n  不错\n    收到\n  购买\n
# Topic 3  效果\n  拍照\n  屏幕\n  外观\n  外形\n  运行\n  速度\n  音效\n  待机时间\n  特色\n
# [4.365358839940256, 5.442695040888964, 2.721347520444482]