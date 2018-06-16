# -*- coding:utf-8 -*-
# @author jokinkuang

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

# // Hard Code //

URL_LOGIN = "https://m.weike.fm/classroom/4303270"
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


g_browser = None
g_wait = None

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


def login():
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


def sendText(text):
    global g_browser
    global g_wait

    textInput = g_browser.find_element_by_id(ID_TEXT_INPUT)
    textInput.send_keys(text)

    form = g_browser.find_element_by_tag_name(TAG_FORM);
    form.submit()

def sendImage(path):
    global g_browser
    global g_wait

    inputs = g_browser.find_elements_by_tag_name(TAG_INPUT);
    imageInput = inputs[0]
    imageInput.send_keys(path)

    form = g_browser.find_element_by_tag_name(TAG_FORM);
    form.submit()

def sendAudio(path):
    global g_browser
    global g_wait

    inputs = g_browser.find_elements_by_tag_name(TAG_INPUT);
    audioInput = inputs[1]
    audioInput.send_keys(path)

    form = g_browser.find_element_by_tag_name(TAG_FORM);
    form.submit()

g_videoMode = False
def sendVideo(path):
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
def sendFile(path):
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

def getButton(cls, text):
    global g_browser
    global g_wait

    buttons = g_browser.find_elements_by_class_name(cls)
    for button in buttons:
        if button.text == text:
            return button
    return None


# @return appNameList[], appIdList[]
def get_app_list():
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

def test():
    global g_browser
    g_browser.get("https://www.baidu.com/")
    print "https OK"

def main():
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
    login()

    sendFile("/Users/jokinkuang/Pictures/eraser.doc")
    time.sleep(15)
    sendFile("/Users/jokinkuang/Pictures/eraser.doc")
    time.sleep(15)
    sendFile("/Users/jokinkuang/Pictures/eraser.doc")

    # sendVideo("/Users/jokinkuang/Pictures/eraser.mp4")
    # sendVideo("/Users/jokinkuang/Pictures/eraser.mp4")
    # sendVideo("/Users/jokinkuang/Pictures/eraser.mp4")
    # sendAudio("/Users/jokinkuang/Pictures/eraser.mp3")
    # sendImage("/Users/jokinkuang/Pictures/eraser.jpeg")

    print "## sending text ##"
    # sendText(u"中国共产党")
    # sendText(u"毛泽东")
    # sendText(u"江泽民")
    # sendText(u"习近平")
    # sendText(u"习近\n平")
    # sendText(u"习\n近\n平")
    # sendText(u"习近 平")
    # sendText(u"习 近平")


print "## exit browser ##"
    # g_browser.quit()
# Main #
main()


