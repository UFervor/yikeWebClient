## 这是一个开源的百度一刻相册客户端，通过逆向网页版API实现。  
### 这是文档，更多请见[Wiki](https://github.com/hexin-lin-1024/yikeWebClientPython/wiki)。  

|依赖|  
|---
|requests  
|Python3|
  
### 使用教程：
引入：`from yike import *`，  
并实例化`yi = yikeENV(cookies, bdstoken)`。  
cookie字符串可以在浏览器开发人员工具中寻得，bdstoken同理，设置筛选条件为XHR寻找。  
  
yikeENV有几个实现其功能的成员方法：  
以下方法都不接受参数，且返回一个包含yikePhoto类的列表  

|方法名称|方法作用|
|---|---
|getvideos()|获取全部视频
|getgifs()|获取全部动图
|getscreenshots()|获取全部截图
|getall()|获取全部
|getrecycled()|获取回收站全部
|clearrecycle()|清空回收站|
  
特别地，以下三个方法接受一个类型为列表(列表)的参数：  
其类型为包含了yikePhoto类的列表，且三个方法都返回包含所有应答JSON(字典)的列表。  
|方法名称|方法作用|
|---|---
|delete()|移入回收站
|restore()|从回收站恢复
|delrecycle()|从回收站删除|
  
yikePhoto是实现功能的基本单位，含有以下几个成员方法：  
以下方法都不接受参数，且返回一个JSON(字典)。  
  
|方法名称|方法作用|
|---|---
|delrecycle()|从回收站删除自身
|restore()|从回收站恢复自身
|delete()|将自身移入回收站
|exif()|获取自身EXIF|
  
特别的，该方法返回字符串（Url）。  
  
|方法名称|方法作用|
|---|---
|getdl()|获取自身下载链接|
  
yikePhoto有一个可能有用的属性：  `yikePhoto.time`。  
该属性为一个字符串，记录了其在一刻中显示的时间（在主页时间轴上）且格式为YYYY:MM:DD HH:MM:SS。  
由于Png，Webp等图片在传输过程中丢失了创建时间信息，而通常情况此类文件没有被写入元信息，故该属性可作为补充。  

使用例：

```Python
from yike import *  
bdstoken=input("bdtoken:")  
cookies=input("cookies:")  
yi = yikeENV(cookies, bdstoken)  
print(yi.delete(yi.getvideos())) #删除全部视频  
```
  
### 注意事项：  
一刻相册的task需要一段时间执行，如果界面无反应请耐心等待，返回的errno为0就说明一定会生效了。
