import logging

def set_init_log(logger_name, file_name):
    # 로그 생성
    logger = logging.getLogger(logger_name)

    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)

    #log 출력 형식
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(filename)s:%(lineno)s ==>> %(message)s')

    #log를 파일에 출력
    file_path = './log/' + file_name
    file_handler = logging.FileHandler(file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info('\n\n--------------------------------------------------------------\n')
    return logger