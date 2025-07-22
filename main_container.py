# main_container.py

import sys
import os
# sys.path 설정 (현재 스크립트의 상위 디렉토리를 PYTHONPATH에 추가)
# 이 부분은 모듈 import 오류를 방지하기 위해 추가된 것으로 보이지만,
# 프로젝트 구조에 따라 불필요할 수도 있습니다.
# 하지만 현재 오류 해결을 위해 잠시 유지합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # RPA_Assignment_01 폴더
if project_root not in sys.path:
    sys.path.append(project_root)

from common_utils.logger_setup import setup_logger
from platform_crawlers.zigbang.zigbang_collector import ZigbangCollector
# from platform_crawlers.dabang.dabang_collector import DabangCollector # 아직 Dabang 관련 파일이 없으므로 주석 처리

# ==== 전역 설정 변수 정의 (config.py가 없으므로 여기에 직접 정의) ====
BBOX_LAT_MIN = 37.493
BBOX_LAT_MAX = 37.527
BBOX_LNG_MIN = 127.025
BBOX_LNG_MAX = 127.065
LOG_FILE_PATH = "crawler_output.log"
LOG_LEVEL = "DEBUG" # 상세 로그를 보기 위해 DEBUG로 설정
# ===============================================================

class MainContainer:
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__, log_level=LOG_LEVEL, log_file=LOG_FILE_PATH)
        self.logger.debug(f"DEBUG: Initializing MainContainer with LOG_LEVEL={LOG_LEVEL}") # DEBUG 추가
        self.zigbang_collector = ZigbangCollector(log_level=LOG_LEVEL, log_file=LOG_FILE_PATH)
        # self.dabang_collector = DabangCollector(log_level=LOG_LEVEL, log_file=LOG_FILE_PATH) # 아직 Dabang 관련 파일이 없으므로 주석 처리
        self.logger.info("MainContainer initialized.")

    def run(self):
        self.logger.info(f"Starting crawlers for BBOX: Lat:[{BBOX_LAT_MIN}-{BBOX_LAT_MAX}], Lng:[{BBOX_LNG_MIN}-{BBOX_LNG_MAX}]")

        # Zigbang 데이터 수집
        self.logger.info("Collecting Zigbang item IDs by area...")
        zigbang_item_ids = self.zigbang_collector.collect_item_ids_by_area(
            BBOX_LAT_MIN, BBOX_LAT_MAX, BBOX_LNG_MIN, BBOX_LNG_MAX
        )
        self.logger.info(f"Total unique Zigbang item IDs collected: {len(zigbang_item_ids)}")

        if zigbang_item_ids:
            # 상세 정보 수집 (현재는 미구현)
            # zigbang_details = self.zigbang_collector.collect_item_details(zigbang_item_ids)
            # self.logger.info(f"Total Zigbang item details collected: {len(zigbang_details)}")
            pass
        else:
            self.logger.info("No Zigbang items found for the specified area.")

        # Dabang 데이터 수집 (현재 DabangCollector 주석 처리)
        # self.logger.info("Collecting Dabang room data by area...")
        # dabang_room_data = self.dabang_collector.collect_room_data_by_area(
        #     BBOX_LAT_MIN, BBOX_LAT_MAX, BBOX_LNG_MIN, BBOX_LNG_MAX
        # )
        # self.logger.info(f"Total Dabang room data collected: {len(dabang_room_data)}")


if __name__ == "__main__":
    container = MainContainer()
    container.run()
