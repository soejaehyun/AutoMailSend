from time import sleep
from naver import naver_mail_send
import util
import pyautogui as pag
import yaml
import log

if __name__ == "__main__":
    #driver = util.init_webdriver()
    util.mkdir('./log/')
    init_log = log.set_init_log('init', 'init.log')
    progress_log = log.set_init_log('progress', 'progress.log')
    running_list = list()

    #init_log.debug('test')
    run = util.run_conf('./conf/run.yml', init_log)

    for running in run.running:
        if running.get('app') == 'naver':
            running_list.append(naver_mail_send(running.get('app'), running.get('conf_path'), init_log))
        else:
            pass

    running_result = dict()
    for start_mail_send in running_list:
        print ('audo mail send start !!!')
        progress_log.info ('audo mail send start !!!')
        running_result[start_mail_send.application] = dict()
        running_result[start_mail_send.application]['total'] = run.repeat
        
        success = 0
        fail = 0
        for rp in range(1, run.repeat + 1):
            try:
                start_mail_send.run_login_mail_write_with_close()
                success += 1
                print (start_mail_send, ' ==> ', rp, ' of ', run.repeat, ' [  OK  ]')
                progress_log.info (str(start_mail_send) + ' ==> ' + str(rp) + ' of ' + str(run.repeat) + ' [  OK  ]')
            except:
                fail += 1
                print (start_mail_send, ' ==> ', rp, ' of ', run.repeat, ' [ FAIL ]')
                progress_log.info (str(start_mail_send) + ' ==> ' + str(rp) + ' of ' + str(run.repeat) + ' [ FAIL ]')

        running_result[start_mail_send.application]['success'] = success
        running_result[start_mail_send.application]['fail'] = fail

        print(running_result)
        progress_log.info (str(running_result))


    #naver = naver_mail_send(driver, 'naver', './conf/naver.yml')
    #naver.run_login_mail_write_with_close()
    #naver.run_login_mail_write_with_close()

    #driver.quit()

    while True :
        # 초당 마우스 커서 위치 print
        print('Current Cursor : ' + str(pag.position()))
        sleep(1)