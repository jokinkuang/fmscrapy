# -*- coding:utf-8 -*-
# @author jokinkuang

import httplib
import logging

import datetime
import os

import requests
import time

from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


URL_LOGIN = "https://m.weike.fm/classroom/4381124"
URL_SELF_INFO = "https://m.weike.fm/api/account/self"
ID_TEXT_INPUT = "controlSendText"


class WordTest:
    g_browser = None
    g_wait = None

    session = None
    cookieMap = None
    passthrough = None

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'origin': "https://m.weike.fm",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }

    post_headers = {
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'content-length': "1084",
        'host': "m.weike.fm",
        'origin': "https://m.weike.fm",
        'pragma': "no-cache",
        'Cache-Control': 'no-cache',
        'referer': URL_LOGIN,
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    }

    formData = {
        "account": (None, "[object Object]"),
        "meta": (None, "[object Object]"),

        "status": (None, "send"),
        "sender_title": (None, ""),
        "type": (None, "text"),
        "content": (None, "text_from_python"),

        "id": (None, '1529111371.312002'),
        "create_time": (None, "2018-06-16 12:27"),
        "timestamp": (None, '1529111381.047179'),
        "ts": (None, '1529111381.047179'),
    }

    def __init__(self):
        self.session = requests.Session()
        httplib.HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    # login with selenium
    def login(self):
        global g_browser
        global g_wait

        g_browser.get(URL_LOGIN)
        time.sleep(1)
        g_wait.until(EC.presence_of_all_elements_located)

        while True:
            textElement = None
            try:
                textElement = g_browser.find_element_by_id(ID_TEXT_INPUT)
            except:
                pass

            if textElement is not None:
                print ("Login Successful.")
                break
            time.sleep(1)
            print ("Login Failed. Waiting manual login.")
        pass

    # switch selenium to python environment
    def switch(self):
        global g_browser
        global g_wait

        self.cookieMap = {}
        cookieList = g_browser.get_cookies()

        for cookie in cookieList:
            self.cookieMap[cookie.get('name')] = cookie.get('value')

        print "## set Cookies to Session ##"
        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookieMap)
        print self.session.cookies

        print "## get Authorization ##"
        response = self.session.get(url = URL_LOGIN, headers=self.headers)
        response = self.session.get(url = URL_SELF_INFO, headers=self.headers)
        self.account = response.json()['data']
        print self.account

    def post(self, text):

        self.formData['content'] = (None, text)

        timeString = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # 保留6位小数的时间戳，默认str会截剩2位
        id = str("{0:10f}").format(time.time())
        time.sleep(0.020)
        timestamp = str("{0:10f}").format(time.time())
        self.formData['id'] = (None, str(id))
        self.formData['create_time'] = (None, timeString)
        self.formData['timestamp'] = (None, timestamp)
        self.formData['ts'] = (None, timestamp)

        # 使用流方式，都是字符串！
        files = self.formData
        print self.formData

        self.post_headers['authorization'] = self.account['token']
        response = self.session.post("https://m.weike.fm/api/classroom/4381124/message/send",
                                     files=files,

                                     headers=self.post_headers)
        result = response.json()
        print result
        if result['code'] == 0 and "*" in result['data']['message']['content']:
            return None
        return text;

    def handleFile(self, path):
        print "handling file:" + path
        if not os.path.isfile(path):
            return None

        if "_passthrough" in path:
            return None

        pass_through_dict = {}
        with open(path) as input:
            with open(path+"_passthrough.txt", "w") as output:
                allLines = input.readlines()
                for line in allLines:
                    # try:
                    pass_text = self.post(line.strip())
                    if pass_text is not None and not pass_through_dict.has_key(pass_text):
                        pass_through_dict[pass_text] = pass_text
                        output.writelines(pass_text+"\n")

                    # except Exception, e:
                    #     print "exception is:"+e.message
                    #     print "exception:"+line
                    #     pass
                    time.sleep(0.5)
        return pass_through_dict

    def handleDir(self, root):
        root_dir = root
        list = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(root_dir, list[i])
            pass_through_dict = self.handleFile(path)
            # if len(pass_through_dict) > 0:
                # self.saveToFile(pass_through_dict, os.path.join(root_dir, list[i]+"_passthrough.txt"))

    def saveToFile(self, dict, path):
        print "save to file:" + path
        file = open(path, 'w')
        for value in dict.values():
            file.writelines(value)
        file.close()

    def run(self, words_file_dir):
        global g_browser
        global g_wait

        startTime = time.time()
        chrome_options = chrome.options.Options()

        g_browser = webdriver.Chrome(chrome_options=chrome_options)
        g_wait = WebDriverWait(g_browser, 10) # wait for at most 10s

        print "## step1. login ##"
        self.login()

        print "## step2. set python environment ##"
        self.switch()

        print "## step3. do request ##"
        self.handleDir(words_file_dir)

        print "## step4. exit browser ##"
        g_browser.quit()

        print "## Cost Time ##"
        print time.strftime(u"%H:%M:%S", time.gmtime(time.time() - startTime))


# Main #
WordTest().run("./words")