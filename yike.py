import base64
import requests
import time


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
            tmp = requests.get(url + self.__cursor__(i, self.limit),
                               cookies=self.cookies, headers=self.ua).json()['list']
            if tmp == []:
                break
            l += tmp
            i += self.limit
        result = []
        for i in l:
            result.append(yikePhoto(i, self.cookies, self.bdstoken))
        return result

    def __list__(self, method):
        url = 'https://photo.baidu.com/youai/file/v1/' + method + '?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken
        l = []
        i = 0
        while True:
            tmp = requests.get(url + self.__cursor__(i, self.limit),
                               cookies=self.cookies, headers=self.ua).json()['list']
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
                    r = requests.get(
                    url + str(tmp).replace(' ', '').replace('\'', ''), cookies=self.cookies, headers=self.ua).json()
                    if r['errno'] == 0:
                        break
                    else:
                        time.sleep(1)
                result.append(r)
            else:
                tmp = fsid_list
                while (True):
                    r = requests.get(
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
        return requests.get(url, cookies=self.cookies, headers=self.ua).json()


class yikePhoto:
    def __init__(self, js, cookies, bdstoken):
        self.fsid = str(js['fsid'])
        self.time = js['extra_info']['date_time'].replace('-',':')
        self.cookies = cookies
        self.bdstoken = str(bdstoken)
        self.ua = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

    def __fo__(self, method):
        url = 'https://photo.baidu.com/youai/file/v1/' + method + '?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&fsid_list=[' + self.fsid + ']'
        return requests.get(url, cookies=self.cookies, headers=self.ua).json()

    def delrecycle(self):
        return self.__fo__('delrecycle')

    def restore(self):
        return self.__fo__('restore')

    def delete(self):
        return self.__fo__('delete')

    def getdl(self):
        url = 'https://photo.baidu.com/youai/file/v2/download?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&fsid=' + self.fsid
        return requests.get(url, cookies=self.cookies, headers=self.ua).json()['dlink']

    def exif(self):
        url = 'https://photo.baidu.com/youai/file/v1/exif?' \
            + 'clienttype=70' \
            + '&bdstoken=' + self.bdstoken \
            + '&fsid=' + self.fsid
        return requests.get(url, cookies=self.cookies, headers=self.ua).json()
