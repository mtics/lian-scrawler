# conding=utf-8

from lib.entity.distance_to_subway import *
from lib.entity.facility import *
from lib.entity.base_info import *


class House(object):
    # 以下为列表页展示信息
    hid = ''  # 房源id
    name = ''  # 房源名字
    pre_img = ''  # 房源列表图
    district = ''  # 区县
    subdistrict = ''  # 区域
    community = ''  # 小区
    area = 0  # 面积
    layout = ''  # 户型
    face = ''  # 朝向
    rent = ''  # 租金
    tags = []  # 标签

    # 以下为详情页信息
    imgs = []  # 房源轮播图
    floor = ''  # 楼层
    description = ''  # 介绍
    update_time = ''  # 维护时间
    decoration = ''  # 装修类型
    lease_mode = ''  # 租赁方式
    payment = ''  # 付款方式
    deposit = ''  # 押金
    charge = ''  # 服务费
    fee = ''  # 中介费
    distance = []  # 地铁距离
    facility = Facility()  # 房间设备
    base_info = BaseInfo()  # 房间基本信息

    def text(self):
        tag_str = ""
        for tag in self.tags:
            tag_str = tag_str + tag + ";"

        img_str = ""
        for img in self.imgs:
            img_str = img_str + img + ';'

        dis_str = ""
        for distance in self.distance:
            dis_str = dis_str + distance.text() + ";"

        return self.hid + ',' + self.name + ',' + \
               self.pre_img + ',' + self.district + ',' + \
               self.subdistrict + ',' + self.community + ',' + \
               str(self.area) + ',' + self.layout + ',' + \
               self.face + ',' + self.rent + ',' + \
               tag_str + ',' + self.floor + ',' + \
               self.update_time + ',' + self.decoration + ',' + \
               self.lease_mode + ',' + self.payment + ',' + \
               str(self.deposit) + ',' + str(self.charge) + ',' + \
               str(self.fee) + ',' + dis_str + ',' + \
               self.facility.text() + ',' + self.base_info.text() + ',' + \
               img_str + ',' + self.description.replace("\n", ',')
