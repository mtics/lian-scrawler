ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'

# 选取<div class='wrapper'>-div-<div class='filter'>-<div id='filter'>-<ul data-target='area'>-所有<li>-<a>
CITY_DISTRICT_XPATH = '///div[3]/div[1]/div[4]/div[1]/ul[2]//li/a'
# 选取<div class='m-filter'>-<div class='position'>-第二个dl-dd-第二个div-所有a
DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]//a'
# 选取<div class='wrapper'>-div-<div class='content w1150'>-<div class='content__article'>-<div class='content__list'>-所有<div class='content__list--item'>
DISTRICT_HOUSE_XPATH = '//div[3]/div[1]/div[5]/div[1]/div[1]//div'
