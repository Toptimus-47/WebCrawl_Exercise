# platform_configs/dabang_config.py

# 다방 API의 기본 URL
DABANG_API_BASE_URL = "https://www.dabangapp.com/api/v1"

# 다방 API 요청 시 기본으로 포함될 페이로드 (필요에 따라 조정)
DABANG_DEFAULT_PAYLOAD = {
    "version": "9",
    "region": "서울", # 기본 검색 지역, 필요에 따라 변경 가능
    "filters": {
        "room_type": ["ONE_ROOM", "TWO_ROOM", "OFFICETEL", "APART"], # 원룸, 투룸, 오피스텔, 아파트
        "sales_type": ["TRADE", "MONTHLY", "JEONSE"], # 매매, 월세, 전세
        "deposit_range": [0, 9999999999],
        "rent_range": [0, 9999999999],
    }
}

# 다방 API 요청 시 사용할 기본 줌 레벨 (예: 지도 확대 정도)
DABANG_DEFAULT_ZOOM_LEVEL = 15

# 다방 API 페이지네이션 시 최대로 수집할 페이지 수 (무한 루프 방지)
DABANG_DEFAULT_MAX_PAGES = 100
