import sys,os
import configparser

curPath = os.path.abspath(os.path.dirname(__file__)).split('\\')
rootPath=curPath[0]
for i in range(1,len(curPath)):
    rootPath=rootPath+str('\\')+curPath[i]
    sys.path.append(rootPath)

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'Config_file.ini')
DRIVER_PATH = os.path.join(BASE_PATH, 'driver','chromedriver.exe')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'reports')

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

#运行环境
VERSION='1'

#数据库配置
db_host=config.get('db' ,'db%s_host'%VERSION)
db_username=config.get('db' , 'db%s_username'%VERSION)
db_password=config.get('db' ,'db%s_password'%VERSION)
db_highso=config.get('db' , 'db%s_highso'%VERSION)

#end,www官网,crmx配置
end_url = config.get('end', 't%s' % VERSION)
www_url = config.get('front', 'w%s' % VERSION)
crmx_url=config.get('crm','c%s'%VERSION)

crmx_jsess=config.get('cookie', 'crm%s_JSESSIONID' % VERSION)
crmx_security=config.get('cookie', 'crm%s_security-cookie-user' % VERSION)

end_jsess = config.get('cookie', 't%s_JSESSIONID' % VERSION)
end_security = config.get('cookie', 't%s_SPRING_SECURITY_REMEMBER_ME_COOKIE' % VERSION)

#邮件配置
receiver=config.get('mail','receiver')
server=config.get('mail','server')
sender=config.get('mail','sender')
password=config.get('mail','password')
report = REPORT_PATH
#浏览器驱动
chrome_driver=DRIVER_PATH









if __name__ == '__main__':
    # print(BASE_PATH)
    # print(config.get('log','file_name'))
    # print(db_highso)
    # print(db_host)
    # print(db_username)
    # print(db_password)
    # print(end_url)
    # print(www_url)
    # print(crmx_url)

    print(server)
    print(receiver)
    print(sender)
    print(password)
    print(crmx_jsess)
    print(crmx_security)
    print(crmx_url)


