# My-test 
crm_testing

python3
https://www.python.org

unittest
https://docs.python.org/2/library/unittest.html

selenium
https://github.com/SeleniumHQ/selenium/tree/master/py

1. 请确保你已经掌握了基本的Python语法
2. 请确保你大概了解python的单元测试框架unittest
3. 请确保你大概了解基本的selenium webdriver相关api
   
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
        
   
   
   
   
## selenium webdriver简单介绍 
 
 一.selenium webdriver的特点

    1.由浏览器原生的API封装而成
    2.可以直接操作浏览器页面里的元素
    3.可以操作浏览器本身（截屏，窗口大小，启动，关闭）
    4.可以执行js代码来实现自己对浏览器的操作
    5.由于不同的浏览器厂商，对Web元素的操作和呈现多少会有一些差异，这就直接导致了Selenium WebDriver要分浏览器厂商不同，而提供不同的实现。 


二.selenium webdriver操作浏览器

    开启浏览器并打开访问网址
    from selenium import webdriver
    self.driver = webdriver.Chrome(self.chrome_driver)
    self.driver.maximize_window()
    self.driver.get(self.url)
    
    系统登录
    a.手动输入
       设置一个等待时间，然后手动输入账号、密码、验证码
    b.利用cookie
      self.driver.get(self.link)
      self.driver.add_cookie({'name': 'JSESSIONID', 'value': self.jsess})
      self.driver.add_cookie({'name': 'SPRING_SECURITY_REMEMBER_ME_COOKIE', 'value': self.security})
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

     3.模拟键盘鼠标相关操作
        from selenium.webdriver.common.action_chains import  ActionChains
        from selenium.webdriver.common.keys import Keys

        self.action = ActionChains(self.driver)
        self.action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        self.action.drag_and_drop(element, target).perform()  
     
     4.等待
       强制等待: 引入time模块,time.sleep(10) 
       隐性等待: WebDriverWait(self.driver, time).until(
                expected_conditions.presence_of_element_located((By.XPATH, localator)),要比time.sleep(10)更加智能一些。
    
     5.执行js脚本
      js='document.getElementsByClassName("reg-input reg-mobAuth")[0].disabled=false;'
      self.driver.execute_script(js)
      
     6.下拉框和iframe
      



    
























      
