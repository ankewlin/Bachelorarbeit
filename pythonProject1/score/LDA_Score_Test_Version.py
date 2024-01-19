import jieba
import pandas as pd
from gensim.models import LdaModel
from gensim.corpora import Dictionary

# 读取CSV文件
data = pd.read_csv(r"/Users/ankew/Desktop/DataAna/data.csv")

pos_eval_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/pos_eval.csv")
neg_eval_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/neg_eval.csv")

pos_emo_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/pos_emo.csv")
neg_emo_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/neg_emo.csv")

most_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/most.csv")  # 2
very_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/very.csv")  # 1.5
more_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/more.csv")  # 1.25
ish_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/ish.csv")  # 0.5
insufficiently_data = pd.read_csv(r"/Users/ankew/Desktop/HowNet-Encoding=GB18030/insufficiently.csv")  # 0.25

# 提取客户评论文档列表
documents = data["comments"].tolist()

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

# 预处理文档
tokenized_documents = [list(jieba.cut(doc)) for doc in documents]
dictionary = Dictionary(tokenized_documents)
# 将文档转换为BoW表示
corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]

# 训练LDA模型
lda = LdaModel(corpus, num_topics=6, id2word=dictionary, passes=10)

# 提取每个主题下的前15个关键词
topics = lda.show_topics(num_topics=6, num_words=15, formatted=False)

# 把关键词存进去
topics_words = []
for topic in range(0, 6):  # num_topics = 6
    topics_words.append([topic])
for each_topic_num in range(0, 6):
    for element_content in range(0, len(topics[each_topic_num][1])):
        topics_words[each_topic_num].append(topics[each_topic_num][1][element_content][0])

# 弹出首位数字
for num in range(0, len(topics_words)):
    topics_words[num].pop(0)  # 得到纯文本链表 ['，', '的', ' ', '。', '了', '很', '也', '！', '是', '手机', '非常', '用', '好', '灵动', '有']

topics_words[0][0] = '很好'
topics_words[0][1] = '好'
topics_words[0][2] = '不好吃'
topics_words[0][3] = '不好看'
topics_words[0][4] = '味道不好'
topics_words[1][0] = "足足"
topics_words[1][2] = "及"
topics_words[5][0] = "相对"

# 运行算法

# 计算基础评价分数
pos_counter = 0
neg_counter = 0
basis_topics_scores = []

for i in range(0, 6):  # num_topics = 6

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

for i in range(0, 6):  # num_topics = 6

    # 把正负指针置零
    pos_emo_counter = 0
    neg_emo_counter = 0

    # 统计正，负面情感词数
    for content in topics_words[i]:
        if content in pos_emo_list:
            pos_emo_counter = pos_emo_counter + 1
        elif content in neg_emo_list:
            neg_emo_counter = neg_emo_counter + 1

    # 基本分数加上情感词分数
    if basis_topics_scores[i] > 0:
        temp_topics_scores.append(basis_topics_scores[i] + pos_emo_counter * 0.5 - neg_emo_counter * 0.5)
    elif basis_topics_scores[i] < 0:
        temp_topics_scores.append(basis_topics_scores[i] - pos_emo_counter * 0.5 + neg_emo_counter * 0.5)
    else:
        temp_topics_scores.append(basis_topics_scores[i])

# 在临时情感分数上计算最终得分
most_counter = 0
very_counter = 0
more_counter = 0
ish_counter = 0
insufficiently_counter = 0
final_topics_scores = []

for i in range(0, 6):  # num_topics = 6

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
    final_topics_scores.append(temp_topics_scores[i] * (most_counter * 2 + very_counter * 1.5 +
                                                        more_counter * 1.25 + ish_counter * 0.5 +
                                                        insufficiently_counter * 0.25))
print(final_topics_scores)
# [-8.75, 11.875, 7.5, 9.5, 12.5, 0.0]
# [-3.75, 18.75, 9.5, 12.5, 12.5, 9.75]
