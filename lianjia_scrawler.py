# -*- coding: utf-8 -*-

import threading
import re
import requests
import threadpool
from bs4 import BeautifulSoup
from lib.util.date import *
from lib.util.path import *
from lib.request.headers import *
from lib.entity.house import *
from lib.position.district import *
from lib.position.subdistrict import *

thread_pool_size = 50

# 防止爬虫被禁，随机延迟设定
# 如果不想delay，就设定False，
# 具体时间可以修改random_delay()，由于多线程，建议数值大于10
RANDOM_DELAY = True


class Scrawler(object):
    @staticmethod
    def random_delay():
        # 防止爬虫被禁，随机延迟设定
        if RANDOM_DELAY:
            time.sleep(random.randint(2, 5))

    def __init__(self):
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.date_string = get_date_string()
        print('Today date is: %s' % self.date_string)
        self.total_num = 0  # 总的小区个数，用于统计
        self.mutex = threading.Lock()  # 创建锁

    def get_house_info(self, house):
        """
        爬取单个房源的详情页，获取剩余信息
        :param hid: 房源id，用来指定房源
        :param house: 房源信息实体类，用来存储房源信息
        :return house: 房源信息实体类，用来存储房源信息
        """
        url = "https://sh.lianjia.com/zufang/{0}.html".format(house.hid)
        headers = create_headers()
        reponse = requests.get(url, timeout=10, headers=headers)
        html = reponse.content  # 获取网页内容
        soup = BeautifulSoup(html, "lxml")
        contents = soup.find("div", class_="content clear w1150")  # 获取信息主体部分
        positions = soup.find("div", class_="content__article__info4 w1150")  # 获取信息位置部分

        # 获取房源信息维护时间
        print("获取房源信息维护时间\n")
        subtitle = contents.find("div", class_="content__subtitle")
        house.update_time = subtitle.contents[0].split("：")[1].strip()

        # 获取房源装修类型以及楼层
        print("获取房源装修类型以及楼层\n")
        aside = contents.find("ul", class_="content__aside__list")
        house.lease_mode = aside.contents[1].contents[1].strip()
        house_type = aside.contents[3].contents[1].split(" ")
        house.layout = house_type[0]
        house.area = house_type[1].replace("㎡", "")
        if len(house_type) == 3:
            house.decoration = house_type[2].strip()
        temp = aside.contents[5].contents[1].split(" ")
        if len(temp) == 2:
            house.face = temp[0]
            house.floor = temp[1]
        elif len(temp) == 1:
            house.floor = temp[0]

        # 获取房源描述
        print("获取房源描述\n")
        article = contents.find("div", class_="content__article__info3")
        description = article.find("p")
        if description is not None:
            house.description = description.attrs["data-desc"].replace("<br />", "")

        # 获取房源图片
        print("获取房源图片\n")
        pic_list = contents.find("ul", class_="piclist")
        try:
            pic_list = pic_list.find_all("li")
            if len(pic_list) > 0:
                pics = []
                for pic in pic_list:
                    pics.append(pic.contents[1].attrs["src"])
                    house.imgs = pics
        except Exception as e:
            print("There is no img")
            print(e)

        # 获取费用信息
        print("获取费用信息\n")
        costs = contents.find("ul", class_="table_row").find_all("li")
        house.payment = costs[0].contents[0].strip()
        house.rent = costs[1].contents[0].strip()
        house.deposit = costs[2].contents[0].strip()
        house.charge = costs[3].contents[0].strip()
        house.fee = costs[4].contents[0].strip()

        # -----------------------------------------
        # |          接下来开始爬取基本信息            |
        # -----------------------------------------

        print("接下来开始爬取基本信息\n")
        base = BaseInfo()
        infos = contents.find("div", "content__article__info")
        base.hid = house.hid
        base.checkin = infos.contents[3].contents[11].contents[0].split("：")[1].strip()

        has_elevator = infos.contents[3].contents[17].contents[0].split("：")[1].strip()
        if has_elevator == "有":
            base.elevator = True
        else:
            base.elevator = False

        base.park = infos.contents[3].contents[21].contents[0].split("：")[1].strip()
        base.water = infos.contents[3].contents[23].contents[0].split("：")[1].strip()
        base.electricity = infos.contents[3].contents[27].contents[0].split("：")[1].strip()
        base.electricity = infos.contents[3].contents[27].contents[0].split("：")[1].strip()

        has_gas = infos.contents[3].contents[29].contents[0].split("：")[1].strip()
        if has_gas == "有":
            base.gas = True
        else:
            base.gas = False

        base.heat = infos.contents[3].contents[33].contents[0].split("：")[1].strip()
        base.lease_time = infos.contents[5].contents[3].contents[0].split("：")[1].strip()
        base.view = infos.contents[5].contents[9].contents[0].split("：")[1].strip()
        house.base_info = base

        # -----------------------------------------
        # |          接下来开始爬取设施信息            |
        # -----------------------------------------
        print("接下来开始爬取设施信息\n")
        facility = Facility()
        facilities_dict = {"电视": False, "冰箱": False, "空调": False, "洗衣机": False,
                           "热水器": False, "暖气": False, "床": False,
                           "宽带": False, "衣柜": False, "天然气": False}
        facilities = contents.find("ul", "content__article__info2").find_all("li")
        for faci in facilities:
            if faci.contents[0] == "配套设施":
                pass
            elif len(faci.attrs['class']) == 2:
                facility_name = faci.contents[2].replace("\n", "").strip()
                facilities_dict[facility_name] = True

        facility.tv = facilities_dict["电视"]
        facility.refri = facilities_dict["冰箱"]
        facility.wash = facilities_dict["洗衣机"]
        facility.air = facilities_dict["空调"]
        facility.water_heater = facilities_dict["热水器"]
        facility.bed = facilities_dict["床"]
        facility.air_heater = facilities_dict["暖气"]
        facility.wideband = facilities_dict["宽带"]
        facility.wardrobe = facilities_dict["衣柜"]
        facility.gas = facilities_dict["天然气"]
        facility.hid = house.hid

        house.facility = facility

        # -----------------------------------------
        # |          接下来开始爬取地图信息            |
        # -----------------------------------------
        print("接下来开始爬取地图信息\n")
        distantce = DistanceToSubway()
        positions = positions.find_all("ul")[1].find_all("li")
        if len(positions) > 0:
            distantces = []
            for position in positions:
                dist = position.contents[1].contents[0].split("-")
                distantce.line = dist[0].strip().replace(",", "，")
                distantce.station = dist[1].strip().replace(",", "，")
                distantce.distance = position.contents[3].contents[0].strip()
                distantce.hid = house.hid
                distantces.append(distantce)
            house.distance = distantces
        return house

    def get_houses_info(self, district, subdistrict, file):
        """
        通过爬取页面获取城市指定版块的租房信息
        :param subdistrict: 区域
        :return: 出租房信息列表
        """
        total_page = 1

        page = 'https://sh.lianjia.com/zufang/{0}/'.format(subdistrict)
        print(page)

        headers = create_headers()
        reponse = requests.get(page, timeout=10, headers=headers)
        html = reponse.content  # 获取网页内容
        soup = BeautifulSoup(html, "lxml")
        content_list = soup.find('div', class_="content__list")
        houses_list = content_list.find_all('div', class_="content__list--item")
        houses = list()

        # 获得总的页数
        try:

            page_box = soup.find('div', class_='content__pg')

            total_page = int(page_box.attrs["data-totalpage"])
            # print(total_page)
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(subdistrict))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        headers = create_headers()
        for num in range(1, total_page + 1):
            page = 'https://sh.lianjia.com/zufang/{0}/pg{1}'.format(subdistrict, num)
            print(page)
            self.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            try:
                content_list = soup.find('div', class_="content__list")
                houses_list = content_list.find_all('div', class_="content__list--item")
                for house_element in houses_list:
                    pic_a = house_element.find('a', class_="content__list--item--aside")
                    house_title = house_element.find('p', class_="content__list--item--title twoline")
                    infos = house_element.find('p', class_="content__list--item--des")
                    tags = house_element.find('p', class_="content__list--item--bottom oneline")
                    rent = house_element.find('span', class_="content__list--item-price")

                    try:
                        house = House()
                        house.pre_img = pic_a.contents[1].attrs["data-src"]
                        house.name = house_title.contents[1].contents[0].replace("\n", "").strip()
                        house.hid = house_title.contents[1].attrs['href'].split("/")[2].replace(".html", "")
                        house.district = infos.contents[1].contents[0]
                        house.subdistrict = infos.contents[3].contents[0]
                        house.community = infos.contents[5].contents[0]

                        # 获取标签
                        tags_list = tags.find_all("i")
                        tag_list = []
                        for tag in tags_list:
                            tag_list.append(tag.contents[0])
                        house.tags = tag_list

                        # 租金，目前含单位
                        # 若爬取结束，发现单位统一，则无需单位
                        house.rent = rent.contents[0].contents[0]

                        # 列表页信息爬取已结束，接下来开始详情页信息爬取
                        house = self.get_house_info(house)
                    except Exception as e:
                        print("+" * 20)
                        print(" page no data hid: " + house.hid)
                        print(e)
                        # print(page)
                        print("=" * 20)

                    # 数据单条保存
                    file.write(house.text() + "\n")

                    houses.append(house)
                    Scrawler().random_delay()
            except Exception as e:
                print(e)

        return houses

    def save_district_rent_data(self, district, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有出租房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param district: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        print(district)
        subdistricts = get_subdistrict(district)
        for subdistrict in subdistricts:
            csv_file = self.today_path + "/{0}-{1}.csv".format(district, subdistrict)
            with open(csv_file, "w") as f:
                # 保存数据到csv文件, 先存表头
                # f.write("房源id,房源标题,列表页展览图,区县,区域,社区,面积,"
                #         "户型,朝向,租金,标签,楼层,维护时间,装修,出租方式,付款方式,"
                #         "押金,服务费,中介费,到地铁站距离,电视,冰箱,空调,洗衣机,热水器,"
                #         "暖气,床,宽带,衣柜,燃气,停车位,用电类型,采暖方式,租期,看房时间,"
                #         "入住时间,是否有电梯,用水类型,是否有天然气,轮播图,房源描述" + "\n")

                f.write("hid,name,pre_img,district,subdistrict,community,area,"
                        "layout,face,rent,tags,floor,update_time,decorate,lease_mode,payment,"
                        "deposit,charge,fee,distance,tv,refri,air,wash,water_heater,"
                        "air_heater,bed,wideband,wardrobe,gas,park,electricity,heat,lease_time,view,"
                        "checkin,elevator,water,natgas,imgs,description" + "\n")

                # 开始获得需要的板块数据
                houses = self.get_houses_info(district, subdistrict, f)
                # 锁定
                if self.mutex.acquire(1):
                    self.total_num += len(houses)
                    # 释放
                    self.mutex.release()

            print("Finish crawl area: " + district + "-" + subdistrict + ", save data to : " + csv_file)

    def start(self):
        """
        该方法为多线程，速度更快
        :return:
        """
        self.today_path = create_date_path("data", "sh1", self.date_string)
        # collect_area_zufang('sh', 'beicai')  # For debugging, keep it here
        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts = get_districts()
        # districts = ["xuhui", "changning","putuo"]
        # districts = ["pudong"]
        # districts = ["baoshan","minhang"]
        # districts = ["jiading","qingpu"]
        # districts = ["chongming"]

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        # pool_size = len(districts)
        pool = threadpool.ThreadPool(pool_size)
        requests_list = threadpool.makeRequests(self.save_district_rent_data, districts)
        [pool.putRequest(request) for request in requests_list]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} districts.".format(len(districts)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))

    # def start(self):
    #     """
    #     该方法为单线程，仅用于调试
    #     """
    #     self.today_path = create_date_path("data", "sh", self.date_string)
    #     # collect_area_zufang('sh', 'beicai')  # For debugging, keep it here
    #     t1 = time.time()  # 开始计时
    #
    #     # 获得城市有多少区列表, district: 区县
    #     # districts = get_districts()
    #     districts = ["jingan"]
    #     for district in districts:
    #         self.save_district_rent_data(district)
    #
    #     # 计时结束，统计结果
    #     t2 = time.time()
    #     print("Total crawl {0} districts.".format(len(districts)))
    #     print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == "__main__":
    scrawler = Scrawler()
    scrawler.start()
