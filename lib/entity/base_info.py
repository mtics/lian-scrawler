# coding=utf-8

class BaseInfo(object):
    hid = ''  # 房源id
    park = ''  # 是否有车位
    electricity = ''  # 用电类型(民电/商电)
    heat = ''  # 采暖方式
    lease_time = ''  # 租期
    view = ''  # 看房
    checkin = ''  # 入住时间
    elevator = False  # 是否有电梯(True/False)
    water = ''  # 用水类型(民水/商水)
    gas = False  # 是否有燃气(True/False)

    def text(self):
        return self.park + ',' + self.electricity + ',' + \
               self.heat + ',' + self.lease_time + "," + \
               self.view + ',' + self.checkin + ',' + \
               str(self.elevator) + ',' + self.water + ',' + str(self.gas)
