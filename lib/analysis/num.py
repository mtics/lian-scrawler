from lib.util.charts import *
from lib.util.file import *


def get_num_pie(dic, title):
    """
    将获取的房源数量生成柱状图
    :param dic: 包含{索引:数量}的词典
    :param title: 饼状图标题
    :return:
    """
    try:
        dict_zip = zip(dic.keys(), dic.values())
        get_pie(dict_zip, title, "房源数量")
    except Exception as e:
        print(e)


def get_num_group(dataframe, group_name):
    """
    获取数量
    :param dataframe:
    :param group_name: 分组标签名
    :return dic: 键值对{分组名:数量}
    """
    dic = dict()
    group = dataframe.groupby(group_name)
    a = group.hid
    for i in a.indices:
        dic[i] = a.groups[i].shape[0]
    return dic


def get_num(dataframe):
    """
    获取数量(不分组)
    :param dataframe:
    :return num: 指定分组中的数据数量
    """
    num = dataframe.shape[0]
    return num
