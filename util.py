from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
import random
import string
import base64
import yaml
import os
import log

def mkdir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def init_webdriver() :
    options = webdriver.ChromeOptions()
    # 브라우저 꺼짐 방지
    options.add_experimental_option('detach', True)
    # 불필요한 에러 메시지 없애기
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(r"./driver/chromedriver.exe", options=options)
    driver.maximize_window()
    return driver

def input_clipboard_with_xpath(xpath, input, driver):
    tmp = pyperclip.paste()  # 사용자 클립보드를 따로 저장

    pyperclip.copy(input)
    driver.find_element(By.XPATH, xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    pyperclip.copy(tmp)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
    time.sleep(1)

def base64_encoding(key):
    # b64 변환을 위해선 bytes type을 사용해야 함.
    # str -> bytes -> b64 encode -> str
    key_bytes = key.encode('ascii')
    key_b64 = base64.b64encode(key_bytes)
    key_b64_bytes = key_b64.decode('ascii')
    return key_b64_bytes

def base64_decoding(key):
    # b64 변환을 위해선 bytes type을 사용해야 함.
    # b64 decode -> str
    key_bytes = base64.b64decode(key)
    ret = key_bytes.decode('ascii')
    return ret

def base64_encoding_important_info(key):
    new_str = key
    # 짝수 인덱스 뽑기
    str = key[1::2]
    
    # 짝수 인덱스 random 문자로 치환
    for idx in range(1, len(key), 2):
        ranch = random.choice(string.ascii_letters + string.digits) 
        new_str = new_str[:idx] + ranch + new_str[idx+1:]
        
    # 새로만든 문자 b64 encoding
    full_str = new_str + str
    ret = base64_encoding(full_str)
    return ret

def base64_decoding_important_info(key):
    # b64 decoding
    str = base64_decoding(key)

    # original string index 구하기
    org_index = len(str) // 3
    org_str = str[-org_index:]
    new_str = str[:-org_index]

    # random 문자를 original 문자로 치환
    i = 0
    for idx in range(1, len(new_str), 2):
        new_str = new_str[:idx] + org_str[i] + new_str[idx+1:]
        i += 1

    return new_str

class app_conf:
    def __init__(self, app, file_path, logger):
        self.application = app
        self.logger = logger
        self.load_yml_conf_file(file_path)
        self.print_yml_conf_file_console()
        self.print_yml_conf_file_log()

    def load_yml_conf_file(self, file_path):
        with open(file_path, encoding='UTF-8') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)

            self.uri = conf['uri']

            self.id = base64_decoding_important_info(conf['login_info']['id'])
            self.pwd = base64_decoding_important_info(conf['login_info']['pwd'])

            self.to = conf['recv']['to']
            self.cc = conf['recv']['cc']
            self.bcc = conf['recv']['bcc']

            self.subject = conf['body_info']['subject']
            self.attach = conf['body_info']['attach']
            self.content = conf['body_info']['content']
            self.file_path = os.path.dirname(os.path.realpath(__file__))+'\\attach'

    def print_yml_conf_file_console(self):
        print ('======================================')
        print (self.application.center(38))
        print ('======================================')
        print ('uri(str) : ', self.uri)

        print ('<< login_info >>')
        print ('id(str) : ', base64_encoding_important_info(self.id))
        print ('pwd(str) : ', base64_encoding_important_info(self.pwd))
        
        print ('<< recv >>')
        print ('to(list) : ', self.to)
        print ('cc(list) : ', self.cc)
        print ('bcc(list) : ', self.bcc)

        print ('<< body_info >>')
        print ('subject(str) : ', self.subject)
        print ('attach(list) : ', self.attach)
        print ('content(str) : ', self.content)
        print ('file_path(str) : ', self.file_path)
        print ('======================================')

    def print_yml_conf_file_log(self):
        self.logger.info('======================================')
        self.logger.info(str(self.application.center(38)))
        self.logger.info('======================================')
        self.logger.info('uri(str) : ' + self.uri)

        self.logger.info('<< login_info >>')
        self.logger.info('id(str) : ' + base64_encoding_important_info(self.id))
        self.logger.info('pwd(str) : ' + base64_encoding_important_info(self.pwd))
        
        self.logger.info('<< recv >>')
        self.logger.info('to(list) : ' + str(self.to))
        self.logger.info('cc(list) : ' + str(self.cc))
        self.logger.info('bcc(list) : ' + str(self.bcc))

        self.logger.info('<< body_info >>')
        self.logger.info('subject(str) : ' + self.subject)
        self.logger.info('attach(list) : ' + str(self.attach))
        self.logger.info('content(str) : ' + self.content)
        self.logger.info('file_path(str) : ' + self.file_path)
        self.logger.info('======================================')
        
class run_conf:
    def __init__(self, file_path, logger):
        self.logger = logger
        self.load_yml_conf_file(file_path)
        self.print_yml_conf_file_console()
        self.print_yml_conf_file_log()
    
    def load_yml_conf_file(self, file_path):
        with open(file_path, encoding='UTF-8') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)

            self.repeat = conf['repeat']
            self.running = conf['running']

    def print_yml_conf_file_console(self):
        print ('======================================')
        print ('running'.center(38))
        print ('======================================')
        print ('repeat(int) : ', self.repeat)
        print ('running : ', self.running)
        print ('======================================')

    def print_yml_conf_file_log(self):
        self.logger.info('======================================')
        self.logger.info('running'.center(38))
        self.logger.info('======================================')
        self.logger.info('repeat(int) : ' + str(self.repeat))
        self.logger.info('running : ' + str(self.running))
        self.logger.info('======================================')