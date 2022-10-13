import base64
import requests
import time
import os
from urllib.parse import unquote
import traceback
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
from email.message import Message
import time
import hashlib

req = requests.Session()

def printProgress(message):
    global printMaxChar
    printMaxChar = max(printMaxChar, len(message))
    print(('\r' + message).ljust(printMaxChar + 4), end='')

class yikeENV():
    def __init__(self, cookies, bdstoken, limit=100):
        self.cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
        self.bdstoken = str(bdstoken)
        self.limit = limit
        self.ua = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        self.s = {
            'videos': '1102',
            'gifs': '1103',
            'screenshots': '22'
        }

    def __cursor__(self, start, limit):
        if start == 0:
            return ''
        return '&cursor=' + str(base64.b64encode(('{\"start\":'+str(start)+',\"limit\":'+str(limit)+'}').encode('utf-8')))[2:-1]

    def __search__(self, method):
        url = 'https://photo.baidu.com/youai/iclass/index/v1/search?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&tag_id=' + self.s[method] \
            + '&need_thumbnail=1'
        l = []
        i = 0
        while True:
            tmp = req.get(url + self.__cursor__(i, self.limit),
                               cookies=self.cookies, headers=self.ua).json()['list']
            if tmp == []:
                break
            l += tmp
            i += self.limit
        result = []
        for i in l:
            result.append(yikePhoto(i, self.cookies, self.bdstoken))
        return result

    def __list__(self, method, extra = ""):
        url = 'https://photo.baidu.com/youai/file/v1/' + method + '?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + extra
        l = []
        i = 0
        while True:
            result = req.get(url + self.__cursor__(i, self.limit),
                            cookies=self.cookies, headers=self.ua).json()
            if 'list' not in result: # r['errno'] == 2, no more result
                break
            tmp = result['list']
            if tmp == []:
                break
            l += tmp
            i += self.limit
        result = []
        for i in l:
            result.append(yikePhoto(i, self.cookies, self.bdstoken))
        return result

    def __fo__(self, method, list):
        result = []
        fsid_list = [i.fsid for i in list]
        url = 'https://photo.baidu.com/youai/file/v1/' + method + '?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&fsid_list='
        while True:
            if len(fsid_list) > 500:
                tmp = fsid_list[:500:]
                fsid_list = fsid_list[500::]
                while (True):
                    r = req.get(
                    url + str(tmp).replace(' ', '').replace('\'', ''), cookies=self.cookies, headers=self.ua).json()
                    if r['errno'] == 0:
                        break
                    else:
                        time.sleep(1)
                result.append(r)
            else:
                tmp = fsid_list
                while (True):
                    r = req.get(
                    url + str(tmp).replace(' ', '').replace('\'', ''), cookies=self.cookies, headers=self.ua).json()
                    if r['errno'] == 0:
                        break
                    else:
                        time.sleep(1)
                result.append(r)
                return result

    def getvideos(self):
        return self.__search__('videos')

    def getgifs(self):
        return self.__search__('gifs')

    def getscreenshots(self):
        return self.__search__('screenshots')

    def getall(self):
        return self.__list__('list')

    def getrecycled(self):
        return self.__list__('listrecycle')

    def listrecent(self):
        return self.__list__('listrecent', '&need_thumbnail=1&sort_field=ctime')

    def delete(self, list):
        return self.__fo__('delete', list)

    def restore(self, list):
        return self.__fo__('restore', list)

    def delrecycle(self, list):
        return self.__fo__('delrecycle', list)

    def clearrecycle(self):
        url = 'https://photo.baidu.com/youai/file/v1/clearrecycle?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken
        return req.get(url, cookies=self.cookies, headers=self.ua).json()
    
    def dlall(self, li, workdir):
        for i in li:
            i.dl(workdir)


class yikePhoto:
    def __init__(self, js, cookies, bdstoken):
        self.fsid = str(js['fsid'])
        self.time = js['extra_info']['date_time'].replace('-',':')
        self.ctime = js['ctime']
        self.mtime = js['mtime']
        #self.shoot_time = js['shoot_time']
        self.cookies = cookies
        self.bdstoken = str(bdstoken)
        self.ua = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

    def __fo__(self, method):
        url = 'https://photo.baidu.com/youai/file/v1/' + method + '?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&fsid_list=[' + self.fsid + ']'
        return req.get(url, cookies=self.cookies, headers=self.ua).json()

    def __modifyFileTime__(self, filePath):
        ctime = time.localtime(self.ctime)
        mtime = time.localtime(self.mtime)
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        #createTimes, accessTimes, modifyTimes = GetFileTime(fh)
        #T = Time(time.mktime(Time_t))
        #SetFileTime(fh, T, T, T)
        try:
            SetFileTime(fh, Time(ctime), Time(mtime), Time(time.time())) # must be a pywintypes time object
        except Exception as e:
            print('[Error] __modifyFileTime__ for ' + filePath + ' to ' + time.strptime(mtime, '%Y:%m:%d %H:%M:%S'))
            #print(traceback.format_exc())
            raise
        finally:
        CloseHandle(fh)

    def delrecycle(self):
        return self.__fo__('delrecycle')

    def restore(self):
        return self.__fo__('restore')

    def delete(self):
        return self.__fo__('delete')

    def getdl(self):
        try:
            url = 'https://photo.baidu.com/youai/file/v2/download?' \
                + 'clienttype=70' \
                + '&bdstoken=' + self.bdstoken \
                + '&fsid=' + self.fsid
            return req.get(url, cookies=self.cookies, headers=self.ua).json()['dlink']
        except Exception as e:
            print('[Error] Failed to get download link of photo with fsid ' + self.fsid)
            print(traceback.format_exc())

    def exif(self):
        url = 'https://photo.baidu.com/youai/file/v1/exif?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&fsid=' + self.fsid
        return req.get(url, cookies=self.cookies, headers=self.ua).json()

    def __md5__(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname,"rb") as f:
            for chunk in iter(lambda :f.read(4096),b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def dl(self, workdir):
        try:
            url = self.getdl()
            r = req.get(url, stream=True, headers=self.ua)
            filename = ''
            if 'Content-Disposition' in r.headers and r.headers['Content-Disposition']:
                m = Message()
                m['Content-Disposition'] = r.headers['Content-Disposition']
                file_name = m.get_param('filename', None, 'Content-Disposition')
                if file_name:
                    f = file_name.encode('ISO-8859-1').decode('utf8')
                    filename = unquote(f)
            if not filename and os.path.basename(url):
                filename = os.path.basename(url).split("?")[0]
            if not filename:
                raise ValueError()
            filename = filename.strip('"')
            filePath = workdir + filename
            if(os.path.isfile(filePath) and 
                'Content-Length' in r.headers and r.headers['Content-Length'] and
                'Content-MD5' in r.headers and r.headers['Content-MD5']): # sometime KeyError: 'content-length'
                if(os.path.getsize(filePath) != int(r.headers['Content-Length']) or 
                    self.__md5__(filePath) != r.headers['Content-MD5']):
                    filePath_ = os.path.splitext(filePath)
                    oldFileNewPath = filePath_[0] + 'old.' + str(int(time.time())) + filePath_[1]
                    os.rename(filePath, oldFileNewPath)
                else:
                    printProgress(os.path.basename(filePath) + ' already exists.')
                    # self.__modifyFileTime__(filePath)
                    return

            file = open(filePath, 'wb')
            for i in r.iter_content(chunk_size=4096):
                if i:
                    file.write(i)
            file.close()
            self.__modifyFileTime__(filePath)
            printProgress(os.path.basename(filePath) + ' done.')
        except Exception as e:
            print('[Error] Error downloading photo with fsid ', self.fsid)
            print('The file path: ', filePath)
            print(traceback.format_exc())
