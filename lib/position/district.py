# coding: utf-8

import requests
from lxml import etree
from lib.request.headers import *
from lib.const.xpath import *

districts_dict = {'jingan': '静安', 'xuhui': '徐汇',
                   'huangpu': '黄浦', 'changning': '长宁',
                   'putuo': '普陀', 'pudong': '浦东',
                   'baoshan': '宝山', 'hongkou': '虹口',
                   'yangpu': '杨浦', 'minhang': '闵行',
                   'jinshan': '金山', 'jiading': '嘉定',
                   'chongming': '崇明', 'fengxian': '奉贤',
                   'songjiang': '松江', 'qingpu': '青浦'}


def get_districts():
    """
    获取上海所有区名（拼音格式）
    """
    url = "https://sh.lianjia.com/zufang/"
    headers = create_headers()
    reponse = requests.get(url, timeout=10, headers=headers)
    html = reponse.content  # 获取网页内容
    root = etree.HTML(html)
    elements = root.xpath(CITY_DISTRICT_XPATH)
    districts = list()
    for element in elements:
        link = element.attrib['href']
        text = element.text
        if link != '/zufang/':
            districts.append(link.split('/')[-2])

    return districts


def get_district_url(district):
    """
    按小区获取链接
    district: 区域
    """
    return "https://sh.lianjia.com/zufang/{0}".format(district)


if __name__ == "__main__":
    get_districts()
