# platform_crawlers/dabang/dabang_collector.py

import time
from common_utils.logger_setup import setup_logger
from platform_crawlers.dabang.dabang_api_client import DabangApiClient
from platform_configs.dabang_config import DABANG_DEFAULT_PAYLOAD, DABANG_DEFAULT_MAX_PAGES, DABANG_DEFAULT_ZOOM_LEVEL

class DabangCollector:
    def __init__(self, log_level="INFO", log_file=None):
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.api_client = DabangApiClient(log_level=log_level, log_file=log_file)
        self.logger.info("DabangCollector initialized.")

    # collect_rooms_data_by_area 메서드가 BBOX 인자를 받도록 수정
    def collect_rooms_data_by_area(self, lat_min, lat_max, lng_min, lng_max):
        self.logger.info(f"Collecting Dabang room data for Lat:[{lat_min}-{lat_max}], Lng:[{lng_min}-{lng_max}]")
        
        all_room_ids = set()
        current_page = 1
        
        while current_page <= DABANG_DEFAULT_MAX_PAGES:
            self.logger.debug(f"Requesting Dabang rooms for page {current_page} with BBOX: ({lat_min}, {lng_min}) to ({lat_max}, {lng_max})")
            
            # DabangApiClient.get_rooms_list_by_bbox() 호출 시 BBOX 인자와 줌 레벨 전달
            data = self.api_client.get_rooms_list_by_bbox(
                lat_min=lat_min,
                lat_max=lat_max,
                lng_min=lng_min,
                lng_max=lng_max,
                zoom=DABANG_DEFAULT_ZOOM_LEVEL, # 설정 파일에서 가져온 줌 레벨 사용
                page=current_page
            )
            
            if data and data.get('rooms'):
                for room in data['rooms']:
                    if 'id' in room:
                        all_room_ids.add(room['id'])
                
                current_page += 1
                time.sleep(0.5) # 요청 간격
            else:
                self.logger.info(f"No more Dabang rooms found or an error occurred on page {current_page}.")
                break
                
        self.logger.info(f"Collected {len(all_room_ids)} unique Dabang room IDs.")
        return list(all_room_ids)

    def collect_room_details(self, room_ids):
        """
        수집된 room_ids를 기반으로 상세 정보를 가져옵니다.
        이 부분은 실제 상세 API 호출 로직으로 채워져야 합니다.
        """
        if not room_ids:
            self.logger.info("No room IDs to collect details for.")
            return []

        self.logger.info(f"Collecting details for {len(room_ids)} Dabang rooms...")
        detailed_rooms = []
        self.logger.warning("Dabang room detail collection is not fully implemented. Please implement `get_room_details` in DabangApiClient.")
        return detailed_rooms
