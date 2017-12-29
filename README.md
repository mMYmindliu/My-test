# My-test 


python3
https://www.python.org

unittest
https://docs.python.org/2/library/unittest.html

selenium
http://selenium-python-zh.readthedocs.io/en/latest/index.html
   
## 轻量级自动化测试框架目录结构

    CRM_UI_Test
    |--config（配置文件）
    |--driver（驱动）
    |--log（日志）
    |--reports（报告）
    |--test_collections（测试集）
    |--src（业务流程方法）
    |--utils（公共方法）
    |--ReadMe.md（说明文件）
        
   
   
   
   
 
 
一.selenium webdriver的特点

    1.由浏览器原生的API封装而成
    2.可以直接操作浏览器页面里的元素
    3.可以操作浏览器本身（截屏，窗口大小，启动，关闭）
    3.可以执行js代码来实现自己对浏览器的操作
    3.由于不同的浏览器厂商，对Web元素的操作和呈现多少会有一些差异，这就直接导致了Selenium WebDriver要分浏览器厂商不同，而提供不同的实现。 

二.selenium webdriver操作浏览器

    1.开启和关闭浏览器、打开访问网址
    from selenium import webdriver
    self.driver = webdriver.Chrome(self.chrome_driver)
    self.driver.maximize_window()
    self.driver.get(self.url)
    self.driver.quit()
    
    2.系统登录
        a.手动输入
           设置一个等待时间，然后手动输入账号、密码、验证码
        b.利用cookie
          self.driver.get(self.link)
          self.driver.add_cookie({'name': 'JSESSIONID', 'value': self.jsess})
          self.driver.add_cookie({'name': 'SPRING_SECURITY_REMEMBER_ME_COOKIE', 'value': self.security})
          self.driver.refresh()
        c.图像识别
         第三方库：
             PIL : Pillow-3.3.0-cp27-cp27m-win_amd64.whl
             Pytesser：依赖于PIL ，Tesseract 了解pytesser及基本使用
             Tesseract
           self.driver.get_screenshot_as_file('C:\Users\MrLevo\image1.jpg') #对验证码进行区域截图
           im=Image.open("C:\Users\MrLevo\image1.jpg")
           imgry = im.convert('L')#图像加强，二值化
           sharpness =ImageEnhance.Contrast(imgry)#对比度增强
           sharp_img = sharpness.enhance(2.0)
           sharp_img.save("C:\Users\split\image1.jpg")
           code= pytesser.image_file_to_string("C:\Users\split\image1.jpg")#code即为识别出的图片数字str类型
     
    3.元素定位及其相关操作
        self.driver.find_element_by_id()  通过id定位
        self.driver.find_element_by_name()  通过name 定位
        self.driver.find_element_by_xpath() 通过xpath定位
        self.driver.find_element_by_className() 通过className定位
        self.driver.find_element_by_CSS () 通过CSS 定位
        self.driver.find_element_by_link_text() 通过linkText
                 .............
        http://www.w3school.com.cn/tags/tag_html.asp
        http://www.w3school.com.cn/xpath/xpath_syntax.asp
        
        result = self.driver.find_element_by_xpath('').text #获取元素的文本
        result = self.driver.find_element_by_xpath('').get_attribute(name) #获得属性值
        result = self.driver.find_element_by_xpath('').is_displayed() #检查该元素是否用户可见

        点击（鼠标左键）页面按钮：self.driver.find_element_by_xpath('').click()
        清空输入框：self.driver.find_element_by_xpath('').clear()
        输入字符串：self.driver.find_element_by_xpath('').send_keys('admin')
      
    4.模拟键盘鼠标相关操作
       from selenium.webdriver.common.action_chains import  ActionChains
       from selenium.webdriver.common.keys import Keys

       self.action = ActionChains(self.driver)
       self.action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
       self.action.drag_and_drop(element, target).perform()
    
    5.等待
       强制等待: 引入time模块,time.sleep(10) 
       隐性等待: WebDriverWait(self.driver, time).until(
                expected_conditions.presence_of_element_located((By.XPATH, localator)),要比time.sleep(10)更加智能一些。             
    
    6.执行js脚本
      js='document.getElementsByClassName("reg-input reg-mobAuth")[0].disabled=false;'
      self.driver.execute_script(js)
      
    7.下拉框和iframe的处理
    
        下拉框
                   <select name="levelTwo" id="levelTwoId">
	                    <option value="3" selected="selected">会计从业资格</option>
						<option value="5">司法考试</option>
						<option value="7">注册会计师</option>
				        <option value="9">一级建造师</option>
						<option value="12">经济师</option>
						<option value="14">初级会计职称</option>
					    <option value="15">中级会计职称</option>
						<option value="16">二级建造师</option>					
					</select>
        
        
        from selenium.webdriver.support.select import Select
        
        s1 = Select(self.driver.find_element_by_id('levelTwoId'))
        s1.select_by_visible_text(parent_category)
        
        iframe
                 <iframe name="main-iframe" id="main-iframe" width="100%" height="auto" scrolling="Auto" 
                    frameborder="0" allowtransparency="true" src="/user/findAll.do" style="height: 336px;"></iframe>
    
        先进入，然后才能对iframe下的元素进行操作
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="main-iframe"]'))
        最后一定要出来，不然是找不到在iframe之外的元素
        self.driver.switch_to.default_content()

三.unittest单元测试框架
        
      unittest原名为PyUnit，是由java的JUnit衍生而来。对于单元测试，需要设置预先条件，对比预期结果和实际结果。  
      
      1.编写一个python类，继承 unittest模块中的TestCase类，这就是一个测试类。每个测试方法均以 test 开头，否则是不被unittest识别的。
            
            import unittest
            from crm_test_demo import cal
     
            class CalTest(unittest.TestCase):
            
                def testA(self):
                    expected = 6
                    result = cal(2,4)
                    self.assertEqual(expected,result)
        
                def testB(self):
                    expected = 0
                    result = cal(2,1)
                    self.assertEqual(expected,result)

      2.常用断言方法
            
            assertEqual(a,b [,msg])   检测a==b,这个方法检查a是否等于b
            assertNotEqual(a, b)      判断a！=b
            assertTrue(x)    bool(x) is True
            assertFalse(x)    bool(x) is False            
            assertIs(a, b)     a is b            
            assertIsNot(a, b)   a is not b            
            assertIsNone(x)     x is None            
            assertIsNotNone(x)   x is not None            
            assertIn(a, b)        a in b            
            assertNotIn(a, b)      a not in b
              ..........

      3.测试前准备环境，执行完之后清理环境

            class TestMathFunc(unittest.TestCase):
                """Test mathfuc.py"""
            
                @classmethod
                def setUpClass(cls):       #类方法，开始执行测试时会首先执行setUpClass
                
                
                @classmethod
                def tearDownClass(cls):    #类方法，执行测试结束时会最后执行setUpClass
                
          
                def setUp(self):
                    print "do something before test.Prepare environment."  #每次执行测试方法开始前会执行setUp
            
                def tearDown(self):
                    print "do something after test.Clean up."     #每次执行测试方法结束时会执行setUp

                def testA(self):
                    expected = 6
                    result = cal(2,4)
                    self.assertEqual(expected,result)
        
                def testB(self):
                    expected = 0
                    result = cal(2,1)
                    self.assertEqual(expected,result)

      4.组织测试代码
           
           widgetTestSuite = unittest.TestSuite() #创建一个测试套件实例
           widgetTestSuite.addTest(WidgetTestCase('test_default_size')) #添加测试用例到套件，抽取WidgetTestCase类中的test_default_size测试用例添加到testsuite
           widgetTestSuite.addTest(WidgetTestCase('test_resize'))  #添加测试用例到套件，抽取WidgetTestCase类中的test_resize测试用例添加到testsuite

           #此用法可以同时测试多个类
           suite1 = unittest.TestLoader().loadTestsFromTestCase(TestCase1) 
           suite2 = unittest.TestLoader().loadTestsFromTestCase(TestCase2) 
           suite = unittest.TestSuite([suite1, suite2]) 
           

      5.使用HTMLTestRunner生成报告
        
           import HTMLTestRunner
           
           filename=str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
            with open(os.path.join(REPORT_PATH,'%s.html'%filename), 'wb') as f:
                runner = HTMLTestRunner(f, verbosity=2, title='CRM系统测试报告', description='执行人：刘志文')
                runner.run(suite)
      
      







      
