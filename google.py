from util import input_clipboard_with_xpath
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from util import *

class google_mail_send(app_conf):
    def __init__(self, app, file_path, logger):
        super().__init__(app, file_path, logger)

        # 필요한 계정, 메일 내용 정보 저장
        '''
        self.uri = 'https://www.google.com'
        self.account = {
            "id" : 'seojaehyun12',
            "pwd" : 'ghswjfrkt12'
        }
        self.recv = {
            "to" : [ "seojaehyun2@nate.com", "seojaehyun12@google.com", "wogus123001@gmail.com" ],
            "cc" : [ "seojaehyun2@nate.com", "seojaehyun12@google.com", "wogus123001@gmail.com" ],
            "bcc" : [ "seojaehyun2@nate.com", "seojaehyun12@google.com", "wogus123001@gmail.com" ],
        }
        self.body = {
            "subject" : "테스트 메일 쓰기 !!",
            "content" : "본문!!",
            "filepath" : os.path.dirname(os.path.realpath(__file__))+'\\attach',
            "attach" : [ "06_26.docx", "test1.mp4" ]
        }
        '''

        # 필요한 xpath 저장
        self.loginXpath = '//*[@id="account"]/a'
        self.idXpath = '//*[@id="id"]'
        self.pwdXpath = '//*[@id="pw"]'
        self.okXpath = '//*[@id="log.login"]'
        self.mailXpath = '///*[@id="gb"]/div[2]/div[3]/div[1]/div/div[1]/a'
        self.mailWriteXpath = '//*[@id="nav_snb"]/div[1]/a[1]/strong'
        self.toXpath = '//*[@id="toInput"]'
        self.ccXpath = '//*[@id="ccInput"]'
        self.bcclistXpath = '//*[@id="divWrite"]/table/tbody/tr[2]/th/a'
        self.bccXpath = '//*[@id="bccInput"]'
        self.subjectXpath = '//*[@id="subject"]'
        self.bodyIframe = '//*[@id="se2_iframe"]'
        self.bodyXpath = '/html/body'
        self.mailSendXpath = '//*[@id="sendBtn"]'
        #self.attachXpath = '//*[@id="AddButton_html5"]'
    def __str__(self):
        return '[   NAVER   ]'

    # connect uri        
    def connect_uri(self):
        self.driver = init_webdriver()
        self.driver.get(self.uri)

    # login
    def run_login(self):
        # loginXpath 찾고 클릭
        self.driver.find_element(By.XPATH, self.loginXpath).click()
        # 캡차 우회하기 위해 clipboard에서 복사, 붙여넣기 하는 방식을 사용
        input_clipboard_with_xpath(self.idXpath, self.id, self.driver)
        input_clipboard_with_xpath(self.pwdXpath, self.pwd, self.driver)
        # okXpath 찾기 클릭
        self.driver.find_element(By.XPATH, self.okXpath).click()

    def connect_uri_with_login(self):
        self.connect_uri()
        self.run_login()

    def connect_mail_write(self):
        self.driver.find_element(By.XPATH, self.mailXpath).click()
        self.driver.find_element(By.XPATH, self.mailWriteXpath).click()
        # 클릭하는 구문 뒤엔 약간의 sleep 필요
        time.sleep(1)

        self.run_mail_write_require_data()

    def run_mail_write_require_data(self):
        # to list가 있으면 추가
        for x in self.to:
            self.driver.find_element(By.XPATH, self.toXpath).send_keys(Keys.ENTER, x)
        # cc list가 있으면 추가
        for x in self.cc:
            self.driver.find_element(By.XPATH, self.ccXpath).send_keys(Keys.ENTER, x)
        # bcc list가 있으면 추가
        if len(self.bcc):
            self.driver.find_element(By.XPATH, self.bcclistXpath).click()
            for x in self.bcc:
                self.driver.find_element(By.XPATH, self.bccXpath).send_keys(Keys.ENTER, x)

        # subject 추가
        self.driver.find_element(By.XPATH, self.subjectXpath).send_keys(self.subject)

        # content 추가
        # content는 iframe안에 있어 element를 찾지 못함
        # 따라서 iframe 안에서 찾아야 됨
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, self.bodyIframe))
        elem = self.driver.find_element(By.XPATH, self.bodyXpath)
        elem.send_keys(self.content)
        self.driver.switch_to.default_content()
        
        if len(self.attach):
            # 첨부 파일은 이미지를 이용하여 키보드, 마우스 제어로 구현
            import pyautogui as pag
            # my_pc.png 이미지를 찾아 좌표를 return
            mypc_locate = pag.locateCenterOnScreen('./images/my_pc.PNG')

            print (self.attach)
            for x in self.attach:
                print (x)
                print ('my_pc.png locate ==> ' + str(mypc_locate))
                # my_pc.png 의 좌표 클릭
                pag.click(mypc_locate)
                time.sleep(1)

                # 경로 좌표 클릭
                pag.click(740, 70)
                # filepath 입력 후 enter
                pag.typewrite(self.file_path)
                pag.press('enter')
                time.sleep(1)

                search_locate = pag.locateCenterOnScreen('./images/search.PNG')
                print ('search.png locate ==> ' + str(search_locate))
                pag.click(search_locate)
                time.sleep(1)

                # filename 입력 후 enter
                #pag.typewrite(x)
                pag.write(x, interval=0.1)
                pag.press('enter')
                time.sleep(2)

                # 검색한 파일 위치 클릭 (자세히 보기로 되어있어야함)
                file_locate = pag.moveTo(642,209,0)
                pag.leftClick(file_locate)
                time.sleep(1)

                # 열기 클릭
                open_locate = pag.locateCenterOnScreen('./images/open.PNG')
                print ('open.png locate ==> ' + str(open_locate))
                pag.click(open_locate)
                time.sleep(1)

    def run_login_mail_write(self):
        self.connect_uri_with_login()
        self.connect_mail_write()

        #self.driver.find_element(By.XPATH, self.mailSendXpath).click()

    def close_driver(self):
        self.driver.quit()

    def run_login_mail_write_with_close(self):
        self.run_login_mail_write()
        self.close_driver()
