# platform_crawlers/dabang/dabang_api_client.py

import requests
import json
from common_utils.logger_setup import setup_logger
from platform_configs.dabang_config import DABANG_API_BASE_URL, DABANG_DEFAULT_PAYLOAD

class DabangApiClient:
    def __init__(self, log_level="INFO", log_file=None):
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.base_url = DABANG_API_BASE_URL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger.info("DabangApiClient initialized.")

    def _make_request(self, method, url, params=None, json_data=None):
        try:
            response = self.session.request(method, url, params=params, json=json_data, timeout=10)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err} - Status: {response.status_code}, Response: {response.text}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            self.logger.error(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"An error occurred during the request: {req_err}")
        except json.JSONDecodeError as json_err:
            self.logger.error(f"Failed to decode JSON from response: {json_err}. Response text (first 500 chars): {response.text[:500]}...")
        return None

    # get_rooms_list_by_bbox 메서드가 BBOX 인자와 줌 레벨, 페이지를 받도록 수정
    def get_rooms_list_by_bbox(self, lat_min, lat_max, lng_min, lng_max, zoom, page=1):
        url = f"{self.base_url}/markers/category/one-two" # 또는 apt, officetel 등
        
        params = DABANG_DEFAULT_PAYLOAD.copy()
        
        # HAR 파일 분석을 통해 확인된 다방 API의 BBOX 및 줌 파라미터 이름을 사용해야 합니다.
        # 아래는 일반적인 예시이며, 실제 파라미터 이름과 다를 수 있습니다.
        params.update({
            "page": page,
            "ne_lat": lat_max, # 북동 위도
            "ne_lng": lng_max, # 북동 경도
            "sw_lat": lat_min, # 남서 위도
            "sw_lng": lng_min, # 남서 경도
            "zoom": zoom, # 줌 레벨
            # "map_zoom": zoom, # 만약 m_zoom이 아닌 map_zoom을 사용한다면
            # "latitude": (lat_min + lat_max) / 2, # 지도의 중심 위도
            # "longitude": (lng_min + lng_max) / 2, # 지도의 중심 경도
        })
        
        self.logger.info(f"Requesting Dabang rooms for page {page} with BBOX: ({lat_min}, {lng_min}) to ({lat_max}, {lng_max}) at zoom {zoom}")
        return self._make_request("GET", url, params=params)

    def get_room_details(self, room_id):
        """
        단일 방에 대한 상세 정보를 가져옵니다.
        """
        url = f"{self.base_url}/room/{room_id}" # 예시 URL
        self.logger.debug(f"Requesting details for room ID: {room_id}")
        return self._make_request("GET", url)
