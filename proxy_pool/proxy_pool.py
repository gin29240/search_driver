import random
import time
from threading import Thread

import requests
from bs4 import BeautifulSoup

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    'Mozilla/5.0 (Windows NT 4.0) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/52.0.855.0 Safari/532.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/47.0.884.0 Safari/532.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.0 (KHTML, like Gecko) Chrome/63.0.863.0 Safari/536.0',
    'Mozilla/5.0 (Linux; Android 4.0.4) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/15.0.854.0 Safari/534.0',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/53.0.849.0 Safari/531.2',
    'Mozilla/5.0 (Linux; Android 4.3) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/19.0.832.0 Safari/531.2',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/38.0.881.0 Safari/532.0',
    'Mozilla/5.0 (Windows NT 4.0) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/22.0.814.0 Safari/532.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.1 (KHTML, like Gecko) Chrome/20.0.884.0 Safari/536.1',
    'Mozilla/5.0 (Windows 98) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/23.0.802.0 Safari/534.',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/21.0.814.0 Safari/531.2',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/40.0.883.0 Safari/534.0',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_7) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/19.0.828.0 Safari/533.2',
    'Mozilla/5.0 (Linux; Android 2.3.3) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/49.0.840.0 Safari/534.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_11_4) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/57.0.863.0 Safari/532.0',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_12_4) AppleWebKit/533.0 (KHTML, like Gecko) Chrome/44.0.858.0 Safari/533.0',
    'Mozilla/5.0 (Linux; Android 6.0.1) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/54.0.850.0 Safari/532.0',
    'Mozilla/5.0 (Windows 98) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/40.0.896.0 Safari/532.1',
]
cookie_pool = [
    # 'BDUSS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BDUSS_BFESS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BAIDUID=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; PSTM=1701310855; BIDUPSID=D7E1D1CDBC8C5AEFCAFAA6F3E239FAC7; BD_UPN=12314753; MCITY=-158%3A; MAWEBCUID=web_DnAfsbAbeeprrlcdaUTlQsdsjCjkXXIqEALivcSbApyhbWKFHT; H_PS_PSSID=60364; H_WISE_SIDS=60364; H_WISE_SIDS_BFESS=60364; kleck=94ecedd597d7fe78d94b84d8a7d041a7; BAIDUID_BFESS=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; BA_HECTOR=01800421a1ak0401858k0g208k66kb1j8dhvq1v; ZFY=YDUr9WWKJkcn20newQHDYSrfqyYILzP4DL8q3XI6O08:C; BDRCVFR[pRAxDSK7ZeD]=mk3SLVN4HKm; delPer=0; BD_CK_SAM=1; PSINO=6; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=a876i9EXtEb3BMthbvkTVI7ECc7fA5iPDeYbnO4d1nm7HvT5YhzAjxmmaQPR8sEQSYiSHuE; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; B64_BOT=1; ab_sr=1.0.1_NmU0NWZlNjI2NzcxNDllMzE1YzVjZDgxODM0ZTc0NDI4NGJmYmI1OTA4MTRkZDVhNGIzMzNlNTljOWIxN2Q3MjYxY2Q4MmY4ZjUzYTVjMzFhN2I3MDk2YjRjMzg4NjA2OWUwNWUwMDNlYTlhNjZjN2VhNTVhMGYyNzhkZTRiN2ViYjRiMTRhOTg2ZDI0Y2VmNjFhMjRmNDYxNDcwYzY3ZDg1NmRmNjQ3MDI1YjVhZjA3NTgyMTYxNmI5ZGFiNGI1',
    'BDUSS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BDUSS_BFESS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BAIDUID=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; PSTM=1701310855; BIDUPSID=D7E1D1CDBC8C5AEFCAFAA6F3E239FAC7; BD_UPN=12314753; MCITY=-158%3A; MAWEBCUID=web_DnAfsbAbeeprrlcdaUTlQsdsjCjkXXIqEALivcSbApyhbWKFHT; H_PS_PSSID=60364; H_WISE_SIDS=60364; H_WISE_SIDS_BFESS=60364; kleck=94ecedd597d7fe78d94b84d8a7d041a7; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; sug=3; sugstore=0; ORIGIN=0; bdime=0; BD_CK_SAM=1; PSINO=6; BAIDUID_BFESS=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; delPer=0; BA_HECTOR=0hak8ka4040020a42k8lal2198eje21j8f5lb1u; COOKIE_SESSION=3_0_6_9_7_16_0_0_3_7_3_1_14046_0_0_0_1720161768_0_1720161960%7C9%23192359_21_1719996389%7C9; ZFY=8WyjQ4s928nC6MG3rAddm1DL2chqlY2gAHUtZQuBwPE:C; H_PS_645EC=4836gg6d9q6tskPA8c6SNRuZ8EXD7ASb9%2F5wzSn5oU5VpljziMOFTp5Aas92J7a6Z1fouv4; BDSVRTM=0',
    # 'BDUSS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BDUSS_BFESS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BAIDUID=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; PSTM=1701310855; BIDUPSID=D7E1D1CDBC8C5AEFCAFAA6F3E239FAC7; BD_UPN=12314753; MCITY=-158%3A; MAWEBCUID=web_DnAfsbAbeeprrlcdaUTlQsdsjCjkXXIqEALivcSbApyhbWKFHT; H_PS_PSSID=60364; H_WISE_SIDS=60364; H_WISE_SIDS_BFESS=60364; kleck=94ecedd597d7fe78d94b84d8a7d041a7; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; sug=3; sugstore=0; ORIGIN=0; bdime=0; ab_sr=1.0.1_YTEwOWZjMTE5MDBiODU5NzBlZDQzMjFhNzE2MDM2NThkZGUzMzkzZWY2ZDMyY2RlM2ZjOTI3MDg1ZTc3ZDBhMDFkZDQ3ODkyNDAzMTAyMjhhZDNiZTYyYmNhNDMzYmI3Y2QyYzIwMjdiZDIxZTMxYjhjZTAzZTk5YTcyYmRhZTJjZmM0M2UyZmI3OGY2ODg0OWRkZGUzZTdkNjg0ZGQ0Yg==; BD_CK_SAM=1; PSINO=6; BAIDUID_BFESS=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; delPer=0; BA_HECTOR=0hak8ka4040020a42k8lal2198eje21j8f5lb1u; COOKIE_SESSION=3_0_6_9_7_16_0_0_3_7_3_1_14046_0_0_0_1720161768_0_1720161960%7C9%23192359_21_1719996389%7C9; ZFY=8WyjQ4s928nC6MG3rAddm1DL2chqlY2gAHUtZQuBwPE:C; H_PS_645EC=4836gg6d9q6tskPA8c6SNRuZ8EXD7ASb9%2F5wzSn5oU5VpljziMOFTp5Aas92J7a6Z1fouv4; BDSVRTM=0',
    # 'BDUSS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BDUSS_BFESS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BAIDUID=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; PSTM=1701310855; BIDUPSID=D7E1D1CDBC8C5AEFCAFAA6F3E239FAC7; BD_UPN=12314753; MCITY=-158%3A; MAWEBCUID=web_DnAfsbAbeeprrlcdaUTlQsdsjCjkXXIqEALivcSbApyhbWKFHT; H_PS_PSSID=60364; H_WISE_SIDS=60364; H_WISE_SIDS_BFESS=60364; kleck=94ecedd597d7fe78d94b84d8a7d041a7; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; sug=3; sugstore=0; ORIGIN=0; bdime=0; BD_CK_SAM=1; PSINO=6; BAIDUID_BFESS=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; delPer=0; BA_HECTOR=0hak8ka4040020a42k8lal2198eje21j8f5lb1u; COOKIE_SESSION=3_0_6_9_7_16_0_0_3_7_3_1_14046_0_0_0_1720161768_0_1720161960%7C9%23192359_21_1719996389%7C9; ZFY=8WyjQ4s928nC6MG3rAddm1DL2chqlY2gAHUtZQuBwPE:C; H_PS_645EC=4836gg6d9q6tskPA8c6SNRuZ8EXD7ASb9%2F5wzSn5oU5VpljziMOFTp5Aas92J7a6Z1fouv4; BDSVRTM=0',
]


class ProxyPool(object):
    def __init__(self):
        self.headers = {
            'Cookie': random.choice(cookie_pool),
            'Host': 'www.baidu.com',
            'referer': 'https://www.baidu.com/s',
            'User-Agent': random.choice(user_agents),
        }
        self.pool = [
            '115.195.213.221:64256',
            '113.128.34.131:64256',
            '113.120.174.114:64256',
            '119.41.198.253:64256',
            '49.76.41.218:64256',
            '222.187.65.18:64256',
            '112.194.90.185:64256',
            '123.171.206.66:64256',
            '113.235.78.145:64256',
            '42.179.167.44:64256',
            '221.202.130.233:64256',
            '117.95.7.31:64256',
            '42.84.175.237:64256',
            '36.25.152.67:64256',
            '119.102.41.223:64256',
            '113.226.102.78:64256',
            '42.6.109.180:64256',
            '60.17.168.54:64256',
            '106.111.168.18:64256',
            '220.176.250.41:64256',
            '117.31.55.48:64256',
            '202.105.64.119:64256',
            '122.238.171.124:64256',
            '124.116.165.162:64256',
            '111.72.130.8:64256',
            '119.132.28.31:64256',
            '58.19.47.146:64256',
            '140.224.119.157:64256',
            '110.86.183.34:64256',
            '113.241.136.165:64256',
            '222.35.227.191:64256',
            '125.78.229.182:64256',
            '60.172.70.207:64256',
            '122.137.49.195:64256',
            '117.94.115.134:64256',
            '121.207.45.236:64256',
            '120.34.36.84:64256',
            '180.127.206.38:64256',
            '222.223.68.209:64256',
            '183.136.125.13:64256',
            '49.70.32.74:64256',
            '113.76.131.67:64256',
            '111.76.67.88:64256',
            '115.196.61.152:64256',
            '106.122.231.166:64256',
            '121.233.159.144:64256',
            '59.54.238.122:64256',
            '120.41.131.183:64256',
            '122.245.114.196:64256',
            '1.84.252.206:64256',
        ]
        self.check_interval = 6  # 代理IP检查周期，单位为秒
        Thread(target=self.check_proxy_loop).start()

    # def add_proxy(self, proxy):
    #     if self.check_proxy(proxy):
    #         self.pool.append(proxy)

    def check_proxy(self, proxy):
        v_proxy = {"http": "http://" + proxy}
        try:
            # res = requests.get('http://www.baidu.com', proxies=proxy, timeout=5)
            res = requests.get('https://www.baidu.com', headers=self.headers, proxies=v_proxy)
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            result_list = soup.find_all('h3')
            # if res.status_code == 200 & len(result_list) > 0:
            if res.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def get_proxy(self):
        if not self.pool:
            return None
        return random.choice(self.pool)

    def check_proxy_loop(self):
        while True:
            for proxy in self.pool:
                if not self.check_proxy(proxy):
                    self.pool.remove(proxy)
                    print('{} removed from proxy pool'.format(proxy))
                    print(' proxy pool还剩{}个'.format(len(self.pool)))
                    print(self.pool)
            time.sleep(self.check_interval)


# def main():
#     proxy_pool = ProxyPool()
#     print(proxy_pool.pool)
#     # proxy_pool.get_proxy()
#
#
# if __name__ == '__main__':
#     main()
