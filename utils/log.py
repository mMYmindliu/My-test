import logging
from logging.handlers import TimedRotatingFileHandler
import sys,os

curPath = os.path.abspath(os.path.dirname(__file__)).split('\\')
rootPath=curPath[0]
for i in range(1,len(curPath)):
    rootPath=rootPath+str('\\')+curPath[i]
    sys.path.append(rootPath)

from crm_test_demo.utils.config import *


class Logger():
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)

        self.log_file_name = 'test.log'  # 日志文件
        self.backup_count = 5
        # 日志输出级别
        self.console_output_level =  'INFO'
        self.file_output_level = 'DEBUG'
        # 日志输出格式
        pattern = '%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
        两个句柄的日志级别不同，在配置文件中可设置。
        """
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)


            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='M',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()
if __name__ == '__main__':

    logger.debug('where are you from?')
    logger.error('who are you?')
    logger.warning('what do you want?')
    logger.info('sorry,i can\'t understand what you said')
    logger.info('please,pardon!!!')

