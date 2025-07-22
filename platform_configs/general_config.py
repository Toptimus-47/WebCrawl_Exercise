# platform_configs/general_config.py
import os

# --- 공통 로깅 설정 ---
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "crawler.log")
LOG_LEVEL = "INFO" # DEBUG, INFO, WARNING, ERROR, CRITICAL 중 선택

# --- 공통 출력 디렉토리 설정 ---
OUTPUT_BASE_DIR = "data"
