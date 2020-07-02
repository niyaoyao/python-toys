from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import re
import time

def request_html(url):
    print("Load:%s" % (url))
    time.sleep(3)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36')
    html = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    return soup

def house_detail(url):
    house = {}
    house_html = request_html(url)
    house['title'] = house_html.find('h3', class_="detail_title").string.encode('utf-8')
    print(house['title'])
    house_detail = house_html.find_all('div', class_="similar_data_detail")
    house['price'] = float(filter(str.isdigit, house_detail[0].find('span').string.encode('utf-8'))) * 10000
    house['format'] = house_detail[1].find('p', class_="red").string.string.encode('utf-8')
    house['square'] = float(filter(str.isdigit, house_detail[2].find('p', class_="red").string.string.encode('utf-8')))
    house_descriptions = house_html.find('ul', class_="house_description").find_all('li')
    print(house)
    return house

def access_houses(route, page, community):
    url = "%s%s%s" % (route, page, community)
    soup = request_html(url)
    house_list = soup.find("div", class_="list-view-section-body").find_all("div", class_="lj-track")
    houses = []

    for house_item in house_list:
        a = house_item.find(href=re.compile('m.lianjia.com/jn/ershoufang/'))
        if a:
            houses.append(house_detail(a['href']))
    return houses

house = house_detail('https://m.lianjia.com/jn/ershoufang/103109000082.html?fb_expo_id=313711251031756825')

print(house)

# route = 'https://m.lianjia.com/jn/ershoufang/'
# index = 1
# page = "pg%d" % (index) 
# community = 'rs%E5%90%89%E5%B0%94%E5%8C%97%E8%8B%91/'
# currentHouses = access_houses(route, page, community)
# pageSize = len(currentHouses)
# print('pageSize:%d' % pageSize)
# houses = []
# houses.extend(currentHouses)
# print(houses, len(houses))

# while len(currentHouses) >= pageSize :
#     index += 1
#     page = "pg%d" % (index)
#     currentHouses = access_houses(route, page, community)
#     houses.extend(currentHouses)

# print (houses, len(houses))
