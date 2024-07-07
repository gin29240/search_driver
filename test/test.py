import os
import queue
import random
import re
import threading
import time
from time import sleep

import pandas as pd
import pyautogui as pyautogui
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from is_thinkPhP.is_thinkPhp import Is_ThonkPHP

is_thinkPHP = Is_ThonkPHP()
wait_seconds2 = random.uniform(1, 2)  # 等待时长秒


def mous_move():
    # 滚轮向上滑动
    roll_num = random.uniform(200, 300)

    # 移动鼠标到起始位置
    # pyautogui.moveTo(roll_num, roll_num, duration=0.25)
    pyautogui.scroll(300)  # 向上滚动200个单位
    time.sleep(wait_seconds2)  # 等待1秒

    # 滚轮向下滑动
    pyautogui.scroll(-2900)  # 向下滚动200个单位
    time.sleep(wait_seconds2)  # 等待1秒
    # # 设置滑动的起始和终止位置


if __name__ == '__main__':
    result_file = 'ThinkPhp_{}.csv'.format(802)
    if os.path.exists(result_file):
        os.remove(result_file)
        print("结果文件{}已存在，已删除", result_file)
    page = 0

    while True:
        print("开始爬取第{}页".format(page + 1))
        wait_seconds = random.uniform(1, 3)  # 等待时长秒
        # wait_seconds2 = random.uniform(1, 2)  # 等待时长秒
        v_query = 'inurl:index.php?s=/Home'
        # url = "https://www.baidu.com/s?wd=" + v_query + "&pn=" + str(page * 10)
        url = "https://www.google.com/search?q=" + v_query + "&pn=" + str(page * 10)
        page += 1
        chrome_options = Options()
        driver_path = 'D:\chrome-win64\chromedriver.exe'
        s = Service(driver_path)
        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.get(url)
        print('您已成功打开网页')
        result_list = driver.find_elements(By.TAG_NAME, "h3")
        # page += len(result_list) / 10
        print("正在爬取：{}，爬取{}个结果".format(url, len(result_list)))
        if len(result_list) <= 0:
            # driver.close()
            sleep(100)
        kw_list = []  # 关键字1
        title_list = []  # 标题
        real_href_list = []  # 百度链接
        # 获取当前窗口
        current_window = driver.current_window_handle
        # 百度跳转地址
        for a in driver.find_elements(By.XPATH, "//div[@srcid='1599']//div/h3/a"):#baidu
        # for a in driver.find_elements(By.XPATH, "//a[@jsname='UWckNb']"):#google
            a.click()  # 点击进行跳转# 获取打开的所有窗口，一会要将打开的窗口关闭，防止耗用电脑性能
            mous_move()
        all_windows = driver.window_handles
        # 所有窗口包含打开的搜索页面，不能将手搜页面关闭，所以将搜索页面剔除
        all_windows.remove(current_window)

        # 对打开的页面进行关闭操作，这里一定要先关闭，再切换窗口，当前的driver是最后一个打开页面的窗口
        # 因此如果先关闭的话容易导致出错，自行switchs 切换窗口已经销毁
        for window in all_windows:
            driver.switch_to.window(window)
            real_url = driver.current_url
            if not is_thinkPHP.is_thinkphp(real_url):
                continue
            print("real_url is {}".format(real_url))  # 统计获取到的URL   真实ur
            real_href_list.append(real_url)  # 统计获取到的URL   真实url
            kw_list.append(v_query)
            title_list.append(1)
            df = pd.DataFrame(
                {
                    '关键字': kw_list,
                    '标题': title_list,
                    '真实链接': real_href_list,
                }
            )
            if os.path.exists(result_file):
                header = None
            else:
                header = ['关键字', '标题', '真实链接', ]
            df.to_csv(result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
        # 复原
        # 执行 其实这里可以和上面的循环一起处理
        for window in all_windows[:]:
            driver.switch_to.window(window)
            sleep(wait_seconds2)
            driver.close()
        # driver.close()
        # 重新切换到搜索页面的窗口
        # driver.switch_to.window(current_window)
        sleep(wait_seconds)
