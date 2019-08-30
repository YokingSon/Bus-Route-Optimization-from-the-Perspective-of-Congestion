import urllib.request
import json
import math
import time
import socket
x_pi = 3.14159265358979324 * 3000.0 / 180.0
def gcj02tobd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]
def bd09togcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]
left_bottom = gcj02tobd09(118.609648,31.953192);  # 设置区域左下角坐标（百度坐标系）
right_top = gcj02tobd09(119.011679,32.156586); # 设置区域右上角坐标（百度坐标系）
part_n=4
f=open('茶座.txt', 'w', encoding='utf-8')
url0 = 'http://api.map.baidu.com/place/v2/search?';
x_item = (right_top[0]-left_bottom[0])/part_n;
y_item = (right_top[1]-left_bottom[1])/part_n;
query = '茶座'; #搜索关键词设置
query=urllib.parse.quote(query)
ak = 'iS73xXLWojWBgK7wGMYzvp2DXRc2dvzo'; #百度地图api信令
n=0

for i in range(part_n):
    for j in range(part_n):
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        right_top_part = [left_bottom_part[0]+x_item,left_bottom_part[1]+y_item]; # 切片的右上角坐标
        for k in range(20):
            url = url0 + 'query=' + query + '&page_size=20&page_num=' + str(k) + '&scope=1&bounds=' + str(left_bottom_part[1]) + ',' + str(left_bottom_part[0]) + ','+str(right_top_part[1]) + ',' + str(right_top_part[0]) + '&output=json&ak=' + ak;      
            data = urllib.request.urlopen(url,timeout=20);
            hjson = json.loads(data.read());
            if hjson['message'] == 'ok':
                results = hjson['results'];          
                for m in range(len(results)): # 提取返回的结果
                    gaode=bd09togcj02(results[m]['location']['lng'],results[m]['location']['lat'])
                    pointt=results[m]['name']+','+str(gaode[0])+','+str(gaode[1])+'\n'
                    f.write(pointt)
            data.close()
        n += 1;
        print('第',str(n),'个切片入库成功')
        time.sleep(5)
f.close()
