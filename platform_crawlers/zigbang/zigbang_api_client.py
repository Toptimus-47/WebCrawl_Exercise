# platform_crawlers/zigbang/zigbang_api_client.py

import requests
import json
from common_utils.logger_setup import setup_logger
from platform_configs.zigbang_config import ZIGBANG_API_BASE_URL, ZIGBANG_DEFAULT_HEADERS, ZIGBANG_DEFAULT_PARAMS

class ZigbangApiClient:
    def __init__(self, log_level="INFO", log_file=None):
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.base_url = ZIGBANG_API_BASE_URL
        self.logger.debug(f"DEBUG_INIT: ZigbangApiClient base_url is set to: {self.base_url}")
        self.session = requests.Session()
        self.session.headers.update(ZIGBANG_DEFAULT_HEADERS)
        self.logger.info("ZigbangApiClient initialized.")

    def _make_request(self, method, url, params=None, json_data=None):
        try:
            response = self.session.request(method, url, params=params, json=json_data, timeout=10)
            response.raise_for_status()

            if response.status_code == 204:
                self.logger.info(f"[{response.status_code}] No content (no items) found for: {url} with params: {params}")
                return []
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            response_text_snippet = response.text[:500] if response else "No response text"
            response_status_code = response.status_code if response else "N/A"
            self.logger.error(f"HTTP error occurred: {http_err} - Status: {response_status_code}, Response: {response_text_snippet}...")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            self.logger.error(f"Timeout error occurred: {timeout_err}")
        except json.JSONDecodeError as json_err:
            response_text_snippet = response.text[:500] if response else "No response text"
            response_status_code = response.status_code if response else "N/A"
            self.logger.error(f"Failed to decode JSON from response: {json_err}. Response status: {response_status_code}, Response text (first 500 chars): {response_text_snippet}...")
        return None

    def get_items_by_geohash(self, geohash, item_type, lat_min, lat_max, lng_min, lng_max):
        # API URL 구성: /v2/items/{item_type} 대신 /v2/search를 사용
        url = f"{self.base_url}/v2/search" # 이 줄을 /v2/search로 수정합니다.
        self.logger.debug(f"DEBUG_GET_ITEMS: Requesting URL constructed as: {url}")

        # ZIGBANG_DEFAULT_PARAMS와 전달된 BBOX 파라미터를 결합하여 요청 파라미터 생성
        params = ZIGBANG_DEFAULT_PARAMS.copy()
        params.update({
            "geohash": geohash,
            "lat_min": lat_min,
            "lat_max": lat_max,
            "lng_min": lng_min,
            "lng_max": lng_max,
            "serviceType": item_type, # item_type을 URL 경로가 아닌 파라미터로 추가
        })

        self.logger.info(f"Requesting item list for {item_type} with geohash: {geohash}")
        return self._make_request("GET", url, params=params)

    def get_item_details_by_ids(self, item_ids):
        if not item_ids:
            self.logger.info("No item IDs provided for detail collection.")
            return []

        # 최대 100개의 ID씩 묶어서 요청
        # 직방 API가 한 번에 처리할 수 있는 ID 개수 제한에 따라 조정 필요
        chunk_size = 100
        all_details = []
        for i in range(0, len(item_ids), chunk_size):
            chunk = item_ids[i:i + chunk_size]
            # API URL 구성
            url = f"{self.base_url}/v3/items/list"
            self.logger.debug(f"DEBUG_GET_DETAILS: Requesting URL constructed as: {url} with {len(chunk)} item IDs")

            # POST 요청 본문에 itemIds 포함
            json_data = {"itemIds": chunk}

            self.logger.info(f"Requesting details for {len(chunk)} items.")
            data = self._make_request("POST", url, json_data=json_data)
            if data and data.get('items'):
                all_details.extend(data['items'])
            
            # 요청 간격 늘리기 (선택 사항)
            import time
            time.sleep(0.1)

        self.logger.info(f"Collected details for {len(all_details)} items.")
        return all_details
