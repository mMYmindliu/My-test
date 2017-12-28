import time
import unittest
from crm_test_demo.src.end.end import operate_end
from crm_test_demo.src.crmx.crmx import crmx_operation
from crm_test_demo.src.www.first_chance_create import haixue_operation
from crm_test_demo.src.data_base.sql_operation import sql
from crm_test_demo.utils.config import *
from crm_test_demo.utils.log import logger



class CRM_Test_Case(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.sql=sql
        cls.sql.connect_sql()
        cls.sql.delete(115577, 100051)
        cls.sql.update_chance(115577, 100051, 9, 250, 13)
        cls.sql.update_chance(115577, 100051, 9, 250, 15)

        cls.crm = crmx_operation
        cls.crm.login()

        cls.end = operate_end
        cls.end.login()

        cls.data={}



    @classmethod
    def tearDownClass(cls):

        sql.cursor.close()
        operate_end.driver.quit()
        crmx_operation.driver.quit()
        # haixue_operation.driver.quit()


    def tearDown(self):
        self.end.initial_login()
        self.crm.driver.get(crmx_url)
        logger.info('data:%s'%self.data)


    def test_1(self):
        """创建升级机会测试"""
        haixue_operation.open()
        self.mobile=haixue_operation.register(haixue_operation.get_code())
        self.data['mobile_list']=[self.mobile]
        haixue_operation.judge_button(45851)
        self.end.activate_order(haixue_operation.create_order())
        time.sleep(8)
        num=self.sql.find_upgrade(str(self.mobile))
        self.assertIsNotNone(num,'数据无数据或者相关服务没启动？')

    def test_2(self):
        """升级机会索取上限测试"""
        num=self.crm.driver.find_element_by_xpath('//*[@id="numOfLimt"]').text
        logger.info('索取上限为%s'%num)
        self.assertEqual(num,'500')

    def test_3(self):
        """索取升级机会测试"""
        crmx_operation.back_library()
        t = crmx_operation.ask_upgrade()
        self.data['ask_upgrade']=t
        self.assertIsNotNone(t)

    def test_4(self):
        """坐席名下机会标签升级测试"""
        self.end.bole(self.data['ask_upgrade'][0])
        time.sleep(4)
        label_Id = self.sql.find_label(self.data['ask_upgrade'][0])
        self.crm.switch_tab('/html/body/div[3]/div[4]/ul/li[7]/a')
        new_label=self.crm.driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/ul/li/div[3]/div[3]/div/input[2]').get_attribute('value')
        self.assertEqual(label_Id[0]['label_id'],11,)
        self.assertEqual(self.data['ask_upgrade'][1],new_label)

if __name__ == '__main__':
    unittest.main()