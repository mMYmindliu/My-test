import sys,os
from datetime import datetime

curPath = os.path.abspath(os.path.dirname(__file__)).split('\\')
rootPath=curPath[0]
for i in range(1,len(curPath)):
    rootPath=rootPath+str('\\')+curPath[i]
    sys.path.append(rootPath)

from crm_test_demo.test_collections.test_suite_01.test_crm_01 import CRM_Test_Case
import unittest
from crm_test_demo.utils.mail import Email
from crm_test_demo.utils.config import *
from crm_test_demo.utils.HTMLTestRunner_PY3 import HTMLTestRunner







if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CRM_Test_Case("test_1"))
    suite.addTest(CRM_Test_Case("test_2"))
    suite.addTest(CRM_Test_Case("test_3"))
    suite.addTest(CRM_Test_Case("test_4"))
    filename=str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

    with open(os.path.join(REPORT_PATH,'%s.html'%filename), 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='CRM系统测试报告', description='执行人：刘志文')
        runner.run(suite)


    email = Email(title='自动化demo测试报告',
                  message='这是今天的测试报告，请查收！',
                  receiver=receiver,
                  server=server,
                  sender=sender,
                  password=password,
                  path=os.path.join(REPORT_PATH,'%s.html'%filename)
                  )
    email.send()


