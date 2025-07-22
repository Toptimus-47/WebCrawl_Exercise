# platform_data_processors/dabang/dabang_data_converter.py
import pandas as pd
import logging
from common_utils.logger_setup import setup_logger

class DabangDataConverter:
    def __init__(self, log_level="INFO", log_file=None):
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.logger.info("DabangDataConverter initialized.")

    def convert_raw_to_dataframe(self, raw_rooms_data):
        """
        다방 API로부터 받은 원시 매물 데이터를 전처리하여 DataFrame으로 변환합니다.
        """
        if not raw_rooms_data:
            self.logger.warning("No raw rooms data to preprocess.")
            return pd.DataFrame()

        processed_data = []
        for room in raw_rooms_data:
            # 다방 API 응답 구조에 따라 필드 추출 및 정제
            # 예시 필드 (실제 API 응답을 보고 정확히 매핑 필요)
            room_id = room.get('id')
            room_type_text = room.get('room_type_text')
            building_type = room.get('building_type')
            
            deal_type_raw = room.get('dealType') # '월세', '전세', '매매' 등
            
            deposit = room.get('deposit')
            rent = room.get('rent')
            # 'price' 필드가 매매가 또는 총 보증금 등일 수 있음
            sales_price = room.get('price') # 매매가로 가정 (혹은 deal_type에 따라 다른 필드)

            address_road = room.get('address_road') # 도로명 주소
            address_jibun = room.get('address_jibun') # 지번 주소
            
            lat = room.get('lat')
            lng = room.get('lng')

            floor_string = room.get('floor_string') # 층수 문자열 (예: '고층', '10/20층')
            size_m2 = room.get('size_m2') # 공급 면적 (m2)

            processed_data.append({
                '매물ID': room_id,
                '방유형': room_type_text,
                '건물유형': building_type,
                '거래유형': deal_type_raw,
                '보증금(만원)': deposit,
                '월세(만원)': rent,
                '매매가(만원)': sales_price,
                '도로명주소': address_road,
                '지번주소': address_jibun,
                '위도': lat,
                '경도': lng,
                '층수': floor_string,
                '면적(m2)': size_m2,
                # 필요에 따라 더 많은 필드 추가
            })
        
        df = pd.DataFrame(processed_data)
        
        # 숫자형 데이터 타입 변환 및 결측치 처리
        for col in ['보증금(만원)', '월세(만원)', '매매가(만원)', '면적(m2)']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        self.logger.info("Dabang raw data conversion to DataFrame completed.")
        return df

