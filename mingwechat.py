import pandas as pd
from datetime import datetime
import re
from operator import itemgetter
import json
import os

#把下面的字符串值改为你的csv文件地址
csv_address = 'E:\\Document\\NoteLibrary\\WeChat\\messages.csv'

ME = '我'
SFI = []
JS_JSON = {}
NickName2Remarks = {}

HTMLSTR = '''
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport"content="width=device-width, initial-scale=1.0"/><title>微信使用报告</title><style>*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}body{background-color:rgb(10,14,21);scrollbar-width:none;-ms-overflow-style:none;-webkit-tap-highlight-color:transparent;font-family:"dianz";cursor:default}body::-webkit-scrollbar{display:none}li,dd,dt{list-style:none}select,textarea,input,button{outline:none}abbr{text-decoration:none}a:-webkit-any-link{text-decoration:none}.noSelect{-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;-khtml-user-select:none;user-select:none}.main{width:50rem;margin:0 auto;margin-top:20vh;background-color:rgba(178,132,34,0.072);background-color:transparent;padding-bottom:5rem}h1{letter-spacing:0.4rem;font-weight:600;font-size:2rem;color:rgb(218,218,218)}p{margin-top:1rem;color:rgb(200,200,200)}.statement{width:100%;background-color:rgba(28,43,61,0.404);border-radius:1rem;margin:0 auto;padding:1rem 2rem;margin-top:2rem}.statement p{font-size:0.8rem;letter-spacing:0.1rem}.statement h2{font-size:1.1rem;font-weight:550;color:rgb(200,191,27)}.lightStyle1{color:rgba(189,186,26,0.876);font-weight:550;font-size:0.9rem;font-family:'consolas'}.linedown{width:100%;height:5rem}.indent2{padding-left:2rem;font-size:0.8rem;line-height:1.3rem}em{display:inline-block;font-style:normal;margin-right:1rem}i{display:block;font-weight:450;font-style:normal;margin-bottom:1rem}#locationpy i span{font-size:0.8rem!important}#timeQuantum em span{font-size:0.8rem!important}.annotation{font-size:0.9rem;color:rgb(158,158,158)}</style></head><body><section class="main"><h1>微信使用报告</h1><p>以下统计的信息均来源于你在<span id="interval"class="lightStyle1">xxx</span>期间的微信记录</p><p>报告置信度为:<abbr title="该数值与能查找到的微信记录有关, 微信数据库记录越多, 该报告就越准确, 且置信度越接近100%"><span id="confidence"class="lightStyle1">xxx</span></abbr></p><div class="statement"><h2>🚨声明</h2><p>本程序是一款用于生成微信使用报告的开源工具，旨在帮助用户回顾自己过去的微信使用情况，包括聊天、支付、亲密关系分析等方面的数据。</p><p>本程序不会收集、存储、泄露或出售用户的任何个人信息，包括但不限于手机号、昵称、头像、地区、性别、聊天内容、转账红包记录等。本程序仅通过读取用户的微信记录，获取用户的微信数据，并在本地生成使用报告。用户可以自由选择是否分享或删除报告。</p><p>本程序不代表微信官方，也不涉及任何商业目的。本程序仅供娱乐和参考，不对报告的准确性和完整性负责。如有任何疑问或建议，请联系开发者。</p></div><div class="linedown"></div><p>1.有效联系人个数为<span id="effectContacts"class="lightStyle1">xxx</span>;有效群聊个数为<span id="effectGroup"class="lightStyle1">xxx</span></p><p>2.下面的这些人还没有备注过哦,你还记得Ta们是谁吗?</p><p class="indent2"id="noRemarks">xxx</p><p>3.你最常在什么时间点发送微信消息呢?<span class="annotation">(一天24小时的时间分布占比,单位:千分比)</span></p><p class="indent2"id="myTimeHour"></p><p>4.你平均发送消息最多的月份是哪一个月呢?<span class="annotation">(12个月份分布占比,单位:千分比)</span></p><p class="indent2"id="myTimeMonth"></p><p>5.你发送消息的类型分布</p><p class="indent2"id="myMessageRatio"></p><p>6.与你金钱来往密切的人<span class="annotation">(格式:昵称->金钱来往次数，红包+转账)</span></p><p class="indent2"id="money"></p><p>7.你在这段期间,添加了一些新的微信好友<span class="annotation">(格式:昵称->加好友的时间)</span></p><p class="indent2"id="newFriends"></p><p>8.在这段期间,你可能去过这些地方</p><p class="indent2"id="locationpy"></p><p>9.<b>你的联系人</b>在与你聊天中撤回消息的数量</p><p class="indent2"id="withdrawOther"></p><p>10.<b>你</b>在与你的联系人聊天中所撤回消息的数量</p><p class="indent2"id="withdrawMe"></p><p>11.你与Ta们的聊天记录非常少,你还记得Ta们吗<span class="annotation">(越前面的人与你的聊天记录越少)</span></p><p class="indent2"id="distantRelationship"></p><p>12.现在依然和你保持联系的联系人</p><p class="indent2"id="activeList"></p><p>13.聊天密度<span class="annotation">(聊天密度=互相发送的消息总数量/有效聊天总时长)</span></p><p class="indent2"id="chatDensity"></p><p>14.聊天密度较高,但是已经很久没有和你联系过的联系人</p><p class="indent2"id="inactiveList"></p><p>15.与你长时间保持联系的人<span class="annotation">(格式:联系人->有效聊天月数)</span></p><p class="indent2"id="keepTime"></p><p>16.不同年月与你聊天最频繁的人</p><p class="indent2"id="timeQuantum"></p><p>17.你在意/关注的人,或者至少曾经这样过<span class="annotation">(计算方法:你发送的消息总数量/对方发送的消息总数量)</span></p><p class="indent2"id="chatRatioMe"></p><p>18.在意/关注你的人,或者Ta们至少曾经这样过</p><p class="indent2"id="chatRatioOther"></p></section><script type="text/javascript">let strFromPython=`==Narrastory==`;let jsonFromPython=JSON.parse(strFromPython);let interval=document.getElementById("interval");let confidence=document.getElementById("confidence");let effectContacts=document.getElementById("effectContacts");let effectGroup=document.getElementById("effectGroup");let noRemarks=document.getElementById("noRemarks");let myTimeHour=document.getElementById("myTimeHour");let myTimeMonth=document.getElementById("myTimeMonth");let myMessageRatio=document.getElementById("myMessageRatio");let money=document.getElementById('money');let newFriends=document.getElementById('newFriends');let locationpy=document.getElementById('locationpy');let withdrawOther=document.getElementById('withdrawOther');let withdrawMe=document.getElementById('withdrawMe');let distantRelationship=document.getElementById('distantRelationship');let activeList=document.getElementById('activeList');let chatDensity=document.getElementById('chatDensity');let inactiveList=document.getElementById('inactiveList');let keepTime=document.getElementById('keepTime');let timeQuantum=document.getElementById('timeQuantum');let chatRatioMe=document.getElementById('chatRatioMe');let chatRatioOther=document.getElementById('chatRatioOther');interval.innerHTML=jsonFromPython.interval[0].slice(0,10)+" => "+jsonFromPython.interval[1].slice(0,10);confidence.innerHTML=jsonFromPython.confidence+" %";effectContacts.innerHTML=jsonFromPython.effective_contact[1];effectGroup.innerHTML=jsonFromPython.effective_contact[0];noRemarks.innerHTML=jsonFromPython.no_remarks.join(", ");distantRelationship.innerHTML=jsonFromPython.distantRelationship.join(", ");activeList.innerHTML=jsonFromPython.activeList.join(", ");inactiveList.innerHTML=jsonFromPython.inactiveList.join(', ');const myRatio=()=>{let a=jsonFromPython.my_message_ratio;out='你总共发送了<span class="lightStyle1">'+a.text_count+'</span>条文字信息, <span class="lightStyle1">'+a.emoji_count+'</span>张表情包, <span class="lightStyle1">'+a.pic_count+'</span>张图片, <span class="lightStyle1">'+a.voice_count+'</span>个语音消息; 你总计发送的字数为<span class="lightStyle1">'+a.total_text+'</span>, 平均每个聊天气泡<span class="lightStyle1">'+a.aver_text+"</span>个字";myMessageRatio.insertAdjacentHTML("beforeend",out)};const myTime=()=>{jsonFromPython.my_time_distribution.hour.forEach((x,i)=>{let a1=i<10?"0"+i:i;let a2=(x*1000).toFixed(2);out="<em><b>"+a1+':00</b>-><span class="lightStyle1">'+a2+"</span></em>";myTimeHour.insertAdjacentHTML("beforeend",out)});jsonFromPython.my_time_distribution.month.forEach((x,i)=>{let a1=i+1;let a2=(x*1000).toFixed(2);out="<em><b>"+a1+'月</b>-><span class="lightStyle1">'+a2+"</span></em>";myTimeMonth.insertAdjacentHTML("beforeend",out)})};const moneyFun=()=>{let v=jsonFromPython.money.values;jsonFromPython.money.name.forEach((x,i)=>{let a1=x;let a2=v[i];out="<em><b>"+a1+'</b>-><span class="lightStyle1">'+a2+"</span></em>";money.insertAdjacentHTML("beforeend",out)})};const newFriend=()=>{let v=jsonFromPython.new_friends;Object.entries(v).forEach((x)=>{out="<em><b>"+x[0]+'</b>-><span class="lightStyle1">'+x[1]+"</span></em>";newFriends.insertAdjacentHTML("beforeend",out)})};const locations=()=>{jsonFromPython.location.forEach((k,i)=>{m=i+1;out='<i><b>'+m+'. 经度:</b> <span class="lightStyle1">'+k.x+'</span><b>, 纬度: </b><span class="lightStyle1">'+k.y+'</span><b>, 标签: </b><span class="lightStyle1">'+k.label+'</span><b>, 地点: </b><span class="lightStyle1">'+k.poiname+'</span><b>, 与此地点相关的联系人: </b><span class="lightStyle1">'+k.name+'</span></i>';locationpy.insertAdjacentHTML('beforeend',out)})};const withdraw=()=>{otherValues=jsonFromPython.withdraw.other.values;jsonFromPython.withdraw.other.name.forEach((x,i)=>{out='<em><b>'+x+'</b>-><span class="lightStyle1">'+otherValues[i]+'</span></em>';withdrawOther.insertAdjacentHTML('beforeend',out)});myValues=jsonFromPython.withdraw.me.values;jsonFromPython.withdraw.me.name.forEach((x,i)=>{out='<em><b>'+x+'</b>-><span class="lightStyle1">'+myValues[i]+'</span></em>';withdrawMe.insertAdjacentHTML('beforeend',out)})};const chatDensitys=()=>{value=jsonFromPython.chatDensity.values;jsonFromPython.chatDensity.name.forEach((x,i)=>{out='<em><b>'+x+'</b>-><span class="lightStyle1">'+value[i]+'</span></em>';chatDensity.insertAdjacentHTML('beforeend',out)})};const keepTimes=()=>{value=jsonFromPython.keepTime.values;jsonFromPython.keepTime.name.forEach((x,i)=>{out='<em><b>'+x+'</b>-><span class="lightStyle1">'+value[i]+'</span></em>';keepTime.insertAdjacentHTML('beforeend',out)})};const timeQuantums=()=>{let v=jsonFromPython.timeQuantum;Object.entries(v).forEach((x)=>{out="<em><b>"+x[0]+'</b>-><span class="lightStyle1">'+x[1]+"</span></em>";timeQuantum.insertAdjacentHTML("beforeend",out)})};const chatRatio=()=>{let a1=jsonFromPython.chatRatio[0];let a2=jsonFromPython.chatRatio[1];Object.entries(a1).forEach((x)=>{out="<em><b>"+x[0]+'</b>-><span class="lightStyle1">'+x[1]+"</span></em>";chatRatioMe.insertAdjacentHTML("beforeend",out)});Object.entries(a2).forEach((x)=>{out="<em><b>"+x[0]+'</b>-><span class="lightStyle1">'+x[1]+"</span></em>";chatRatioOther.insertAdjacentHTML("beforeend",out)})};myTime();myRatio();moneyFun();newFriend();locations();withdraw();chatDensitys();keepTimes();timeQuantums();chatRatio();</script></body></html>
'''

#表预处理
rows_deleted = []
#群聊列表
group_chat_list = set()
df = pd.read_csv(csv_address)
df.drop(columns=['localId', 'TalkerId','IsSender','CreateTime','Status'],inplace=True)
df.dropna(axis=0,subset=['Sender'],how='any',inplace=True)
print('表预处理中...')
for x in df.index:
  k1 = df.loc[x,"Sender"]
  k2 = df.loc[x,"NickName"]
  k3 = df.loc[x,"Remark"]
  if k1 != ME and k1 != k2:
    group_chat_list.add(k2)
    rows_deleted.append(x)
  elif  k3 == k3:
    NickName2Remarks[k2] = k3
df.drop(index=rows_deleted,axis=0,inplace=True)
del rows_deleted
#自定义函数区块
def split_dict(dict):
    sorted_items = sorted(dict.items(), key=itemgetter(1), reverse=True)
    return {'name': [k for k, v in sorted_items], 'values': [v for k, v in sorted_items]}
def str_nickname2remarks(NickName:str)->str:
    return NickName2Remarks.get(NickName,NickName)
#字符串->时间戳
def s2t(s:str) -> float:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timestamp()

#报告置信度
def confidence_coefficient():
    fun = lambda x:x/(1+x)*0.5
    start,stop = s2t(df.head(1).iloc[0,3]),s2t(df.tail(1).iloc[0,3])
    a,days = df.shape[0]/10000,(stop - start)/3600/24/365
    return round((fun(a) + fun(days))*100,2)
#时间段
def interval():
    return [df.head(1).iloc[0,3],df.tail(1).iloc[0,3]]

#备注信息
#remarks_name:set存储的是字符串，是未备注的昵称
class Item_01:
    def __init__(self):
        self.remarks_name = set()
    def __call__(self,line_info):
        Remark = line_info[4]
        NickName = line_info[5]
        if Remark != Remark:
            self.remarks_name.add(NickName)
    def calculation_proportion(self) -> list:
        return list(self.remarks_name)
SFI.append(Item_01())

#时间分布
#输出字典，字典的值是np类，序列序号对应时间，值对应比例
class Item_02:
    def __init__(self) -> None:
        self.hour_times = [0] * 24
        self.month_times = [0] * 12
    def __call__(self, line_info):
        StrTime = line_info[3]
        Sender = line_info[6]
        if Sender == ME:
            self.hour_times[int(StrTime[11:13])] += 0.1
            self.month_times[int(StrTime[5:7]) - 1] += 0.1
    def calculation_proportion(self) -> dict:
        temp_hour = self.hour_times
        temp_month = self.month_times
        sum_hour = sum(temp_hour)
        sum_month = sum(temp_month)
        return {'hour': [x / sum_hour for x in temp_hour], 'month': [x / sum_month for x in temp_month]}
SFI.append(Item_02())

#与每个人的聊天详细消息统计
class Item_03:
    def __init__(self) -> None:
        self.contacts_list= {}
    def __call__(self,line_info):
        l,n = int(line_info[0]),str_nickname2remarks(str(line_info[5]))
        if l not in [1,3,34,47] :
            return
        #'text':0,'pic':0,'voice':0,'emoji':0
        b = self.contacts_list.get(n,[{1: 0, 3: 0, 34: 0, 47: 0, 'total_text': 0,'min_date':1893492296,'max_date':0} for _ in range(2)])
        sender_num = 0 if line_info[6] == ME else 1
        q,t = b[sender_num],s2t(line_info[3])
        q[l] += 1
        q['min_date'] = t if t < q['min_date'] else q['min_date']
        q['max_date'] = t if t > q['max_date'] else q['max_date']
        if l == 1:
            q['total_text'] += len(line_info[2])
        self.contacts_list[n] = b
    def calculation_proportion(self):
        return self.contacts_list
SFI.append(Item_03())

#发送的消息类型比例（文本，语音，图片，表情包）
#输出各消息类型计数数量，以及纯文本总数和平均发送文本数量
class Item_04:
    def __init__(self) -> None:
        #'text':0,'pic':0,'voice':0,'emoji':0
        self.type_base = {1:0,3:0,34:0,47:0}
        self.total_text = 0
    def __call__(self,line_info):
        k = int(line_info[0])
        if line_info[6] == ME and k in [1,3,34,47]:
            self.type_base[k] += 1
            if k == 1:
                self.total_text += len(line_info[2])
    def calculation_proportion(self) -> dict:
        m = self.type_base
        return {'text_count':m[1],'pic_count':m[3],'voice_count':m[34],'emoji_count':m[47],'total_text':self.total_text,'aver_text':round(self.total_text/m[1],2)}
SFI.append(Item_04())

#金钱来往
#输出字典
class Item_05:
    def __init__(self) -> None:
        self.contacts_list = {}
    def __call__(self,line_info):
        l,n,s = int(line_info[0]),str_nickname2remarks(str(line_info[5])),int(line_info[1])
        condition_1 = l == 10000 and s == 0 and line_info[2].find('领取了') >= 0
        condition_2 = l == 11000 and s == 0
        condition_3 = l == 49 and s == 2000
        if condition_1 or condition_2 or condition_3:
            t = self.contacts_list.get(n,0) + 1
            self.contacts_list[n] = t
    def calculation_proportion(self):
        return split_dict(self.contacts_list)
SFI.append(Item_05())

#有效联系人群聊统计
class Item_06:
    def __init__(self) -> None:
        self.contacts = set()
    def __call__(self,line_info):
        self.contacts.add(line_info[5])
    def calculation_proportion(self) -> list:
        return [len(group_chat_list),len(self.contacts)]
SFI.append(Item_06())

#位置信息统计
class Item_07:
    def __init__(self) -> None:
        self.locations = []
    def __call__(self,line_info):
        if int(line_info[0]) == 48:
            self.locations.append(self.extract_location(str(line_info[2]),line_info[5]))
    def extract_location(self,string,sender):
        attributes = ['x', 'y', 'label', 'poiname']
        a = {attr: re.search(rf'{attr}="(.*?)"', string).group(1) for attr in attributes if re.search(rf'{attr}="(.*?)"', string)}
        a['name'] = str_nickname2remarks(str(sender))
        return a
    def calculation_proportion(self) -> list:
        return list({frozenset(d.items()): d for d in self.locations}.values())
SFI.append(Item_07())

#撤回信息统计
class Item_08:
    def __init__(self) -> None:
        self.name_list = {}
        self.my_list = {}
    def __call__(self,line_info):
        if int(line_info[0]) == 10000 and int(line_info[1]) == 0 and str(line_info[2]).find('撤回了一条消息') >= 0:
            k = self.get_name(str(line_info[2]))
            m = str_nickname2remarks(str(line_info[5]))
            if k == '你':
                self.my_list[m] = self.my_list.get(m,0) + 1
            else:
                self.name_list[m] = self.name_list.get(m,0) + 1
    def get_name(self,text):
        match = re.search(r"(.+)撤回了一条消息", text)
        a = match.group(1) if match else '"None"'
        return a if a == '你' else a[1:-2]
    def calculation_proportion(self):
        return {'other':split_dict(self.name_list),'me':split_dict(self.my_list)}
SFI.append(Item_08())

#新朋友，认识的日期
class Item_09:
    def __init__(self) -> None:
        self.name_list = {}
    def __call__(self,line_info):
        if int(line_info[0]) == 10000 and int(line_info[1]) == 0 and str(line_info[2]).find('现在可以开始聊天了') >= 0:
            self.name_list[str_nickname2remarks(str(line_info[5]))] = line_info[3]
    def calculation_proportion(self):
        return self.name_list
SFI.append(Item_09())

#对方时间分布+年份
class Item_10:
    def __init__(self) -> None:
        self.contacts_dict = {}
    def __call__(self,line_info):
        if int(line_info[0]) not in [1,3,34,47] or line_info[6] == ME:
            return
        n,s = str_nickname2remarks(str(line_info[5])),line_info[3]
        t = self.contacts_dict.get(n,{'hour':[0]*24,'month':[0]*12,'year_month':{}})
        t['hour'][int(s[11:13])] += 1
        t['month'][int(s[5:7]) - 1] += 1
        t['year_month'][str(s[0:7])] = t['year_month'].get(str(s[0:7]),0) + 1
        self.contacts_dict[n] = t
    def calculation_proportion(self):
        return self.contacts_dict
SFI.append(Item_10())

#亲密关系
def intimacy_relationships(a:Item_03) -> dict:
    everyone_details = a.calculation_proportion()
    intimacy = {}
    for name,value in everyone_details.items():
        a_list = [value[i][j] for i in [0, 1] for j in [1, 3, 34, 47]]
        a = sum(a_list)
        intimacy[name] = a
    return intimacy

#疏远关系 返回名字str列表，疏远关系最高排在第一 输入亲密关系
def distant_relationships(a) -> list:
    a = split_dict(a)
    rate = round(len(a['name'])*0.3)
    return a['name'][rate:][::-1]

#聊天密度 输入：疏远关系列表，itme10,亲密关系 + 连续联系时长 聊天年份+月份统计month_year
def chat_density(a:list,b:Item_10,c):
    other = b.calculation_proportion()
    chat_density_dict,durations = {},{}
    for name,value in other.items():
        k = len(value['year_month'].keys())
        durations[name] = k
        if name in a or name not in c.keys():
            continue
        chat_density_dict[name] = round(c[name]/k,2)
    return [chat_density_dict,durations]

#现在依然保持联系的人 3个月
#输入，item03，疏远关系列表,chat_density函数输出
def active_list(a:Item_03,remote:list,chat_density) -> list:
    everyone_details = a.calculation_proportion()
    active_contacts = []
    chat_density = split_dict(chat_density[1])
    name_nums = len(chat_density['name'])
    col = chat_density['name'][::-1][0:round(name_nums*0.3)]
    for name,value in everyone_details.items():
        if name in remote or name in col:
            continue
        if int(datetime.now().timestamp()) - value[1]['max_date'] < 3600*24*90:
            active_contacts.append(name)
    return active_contacts

#聊天密度较高但是3月内没有聊过天的人
#输入：聊天密度函数输出，item03
def inactive_list(chat_density,a:Item_03) -> list:
    everyone_details = a.calculation_proportion()
    chat_density = split_dict(chat_density[0])
    length = len(chat_density['name'])
    col = []
    for i in range(0,round(length*0.5)):
        name = chat_density['name'][i]
        if int(datetime.now().timestamp()) - everyone_details[name][1]['max_date'] > 3600*24*90:
            col.append(name)
    return col

#每段时间聊天次数（无视种类）最多的1个人
def time_quantum(a:Item_10):
    def filter_and_sort(data):
        result = {}
        for date, value in data.items():
            name = value['name']
            result[date] = name
        result = dict(sorted(result.items(), reverse=True))
        return result
    other = a.calculation_proportion()
    col = {}
    for name,value in other.items():
        for year_month,i in value['year_month'].items():
            k = col.get(year_month,{'chat_value':0,'name':''})
            if i > k['chat_value']:
                k['chat_value'] = i
                k['name'] = name
                col[year_month] = k
    return filter_and_sort(col)

#双方聊天比例失调 你在意的人/或者至少曾经在意
#输入 item03，疏远关系函数输出
#返回在意和被在意列表
def chat_ratio(a:Item_03,b:list):
    everyone_details = a.calculation_proportion()
    col = {}
    for name,value in everyone_details.items():
        k1 = sum([value[0][m] for m in [1,3,34,47]])
        b1 = value[0]['total_text']
        k2 = sum([value[1][m] for m in [1,3,34,47]])
        b2 = value[1]['total_text']
        if 0 in [k1,b1,k2,b2] or name in b:
            continue
        col[name] = round(1/2*(k1/k2+b1/b2),5)
    kk = split_dict(col)
    length = len(kk['name'])
    return [{a:col[a] for a in kk['name'][0:round(length*0.25)]},{a:col[a] for a in kk['name'][round(length*0.75):][::-1]}]

if __name__ == '__main__':
    print('分析数据中...')
    for x in df.index:
        #Type,SubType,StrContent,StrTime,Remark,NickName,Sender = df.loc[x]
        line = df.loc[x]
        if line[5] in group_chat_list:
            continue
        for sfun in SFI:
            sfun(line)
    
    no_remarks,my_time_distribution,everyone_details,my_message_ratio,money,effective_contact,location,withdraw,new_friends,other_time_distribution = SFI
    JS_JSON = {key: obj.calculation_proportion() for key, obj in zip(
        ['no_remarks', 'my_time_distribution', 'my_message_ratio', 'money', 'effective_contact', 'location', 'withdraw', 'new_friends'],
        [no_remarks, my_time_distribution, my_message_ratio, money, effective_contact, location, withdraw, new_friends]
    )}
    JS_JSON['confidence'] = confidence_coefficient()
    JS_JSON['interval'] = interval()
    intimacyRelationship = intimacy_relationships(everyone_details)
    distantRelationship = distant_relationships(intimacyRelationship)
    chatDensity = chat_density(distantRelationship,other_time_distribution,intimacyRelationship)
    activeList = active_list(everyone_details,distantRelationship,chatDensity)
    inactiveList = inactive_list(chatDensity,everyone_details)
    timeQuantum = time_quantum(other_time_distribution)
    chatRatio = chat_ratio(everyone_details,distantRelationship)
    JS_JSON['distantRelationship'] = distantRelationship
    JS_JSON['chatDensity'] = split_dict(chatDensity[0])
    JS_JSON['keepTime'] = split_dict(chatDensity[1])
    JS_JSON['activeList'] = activeList
    JS_JSON['inactiveList'] = inactiveList
    JS_JSON['timeQuantum'] = timeQuantum
    JS_JSON['chatRatio'] = chatRatio
    foutput = json.dumps(JS_JSON,ensure_ascii=False)
    K = re.sub("==Narrastory==", foutput, HTMLSTR)
    with open( os.path.dirname(csv_address) + '\\' + "微信使用报告.html", "w",encoding='utf-8') as f:
        f.write(K)
    print('分析完成,已保存为 微信使用报告.html')

