import urllib.request
import json
import time
left_bottom=[118.609648,31.953192]
right_top=[119.011679,32.156586]
part_n=5
f=open('TrafficStatus_XY5.txt','a',encoding='utf-8')
f2=open('TrafficStatus5.txt','a',encoding='utf-8')
count=0
num=0
url0='http://restapi.amap.com/v3/traffic/status/rectangle?level=5&rectangle='
x_item = (right_top[0]-left_bottom[0])/part_n;
y_item = (right_top[1]-left_bottom[1])/part_n;
ak='2aca7b77d2914d26a9e93da027825479'
n=0
panduan=0
L=[]
for i in range(part_n):
    for j in range(part_n):
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        right_top_part = [left_bottom_part[0]+x_item,left_bottom_part[1]+y_item]; # 切片的右上角坐标
        url=url0+str(left_bottom_part[0])+','+str(left_bottom_part[1])+';'+str(right_top_part[0])+','+str(right_top_part[1])+'&output=json&key='+ak+'&extensions=all'
        #url = 'http://restapi.amap.com/v3/traffic/status/rectangle?rectangle=116.351147,39.966309;116.357134,39.968727&output=json&key=yourkey';
        #url=url0+'116.351147'+','+'39.966309'+';'+'116.357134'+','+'39.968727'+'&output=json&key='+ak
        
        data=urllib.request.urlopen(url)
        hjson=json.loads(data.read())
        if hjson['info']=='OK':
            for road in hjson['trafficinfo']['roads']:
                for h in range(len(L)):
                    if road==L[h]:
                    
                        panduan=1
                        break
                if(panduan==1):
                    panduan=0
                    continue
                L.append(road)
            
                count=count+1
                try:
                    traffisstatus=str(count)+','+road['name']+','+road['status']+','+road['direction']+','+road['angle']+','+road['speed']+','+road['name']+'-'+road['direction']+'\n'
                except:
                    print(url)
                else:
                    print(traffisstatus)
                    f2.write(traffisstatus)
                    rname=road['name']
                    rdirection=road['direction']
                    rployline=road['polyline'].split(';')
                    num = num + 1
                    for tt in range(0,len(rployline)):
                        RoadLoc=str(num)+','+rname+','+rdirection+','+rployline[tt]+','+rname+'-'+rdirection+'\n'
                        f.write(RoadLoc)
f.close()
f2.close()
