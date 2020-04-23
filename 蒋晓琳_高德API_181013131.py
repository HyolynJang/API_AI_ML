#!/usr/bin/env python
# coding: utf-8

# # 课后作业：调用高德Web服务API文档中所有功能
# 
# 至少完成每一个模块中的一个子功能的API调用，封装成函数，开源到github/gitee上  ✅
# 
# 在调用每一个功能的同时，思考其背后是否含有ML、AI的功能（比如计算机视觉、语音识别、推荐算法等），并整理思考的结果，在调用API代码模块中用markdown说明。  ✅ (见每个功能的标题下方)
# 
# 尝试设计一个简单的应用（不要求写代码），至少涉及3个API功能。 ✅ (见总结处)
# <br/>
# <br/>
# 
# ----
# 
# 
# <br/>
# <br/>
# 
# # 细读地图API（高德）
# 

# In[3]:


get_ipython().run_cell_magic('html', '', '<style>\n/* 本电子讲义使用之CSS */\ndiv.code_cell {\n    background-color: #e5f1fe;\n}\ndiv.cell.selected {\n    background-color: #effee2;\n    font-size: 2rem;\n    line-height: 2.4rem;\n}\ndiv.cell.selected .rendered_html table {\n    font-size: 2rem !important;\n    line-height: 2.4rem !important;\n}\n.rendered_html pre code {\n    background-color: #C4E4ff;   \n    padding: 2px 25px;\n}\n.rendered_html pre {\n    background-color: #99c9ff;\n}\ndiv.code_cell .CodeMirror {\n    font-size: 2rem !important;\n    line-height: 2.4rem !important;\n}\n.rendered_html img, .rendered_html svg {\n    max-width: 100%;\n    height: auto;\n    float: center;\n}\n/* Gradient transparent - color - transparent */\nhr {\n    border: 0;\n    border-bottom: 1px dashed #ccc;\n}\n.emoticon{\n    font-size: 5rem;\n    line-height: 4.4rem;\n    text-align: center;\n    vertical-align: middle;\n}\n\n</style>')


# ## 📌 地理编码、逆地理编码、步行路径规划（代码A）

# In[4]:


import pandas as pd


# In[5]:


import requests
key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"


# ### A-1 获取地理编码
# 
# * ML机器学习

# In[241]:


# A-1 地理编码     
def geocode(address,city=None,batch=None,sig=None)->dict:
    """获取地理编码"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    params={
        'key': key1,
        'address':address,
        'city':city,
        'batch':batch,
        'sig':sig,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[242]:


大剧院 = geocode('广东省广州市广州大剧院')
display(大剧院)
大剧院地理编码 = pd.json_normalize(大剧院['geocodes'])
display(大剧院地理编码)
大剧院地理编码 = 大剧院['geocodes'][0]['location']
print("广州大剧院地理编码:",大剧院地理编码)


# ### A-2 逆地理编码（基础/全）
# 
# * ML机器学习

# In[245]:


# A-2 基础逆地理编码分析   
def regeocode(location,poitype=None,radius=None,extensions="base",batch=False,roadlevel=None,sig=None,homeorcorp=None)->dict:
    """获取逆地理编码"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/geocode/regeo?parameters'
    params={
        'key': key1,
        'location':location,
        'poitype':poitype,
        'radius':radius,
        'extensions':extensions,
        'batch':batch,
        'roadlevel':roadlevel,
        'homeorcorp':homeorcorp,
        'sig':sig,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[246]:


大剧院逆地理编码 = regeocode(大剧院地理编码)
print(大剧院逆地理编码)
df_大剧院逆地理编码 = pd.json_normalize(大剧院逆地理编码).T
display(df_大剧院逆地理编码)


# In[247]:


# A-2 Extra 全部逆地理编码分析
大剧院逆地理编码_all = regeocode(大剧院地理编码,extensions="all")
print(大剧院逆地理编码_all)
df_大剧院逆地理编码_all = pd.json_normalize(大剧院逆地理编码_all)
display(df_大剧院逆地理编码_all)


# ### A-3 全部逆地理编码分析细节
# 
# * ML机器学习

# In[249]:


# A-3 分析细节     
roads = pd.json_normalize(大剧院逆地理编码_all['regeocode']['roads'])
roadinters = pd.json_normalize(大剧院逆地理编码_all['regeocode']['roadinters'])
aois = pd.json_normalize(大剧院逆地理编码_all['regeocode']['aois'])
pois = pd.json_normalize(大剧院逆地理编码_all['regeocode']['pois'])
display(roads,roadinters,aois,pois)


# ### 学生练习：
# 1. 观察和练习其他参数
# 2. 想得到更大范围的搜索POI如何操作    答：调整radius参数的值
# 3. * 请pandas学过的同学对address进行分组groupby练习，尝试找寻不同根类地址下的type
# 4. * 请思考如何对不同类型的服务进行分类？如美食、旅馆、加油站...等         答：遍历type，为不同类型建立字典
# ![](lianxi01.png)

# In[256]:


import pandas as pd
pois.groupby(["type","address"]).agg({"distance":sum})


# ## 📌 路径规划（点到点的过程）  
# 
# 
# ### 产品的设计思维 
# 
# 1. 请思考，什么样的产品需要路径规划？      答: 出行类
# 2. 如果你的产品需要，你会如何使用？      答: 根据使用场景选择对应的api
# 3. 最优路线如何选择？高德会用到什么算法？（推荐系统）
#     1. 推荐系统输入location么？  答: 起点和终点
#     2. 实时的定位？（多长时间定位一次） 答: 实时更新
#     3. 定位完成其他点的变化？距离的选择（用户希望路边有更多的需求还是希望快速找到目的地？）    答:提供不同需求的筛选按钮
#     4. 以上思考的越多，你的产品考虑的会越周全，避免产品后期的大量更改。
#     
# 4. 可能了解的知识面，不需要清楚怎么做，但可以了解输入输出的结果是什么。参考如下图
# 
# ![](http://imgtec.eetrend.com/files/2019-03/%E5%8D%9A%E5%AE%A2/100018447-63696-10.jpg)
# 
# -----
# ![](https://pic2.zhimg.com/50/v2-45a26a9985308d90405dea78e6892dd0_r.jpg)

# ### 步行路径规划（API基本流程）（代码B）
# 
# * ML机器学习

# In[10]:


# B-1 准备base url、params、response.json（）   
def walking(origin,destination,sig=None)->dict:
    """步行路径规划"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/direction/walking?parameters'
    params={
        'key':key1,
        'origin':origin,
        'destination':destination,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[11]:


# B-2 准备walking 参数
广州塔 = geocode('广东省广州市天河区广州塔')
广州塔_location = 广州塔['geocodes'][0]['location']
大剧院_location = 大剧院['geocodes'][0]['location']
print("(起点)广州塔_location:",广州塔_location,"(终点)大剧院_location:",大剧院_location)


# In[12]:


# B-3 路径规划
大剧院_广州塔 = walking(大剧院_location,广州塔_location)
df = pd.json_normalize(大剧院_广州塔["route"]["paths"][0]['steps'])
display(df)
df["instruction"]


# ###  公交路线规划（代码C）
# 
# * ML机器学习，AI计算机视觉
# 

# In[277]:


# C-1        
def public_transportation(origin,destination,city,cityd=None,extensions='base',strategy=None,nightflag=0,date=None,time=None,sig=None)->dict:
    """公交规划"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/direction/transit/integrated?parameters'
    params={
        'key':key1,
        'origin':origin,
        'destination':destination,
        'city':city,
        'cityd':cityd,
        'extensions':extensions,
        'strategy':strategy,
        'nightflag':nightflag,
        'date':date,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[278]:


# C-2 准备walking 参数
美术馆 = geocode('广东省广州市广东省美术馆')
print(美术馆)
美术馆_location = 美术馆['geocodes'][0]['location']
大剧院_location = 大剧院['geocodes'][0]['location']
print("(起点)美术馆_location:",美术馆_location,"(终点)大剧院_location:",大剧院_location)

# C-3 公交路径规划
美术馆_大剧院 = public_transportation(美术馆_location,大剧院_location,city='广州',extensions='all')
print(美术馆_大剧院)


# In[14]:



df_bus = pd.json_normalize(美术馆_大剧院)
df_bus


# In[15]:


pd.json_normalize(美术馆_大剧院["route"]['transits'])


# In[16]:


pd.json_normalize(美术馆_大剧院["route"]['transits'][0]['segments'])


# In[17]:


df_bus_基本信息 = pd.json_normalize(美术馆_大剧院["route"]['transits'][0]['segments'][0]['bus']["buslines"])
df_bus_基本信息


# In[18]:


# C-4 公交车信息处理结果
B21路公交车 = pd.json_normalize(美术馆_大剧院["route"]['transits'][0]['segments'][0]['bus']["buslines"][0]["via_stops"]).rename(columns={"name":"B21路公交车"})
display(B21路公交车)


# ## 📌 行政区域查询（代码D）
# 
# * ML机器学习

# In[19]:


# D-1 请注意行政区域级别划分参数
def district(keywords,subdistrict=None,page=None,offset=None,extensions='base',filter=None,)->dict:
    """行政区域查询"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/config/district?parameters'
    params={
        'key':key1,
        'keywords':keywords,
        'subdistrict':subdistrict,
        'page':page,
        'offset':offset,
        'extensions':extensions,
        'filter':filter,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data
行政区域 = district(keywords='广东',extensions='all',subdistrict=2)

df_行政区域_1级 = pd.json_normalize(行政区域["districts"][0]['districts'])

df_行政区域_2级_广州市 = pd.json_normalize(行政区域["districts"][0]['districts'][20]['districts'])
display(df_行政区域_1级,df_行政区域_2级_广州市)


# In[20]:


# D-2 2级区域地址
df_行政区域_2级_广州市


# ## 📌 搜索POI

# ###  关键字搜索（代码E）
# 
# * ML机器深度学习

# In[21]:


# E-1
def place_text(keywords,types,city=None,citylimit=None,children=None,page=None,extensions='base',sig=None)->dict:
    """关键字搜索"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/place/text?parameters'
    params={
        'key':key1,
        'keywords':keywords,
        'types':types,
        'city':city,
        'citylimit':citylimit,
        'children':children,
        'page':page,
        'extensions':extensions,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data

广州_美术馆 = place_text('科教文化','美术馆',city="广州市",children=1,extensions='all')
广州_美术馆


# In[22]:


df_广州_美术馆 = pd.json_normalize(广州_美术馆["pois"])
df_广州_美术馆_广东美术馆 = pd.json_normalize(广州_美术馆["pois"][12]["children"])
display(df_广州_美术馆,df_广州_美术馆_广东美术馆)


# ###  周边搜索 (代码F)
# 
# * ML机器学习

# In[23]:


# F-1 
def place_around(location,keywords=None,types=None,city=None,redius=None,sortrule=None,offset=None,page=None,extensions='base',sig=None)->dict:
    """周边搜索"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/place/around?parameters'
    params={
        'key':key1,
        'keywords':keywords,
        'location':location,
        'types':types,
        'city':city,
        'redius':redius,
        'sortrule':sortrule,
        'offset':offset,
        'page':page,
        'extensions':extensions,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[24]:


# F-2 json信息
大剧院_周边POI = place_around(大剧院_location)
大剧院_周边POI


# In[39]:


# F-3 表格化，可扩展pandas处理
df_大剧院_周边POI = pd.json_normalize(大剧院_周边POI['pois'])
df_大剧院_周边POI


# ###  多边形搜索 （学生练习）
# 
# * ML深度学习

# In[52]:


def polygon_search(types,polygon=None,keywords=None,offset=None,page=None,extensions='base')->dict:
    """多边形搜索"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/place/polygon?parameters'
    params={
        'key':key1,
        'keywords':keywords,
        'types':types,
        'offset':offset,
        'page':page,
        'extensions':extensions,
        'polygon':polygon,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[56]:


周边POI_肯德基 = polygon_search('050301',"116.460988,40.006919|116.48231,40.007381;116.47516,39.99713|116.472596,39.985227|116.45669,39.984989|116.460988,40.006919",keywords="肯德基")
周边POI_肯德基


# ## 📌 静态地图
# 
# * AI计算机视觉、ML机器学习

# In[211]:


from PIL import Image     
from io import BytesIO

def staticmap(location,zoom,size=None,scale=1,markers=None,labels=None,paths=None,traffic=0,page=None,sig=None)->dict:
    """静态地图"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/staticmap?parameters'
    params={
        'key':key1,
        'location':location,
        'zoom':zoom,
        'size':size,
        'scale':scale,
        'markers':markers,
        'labels':labels,
        'paths':paths,
        'traffic':traffic,
        'sig':sig,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = Image.open(BytesIO(response.content))
    return data


# In[212]:


staticmap(location=大剧院_location,zoom=16)


# ## 📌 坐标转换    
# 
# * ML机器学习

# In[57]:


def location_convert(locations,coordsys='gps',extensions='base')->dict:
    """坐标转换"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/assistant/coordinate/convert?parameters'
    params={
        'key':key1,
        'locations':locations,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[58]:


location = location_convert(大剧院_location)
location


# ## 📌 天气查询
# 
# * ML机器学习

# In[86]:


def weather(city,extensions='all')->dict:
    """预报天气"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
    params={
        'key':key1,
        'city':city,
        'extensions':extensions,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[87]:


weather_info = weather(city='131182')
weather_info


# ## 📌 输入提示
# 
# * ML机器学习

# In[99]:


def input_tips(keywords,type,location,city='adcode',citylimit='false')->dict:
    """输入提示"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/assistant/inputtips?parameters'
    params={
        'key':key1,
        'keywords':keywords,
        'type':type,
        'location':location,
        'city':city,
        'citylimit':citylimit,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[100]:


input_tips = input_tips('肯德基',type='050301',location='113.323369,23.115515',city='广州')
input_tips


# ##  📌 交通态势

# In[71]:


def traffic_status(rectangle=None,level=None,extensions='base')->dict:
    """交通态势查询"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/traffic/status/rectangle?parameters'
    params={
        'key':key1,
        'level':level,
        'extensions':extensions,
        'rectangle':rectangle,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data


# In[72]:


态势查询 = traffic_status(rectangle='116.351147,39.966309;116.357134,39.968727')
态势查询


# ###  圆形区域交通态势
# 
# * ML机器学习

# In[73]:


def circle_status(location=None,rectangle=None,level=None,extensions='base')->dict:
    """圆形区域交通态势"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    url = 'https://restapi.amap.com/v3/traffic/status/circle?parameters'
    params={
        'key':key1,
        'level':level,
        'location':location,   # 经纬度
        'extensions':extensions,
        'rectangle':rectangle,
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data

态势查询_circle = circle_status(location='116.3057764,39.98641364')
态势查询_circle


# ###  制定路线交通态势
# 
# * ML机器学习

# In[79]:


def road_status(name=None,adcode=None,level=None,extensions='base')->dict:
    """制定路线交通态势"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"    
    url = 'https://restapi.amap.com/v3/traffic/status/road?parameters'
    params={
        'key':key1,
        'level':level,
        'extensions':extensions,
        'name':name,
        'adcode':adcode,   #城市编码，需查询高德API文档
        'output':'json'
    }
    response = requests.get(url,params=params)
    data = response.json()
    return data

态势查询_road = road_status(name='北环大道',adcode=440300)
态势查询_road


# ## 📌 地理围栏
# 
# * ML机器学习

# In[261]:


def geo_fence(name,center,radius='1000',enable=True,valid_time='2020-02-14',repeat="Mon,Tues,Wed,Thur,Fri,Sat,Sun",time= "00:00,11:59;13:00,20:59",desc="测试围栏描述",alert_condition="enter;leave")->dict: 
    """新增地理围栏"""
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"
    body={
            "name": name,
            "center": center,
            "radius": "1000",  #范围
            "enable": "true",
            "valid_time": "2020-09-25", #时间要未来
            "repeat": "Mon,Tues,Wed,Thur,Fri,Sat,Sun",
            "time": "00:00,11:59;13:00,20:59",
            "desc": "围栏1",
            "alert_condition": "enter;leave"
}
    url = 'https://restapi.amap.com/v4/geofence/meta?key=58c78852bf1ee4965c7e3fa78b6b9dd7' 
    response = requests.post(url,json=body) #这里用post
    data = response.json()
    return data


# In[262]:


geofence = geo_fence(name='海淀大街',center='116.3057764,39.98641364')
geofence


# ### 查询围栏
# 
# * ML机器学习

# In[263]:


def inquiry_fence(name)->dict: 
    '''查询围栏'''
    key1 ="58c78852bf1ee4965c7e3fa78b6b9dd7"   
    param={
        'key':key1
}

    body={
      #  "id": 0,     # 可选
      #  "gid": 'fd2cb95d-5992-496b-bbd5-3aa56dbc7256',  # 可选
        "name": name,   #只填name即可查询到
      #  "page_no": 1,
      #  "page_size": 20,
      #  "enable": "True",
}

    url = 'https://restapi.amap.com/v4/geofence/meta?' 
    response = requests.get(url,params=param,json=body) #这里用GET
    data = response.json()
    return data


# In[264]:


查询围栏 = inquiry_fence("海淀大街")
查询围栏


# ### 更新围栏
# 
# * ML机器学习

# In[269]:


def inquiry_fence(name)->dict: 
    '''更新围栏'''
    
    key1="58c78852bf1ee4965c7e3fa78b6b9dd7"
    param={
        'key':key1,
        'gid':'fd2cb95d-5992-496b-bbd5-3aa56dbc7256',
}

    body={
     "name": "圆形围栏1",
     "center": "116.3057764,39.98641364",   # 圆形围栏中心点
     "radius": "1148.8",
     "valid_time": "2020-09-14",    # 日期要写未来的
     "repeat": "Mon,Wed,Fri,Sat,Sun",
     "time": "07:00,12:00;15:00,21:00",
     "desc": "圆形围栏1",
     "alert_condition": "enter"
}

    url = 'https://restapi.amap.com/v4/geofence/meta' 
    response = requests.post(url,params=param,json=body) 
    data = response.json()
    return data


# In[270]:


inquiry_fence("圆形围栏1")


# ### 围栏启动&停止
# 
# * ML机器学习

# In[273]:


def inquiry_fence()->dict: 
    '''围栏启动&停止'''
    key1="58c78852bf1ee4965c7e3fa78b6b9dd7"
    param={
        'key':key1,
        'gid':'d6149af7-c8b6-4998-8599-58df40902f07',    
}

    body={
      "enable": "false"
}

    url = 'https://restapi.amap.com/v4/geofence/meta' 
    response = requests.patch(url,params=param,json=body) 
    data = response.json()
    return data


# In[274]:


fence_stop = inquiry_fence()
fence_stop


# ### 删除围栏
# 
# * ML机器学习

# In[275]:


def delete_fence(name)->dict: 
    '''删除围栏'''
    key1= '58c78852bf1ee4965c7e3fa78b6b9dd7'
    param={
        'key':key1,
        'gid':'d6149af7-c8b6-4998-8599-58df40902f07',
}

    body={
      "name":name,
}

    url = 'https://restapi.amap.com/v4/geofence/meta' 
    response = requests.delete(url,params=param) 
    data = response.json()
    return data


# In[276]:


删除围栏 = delete_fence("更新圆形围栏")
删除围栏


# ### 围栏设备监控
# 
# * AI计算机视觉、ML机器学习

# In[229]:


def status_fence()->dict: 
    '''围栏设备监控'''
    key1= '58c78852bf1ee4965c7e3fa78b6b9dd7'
    param={
        'key':key1,
        "diu":'866013038007155',
        "locations":"113.323369,23.115515,1587614806"
}


    url = 'https://restapi.amap.com/v4/geofence/status' 
    response = requests.get(url,params=param) 
    data = response.json()
    return data


# In[231]:


围栏_status = status_fence()
围栏_status 


# ## 📌 轨迹纠偏
# 
# * ML机器学习，AI计算机视觉

# In[175]:


def grasp_road()->dict: 
    
    """根据给定的坐标点、车辆的方位角以及行驶速度，将用户的轨迹纠偏到路上，从而返回用户实际驾车经过的道路坐标"""
    
    key1= '58c78852bf1ee4965c7e3fa78b6b9dd7'
    url = 'https://restapi.amap.com/v4/grasproad/driving'
    params={
        'key': key1,
        'output':'json'
    }
    body=[{
      "x": 116.449429,  #x、y为坐标经、纬度
      "y": 40.014844,
      "sp": 4,          #行驶速度
      "ag": 110,        #方位角
      "tm": 1478831753   
   }, {
      "x": 116.449639,
      "y": 40.014776,
      "sp": 3,
      "ag": 110,
      "tm": 23
   }, {
      "x": 116.449859,
      "y": 40.014716,
      "sp": 3,
      "ag": 111,
      "tm": 33
  }, {
      "x": 116.450074,
      "y": 40.014658,
      "sp": 3,
      "ag": 110,
      "tm": 31
  }, {
      "x": 116.450273,
      "y": 40.014598,
      "sp": 3,
      "ag": 111,
      "tm": 20
  }]
  
    response = requests.post(url,params=params,json=body) #这里用post
    data = response.json()
    return data


# In[176]:


北环大道 = grasp_road()
北环大道


# # 📍总结及展望
# 
# 
# ## 地图POI中的推荐算法工作原理
# * 将POI名称作为标签处理
# * 一群用户对某个地点感兴趣，那么这群用户中的一部分人感兴趣的其他地点可能与该地点相似
# 
# ## 设计一个简单的应用
# 
# **周末出游小程序**
# * 可根据位置查询周边休闲娱乐服务、活动;
# * 根据好友的点击量或区域内的点击热度推荐出行地点；
# * 选择出行目的地后可查看地图，提供路线规划服务。
# 
# 涉及的API功能
# * 地图API
# * 搜索POI
#     * 关键字搜索
#     * 周边搜索
# * 路径规划API
#     * 步行路径规划
#     * 公交路线规划
# * 输入提示API

# In[ ]:




