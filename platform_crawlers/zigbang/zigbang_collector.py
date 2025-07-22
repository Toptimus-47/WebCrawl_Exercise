# platform_crawlers/zigbang/zigbang_collector.py
import sys
print("sys.path:", sys.path)
import geohash2 as geohash
import time
from common_utils.logger_setup import setup_logger
from platform_crawlers.zigbang.zigbang_api_client import ZigbangApiClient

class ZigbangCollector:
    def __init__(self, log_level="INFO", log_file=None):
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.api_client = ZigbangApiClient(log_level=log_level, log_file=log_file)
        self.logger.info("ZigbangCollector initialized.")

    def _generate_geohashes_in_bbox(self, lat_min, lat_max, lng_min, lng_max, precision=6):
        """
        주어진 BBOX 내에서 Geohash들을 생성합니다.
        직방 API가 특정 Geohash를 기반으로 데이터를 반환하는 방식에 맞춰야 합니다.
        현재는 BBOX의 중심 Geohash 하나만 생성하는 예시입니다.
        실제 서비스의 Geohash 사용 방식에 따라 더 정교한 그리드 생성 로직이 필요할 수 있습니다.
        """
        geohashes = set()
        
        # BBOX의 중심 좌표로 Geohash 생성
        center_lat = (lat_min + lat_max) / 2
        center_lng = (lng_min + lng_max) / 2
        
        # geohash.encode는 (위도, 경도, 정밀도) 순서입니다.
        geohash_str = geohash.encode(center_lat, center_lng, precision=precision)
        geohashes.add(geohash_str)

        self.logger.info(f"Generated {len(geohashes)} unique geohashes for the BBOX at precision {precision}.")
        return list(geohashes)

    def collect_item_ids_by_area(self, lat_min, lat_max, lng_min, lng_max, item_type="villa"):
        self.logger.info(f"Collecting item IDs for {item_type} in Lat:[{lat_min}-{lat_max}], Lng:[{lng_min}-{lng_max}]")
        
        # BBOX 정보를 _generate_geohashes_in_bbox로 전달
        geohashes_to_crawl = self._generate_geohashes_in_bbox(
            lat_min=lat_min,
            lat_max=lat_max,
            lng_min=lng_min,
            lng_max=lng_max,
            precision=6 # 이 정밀도는 ZIGBANG_DEFAULT_PARAMS에 있는 zoom과 연관될 수 있음
        )
        
        all_item_ids = set()
        for geohash_code in geohashes_to_crawl:
            self.logger.debug(f"Requesting item IDs for geohash: {geohash_code}")
            data = self.api_client.get_items_by_geohash(
                geohash=geohash_code,
                item_type=item_type,
                lat_min=lat_min,
                lat_max=lat_max,
                lng_min=lng_min,
                lng_max=lng_max
            )
            if data and data.get('items'):
                for item_group in data['items']:
                    if 'itemIds' in item_group:
                        all_item_ids.update(item_group['itemIds'])
            
            # 요청 간격 늘리기
            time.sleep(0.5)
            
        self.logger.info(f"Collected {len(all_item_ids)} unique item IDs for Zigbang.")
        return list(all_item_ids)

    def collect_item_details(self, item_ids):
        """
        수집된 item_ids를 기반으로 상세 정보를 가져옵니다.
        이 부분은 실제 상세 API 호출 로직으로 채워져야 합니다.
        """
        if not item_ids:
            self.logger.info("No item IDs to collect details for.")
            return []

        self.logger.info(f"Collecting details for {len(item_ids)} Zigbang items...")
        detailed_items = []
        # API 클라이언트를 사용하여 상세 정보를 가져오는 로직 구현
        self.logger.warning("Zigbang item detail collection is not fully implemented. Please implement `get_item_details_by_ids` in ZigbangApiClient.")
        return detailed_items
