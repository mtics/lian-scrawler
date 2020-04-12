# 导入扩展库
import re  # 正则表达式库
import collections  # 词频统计库
import numpy as np  # numpy数据处理库
import jieba  # 结巴分词
import wordcloud
from PIL import Image  # 图像处理库
import matplotlib.pyplot as plt  # 图像展示库


def get_hot_words(dataframe):
    # 文本预处理
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|\"|[0-9]*')  # 定义正则表达式匹配模式
    string_data = re.sub(pattern, '', str(dataframe['description']))  # 将符合模式的字符去除

    # 文本分词
    seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
    object_list = []
    remove_words = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。',
                    u' ', u'、', u'中', u'在', u'了', u'通常', u'如果', u'我们', u'需要',
                    u'【', u'】', u'路', u'NaN', u'站', u'就', u'到', u'这', u'NaNName', u'dtype',
                    u'min', u'object', 'description', u'：', u'上海', u'松江', u'您', u'有',
                    u'Unnamed', u'魔', u'之所以', u'源于', u'一席之地', u'（', u'）', u'车墩',u'_',
                    u'自', u'level', u'描述', u'介绍', u'columns', u'rows', u'房源', u',', u'Length',
                    u'小区', u'线', u'米', u'号', u'本', u'亮点']  # 自定义去除词库

    for word in seg_list_exact:  # 循环读出每个分词
        if word not in remove_words:  # 如果不在去除词库中
            object_list.append(word)  # 分词追加到列表

    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
    print(word_counts_top10)  # 输出检查

    # 词频展示
    wc = wordcloud.WordCloud(background_color='white',
                             font_path='resources/simsun.ttc',
                             max_words=200,
                             max_font_size=100,
                             scale=32)
    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    wc.to_file("data/analysis/description_hot_words.jpg")  # 将图片输出为文件
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像
