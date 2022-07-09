# yikeWebClientPython
首先</br>
from yike import *</br>
</br>
先使用cookie(字符串)与bdstoken(字符串)（F12去找）实例化</br>
yi = yikeENV(cookies, bdstoken)</br>
</br>
yikeENV有几个方法：</br>
以下方法返回一个包含yikePhoto类的列表</br>
getvideos() #获取全部视频</br>
getgifs() #获取全部动图</br>
getscreenshots() #获取全部截图</br>
getall() #获取全部</br>
getrecycled() #获取回收站全部</br>
clearrecycle() #清空回收站</br>
特别地，以下三个方法接受一个参数</br>
其类型为包含了yikePhoto类的列表</br>
三个方法都返回包含所有应答JSON(字典)的列表</br>
delete(list) #移入回收站</br>
restore(list) #从回收站恢复</br>
delrecycle(list) #从回收站删除</br>
</br>
yikePhoto有以下几个方法：</br>
delrecycle() #从回收站删除自身</br>
restore() #从回收站恢复自身</br>
delete() #将自身移入回收站</br>
exif() #获取自身EXIF</br>
以上方法都返回一个JSON(字典)</br>
特别地，该方法返回一个URL字符串</br>
getdl() #获取自身下载链接</br>
yikePhoto有一个可能有用属性</br>
yikePhoto.time</br>
该属性为一个字符串，记录了其在一刻中显示的时间（在主页时间轴上）</br>
格式为YYYY:MM:DD HH:MM:SS</br>
</br>
使用例：</br>
from yike import *</br>
bdstoken=input("bdtoken:")</br>
cookies=input("cookies:")</br>
yi = yikeENV(cookies, bdstoken)</br>
print(yi.delete(yi.getvideos())) #删除全部视频</br>
