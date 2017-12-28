from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


import sys,os
from datetime import datetime

curPath = os.path.abspath(os.path.dirname(__file__)).split('\\')
rootPath=curPath[0]
for i in range(1,len(curPath)):
    rootPath=rootPath+str('\\')+curPath[i]
    sys.path.append(rootPath)

from crm_test_demo.utils.config import *
from selenium.webdriver.common.by import By
from crm_test_demo.utils.log import logger
import time

class Crm():
    def __init__(self,url,jsess,security,driver):
        self.url=url
        self.jsess=jsess
        self.security=security
        self.chrome_driver=driver

    def login(self):
        self.link = "%s/satWorkbench/satWorkbench.do" % self.url
        self.driver = webdriver.Chrome(self.chrome_driver)
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)
        logger.info('CRM系统打开浏览器成功！')
        try:
            self.driver.get(self.link)
            self.driver.add_cookie({'name': 'JSESSIONID', 'value': self.jsess})
            self.driver.add_cookie({'name': 'security-cookie-user', 'value': self.security})
            self.driver.get(self.link)
        except:
            logger.exception('cookie已经过期,请更新cookie')
            raise Exception('crm登录失败')
        else:
            logger.info('crmx登录成功！')
            self.action = ActionChains(self.driver)


    def back_library(self):

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/ul/li[7]/a')))
        self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/ul/li[7]/a').click()
        time.sleep(2)
        while self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]').get_attribute('style')!='display: none;':
            time.sleep(3)
            logger.info('回库')
            self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[2]/ul/li[6]/a').click()
            self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()
            time.sleep(5)
        logger.info('机会全部回库')


    def switch_tab(self,xpath):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(2)

    def ask_upgrade(self):

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="j-askforUpBtn"]')))
            self.driver.find_element_by_xpath('//*[@id="j-askforUpBtn"]').click()
            logger.info('点击索取升级机会按钮')
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button')))
            re=self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div').text
            if re=='当前升级机会库暂无机会':
                logger.info(re)
                raise Exception('无升级机会')
            elif re=='操作成功！':
                logger.info(re)
            self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button').click()
            time.sleep(1)
            self.driver.refresh()
            time.sleep(2)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/ul/li[7]/a').click()
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/ul/li[1]')))
            mobile=self.driver.find_element_by_xpath('html/body/div[3]/div[4]/div[1]/div[3]/div[1]/ul/li').get_attribute('mobile')
            time.sleep(2)
            label_name = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/ul/li/div[3]/div[3]/div/input[2]').get_attribute('value')
            time.sleep(2)
            logger.info('索取机会%s'%mobile)
        except:
            logger.exception('索取升级机会失败！')
            raise Exception('索取升级机会失败！')
        else:
             return mobile,label_name


crmx_operation=Crm(crmx_url,crmx_jsess,crmx_security,chrome_driver)


if __name__ == '__main__':
    crmx_operation.login()
    crmx_operation.back_library()
    t= crmx_operation.ask_upgrade()
    print(t)