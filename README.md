# 毕业设计/Graduation Project

这是我在四川农业大学的毕业设计/ This is my graduation project at SAU

# 语言/Computer Language
Pure Python

# 目录/Contents

* data: 测试数据
* nlp: LDA模型实现、部分结果
* score: 关键词打分
* scrap: 爬虫
* tools: 一些杂工具
* wordsClound: 词云实现

# 功能/Functions

* LDA模型实现
* 文本分类
* 文本聚类
* 文本相似性
* 关键词抽取
* 关键短语抽取
* 情感分析
* 文本摘要
* 主题关键词
* 同义词、近义词
* 词云
* 爬虫
* 客户评论
* 文本拆分

# 详细说明/Details

* data : 有三个文件分别存储通过scrap包爬去的电脑、手机、显示器的客户评论
* nlp：FullVersionIdaModel.py 是完全LDA模型实现; Basic_IDATopic是基本LDA框架；其余的根据不同数量而为生成的结果
* score：linear_results包是折线图的结果；log_results包是使用tools中均衡函数设计后的结果；result_of_models_by_types包是有无均衡函数后的对比结果；LDA_Score_Test_Version.py是生成最终综合打分的一个类；其余HTML文件为不同评论生成的结果
* scrap：爬去电脑、手机、显示器客户评论的包
* tools：工具包包括：均衡函数的设计，网络爬虫，显示程序运行时间
* wordsClound: 词云包：是为毕业论文其中一个有个词云显示板块服务。SimppleDiagramByNews.py的目的是为了引入中文字体做测试；WordsCloundDemo：是最终结果展示



