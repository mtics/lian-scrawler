# -*- coding: utf-8 -*-

import pandas as pd
from lib.util.charts import *
from lib.util.file import *


def get_average_rent_bar(average_rent, bar_info):
    """
    将获取的租房均价生成柱状图
    :param average_rent: 租房均价列表
    :param bar_info: 柱状图信息列表 [title, series_name, xaxis_name]
    :return:
    """
    try:
        rent_list = [round(i, 2) for i in average_rent.values.tolist()]
        get_bar(bar_info[0], bar_info[1], bar_info[2], '元/m²',
                average_rent.index.tolist(), rent_list, '房租均价')
    except Exception as e:
        print(e)


def get_average_rent(dataframe, group_name):
    """
    求租房均价（元/㎡）
    :param dataframe:
    :param group_name: 分组标签名
    :return average_rent:键值对{分组依据：租房均价}
    """
    try:
        all_average = dataframe['area'].mean()
        dataframe = get_required_columns(dataframe, [group_name, 'rent', 'area'])
        dataframe['average_rent'] = dataframe.apply(lambda x: x['rent'] / x['area'], axis=1)
        average_rent = dataframe.groupby(group_name)['average_rent'].mean()
        print(all_average)
        return average_rent
    except Exception as e:
        print(e)


def get_distance_rent(dataframe, group_name):
    dataframe = get_required_columns(dataframe, [group_name, "rent", "distance"])
    dataframe = dataframe.dropna(how="any")
    groups = dataframe.groupby(group_name)
    data_dict = dict()
    for gn, ga in groups:
        data_list = []
        for row in ga.iterrows():
            ds_list = row[1].values[2].strip().split(";")
            for data in ds_list:
                if data is not '':
                    ds = int(data.split("-")[2].replace("m", ""))
                    data_list.append([row[1].values[1], ds])
        data_dict[gn] = data_list

    return data_dict


def get_distance_rent_scatter(data_dict, title):
    get_scatter(data_dict, title, "分布图")
