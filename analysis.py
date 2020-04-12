# -*- coding: utf-8 -*-

from lib.analysis.rent import *
from lib.analysis.description import *
from lib.analysis.num import *
from lib.analysis.analysis import *
from lib.util.file import *
from lib.position.district import *
from lib.position.subdistrict import *

file_path = "data/data/sh/20200226"


def average_rent():
    districts = get_districts()

    house_data = open_many_as_dataframe(file_path, "*")
    subdistrict_average_rent = get_average_rent(house_data, 'district')
    bar_info = ['上海市租房均价', '', '区县']
    get_average_rent_bar(subdistrict_average_rent, bar_info)

    for district in districts:
        house_data = open_many_as_dataframe(file_path, district + "*")

        subdistrict_average_rent = get_average_rent(house_data, 'subdistrict')
        bar_info = ['上海市{0}区(县)租房均价'.format(districts_dict[district]), '', '区域']
        get_average_rent_bar(subdistrict_average_rent, bar_info)

        subdistricts = get_subdistricts(district)
        if subdistricts == None:
            pass

        for subdistrict in subdistricts:
            subdistrict_average_rent = get_average_rent(house_data, 'community')
            bar_info = ['上海市{0}区(县){1}租房均价'.format(districts_dict[district], subdistricts_dict[subdistrict]), '', '小区']
            get_average_rent_bar(subdistrict_average_rent, bar_info)


def get_nums():
    districts = get_districts()

    house_data = open_many_as_dataframe(file_path, "*")
    total_num = get_num(house_data)
    print(total_num)

    district_num_dict = dict()
    for district in districts:
        house_data = open_many_as_dataframe(file_path, district + "*")

        district_num_dict[districts_dict[district]] = get_num(house_data)

        subdistricts = get_subdistricts(district)
        if subdistricts == None:
            pass

        subdistrict_num_dict = get_num_group(house_data, "subdistrict")

        print(subdistrict_num_dict)
        get_num_pie(subdistrict_num_dict, "上海市{0}区(县)房源数量".format(district))

    print(district_num_dict)
    get_num_pie(district_num_dict, "上海市房源数量")


def distance_rent():
    districts = get_districts()

    house_data = open_many_as_dataframe(file_path, "*")

    for district in districts:
        house_data = open_many_as_dataframe(file_path, district + "*")

        subdistricts = get_subdistricts(district)
        if subdistricts == None:
            pass

        subdistrict_num_dict = get_distance_rent(house_data, "subdistrict")

        print(subdistrict_num_dict)
        get_distance_rent_scatter(subdistrict_num_dict, "上海市{0}区(县)区域房源数量".format(districts_dict[district]))
        # get_num_pie(subdistrict_num_dict, "上海市{0}区(县)房源数量".format(district))


def get_analysis():
    house_data = open_many_as_dataframe(file_path, "*")

    df = change_data_type(house_data)
    # test(df)
    # get_rent_describe(df)
    # get_correlation_between_rent_area_facilities(df)
    construct_features(df)
    # get_rent_area_layout(df)
    # get_rent_distance(df)
    # get_rent_facilities(df)

if __name__ == "__main__":
    # house_data = open_many_as_dataframe(file_path, "*")

    # 获取房源描述中的热词
    # get_hot_words(house_data)

    # 获取平均租金
    # average_rent()

    # 获取房源信息条数
    # get_nums()

    # 获取到地铁站的距离与租金的散点图
    # distance_rent()

    # 进行具体分析
    get_analysis()
