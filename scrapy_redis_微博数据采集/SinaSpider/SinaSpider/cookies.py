# selenium
# 登陆和cookie`存储
# 发起请求
# 个人用户数据解析

import time
from selenium import webdriver
from .user import account, password
import json
import redis

user_list = [
    (account, password)
]


def get_cookie(account, password):
    # 打开浏览器
    driver = webdriver.Chrome()
    # 打开登陆页面
    driver.get('https://passport.weibo.cn/signin/login')
    # time.sleep(2)
    time.sleep(5)

    # 定位帐号输入框，输入帐号
    username = driver.find_element_by_id('loginName')
    username.clear()
    username.send_keys(account)
    time.sleep(2)

    # 定位密码输入框，输入密码
    password_in = driver.find_element_by_id('loginPassword')
    password_in.clear()
    password_in.send_keys(password)
    time.sleep(2)

    # 定位登陆按钮，点击登陆
    commit = driver.find_element_by_id('loginAction')
    commit.click()  # 点击
    time.sleep(3)

    # 定位验证按钮
    driver.find_element_by_xpath('//span[@class="geetest_radar_tip_content"]').click()
    time.sleep(10)

    # 用OpenCV匹配验证码等.....

    # 获取cookies数据
    cookie = {}
    for item in driver.get_cookies():
        # print(item)
        cookie[item['name']] = item['value']
    # print(cookie)

    # 判断条件，判断有没成功
    return json.dumps(cookie)

def initCookies(rconn):
    # 建立和1redis的连接
    # rconn = redis.Redis(host='127.0.0.1', port=6379) # 通过传参来实现
    # print(rconn.keys())
    for user in user_list: # 获取帐号密码
        # 判断该帐号是否登录成功
        if rconn.get('Cookies:{}'.format(account)) is None:
            print('该cookies不存在....')
            # 没有登录成功 就调用登录的方法
            cookie = get_cookie(user[0], user[1])
            # 如果cookie存在数据，就存入到redis中。
            if len(cookie) > 0:
                rconn.set('Cookies:{}'.format(account), cookie)
        else:
            print('该cookies已存在....')




# rconn = redis.Redis(host='127.0.0.1', port=6379) # 通过传参来实现
# print(rconn.keys())
# for user in user_list: # 获取帐号密码
#        # 判断该帐号是否登录成功
#     if rconn.get('Cookies:{}'.format(account)) is None:
#         print('该cookies不存在....')
#         # 没有登录成功 就调用登录的方法
#         cookie = get_cookie(user[0], user[1])
#         # 如果cookie存在数据，就存入到redis中。
#         if len(cookie) > 0:
#              rconn.set('Cookies:{}'.format(account), cookie)
#     else:
#         print('该cookies已存在....')