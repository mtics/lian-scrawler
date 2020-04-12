# -*- coding:utf-8 -*-

import numpy as np
from pyecharts.charts import *
from pyecharts import options as opts


def get_bar(title, series_name, xaxis_name, yaxis_name, x_data, y_data, save_path):
    bar = Bar()
    bar.add_xaxis(x_data)
    bar.add_yaxis(series_name, y_data)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(name=xaxis_name, axislabel_opts=opts.LabelOpts(rotate=-35)),
        yaxis_opts=opts.AxisOpts(name=yaxis_name)
    )

    bar.render("data/analysis/{0}/{1}.html".format(save_path, title))


def get_pie(data_zip, title, save_path):
    pie = Pie()
    pie.add("", [list(z) for z in data_zip])
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render("data/analysis/{0}/{1}.html".format(save_path, title))


def get_scatter(data_dict, title, save_path):
    scatter = Scatter()

    for key, value_list in data_dict.items():
        nparray = np.array(value_list)
        scatter.add_xaxis(nparray[:, 0])
        scatter.add_yaxis(key, nparray[:, 1])

    scatter.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )

    scatter.width = "1600px"
    scatter.height = "650px"
    scatter.render("data/analysis/{0}/{1}.html".format(save_path, title))
