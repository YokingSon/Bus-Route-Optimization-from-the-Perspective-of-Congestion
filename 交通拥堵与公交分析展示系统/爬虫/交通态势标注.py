'''
高德地图web api单次只允许查询10公里矩形框范围内的交通态势，所以将left_bottom与right_top的矩形范围切分为5*5（参数part_n）的切片，放入for in循环中进行多次请求。
'''

import urllib.request        #Urllib是python内置的HTTP请求库，urllib.request 是请求模块。区别于HTTP客户端库：requests库          
import json
import time                   
left_bottom=[118.609648,31.953192]       #南京市矩形区域内左下角经纬坐标
right_top=[119.011679,32.156586]         #南京市矩形区域内右上角经纬坐标
part_n=5          #分为25个切片
f=open('TrafficStatus_XY1.txt','a',encoding='utf-8')
f2=open('TrafficStatus1.txt','a',encoding='utf-8')
count=0
num=0
url0='http://restapi.amap.com/v3/traffic/status/rectangle?level=1&rectangle='
x_item = (right_top[0]-left_bottom[0])/part_n;
y_item = (right_top[1]-left_bottom[1])/part_n;
ak='2aca7b77d2914d26a9e93da027825479'
n=0
panduan=0
L=[]
for i in range(part_n):  #range() 函数可创建一个整数列表，例如range（5）等价于range（0，5），range（0，5） 是 [0, 1, 2, 3, 4]
    for j in range(part_n):      #循环5*5=25次
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        right_top_part = [left_bottom_part[0]+x_item,left_bottom_part[1]+y_item]; # 切片的右上角坐标
        url=url0+str(left_bottom_part[0])+','+str(left_bottom_part[1])+';'+str(right_top_part[0])+','+str(right_top_part[1])+'&output=json&key='+ak+'&extensions=all'
        #url = 'http://restapi.amap.com/v3/traffic/status/rectangle?rectangle=116.351147,39.966309;116.357134,39.968727&output=json&key=yourkey';
        #url=url0+'116.351147'+','+'39.966309'+';'+'116.357134'+','+'39.968727'+'&output=json&key='+ak

'''
访问url，这里的data相当于response。urlopen一般常用的有三个参数，它的参数如下：urllib.requeset.urlopen(url,data,timeout)。
如果我们添加data参数的时候就是以post请求方式请求，如果没有data参数就是get请求方式。
'''
        data=urllib.request.urlopen(url) 
        hjson=json.loads(data.read())  #data.read()相当于requests库中的data.content
        if hjson['info']=='OK':
            for road in hjson['trafficinfo']['roads']:
                for h in range(len(L)):  #Python len() 方法返回对象（字符、列表、元组等）长度或项目个数
                    if road==L[h]:

                        panduan=1
                        break
                if(panduan==1):
                    panduan=0
                    continue
                L.append(road)  #向L列表中添加一个对象road

                count=count+1 #给数据一个编号
                try:   #写入TrafficStatus_XY文件中
                    traffisstatus=str(count)+','+road['name']+','+road['status']+','+road['direction']+','+road['angle']+','+road['speed']+','+road['name']+'-'+road['direction']+'\n'
                except:
                    print(url)
                else:
                    print(traffisstatus)
                    f2.write(traffisstatus)
					
					#写入TrafficStatus文件
                    rname=road['name']
                    rdirection=road['direction']
                    rployline=road['polyline'].split(';')
					num = num + 1  #作为线字段进行点集转线
                    for tt in range(0,len(rployline)):
                        RoadLoc=str(num)+','+rname+','+rdirection+','+rployline[tt]+','+rname+'-'+rdirection+'\n'
                        f.write(RoadLoc)
f.close()
f2.close()
