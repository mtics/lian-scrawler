# -*- coding: utf-8 -*-
import pandas as pd
import os
import csv
import glob


def get_required_columns(dataframe, columns_names):
    """
    只保留需要用到的列
    :param dataframe:
    :param columns_names: 需要用到的列名称
    :return: 只保留需要用到的列的dataframe
    """
    dataframe = dataframe[columns_names]
    return dataframe


def open_as_dataframe(filename):
    """
    将单个csv文件打开成dataframe格式
    :param filename: 要打开的文件名
    :return df: 存储文件内容的dateframe
    """
    if os.path.exists(filename):
        df = pd.read_csv(filename, encoding="gbk", sep=",")
        # 筛选问题数据
        df = df[df.hid is not None and df.rent > 0]
        df = df.dropna(axis=0, thresh=35)  # 用于去掉因网络连接问题导致的数据丢失行
        # 去掉重复行
        df = df.drop_duplicates()
        return df
    else:
        return []


def open_many_as_dataframe(files_path, files_name):
    """
    批量打开多个csv文件成dataframe对象
    :param files_path: 文件路径
    :param files_name: 匹配文件名
    :return df: 存储文件内容的dateframe
    """
    files = glob.glob(os.path.join(files_path, files_name))
    dl = []
    file_name = ''
    try:
        for file in files:
            file_name = file
            dd = open_as_dataframe(file)
            dl.append(dd)
        if dl != None:
            df = pd.concat(dl)
        return df
    except Exception as e:
        print(file_name + "\n")
        print(e)


def open_as_file(filename):
    """
    检查文件是否存在
    """
    if os.path.exists(filename):
        csv_reader = csv.reader(open(filename))
        # for row in csv_reader:
        #     print(row)

        column = [row[40] for row in csv_reader]
        print(column)
        return csv_reader
    else:
        return []
