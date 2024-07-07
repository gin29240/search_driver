import pandas as pd
import os
from time import sleep
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from is_thinkPhP.is_thinkPhp import Is_ThonkPHP

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
]
headers = {
    'Cookie': """BDUSS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BDUSS_BFESS=FnMUl1WWxVaGI5OWI4S0tDWllkR2ppRUdPSlp4bTNDcFB2NkRjM0xyUnRVbU5sSUFBQUFBJCQAAAAAAAAAAAEAAACAhf6Tu-y31r7eyt6~tL-0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3FO2VtxTtlZl; BAIDUID=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; PSTM=1701310855; BIDUPSID=D7E1D1CDBC8C5AEFCAFAA6F3E239FAC7; BD_UPN=12314753; MCITY=-158%3A; MAWEBCUID=web_DnAfsbAbeeprrlcdaUTlQsdsjCjkXXIqEALivcSbApyhbWKFHT; H_PS_PSSID=60364; H_WISE_SIDS=60364; H_WISE_SIDS_BFESS=60364; delPer=0; BD_CK_SAM=1; PSINO=7; BAIDUID_BFESS=671C49D661F379A303F181B38B20FB92:SL=0:NR=10:FG=1; BA_HECTOR=2l84842gaga5alah2h8l2ka421kia51j8b8j31u; ZFY=5FjtqP:AnQLAvF3Vacu4PEPIWSGjttqvtl74AM9kccGY:C; B64_BOT=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1719543972,1719977460,1720076952; Hm_lpvt_aec699bb6442ba076c8981c6dc490771=1720076952; RT="z=1&dm=baidu.com&si=6b18837d-8f9f-4865-8640-3574c735ae8f&ss=ly6o2z71&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3ry&ul=b9oz9&hd=b9pf1"; BDRCVFR[pRAxDSK7ZeD]=mbxnW11j9Dfmh7GuZR8mvqV; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; kleck=94ecedd597d7fe78d94b84d8a7d041a7; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=2325NjDQwayXfoyTXudSNI9UUzAsFwvfOM7cqxEsOK7dEdweFW5vZ6nCleqZhQ7o2tF8df4; COOKIE_SESSION=456_0_6_5_20_11_0_0_6_2_0_1_430_0_101_0_1720095714_0_1720095613%7C9%23192359_21_1719996389%7C9; BDSVRTM=0; ab_sr=1.0.1_YjRjMTg2YmUyYjQxMDM1YTcxZTNhZDM5OWNkNjQ4YjE3MzgzNDMwN2YzZTg0MzhmZjllZDVlODIwMTU0MWY0MmIyMzBiY2M3ZTdiZTU1NjY1YTc1YmYxYWZmNGI5NjAxNzExZjI2NTlhY2Y5ODhhMzMzNDY2OTFiYTYzZWNmM2JmMGJjYTY4YmM1YmEzYTI4YjQxMjI4YmZhZjkxMjUxOQ==""",
    'Host': 'www.baidu.com',
    'referer': 'https://www.baidu.com/s',
    'User-Agent': random.choice(user_agents),
}


def baidu_search(v_query, v_result_file, v_max_page):
    """
        爬取百度搜索结果
        :param v_query :关键字
        :param v_result_file ：保存文件名称
        :param v_max_page ：爬取页数
        ：return None
        """
    # 获取每页搜索结果
    for page in range(v_max_page):
        print("开始爬取第{}页".format(page + 1))
        wait_seconds = random.uniform(1, 2)  # 等待时长秒
        print("开始等待{}秒".format(wait_seconds))
        sleep(wait_seconds)
        url = "https://www.baidu.com/s?wd=" + v_query + "&pn=" + str(page * 10)
        ## 搜索引擎访问限制 ，暂时无法解决--弃用代码
        # r = requests.get(url, headers=headers)
        # html = r.text
        # print("响应码是：{}".format(r.status_code))
        # soup = BeautifulSoup(html, 'html.parser')
        # # print(soup)
        # # result_list = soup.find_all(class_='result c-container xpath-log new-pmd')
        # result_list = soup.find_all('h3')
        chrome_options = Options()
        driver_path = 'D:\chrome-win64\chromedriver.exe'
        s = Service(driver_path)
        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.get(url)
        # driver.get("https://www.baidu.com")
        result_list = WebDriverWait(driver,4).until(
            driver.find_elements(By.TAG_NAME, "h3")
        )

        print("正在爬取：{}，爬取{}个结果".format(url, len(result_list)))
        kw_list = []  # 关键字
        page_list = []  # 页码
        title_list = []  # 标题
        href_list = []  # 百度的链接
        real_href_list = []  # 百度链接
        desc_list = []  # 简介
        site_list = []  # 网站名称
        for result in result_list:
            title = result.find('a').text
            print('title is: ', title)
            href = result.find('a')['href']
            real_url = get_real_url(v_url=href)
            isthonkPHP = Is_ThonkPHP()
            if not isthonkPHP.is_thinkphp(real_url):
                continue
            # try:
            #     desc = result.find(class_='c-abstract').text
            # except:
            #     desc = ""
            kw_list.append(v_query)
            page_list.append(page + 1)
            title_list.append(title)
            href_list.append(href)
            real_href_list.append(real_url)
            desc_list.append("ThinkPHP")
            site_list.append(1)
        df = pd.DataFrame(
            {
                '关键字': kw_list,
                '页码': page_list,
                '标题': title_list,
                '百度链接': href_list,
                '真实链接': real_href_list,
                '简介': desc_list,
                '网站名称': site_list,
            }
        )
        if os.path.exists(v_result_file):
            header = None
        else:
            header = ['关键字', '页码', '标题', '百度链接', '真实链接', '简介', '网站名称']
        df.to_csv(v_result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')


def get_real_url(v_url):
    r = requests.get(v_url, headers=headers, allow_redirects=False)  # 不允许重定向
    if r.status_code == 302:  # 如果返回302，就从响应头获取真实地址
        real_url = r.headers.get('Location')
    else:  # 否则从返回内容中用正则表达式提取来真实地址
        real_url = re.findall("URL='(.*?)'", r.text)[0]
    print('real_url is： ', real_url)
    return real_url


if __name__ == '__main__':

    query = 'inurl:index.php?s=/Home'
    max_page = 100
    result_file = 'ThinkPhp_{}.csv'.format(max_page)
    if os.path.exists(result_file):
        os.remove(result_file)
        print("结果文件{}已存在，已删除", result_file)
    # 开始爬取
    baidu_search(v_query=query, v_result_file=result_file, v_max_page=max_page)
