# -*- coding:utf-8 -*-
from pyzbar.pyzbar import decode
from PIL import Image
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,logging

def get_seat_no(path):
    '''读取二维码的座位图片'''
    try:
        image=Image.open(path)
    except IOError:
        print('Seat Image file not existed')
        logger.debug('Seat Image file not existed')
        return 1
    else:
        arcode=decode(image)
        for code in arcode:
            url=code.data.decode('utf-8')
        print(url)
        return url

def register_card_no(url,cardno,name):
    '''无界面打开二维码里面的食堂URL，注册用户信息'''
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    #driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
    driver.get(url)
    print(driver.page_source)
    #logger.debug(driver.page_source)
    #driver.maximize_window()
    time.sleep(1)
    driver.find_element_by_xpath("//input[contains(@placeholder,'员工号 / 卡号')]").send_keys(cardno)
    time.sleep(1)
    driver.find_element_by_xpath("//input[contains(@placeholder,'姓名')]").send_keys(unicode(name,'utf-8'))
    time.sleep(1)
    #driver.find_element_by_xpath("//input[contains(@type,'checkbox')]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//div[contains(text(),'提交')]").click()
    time.sleep(1)
    try:
        driver.find_element_by_xpath("//p[contains(text(),'您的信息提交成功')]")
    except:
        print cardno+" "+name+" "+'submit failed'
        logger.debug(cardno+" name "+name+" submit failed")
        driver.close()
    else:
        print(cardno+" "+name+" "+"Submit registion successfully")
        logger.debug(cardno+" name "+name+" submit reigistion successfully")
        driver.close()

def logger():
    global logger
    logger = logging.getLogger('LunchReg')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/home/jenkins_home/mine/LunchReg.txt')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
#开始执行
logger()
logger.debug('-------现在开始注册------------------')
#配置二维码图片地址和文件名
filepath='/home/ubuntu/vivi'
files=['image.jpg','seat1.jpg','seat2.jpg']

#配置用户表位置和读取用户信息
userfiles=filepath+'/'+'user.txt'
print(userfiles)
f=open(userfiles,'r')
users=f.readlines()
userinfo={}
for i in users:
    userinfo[i.strip().split(',')[0]]=i.strip().split(',')[1]
print userinfo
logger.debug(userinfo)
#针对每一个用户随机选择位置二维码图片
choice=str(random.sample(files,1)[0])
path=filepath+'/'+choice
print(path)
logger.debug(path)
url=get_seat_no(path)
#遍历用户字典，打卡用户
if url!=1:
    for cardno in userinfo:
        print "现在注册的号码是：",cardno
        logger.debug('现在注册的号码是：'+cardno)
        print "现在注册的姓名是：",userinfo[cardno]
        logger.debug("现在注册的姓名是："+userinfo[cardno])
        register_card_no(url,cardno,userinfo[cardno])
