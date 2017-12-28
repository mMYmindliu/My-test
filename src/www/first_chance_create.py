from selenium import webdriver
import time
import pymysql
from crm_test_demo.utils.config import *
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import requests
from crm_test_demo.utils.log import logger


class Register():

    def __init__(self,url,Version,host,user,password,db_highso,driver):
        self.w_url=url
        self.version=Version
        self.host = host
        self.user = user
        self.password = password
        self.db_highso = db_highso
        self.chrome_driver=driver

    def assert_element(self,xpath=None,id=None,class_name=None):

        if xpath !=None:
            try :
                self.driver.find_element_by_xpath(xpath)
            except Exception :
                return False
            else:
                return True
        elif id !=None :
            try :
                self.driver.find_element_by_id(id)
            except Exception :
                return False
            else:
                return True
        elif class_name !=None :
            try :
                self.driver.find_element_by_class_name(class_name)
            except Exception :
                return False
            else:
                return True

    def get_code(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        port=3306,
                                        user=self.user,
                                        passwd=self.password,
                                        db=self.db_highso,
                                        charset='utf8')
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

            sql='SELECT code FROM `universalcode` where openingDate =\'%s\''
            self.cursor.execute(sql%str(datetime.now().strftime('%Y-%m-%d')))
            date = self.cursor.fetchall()[0]['code']
            logger.info('万能验证码%s'%date)
            return date
        except:
            logger.exception('数据库连接失败!')
            raise Exception
        finally:
            self.cursor.close()
            self.conn.close()

    def open(self):
        try:
            self.driver = webdriver.Chrome(self.chrome_driver)
            self.driver.maximize_window()
            self.action = ActionChains(self.driver)
            self.driver.get(self.w_url)
            logger.info('打开浏览器成功！')
        except:
            logger.exception('打开浏览器失败！')

    def register(self,code):
        '''
        此函数用于注册机会；
        :num: 注册机会个数
        code: 验证码
        '''

        try:
                self.driver.get(self.w_url+'/customerRegister/showRegister.do')
                email = '877%s@qq.com'%str(time.time())[5:10]
                mobile= '158995%s'%str(time.time())[5:10]
                self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(email)
                self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
                self.driver.find_element_by_xpath('//*[@id="mobile"]').send_keys(mobile)
                js='document.getElementsByClassName("reg-input reg-mobAuth")[0].disabled=false;'
                self.driver.execute_script(js)
                self.driver.find_element_by_xpath('//*[@id="mobileAuthCode"]').send_keys(code)
                time.sleep(0.7)
                self.driver.find_element_by_xpath('//*[@id="registerForm"]/div[8]/div/a[1]').click()
                self.driver.find_element_by_xpath('//*[@id="doneBtn"]').click()
                logger.info('注册机会:%s'%mobile)
        except:
            logger.exception('注册失败！')
            raise Exception
        else:
            return mobile


    def judge_button(self,goodId):
        '''
        判断购买按钮存在；
        :goodId：商品id  45851
        '''

        try:
            self.driver.get(self.w_url)
            link = '%s/goods/info.do?goodsId=%s' % (self.w_url,goodId)
            self.driver.get(link)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/h4')))
            if self.assert_element(xpath='/html/body/div[2]/h3/a'):
                if self.driver.find_element_by_xpath('/html/body/div[2]/h3/a').text != '购买课程':
                    logger.info('不可以下单，需要换商品')
                    raise Exception
                else:
                    logger.info('可以下单')

            elif self.assert_element(xpath='/html/body/div[2]/h3/span[2]'):
                logger.info('商品只有金额，无法点击购买')
                raise Exception
        except:
            logger.exception('购买按钮有问题')
            raise Exception




    def create_order(self):
        '''
        此函数用创建订单；
        :mobile:手机号
        :goodId：商品id  45851
        '''
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/h3/a')))
            self.driver.find_element_by_xpath('/html/body/div[2]/h3/a').click()
            time.sleep(2)
            if self.assert_element(xpath='//*[@id="address-layout"]/div[1]/h2') and self.driver.find_element_by_xpath(
                    '//*[@id="address-layout"]/div[1]/h2').text == '确认收货地址':
                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id="add-new-address-only"]').click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="address-form"]/div[1]/div/input')))

                self.driver.find_element_by_xpath('//*[@id="address-form"]/div[1]/div/input').send_keys('liuzhiwen')
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'provinceId')))
                time.sleep(3)
                Select(self.driver.find_element_by_id('provinceId')).select_by_visible_text('北京市')
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'cityId')))
                time.sleep(3)
                Select(self.driver.find_element_by_id('cityId')).select_by_visible_text('北京辖区')
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'townId')))
                time.sleep(3)
                Select(self.driver.find_element_by_id('townId')).select_by_visible_text('东城区')
                self.driver.find_element_by_xpath('//*[@id="address-form"]/div[3]/div/input').send_keys('中南海')
                time.sleep(3)
                self.driver.find_element_by_xpath('//*[@id="address-form"]/div[4]/div/input').send_keys('100017')
                self.driver.find_element_by_xpath('//*[@id="address-form"]/div[5]/div/input').send_keys('15708487553')
                self.driver.find_element_by_xpath('//*[@id="address-save"]').click()
            self.driver.find_element_by_xpath('//*[@id="submitBtnContract"]').click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="orderonline"]')))
            orderNum = self.driver.find_element_by_xpath('//*[@id="orderonline"]').text
        except:
            logger.exception('下单失败')
            self.driver.get(self.w_url)
        else:
            logger.info('下单成功')
            return orderNum

haixue_operation=Register(www_url,VERSION,db_host,db_username,db_password,db_highso,chrome_driver)




if __name__ == '__main__':
    haixue_operation.open()

    list=haixue_operation.register(haixue_operation.get_code())
    # haixue_operation.judge_button(45851)
    # haixue_operation.create_order()
