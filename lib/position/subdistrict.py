# coding=utf-8

from lib.position.district import *
from lib.const.xpath import *
from lib.request.headers import *

subdistricts_dict = {'buyecheng': '不夜城', 'caojiadu': '曹家渡', 'daning': '大宁', 'jiangninglu': '江宁路',
                      'jingansi': '静安寺', 'nanjingxilu': '南京西路', 'pengpu': '彭浦', 'xizangbeilu': '西藏北路',
                      'yangcheng': '阳城', 'yonghe': '永和', 'zhabeigongyuan': '闸北公园', 'caohejing': '漕河泾',
                      'changqiao': '长桥', 'hengshanlu': '衡山路', 'huadongligong': '华东理工', 'huajing': '华泾',
                      'jianguoxilu': '建国西路', 'kangjian': '康健', 'longhua': '龙华', 'shanghainanzhan': '上海南站',
                      'tianlin': '田林', 'wantiguan': '万体馆', 'xietulu': '斜土路', 'xuhuibinjiang': '徐汇滨江',
                      'xujiahui': '徐家汇', 'zhiwuyuan': '植物园', 'dapuqiao': '打浦桥', 'dongjiadu': '董家渡',
                      'huaihaizhonglu': '淮海中路', 'huangpubinjiang': '黄浦滨江', 'laoximen': '老西门', 'nanjingdonglu': '南京东路',
                      'penglaigongyuan': '蓬莱公园', 'renminguangchang': '人民广场', 'shibobinjiang': '世博滨江', 'wuliqiao': '五里桥',
                      'xintiandi': '新天地', 'yuyuan': '豫园', 'beixinjing': '北新泾', 'gubei': '古北',
                      'hongqiao1': '虹桥', 'jingansi': '静安寺', 'tianshan': '天山', 'xianxia': '仙霞',
                      'xijiao': '西郊', 'xinhualu': '新华路', 'zhenninglu': '镇宁路', 'zhongshangongyuan': '中山公园',
                      'caoyang': '曹杨', 'changfeng1': '长风', 'changshoulu': '长寿路', 'changzheng': '长征',
                      'ganquanyichuan': '甘泉宜川', 'guangxin': '光新', 'nanxiang': '南翔', 'taopu': '桃浦',
                      'wanli': '万里', 'wuning': '武宁', 'zhenguang': '真光', 'zhenru': '真如',
                      'zhongyuanliangwancheng': '中远两湾城', 'beicai': '北蔡', 'biyun': '碧云', 'caolu': '曹路',
                      'chuansha': '川沙', 'datuanzhen': '大团镇', 'gaodong': '高东', 'gaohang': '高行',
                      'geqing': '合庆', 'hangtou': '航头', 'huamu': '花木', 'huinan': '惠南',
                      'jinqiao': '金桥', 'jinyang': '金杨', 'kangqiao': '康桥', 'laogangzhen': '老港镇',
                      'lianyang': '联洋', 'lingangxincheng': '临港新城', 'lujiazui': '陆家嘴', 'meiyuan1': '梅园',
                      'nanmatou': '南码头', 'nichengzhen': '泥城镇', 'sanlin': '三林', 'shibo': '世博',
                      'shuyuanzhen': '书院镇', 'tangqiao': '塘桥', 'tangzhen': '唐镇', 'waigaoqiao': '外高桥',
                      'wanxiangzhen': '万祥镇', 'weifang': '潍坊', 'xinchang': '新场', 'xuanqiao': '宣桥',
                      'yangdong': '杨东', 'yangjing': '洋泾', 'yangsiqiantan': '杨思前滩', 'yuanshen': '源深',
                      'yuqiao1': '御桥', 'zhangjiang': '张江', 'zhoupu': '周浦', 'zhuqiao': '祝桥',
                      'dachangzhen': '大场镇', 'dahua': '大华', 'gaojing': '高境', 'gongfu': '共富',
                      'gongkang': '共康', 'gucun': '顾村', 'luodian': '罗店', 'luojing': '罗泾',
                      'shangda': '上大', 'songbao': '淞宝', 'songnan': '淞南', 'tonghe': '通河',
                      'yanghang': '杨行', 'yuepu': '月浦', 'zhangmiao': '张庙', 'beiwaitan': '北外滩',
                      'jiangwanzhen': '江湾镇', 'liangcheng': '凉城', 'linpinglu': '临平路', 'luxungongyuan': '鲁迅公园',
                      'quyang': '曲阳', 'sichuanbeilu': '四川北路', 'anshan': '鞍山', 'dongwaitan': '东外滩',
                      'gaojing': '高境', 'huangxinggongyuan': '黄兴公园', 'kongjianglu': '控江路', 'wujiaochang': '五角场',
                      'xinjiangwancheng': '新江湾城', 'zhongyuan1': '中原', 'zhoujiazuilu': '周家嘴路', 'chunshen': '春申',
                      'gumei': '古美', 'hanghua': '航华', 'huacao': '华漕', 'jinganxincheng': '静安新城',
                      'jinhongqiao': '金虹桥', 'jinhui': '金汇', 'laominhang': '老闵行', 'longbai': '龙柏',
                      'maqiao': '马桥', 'meilong': '梅陇', 'pujiang1': '浦江', 'qibao': '七宝',
                      'wujing': '吴泾', 'xinzhuang5': '莘庄', 'zhuanqiao': '颛桥', 'caojing': '漕泾',
                      'fengjing': '枫泾', 'jinshan1': '金山', 'langxia': '廊下', 'luxiang': '吕巷',
                      'shanyang': '山阳', 'shihua': '石化', 'tinglin': '亭林', 'zhangyan': '张堰',
                      'zhujing': '朱泾', 'anting': '安亭', 'fengzhuang': '丰庄', 'huating': '华亭',
                      'jiadinglaocheng': '嘉定老城', 'jiadingxincheng': '嘉定新城', 'jiangqiao': '江桥', 'juyuanxinqu': '菊园新区',
                      'malu': '马陆', 'nanxiang': '南翔', 'shangda': '上大', 'taopu': '桃浦',
                      'waigang': '外冈', 'xinchenglu1': '新成路', 'xuxing': '徐行', 'baozhen': '堡镇',
                      'changxingdao21211': '长兴岛', 'chenjiazhen': '陈家镇', 'chongmingqita': '崇明其它',
                      'chongmingxincheng': '崇明新城',
                      'hengshadao': '横沙岛', 'fengcheng': '奉城', 'fengxianjinhui': '奉贤金汇', 'haiwan': '海湾',
                      'nanqiao': '南桥', 'qingcun': '青村', 'situan': '四团', 'xidu': '西渡',
                      'zhelin': '柘林', 'zhuanghang': '庄行', 'chedun': '车墩', 'jiuting': '九亭',
                      'maogang': '泖港', 'shenminbieshu': '莘闵别墅', 'sheshan': '佘山', 'shihudang': '石湖荡',
                      'sijing': '泗泾', 'songjiangdaxuecheng': '松江大学城', 'songjianglaocheng': '松江老城',
                      'songjiangxincheng': '松江新城',
                      'xiaokunshan': '小昆山', 'xinbang': '新浜', 'xinqiao': '新桥', 'yexie': '叶榭',
                      'baihe': '白鹤', 'chonggu': '重固', 'huaxin': '华新', 'jinze': '金泽',
                      'liantang1': '练塘', 'xianghuaqiao': '香花桥', 'xiayang': '夏阳', 'xujing': '徐泾',
                      'yingpu': '盈浦', 'zhaoxiang': '赵巷', 'zhujiajiao': '朱家角'}


def get_districts_url(district):
    """
    拼接指定城市的区县url
    :param city: 城市
    :param district: 区县
    :return:
    """
    return "https://sh.lianjia.com/xiaoqu/{0}".format(district)


def get_subdistricts(district):
    """
    通过城市和区县名获得下级板块名
    :param district: 区县
    :return: 区域列表
    """
    page = get_districts_url(district)
    areas = list()
    try:
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        root = etree.HTML(html)
        links = root.xpath(DISTRICT_AREA_XPATH)
        # 针对a标签的list进行处理
        for link in links:
            relative_link = link.attrib['href']
            # 去掉最后的"/"
            relative_link = relative_link[:-1]
            # 获取最后一节
            area = relative_link.split("/")[-1]
            # 去掉区县名,防止重复
            if area != district:
                chinese_area = link.text
                # print(chinese_area)
                areas.append(area)
        return areas
    except Exception as e:
        print(e)


if __name__ == "__main__":
    pass
