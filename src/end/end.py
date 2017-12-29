from selenium import webdriver
import time
from crm_test_demo.utils.config import *
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from crm_test_demo.utils.log import logger


class Operation_end():

    def __init__(self,url,driver):
        self.url = url
        self.chrome_driver = driver


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




    def login(self):

        self.driver = webdriver.Chrome(self.chrome_driver)
        self.driver.maximize_window()
        self.link = '%s/login/index.do' % self.url
        logger.info('end系统打开浏览器成功！')
        self.driver.get(self.link)
        self.driver.find_element_by_xpath('//*[@id="j_username"]').send_keys('liuzhiwen')
        self.driver.find_element_by_xpath('//*[@id="j_password"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="captchaHolder"]').click()
        time.sleep(6)
        self.driver.find_element_by_xpath('//*[@id="logBtn"]').click()
        self.action = ActionChains(self.driver)
        self.action.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
        logger.info('end登录成功！')

  

    def run_modify(self, mobile):
        '''
        此函数用于重置用户密码。
        :mobile: 手机号
        '''
        try:
            global result
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[2]/div[2]/h2')
            except:
                self.driver.find_element_by_xpath('//*[@id="quick"]/li[3]/a/span').click()
            else:
                self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[1]/div/ul/li[3]/a').click()
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="main-iframe"]'))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/a[1]')))
            self.driver.find_element_by_xpath('//*[@id="customer.mobile_string_rlike"]').send_keys(mobile)
            self.action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

            # 点击修改的button存在否
            self.driver.find_element_by_xpath('//*[@id="listDataTable"]/tbody/tr/td[9]/a[4]').click()
            # 点击弹窗确认
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()
            self.driver.switch_to.default_content()
            logger.info('重置密码成功')
            result = True
        except:
            logger.exception('重置密码失败')
            result = False
            raise Exception('重置密码失败')
        finally:
            return result





    def modify_first_chance(self,parent_category,child_category):
        '''
        此函数用于修改首咨的索取上限；
        通过修改数据库数据的方式不能改变坐席首咨索取上限，所以还需在end系统的新分配规则点击保存。
        :parent_category: 坐席所属父项目
        :child_category: 坐席所属子项目
        '''
        try:
            time.sleep(2)
            try:
                self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[2]/div[2]/h2')
            except:
                self.driver.find_element_by_xpath('//*[@id="quick"]/li[10]/a/span').click()
            else:
                self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[1]/div/ul/li[15]').click()
            self.driver.find_element_by_xpath('//*[@id="CRM"]/ul/li[19]/a').click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-iframe"]')))
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="main-iframe"]'))
            s1 = Select(self.driver.find_element_by_id('levelTwoId'))
            s1.select_by_visible_text(parent_category)
            time.sleep(2)
            s2 = Select(self.driver.find_element_by_id('levelThree'))
            s2.select_by_visible_text(child_category)
            self.driver.find_element_by_xpath('//*[@id="form1"]/div[3]/input').click()
            logger.info('修改首咨的索取上限成功！')
            self.driver.switch_to.default_content()
        except:
            logger.exception('修改首咨的索取上限失败！')
            raise Exception('修改首咨的索取上限失败！')



    def activate_order(self,order_num):

        '''
        此函数用于激活订单；
        :order_num: 订单号
        '''
        try:
            time.sleep(2)
            try:
                global re
                self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[2]/div[2]/h2')
            except:
                self.driver.find_element_by_xpath('//*[@id="quick"]/li[4]/a/span').click()
            else:
                self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[1]/div/ul/li[5]').click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-iframe"]')))
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="main-iframe"]'))
            if 't0.highso' in self.driver.current_url:
                self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/a[4]').click()
            else:
                self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/a[3]').click()
            self.driver.find_element_by_xpath('//*[@id="orderNo"]').send_keys(order_num)
            if 't0.highso' in self.driver.current_url:
                time.sleep(5)
            else:
                time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="payTime"]').send_keys(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div/form/table/tbody/tr[6]/td/textarea').send_keys('aaa')
            self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/div/h4')))
            self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()
            self.driver.switch_to.default_content()
            logger.info('激活订单%s'%order_num)
            re = True
        except:
            logger.exception('激活订单%s失败'%order_num)
            re = False
        finally:
            return re


    def bole(self,mobile):
        '''
        此函数用于产生伯乐订单；
        :mobile_list: 电话号码列表
        '''
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[2]/div[2]/h2')
        except:
            self.driver.find_element_by_xpath('//*[@id="quick"]/li[10]/a/span').click()
        else:
            self.driver.find_element_by_xpath('//*[@id="main-index-con"]/div[1]/div/ul/li[15]').click()

        if 't0' in self.driver.current_url:
            WebDriverWait(self.duriver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CRM"]/ul/li[24]')))
            self.driver.find_element_by_xpath('//*[@id="CRM"]/ul/li[24]').click()
        else:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CRM"]/ul/li[25]')))
            self.driver.find_element_by_xpath('//*[@id="CRM"]/ul/li[25]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-iframe"]')))
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="main-iframe"]'))


        if 't0' in self.driver.current_url:
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[2]/form/table[1]/tbody/tr[2]/td/span/input[1]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[3]/div/ul/li[4]/div/span[1]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[3]/div/ul/li[4]/ul/li[1]/div/span[4]/span').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[2]/form/table[1]/tbody/tr[3]/td/span/input[1]   ').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[5]/div/ul/li[2]/div/span[1]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[5]/div/ul/li[2]/ul/li[1]/div/span[4]/span').click()
                self.driver.find_element_by_xpath('/html/body/div[2]/form/table[2]/tbody/tr[2]/td/label/input').click()
        else:
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[2]/form/table[1]/tbody/tr[2]/td/span/input[1]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[3]/div/ul/li[2]/div/span[1]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[3]/div/ul/li[2]/ul/li[1]/div/span[4]/span   ').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[2]/form/table[1]/tbody/tr[3]/td/span/input[1]   ').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[5]/div/ul/li[2]/div/span[1]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[5]/div/ul/li[2]/ul/li[1]/div/span[4]/span').click()
        if isinstance(mobile,list):
            for i in mobile:
                    try:
                        self.driver.find_element_by_xpath('//*[@id="mobile"]').send_keys(i)
                        time.sleep(1)
                        self.driver.find_element_by_xpath('//*[@id="comfireBtn"]').click()
                        time.sleep(1)
                        self.driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button').click()
                        self.driver.find_element_by_xpath('//*[@id="mobile"]').clear()
                        logger.info('生成伯乐机会%s'%i)
                    except:
                        logger.exception('生成伯乐机会%s失败'%i)
                        self.action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
                        self.driver.find_element_by_xpath('//*[@id="mobile"]').clear()
                        time.sleep(0.5)
        else:
            try:
                self.driver.find_element_by_xpath('//*[@id="mobile"]').send_keys(mobile)
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="comfireBtn"]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button').click()
                self.driver.find_element_by_xpath('//*[@id="mobile"]').clear()
                logger.info('生成伯乐机会%s'% mobile)
            except:
                logger.exception('生成伯乐机会%s失败'%mobile)
                self.action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
                self.driver.find_element_by_xpath('//*[@id="mobile"]').clear()
                time.sleep(0.5)

operate_end=Operation_end(end_url,chrome_driver)


if __name__ == '__main__':
        pass

    
