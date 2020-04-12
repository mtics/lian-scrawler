# -*- coding:utf-8 -*-

from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns

sns.set_style("whitegrid")

plt.style.use(style="ggplot")
plt.rcParams['font.family'] = 'SimHei'  # 配置中文字体
plt.rcParams['font.size'] = 15  # 更改默认字体大小

transfer = DictVectorizer()

model_gbr_GridSearch = GradientBoostingRegressor()

param_dict = {'n_estimators': [60, 90, 120, 150, 180, 200],
              'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2],
              'max_depth': [4, 6, 8, 11],
              'min_samples_leaf': [1, 2, 4, 6, 8],
              'max_features': [0.1, 0.3, 0.5, 0.8]}

features = ["rent", "area", "floor", "distance", "tv", "refri", "air", "wash", "water_heater", "air_heater",
            "bed",
            "wideband", "wardrobe", "gas", "park", "elevator", "natgas"]


def test(dataframe):
    """
    本方法用来输出数据集中的一些数据，
    同时也能用来验证数据集是否正常读取
    :param dataframe: 存储文件内容的dateframe
    """
    print(dataframe.shape)
    print(dataframe.info())
    print(dataframe.isnull().sum())

    dataframe = dataframe[["rent", "area", "floor", "distance"]]
    dataframe.hist(bins=50, figsize=(15, 15))

    plt.show()


def change_data_type(dataframe):
    """
    修改数据类型,同时去掉了部分极端数据
    :param dataframe:存储文件内容的dateframe
    :return:类型修改后的dateframe
    """
    dataframe = dataframe[dataframe.rent < 40000]
    dataframe = dataframe[dataframe.area <= 400]
    dataframe = dataframe[dataframe.area > 0]
    dataframe = dataframe[dataframe.distance.notna()]

    # 楼层数据信息中只保存楼层数
    dataframe["floor"] = dataframe["floor"].str.extract(r'(\d+)', expand=False)
    dataframe["floor"] = dataframe["floor"].astype("int64")
    dataframe = dataframe[dataframe.floor <= 40]

    # 因能力有限，没办法计算所有的房源到地铁站的距离
    # 故房源到地铁站的距离暂时只保留第一个
    dataframe["distance"] = dataframe["distance"].apply(lambda x: eval(x.split(';')[0].split("-")[2].replace("m", "")))
    dataframe["distance"] = dataframe["distance"].astype("int64")

    # 计算每平米租金
    dataframe["area"] = dataframe["area"].astype("int64")
    dataframe['avg_rent'] = dataframe.apply(lambda x: x['rent'] / x['area'], axis=1)

    dataframe["update_time"] = dataframe["update_time"].astype("datetime64")
    dataframe["tv"] = dataframe["tv"].astype("bool")
    dataframe["refri"] = dataframe["refri"].astype("bool")
    dataframe["air"] = dataframe["air"].astype("bool")
    dataframe["wash"] = dataframe["wash"].astype("bool")
    dataframe["water_heater"] = dataframe["water_heater"].astype("bool")
    dataframe["air_heater"] = dataframe["air_heater"].astype("bool")
    dataframe["bed"] = dataframe["bed"].astype("bool")
    dataframe["wideband"] = dataframe["wideband"].astype("bool")
    dataframe["wardrobe"] = dataframe["wardrobe"].astype("bool")
    dataframe["gas"] = dataframe["gas"].astype("bool")
    dataframe["elevator"] = dataframe["elevator"].astype("bool")
    dataframe["natgas"] = dataframe["natgas"].astype("bool")

    return dataframe


def get_rent_describe(dataframe):
    print(dataframe.rent.describe())

    plt.figure(figsize=(10, 5))

    print("skew", dataframe.rent.skew())

    # sns.distplot(dataframe["rent"])

    # 对目标进行对数变换
    target = np.log(dataframe.rent)
    sns.distplot(target)

    plt.show()


def get_correlation_between_rent_area_facilities(dataframe):
    """
    将房租价格与部分信息进行比较，获取相关性
    :param dataframe: 存储文件内容的dateframe
    :return:
    """
    corrMat = dataframe[features].corr()
    mask = np.array(corrMat)
    mask[np.tril_indices_from(mask)] = False
    plt.subplots(figsize=(20, 10))
    plt.xticks(rotation=60)
    sns.heatmap(corrMat, mask=mask, vmax=.8, square=True, annot=True)
    print(corrMat["rent"].sort_values(ascending=False))
    plt.show()


def get_rent_area_layout(dataframe):
    area = dataframe["area"]
    rent = dataframe["rent"]
    layout = dataframe["layout"]

    # 房屋面积和价格的分析
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)  # 一行两列第一个图
    plt.scatter(area, rent)
    plt.xlabel('房屋面积')
    plt.ylabel('租金')

    plt.subplot(1, 2, 2)  # 一行两列第一个图
    plt.title('面积统计', fontsize=20, )
    plt.hist(area, bins=15)  # bins指定有几条柱状
    plt.xlabel('房屋面积')
    # plt.show()

    # 房屋户型和租金的分析
    plt.figure(figsize=(30, 5))
    plt.subplot(1, 2, 1)  # 一行两列第一个图
    # type = list(type)
    plt.scatter(layout, rent)
    plt.xlabel('房屋户型')
    plt.ylabel('租金')

    plt.subplot(1, 2, 2)  # 一行两列第二图
    plt.title('户型统计', fontsize=12)
    layout.value_counts().plot(kind='bar', )  # 绘制条形图
    plt.xticks(ticks=30)
    plt.xlabel('房屋户型')
    plt.show()


def get_rent_distance(dataframe):
    plt.subplots(figsize=(10, 20))
    sns.jointplot(x="distance", y='avg_rent', kind="hex", data=dataframe)
    sns.regplot(x="distance", y='avg_rent', data=dataframe, scatter=False)
    plt.show()


def get_rent_facilities(dataframe):
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='tv', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='refri', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='air', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='wash', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='water_heater', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='air_heater', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='bed', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='wideband', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='wardrobe', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='gas', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='electricity', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='elevator', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='water', data=dataframe)
    plt.subplots(figsize=(10, 15))
    sns.violinplot(x='avg_rent', y='district', hue='natgas', data=dataframe)

    plt.show()


def construct_features(dataframe):
    # 构造特征向量与目标向量
    # X_features = ["area", "floor", "distance"]
    X_features = ["area", "floor", "distance", "tv", "refri", "air", "wash", "water_heater", "air_heater", "bed",
                  "wideband", "wardrobe", "gas", "park", "elevator", "natgas"]
    X = dataframe[X_features]
    X = X.to_dict(orient="records")
    y = dataframe["avg_rent"]

    # 创建训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=22)

    X_train = transfer.fit_transform(X_train)
    X_test = transfer.transform(X_test)

    # 因寻找最优参数时间过长，故暂时不寻找最优参数
    # estimator = GridSearchCV(model_gbr_GridSearch, param_grid=param_dict)
    # estimator.fit(X_train, y_train)
    # print(estimator.best_params_)
    # print(estimator.score(X_test, y_test))

    gdbt_regression(X_train, X_test, y_train, y_test)
    rfr_regression(X_train, X_test, y_train, y_test)


def gdbt_regression(X_train, X_test, y_train, y_test):
    """
    GDBT回归分析
    :param X_train:
    :param X_test:
    :param y_train:
    :param y_test:
    :return:
    """
    model_gbr = GradientBoostingRegressor()
    model_gbr.fit(X_train, y_train)
    mlp_score = model_gbr.score(X_test, y_test)
    print(mlp_score)

    model_best_gbr = GradientBoostingRegressor(learning_rate=0.2, max_features=0.5, min_samples_leaf=1, max_depth=11,
                                               n_estimators=200)
    model_best_gbr.fit(X_train, y_train)
    y_predict1 = model_best_gbr.predict(X_test)
    mlp_best_score = model_best_gbr.score(X_test, y_test)
    print(mlp_best_score)
    # 设置大小
    fig = plt.figure(figsize=(300, 5))
    # 绘制数据
    line1, = plt.plot(range(len(y_test)), y_predict1, 'b-', label='gbr', linewidth=2)
    line2, = plt.plot(range(len(y_test)), y_test, 'r-', label='实际', linewidth=2)
    # 添加网格线
    plt.grid(True, linewidth=2)
    # 优化图表
    fig.tight_layout()
    # 添加图
    plt.legend(handles=[line1, line2])
    plt.show()


def rfr_regression(X_train, X_test, y_train, y_test):
    """
    随机森林回归分析
    :param X_train:
    :param X_test:
    :param y_train:
    :param y_test:
    :return:
    """
    model_RFR = RandomForestRegressor()
    model_RFR.fit(X_train, y_train)
    RFR_score = model_RFR.score(X_test, y_test)
    print(RFR_score)

    model_RFR = RandomForestRegressor(max_features=0.5, min_samples_leaf=1, n_estimators=200)
    model_RFR.fit(X_train, y_train)
    RFR_score = model_RFR.score(X_test, y_test)
    print(RFR_score)
    y_predict2 = model_RFR.predict(X_test)
    # 设置大小
    fig = plt.figure(figsize=(300, 5))
    # 绘制数据
    line1, = plt.plot(range(len(y_test)), y_predict2, 'b-', label='RF', linewidth=2)
    line2, = plt.plot(range(len(y_test)), y_test, 'r-', label='实际', linewidth=2)
    # 添加网格线
    plt.grid(True, linewidth=2)
    # 优化图表
    fig.tight_layout()
    # 添加图
    plt.legend(handles=[line1, line2])
    plt.show()
