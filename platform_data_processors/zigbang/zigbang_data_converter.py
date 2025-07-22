# platform_data_processors/zigbang/zigbang_data_converter.py
import pandas as pd
import logging
from common_utils.logger_setup import setup_logger

class ZigbangDataConverter:
    def __init__(self, log_level="INFO", log_file=None):
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.logger.info("ZigbangDataConverter initialized.")

    def convert_raw_to_dataframe(self, raw_items_data):
        """
        직방 아이템 상세 API로부터 받은 원시 데이터를 DataFrame으로 변환합니다.
        HAR 파일 응답 구조와 기존 코드를 참고하여 필드를 추출합니다.
        """
        if not raw_items_data:
            self.logger.warning("No raw items data to convert.")
            return pd.DataFrame()

        processed_data = []
        for item in raw_items_data:
            # 이 필드명들은 실제 API 응답 JSON을 보고 정확한 필드명과 중첩 구조를 확인해야 합니다.
            
            item_id = item.get('item_id')
            item_title = item.get('title') or item.get('item_title') # 둘 중 하나
            address1 = item.get('address1')
            address2 = item.get('address2')
            address = f"{address1} {address2}".strip() if address1 or address2 else ""
            
            sales_type_info = item.get('sales_type_info', {}) 
            sales_type_text = sales_type_info.get('sales_type_text') or item.get('sales_type')
            deposit = sales_type_info.get('deposit') or item.get('deposit')
            rent = sales_type_info.get('rent') or item.get('rent')
            sales_price = item.get('sales_price') 

            lat = item.get('lat')
            lng = item.get('lng')

            room_type = item.get('item_type_summary') or item.get('room_type')
            floor = item.get('floor_text') or item.get('floor')
            area_m2 = item.get('space_m2') or item.get('size_m2') # 면적 (m2)
            
            building_name = item.get('building_name')
            
            # 이미지 URL
            image_urls = [img.get('url') for img in item.get('images', []) if img.get('url')]
            
            processed_data.append({
                '매물ID': item_id,
                '매물명': item_title,
                '주소': address,
                '거래유형': sales_type_text,
                '보증금(만원)': deposit,
                '월세(만원)': rent,
                '매매가(만원)': sales_price,
                '방유형': room_type,
                '층수': floor,
                '면적(m2)': area_m2,
                '위도': lat,
                '경도': lng,
                '건물명': building_name,
                '이미지_URL': ", ".join(image_urls) # 여러 이미지 URL을 콤마로 구분
            })
        
        df = pd.DataFrame(processed_data)
        
        for col in ['보증금(만원)', '월세(만원)', '매매가(만원)', '면적(m2)']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        self.logger.info("Raw data conversion to DataFrame completed.")
        return df

