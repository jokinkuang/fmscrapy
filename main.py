# -*- coding:utf-8 -*-
# @author jokinkuang
import cookielib

import cookiejar as cookiejar
import datetime
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver

import time
import json

from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import model
from model import KEY_TOTAL, KEY_NAME, KEY_LINK
from model import KEY_CRASH
from model import KEY_ANR
from model import KEY_ERROR
import mailer

import requests
import logging
import httplib

# // Hard Code //

URL_LOGIN = "https://m.weike.fm/classroom/4303270"#4381124" #4303270
ID_TEXT_INPUT = "controlSendText"
CLASS_TEXT_SEND = "text-send"
TAG_INPUT = "input"
TAG_FORM = "form"

CLASS_GENG_DUO = "icon-xinbanketangye-gengduo"
CLASS_GRID_BUTTON = "weui-grid"
BUTTON_SUCAIKU = u"素材库"
BUTTON_FILE = u"文件"
XPATH_SUCAIKU = "//*[@id=\"root\"]/div/div[4]/div[6]/form/div[1]/div[2]/div/a[2]/p"
CLASS_MATERIAL_PANEL = "material-panel"


# // Hard Code End //

class FmScrapy:

    g_browser = None
    g_wait = None

    session = None
    cookieMap = None

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",

        # 'authorization': "MjkwMTMwMzQ:1fTlEW:ulY-ABWxFVlEBxZIrl1SbhexSXk",
        # 'cache-control': "no-cache",
        # 'content-length': "1084",
        # 'content-type': "multipart/form-data;",
        # 'cookie': "gr_user_id=35bf7c6d-8135-4b2c-8bc7-02765c50625a; lecturer=1; sidebar_closed=1; UM_distinctid=163fbee170b712-0023f88ea02b3e-336b7707-13c680-163fbee170c67c; __DAYU_PP=e3Na3Zn3mzierAEmYNij213635dbc984; CNZZDATA1259942212=472673552-1528934906-https%253A%252F%252Fm.weike.fm%252F%7C1529051129; sessionid=\".eJw1jMsKgzAQAP9lzy3GRLQVip-yxGSRBZtIXrSI_24Oep1hZoc5R3YUI-awwgiNNsZnlxq9MS6U0OhEiw9_ZGfph266wUfAAzaDKxcK3n-Rbe2lGl6yHfrqrhPbZ1EwyrdolVDdcQKHPic1:1fTlEQ:VvwwsefD_qjcHdnxi4tRQZTvEQc\"; 944da7a11410b7a8_gr_last_sent_cs1=29013034; 944da7a11410b7a8_gr_session_id=f6f25772-e817-4ee1-bc85-fa17431f3239_false; 944da7a11410b7a8_gr_last_sent_sid_with_cs1=f6f25772-e817-4ee1-bc85-fa17431f3239; 944da7a11410b7a8_gr_cs1=29013034",
        'origin': "https://m.weike.fm",
        # 'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }

    post_headers = {
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",

        # 'authorization': "MjkwMTMwMzQ:1fTlEW:ulY-ABWxFVlEBxZIrl1SbhexSXk",
        'content-length': "1084",
        # 'content-type': "multipart/form-data;",
        # 'cookie': "gr_user_id=35bf7c6d-8135-4b2c-8bc7-02765c50625a; lecturer=1; sidebar_closed=1; UM_distinctid=163fbee170b712-0023f88ea02b3e-336b7707-13c680-163fbee170c67c; __DAYU_PP=e3Na3Zn3mzierAEmYNij213635dbc984; CNZZDATA1259942212=472673552-1528934906-https%253A%252F%252Fm.weike.fm%252F%7C1529051129; sessionid=\".eJw1jMsKgzAQAP9lzy3GRLQVip-yxGSRBZtIXrSI_24Oep1hZoc5R3YUI-awwgiNNsZnlxq9MS6U0OhEiw9_ZGfph266wUfAAzaDKxcK3n-Rbe2lGl6yHfrqrhPbZ1EwyrdolVDdcQKHPic1:1fTlEQ:VvwwsefD_qjcHdnxi4tRQZTvEQc\"; 944da7a11410b7a8_gr_last_sent_cs1=29013034; 944da7a11410b7a8_gr_session_id=f6f25772-e817-4ee1-bc85-fa17431f3239_false; 944da7a11410b7a8_gr_last_sent_sid_with_cs1=f6f25772-e817-4ee1-bc85-fa17431f3239; 944da7a11410b7a8_gr_cs1=29013034",
        'host': "m.weike.fm",
        'origin': "https://m.weike.fm",
        'pragma': "no-cache",
        'Cache-Control': 'no-cache',
        'referer': URL_LOGIN,
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    }


    formData = {
        "id": 1529111371.312002,

        "account":{},
        "meta": None,

        "status": "send",
        "sender_title": "",
        "type": "text",
        "content": "222",

        "create_time": "2018-06-16 12:27",
        "timestamp": 1529111381.047179,
        "ts": 1529111381.047179,
    }

    formData2 = {
        "account":(None, "[object Object]"),
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

    def cookiejar_from_dict(self, cookie_dict, cookiejar=None, overwrite=True):
        """Returns a CookieJar from a key/value dictionary.

        :param cookie_dict: Dict of key/values to insert into CookieJar.
        :param cookiejar: (optional) A cookiejar to add the cookies to.
        :param overwrite: (optional) If False, will not replace cookies
            already in the jar with new ones.
        """
        if cookiejar is None:
            cookiejar = RequestsCookieJar()

        if cookie_dict is not None:
            names_from_jar = [cookie.name for cookie in cookiejar]
            for name in cookie_dict:
                if overwrite or (name not in names_from_jar):
                    cookiejar.set_cookie(self.create_cookie(name, cookie_dict[name]))

        return cookiejar

    def create_cookie(self, name, value, **kwargs):
        """Make a cookie from underspecified parameters.

        By default, the pair of `name` and `value` will be set for the domain ''
        and sent on every request (this is sometimes called a "supercookie").
        """
        result = dict(
            version=0,
            name=name,
            value=value,
            port=None,
            domain='',
            path='/',
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': None},
            rfc2109=False, )

        badargs = set(kwargs) - set(result)
        if badargs:
            err = 'create_cookie() got unexpected keyword arguments: %s'
            raise TypeError(err % list(badargs))

        result.update(kwargs)
        result['port_specified'] = bool(result['port'])
        result['domain_specified'] = bool(result['domain'])
        result['domain_initial_dot'] = result['domain'].startswith('.')
        result['path_specified'] = bool(result['path'])

        return cookielib.Cookie(**result)



    def __init__(self):
        self.session = requests.Session()
        httplib.HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def untilTrue(until):
        while True:
            if until():
                return

    # @return object{ total crash anr error }
    def search(url):
        global g_browser
        print "search:"+url

        g_browser.get(url)
        time.sleep(1)

        htmlElement = None
        while True:
            htmlElement = g_browser.execute_script(ROOT_ELEMENT)
            if htmlElement is not None:
                break
            time.sleep(1)


        g_wait.until(EC.presence_of_all_elements_located)

        btnSearch = None
        while True:
            btnSearch = htmlElement.find_element_by_class_name(SEARCH_BTN_CLASS)
            if btnSearch is not None:
                break
            time.sleep(1)


        # wait for document loaded
        g_wait.until(EC.presence_of_all_elements_located)
        # wait for btn clickable
        g_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, SEARCH_BTN_CLASS)))

        while True:
            try:
                btnSearch.click()
                break
            except:
                time.sleep(1)
                continue

        # wait for document loaded
        g_wait.until(EC.presence_of_all_elements_located)

        time.sleep(5)
        # wait for result

        content = g_browser.find_element_by_class_name(SEARCH_CONTENT_CLASS).text
        print content
        result = []
        list = content.split(' ')
        for item in list:
            if item.isdigit():
                result.append(item)
        obj = {}
        obj[KEY_LINK] = url
        obj[KEY_TOTAL] = 0
        obj[KEY_CRASH] = 0
        obj[KEY_ANR] = 0
        obj[KEY_ERROR] = 0
        if len(result) == 4:
            obj[KEY_TOTAL] = result[0]
            obj[KEY_CRASH] = result[1]
            obj[KEY_ANR] = result[2]
            obj[KEY_ERROR] = result[3]
        return obj
        pass


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
            time.sleep(2)
            print ("Login Failed. Waiting manual login.")
        pass

    def cookie(self):
        global g_browser
        global g_wait

        self.cookieMap = {}
        cookieList = g_browser.get_cookies()

        for cookie in cookieList:
            self.cookieMap[cookie.get('name')] = cookie.get('value')
        print self.cookieMap
        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookieMap)
        print "## session cookies ##"
        print self.session.cookies

        response = self.session.get(url = URL_LOGIN, headers=self.headers)
        print response
        print response.text
        print response.headers
        print response.cookies
        print response.request.headers
        print response.request.url

        url = "https://m.weike.fm/api/account/self"
        response = self.session.get(url = url, headers=self.headers)
        print response
        print response.text
        print response.json()
        print response.headers
        print response.cookies
        print response.request.headers
        print response.request.url
        self.account = response.json()['data']
        print self.account



    def post(self, path):
        files = {'': (None, )}

        # self.formData2['account'] = (None, json.dumps(self.account))
        timeString = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # 保留6位小数的时间戳，默认str会截剩2位
        id = str("{0:10f}").format(time.time())
        time.sleep(0.020)
        timestamp = str("{0:10f}").format(time.time())
        self.formData2['id'] = (None, str(id))
        self.formData2['create_time'] = (None, timeString)
        self.formData2['timestamp'] = (None, timestamp)
        self.formData2['ts'] = (None, timestamp)

        # 使用流方式，都是字符串！
        files = self.formData2

        # files = {'app_id': (None, '123456'),
        #          'version': (None, '2256'),
        #          'platform': (None, 'ios'),
        #          'account': (None, json.dumps("{'id':0, 'name':'jokin'}"))
        #          # 'libzip': (
        #          # 'libmsc.zip', open('C:\Users\danwang3\Desktop\libmsc.zip', 'rb'), 'application/x-zip-compressed')
        #          }

        print "## form data ##"
        print self.formData
        upload_payload = self.formData
        self.post_headers['authorization'] = self.account['token']
        print "########################################"
        print self.post_headers['authorization']

        response = self.session.post("https://m.weike.fm/api/classroom/4381124/message/send",
                                     # data=json.dumps(self.formData),
                                     files=files,
                                     headers=self.post_headers)
        print response.text

    def sendText(self, text):
        global g_browser
        global g_wait

        textInput = g_browser.find_element_by_id(ID_TEXT_INPUT)
        textInput.send_keys(text)

        form = g_browser.find_element_by_tag_name(TAG_FORM);
        form.submit()



    def sendImage(self, path):
        global g_browser
        global g_wait

        inputs = g_browser.find_elements_by_tag_name(TAG_INPUT);
        imageInput = inputs[0]
        imageInput.send_keys(path)

        form = g_browser.find_element_by_tag_name(TAG_FORM);
        form.submit()

    def sendAudio(self, path):
        global g_browser
        global g_wait

        inputs = g_browser.find_elements_by_tag_name(TAG_INPUT);
        audioInput = inputs[1]
        audioInput.send_keys(path)

        form = g_browser.find_element_by_tag_name(TAG_FORM);
        form.submit()

    g_videoMode = False
    def sendVideo(self, path):
        global g_browser
        global g_wait
        global g_videoMode

        if not g_videoMode :
            button = g_browser.find_element_by_class_name(CLASS_GENG_DUO)
            button.click()
            time.sleep(1)

            button = getButton(CLASS_GRID_BUTTON, BUTTON_SUCAIKU)
            button.click()
            g_videoMode = True

        inputs = g_browser.find_elements_by_tag_name(TAG_INPUT);
        videoInput = inputs[1]
        videoInput.send_keys(path)

        form = g_browser.find_element_by_tag_name(TAG_FORM);
        form.submit()

    g_fileMode = False
    def sendFile(self, path):
        global g_browser
        global g_wait
        global g_fileMode

        if not g_fileMode :
            button = g_browser.find_element_by_class_name(CLASS_GENG_DUO)
            button.click()
            time.sleep(1)

            button = getButton(CLASS_GRID_BUTTON, BUTTON_FILE)
            button.click()
            g_fileMode = True

        container = g_browser.find_element_by_class_name("classroom-file-panel-container")
        inputs = container.find_elements_by_tag_name(TAG_INPUT);
        videoInput = inputs[0]
        videoInput.send_keys(path)
        print videoInput.text
        videoInput.send_keys(path)
        print videoInput.text

        form = g_browser.find_element_by_tag_name(TAG_FORM);
        form.submit()

    def getButton(self, cls, text):
        global g_browser
        global g_wait

        buttons = g_browser.find_elements_by_class_name(cls)
        for button in buttons:
            if button.text == text:
                return button
        return None


    # @return appNameList[], appIdList[]
    def get_app_list(self):
        global g_browser
        global g_wait

        htmlElement = None
        names = None
        while True:
            htmlElement = g_browser.execute_script(ROOT_ELEMENT)
            if htmlElement is not None:
                names = htmlElement.find_elements_by_class_name(APP_NAME_CLASS)
                if len(names) > 0:
                    time.sleep(2)
                    break
            time.sleep(1)

        names = htmlElement.find_elements_by_class_name(APP_NAME_CLASS)
        ids = htmlElement.find_elements_by_class_name(APP_ID_CLASS)

        appNameList = []
        appIdList = []
        for name in names:
            name = name.text
            appNameList.append(name)
            print name
        for id in ids:
            id = id.get_attribute('href')
            id = id[id.rindex('/') + 1: len(id)]
            appIdList.append(id)
            print id
        return appNameList, appIdList
        pass

    def test(self):
        global g_browser
        g_browser.get("https://www.baidu.com/")
        print "https OK"

    def main(self):
        global g_browser
        global g_wait
        startTime = time.time()
        chrome_options = chrome.options.Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--remote-debugging-port=9222')
        # chrome_options.binary_location = r'C:\Users\hldh214\AppData\Local\Google\Chrome\Application\chrome.exe'

        g_browser = webdriver.Chrome(chrome_options=chrome_options)
        g_wait = WebDriverWait(g_browser, 10) # wait for at most 10s

        print "## step1. login ##"
        self.login()

        print "## step2. get cookies ##"
        self.cookie()

        print "## step3. do request ##"
        self.post("/Users/jokinkuang/Pictures/eraser.doc")

        # self.sendFile("/Users/jokinkuang/Pictures/eraser.doc")
        # time.sleep(15)
        # self.sendFile("/Users/jokinkuang/Pictures/eraser.doc")
        # time.sleep(15)
        # self.sendFile("/Users/jokinkuang/Pictures/eraser.doc")

        # self.sendVideo("/Users/jokinkuang/Pictures/eraser.mp4")
        # self.sendVideo("/Users/jokinkuang/Pictures/eraser.mp4")
        # self.sendVideo("/Users/jokinkuang/Pictures/eraser.mp4")
        # self.sendAudio("/Users/jokinkuang/Pictures/eraser.mp3")
        # self.sendImage("/Users/jokinkuang/Pictures/eraser.jpeg")

        print "## sending text ##"
        self.sendText(u"中国共产党")
        # sendText(u"毛泽东")
        # sendText(u"江泽民")
        self.sendText(u"习近平")
        # sendText(u"习近\n平")
        # sendText(u"习\n近\n平")
        # sendText(u"习近 平")
        # sendText(u"习 近平")


        print "## exit browser ##"
        g_browser.quit()
# Main #
FmScrapy().main()


