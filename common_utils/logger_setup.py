# common_utils/logger_setup.py
import logging
import os

def setup_logger(name, log_level="INFO", log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 핸들러 중복 방지
    if not logger.handlers:
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 파일 핸들러 (지정된 경우)
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    return logger

