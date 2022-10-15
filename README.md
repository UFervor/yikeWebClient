## 这是一个开源的百度一刻相册客户端，仅供学习使用，通过逆向网页版API实现；并遵循[GPL-3.0 license](https://github.com/hexin-lin-1024/yikeWebClientPython/blob/main/LICENSE)。  
  
### 走过路过，不要错过。只要您是在研究一刻相册网页版的API，[Wiki](https://github.com/hexin-lin-1024/yikeWebClientPython/wiki) 里的东西您就大概率会感兴趣。  
  
### 兼容性  
|Tested On|
|---
|Python 3.7
|Python 3.8
|Python 3.9
|Python 3.10
  
### 安装外部依赖  
`pip3 install requests pywin32`
  
### 使用教程：
引入：`from yike import *`，  
并实例化 `yi = yikeENV(cookies, bdstoken)`。  
cookie字符串可以在浏览器开发人员工具中寻得，bdstoken同理，设置筛选条件为XHR寻找。  
未来展望：实现登录。  
  
### yikeENV类：  
yikeENV有以下成员方法：  
|方法名称|方法作用|方法参数|返回值|
|---|---|---|---
|getvideos|获取全部视频|不接受参数|\[\<yikePhoto object\>\]
|getgifs|获取全部动图|不接受参数|\[\<yikePhoto object\>\]
|getscreenshots|获取全部截图|不接受参数|\[\<yikePhoto object\>\]
|listrecent|列出最近可用|不接受参数|\[\<yikePhoto object\>\]
|getall|获取全部|不接受参数|\[\<yikePhoto object\>\]
|getrecycled|获取回收站全部|不接受参数|\[\<yikePhoto object\>\]
|clearrecycle|清空回收站|不接受参数|\[\<yikePhoto object\>\]

特别地，以下三个方法返回包含所有应答JSON(字典)的列表：
|方法名称|方法作用|方法参数|返回值|
|---|---|---|---
|delete|移入回收站|\[\<yikePhoto object\>\]|\[\<class 'dict'\>\]
|restore|从回收站恢复|\[\<yikePhoto object\>\]|[<<class 'dict'>>]
|delrecycle|从回收站删除|\[\<yikePhoto object\>\]|[<<class 'dict'>>]
  
该方法目前不推荐使用，因为速度过于缓慢：   
|方法名称|方法作用|方法参数|返回值|
|---|---|---|---  
|dlall|将指定的媒体下载到工作目录中|workdir(字符串)|无返回值
  
### yikePhoto类：  
yikePhoto有以下几个成员方法：   
|方法名称|方法作用|方法参数|返回值|
|---|---|---|---
|delrecycle|从回收站删除自身|不接受参数|应答JSON(字典)
|restore|从回收站恢复自身|不接受参数|应答JSON(字典)
|delete|将自身移入回收站|不接受参数|应答JSON(字典)
|exif|获取自身EXIF|不接受参数|应答JSON(字典)
|getdl|获取自身下载链接|不接受参数|Url(字符串)
|dl(会自动信息元信息)|将自身下载到工作目录|workdir(字符串)|没有返回|
  
yikePhoto有一个属性：  `yikePhoto.time` (字符串)：  记录了其在一刻中显示的时间（在主页时间轴上）且格式为YYYY:MM:DD HH:MM:SS。    
由于PNG，Webp等图片在传输过程中丢失了创建时间信息，而通常情况此类文件没有被写入元信息，故该属性可作为补充。  
  
### 使用例：
  
```Python
from yike import *  
bdstoken=input("bdtoken:")  
cookies=input("cookies:")  
yi = yikeENV(cookies, bdstoken)  
print(yi.delete(yi.getvideos())) #删除全部视频  
```
  
### 请注意：  
一刻相册的task需要一段时间执行，如果界面无反应请耐心等待，返回的errno为0就说明一定会生效了。
