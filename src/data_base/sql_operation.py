import pymysql
from crm_test_demo.utils.config import *
from crm_test_demo.utils.log import logger

class SQL_first_chance():
    def __init__(self,host,user,password,db):
        self.host=host
        self.user=user
        self.password=password
        self.db=db

    def connect_sql(self):

        try:

            self.conn = pymysql.connect(host=self.host,
                                        port=3306,
                                        user=self.user,
                                        passwd=self.password,
                                        db=self.db,
                                        charset='utf8')
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logger.info('连接数据成功！')
        except:
            logger.exception('连接数据库失败！')
            raise Exception('连接数据库失败！')

    def first_chance(self,num,categoryid,user_catergory):

        try:
            sql = 'UPDATE crmchanceaskforrule ' \
                  'set extraLevelOne ='+num+',normalLevelTwo='+num+',extraLevelTwo='+num+',normalLevelThree='+num+',extraLevelThree='+num+',normalLevelOne='+num+' where  categoryId=\'%s\' and usedCategoryId=\'%s\''
            self.cursor.execute(sql % (categoryid,user_catergory))
            self.conn.commit()
        except:
            logger.exception('更新首咨索取配置失败')
            self.conn.rollback()
            raise Exception
        finally:
            self.cursor.close()
            self.conn.close()


    def delete(self,userId,category):

        sql_1 = 'SELECT label_id FROM crm_label_chance_ask_for_rule where user_id=\'%s\' and user_category_id=\'%s\''
        sql_2 = 'delete from crm_label_chance_ask_for_rule where user_id=\'%s\' and user_category_id=\'%s\''
        re = self.cursor.execute(sql_1 % (userId, category))
        try:
            if re!=0:
                logger.info('已经配置升级机会上限，需重置')
                self.cursor.execute(sql_2 % (userId, category))
                self.conn.commit()
            else:
                logger.info('需配置升级机会索取上限')
        except:
            logger.exception('删除升级机会上限失败')
            self.conn.rollback()



    def update_chance(self,userId,user_category_id,pa_category_id,count,label_id):

        try:
            sql_3 = 'INSERT INTO crm_label_chance_ask_for_rule (label_id,user_id,count,category_id,user_category_id,create_date)  ' \
                    'VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'2017-09-18 10:57:22\')'
            self.cursor.execute(sql_3 % (label_id,userId,count,pa_category_id,user_category_id))
            self.conn.commit()
            logger.info('配置升级机会上限:坐席%s,标签%s,个数为%s'%(userId,label_id,count))
        except:
            logger.exception('插入升级机会上限失败')
            self.conn.rollback()



    def find_upgrade(self,mobile):

        try:
            sql = 'SELECT crmupgradechancepolling.labelId FROM `crmupgradechancepolling` ' \
                      'join crmchance on crmchance.id=crmupgradechancepolling.crmChanceId ' \
                      'join crmcustomer on crmchance.crmCustomerId=crmcustomer.id ' \
                      'where crmcustomer.mobile=%s'
            self.cursor.execute(sql% (mobile))
            result=self.cursor.fetchall()
            print(result)
            logger.info('产生的标签为%s'%result)
        except:
            logger.exception('查询升级机会的标签失败')
        else:
            return result

    def find_label(self,mobile):

        try:
            sql = 'SELECT crm_label_chance.label_id FROM `crm_label_chance` ' \
                      'join crmchance on crmchance.id=crm_label_chance.chance_id ' \
                      'join crmcustomer on crmchance.crmCustomerId=crmcustomer.id ' \
                      'where crmcustomer.mobile=%s  order BY crm_label_chance.gmt_modified DESC limit 1'
            self.cursor.execute(sql% (mobile))
            result=self.cursor.fetchall()
            logger.info('产生的标签为%s'%result)
        except:
            logger.exception('查询升级机会的标签失败')
        else:
            return result






sql=SQL_first_chance(db_host,db_username,db_password,db_highso)

if __name__ == '__main__':

   pass
