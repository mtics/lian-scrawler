# coding=utf-8

class DistanceToSubway(object):
    hid = ''  # 房源id
    line = ''  # 地铁线路
    station = ''  # 站点
    distance = ''  # 距离

    def text(self):
        return self.line + '-' + self.station + '-' + self.distance
