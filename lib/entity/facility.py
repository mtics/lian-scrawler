# coding=utf-8

class Facility(object):
    hid = ''                # 房源id
    tv = False              # 电视
    refri = False           # 冰箱
    air = False             # 空调
    wash = False            # 洗衣机
    water_heater = False    # 热水器
    air_heater = False      # 暖气
    bed = False             # 床
    wideband = False        # 宽带
    wardrobe = False        # 衣柜
    gas = False             # 天然气

    def text(self):
        return str(self.tv) + ',' + str(self.refri) + ',' + \
               str(self.air) + ',' + str(self.wash) + ',' + \
               str(self.water_heater) + ',' + str(self.air_heater) + ',' + \
               str(self.bed) + ',' + str(self.wideband) + ',' + \
               str(self.wardrobe) + ',' + str(self.gas)
