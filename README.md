[English](https://github.com/hexin-lin-1024/yikeWebClient/blob/main/README.md) | [简体中文](https://github.com/hexin-lin-1024/yikeWebClient/blob/main/README.sc.md)

### This is an open-source Baidu Yike Gallery client for learning purposes only, implemented by reversing the web version API. It follows the [GPL-3.0 license](https://github.com/hexin-lin-1024/yikeWebClientPython/blob/main/LICENSE).
### You would be interested in stuff in [Wiki](https://github.com/hexin-lin-1024/yikeWebClientPython/wiki).
### Compatibility
|Version|Compatible|
|---|---|
|Python 2.x| :x: |
|Python 3.4| :white_check_mark: |
|Python 3.5| :white_check_mark: |
|Python 3.6| :white_check_mark: |
|Python 3.7| :white_check_mark: |
|Python 3.8| :white_check_mark: |
|Python 3.9| :white_check_mark: |
|Python 3.10| :white_check_mark: |
### Install Dependencies
`pip3 install requests pywin32`
### Tutorial
Import
```Python
from yike import *
```
And instantiate
```Python
yi = yikeENV(cookies, bdstoken)
```
The cookie string can be sought in the browser developer tools, bdstoken the same, set the filter to XHR to seek.  
Future outlook: implement login.  
### `yikeENV` class
`yikeENV` has the following member methods:
|Method Name|Function|Args|Return|
|---|---|---|---|
|getvideos|Get all videos|No arguments accepted|\[\<yikePhoto object\>\]|
|getgifs|Get all motion pictures|No arguments accepted|\[\<yikePhoto object\>\]|
|getscreenshots|Get all screenshots|No arguments accepted|\[\<yikePhoto object\>\]|
|listrecent|List recent medias|No arguments accepted|\[\<yikePhoto object\>\]|
|getall|Get all medias|No arguments accepted|\[\<yikePhoto object\>\]|
|getrecycled|Get all recycled medias|No arguments accepted|\[\<yikePhoto object\>\]|
|clearrecycle|Clear the recycle bin|No arguments accepted|\[\<yikePhoto object\>\]|

In particular, the following three methods return a list containing all the responding JSON (dictionaries).
|Method Name|Function|Args|Return|
|---|---|---|---|
|delete|Move to recycle bin|\[\<yikePhoto object\>\]|\[\<class 'dict'\>\]|
|restore|Restore from recycle bin|\[\<yikePhoto object\>\]|\[\<class 'dict'\>\]|
|delrecycle|Delete from recycle bin|\[\<yikePhoto object\>\]|\[\<class 'dict'\>\]||

This method is currently not recommended because it is too slow:
|Method Name|Function|Args|Return|
|---|---|---|---|
|dlall|Downloads the specified media to the working directory|workdir(string)|No return|
### `yikePhoto` class
`yikePhoto` has the following member methods.
|Method Name|Function|Args|Return|
|---|---|---|---|
|delrecycle|Delete from the recycle bin|No arguments accepted|Response JSON(dictionary)|
|restore|Restore|No arguments accepted|Response JSON(dictionary)|
|delete|Recycle|No arguments accepted|Response JSON(dictionary)|
|exif|Get EXIF|No arguments accepted|Response JSON(dictionary)|
|getdl|Get download link|No arguments accepted|Url(string)|
|dl(will automatically write metadata)|Download to working directory|workdir(string)|No return|

yikePhoto has a property: `yikePhoto.time` (string): The time it is displayed in Yike Gallery (on the home page timeline) and is in the format `YYYY:MM:DD HH:MM:SS`.  
This property could be useful since PNG, Webp and other images file types lose their creation time during transfer, and usually, such files are not with meta information.
### Usage
```Python
from yike import *
bdstoken=input("bdtoken:")
cookies=input("cookies:")
yi = yikeENV(cookies, bdstoken)
print(yi.delete(yi.getvideos())) #Delete all videos
```
### Note
Task takes a while to execute. Please wait patiently if the interface does not respond. The return 0 means the task was executed successfully.
