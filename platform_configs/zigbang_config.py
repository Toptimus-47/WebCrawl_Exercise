# platform_configs/zigbang_config.py

# 직방 API의 기본 URL
ZIGBANG_API_BASE_URL = "https://apis.zigbang.com" # 이 줄을 https://apis.zigbang.com으로 수정했습니다.

# 직방 API 요청 시 기본 헤더 (필요에 따라 조정)
ZIGBANG_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}

# 크롤링할 매물 유형
ZIGBANG_DEFAULT_ITEM_TYPE = "villa" # 'villa', 'apt', 'oneroom', 'officetel' 등

# 직방 API 요청 시 필요한 추가 파라미터들 (필터 등)
ZIGBANG_DEFAULT_PARAMS = {
    "depositMin": 0,
    "rentMin": 0,
    "salesTypes": ["전세", "월세", "매매"],
    "salesPriceMin": 0,
    "domain": "zigbang",
    "checkAnyItemWithoutFilter": True,
    "zoom": 6 # Geohash 생성에 사용되는 줌 레벨 (이 값은 API의 특성에 따라 유지)
}
