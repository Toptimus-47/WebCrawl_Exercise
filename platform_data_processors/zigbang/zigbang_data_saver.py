# platform_data_processors/zigbang/zigbang_data_saver.py
import pandas as pd
import logging
import os
import requests
from common_utils.logger_setup import setup_logger
from platform_configs.zigbang_config import ZIGBANG_IMAGE_BASE_DIR

class ZigbangDataSaver:
    def __init__(self, output_filename, log_level="INFO", log_file=None):
        self.output_filename = output_filename
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.logger.info("ZigbangDataSaver initialized.")

    def save_dataframe_to_csv(self, dataframe):
        """
        DataFrame을 CSV 파일로 저장합니다.
        """
        if dataframe.empty:
            self.logger.warning("No data to save to CSV.")
            return

        # 출력 디렉토리 확인 및 생성
        output_dir = os.path.dirname(self.output_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            dataframe.to_csv(self.output_filename, index=False, encoding='utf-8-sig')
            self.logger.info(f"Successfully saved {len(dataframe)} unique records to {self.output_filename}")
        except Exception as e:
            self.logger.error(f"Failed to save data to {self.output_filename}: {e}")

    def save_images(self, item_ids_with_image_urls):
        """
        매물 ID와 이미지 URL을 바탕으로 이미지를 저장합니다.
        item_ids_with_image_urls는 리스트 내 딕셔너리 형태: 
        [{'item_id': '12345', 'image_urls': ['url1', 'url2']}, ...]
        """
        self.logger.info(f"Starting image saving process for {len(item_ids_with_image_urls)} items.")
        
        # 이미지 저장 기본 디렉토리 생성
        if not os.path.exists(ZIGBANG_IMAGE_BASE_DIR):
            os.makedirs(ZIGBANG_IMAGE_BASE_DIR)

        for item_info in item_ids_with_image_urls:
            item_id = item_info.get('item_id')
            image_urls = item_info.get('image_urls', [])

            if not item_id or not image_urls:
                self.logger.warning(f"Skipping image save for invalid item_info: {item_info}")
                continue

            img_item_dir = os.path.join(ZIGBANG_IMAGE_BASE_DIR, str(item_id))

            # 디렉토리가 있으면 이미 이미지가 저장된 상태로 간주
            if os.path.exists(img_item_dir):
                # self.logger.debug(f"Image directory for item {item_id} already exists. Skipping.")
                continue
            
            os.makedirs(img_item_dir, exist_ok=True) # 디렉토리 생성

            for idx, img_url in enumerate(image_urls):
                try:
                    img_response = requests.get(img_url, timeout=10)
                    img_response.raise_for_status()
                    img_name = os.path.join(img_item_dir, f"{idx+1}.jpg")
                    with open(img_name, 'wb') as f:
                        f.write(img_response.content)
                    self.logger.debug(f"Saved image {idx+1} for item {item_id}")
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Failed to download image from {img_url} for item {item_id}: {e}")
                except Exception as e:
                    self.logger.critical(f"An unhandled error occurred during image save for {item_id}: {e}")
            self.logger.info(f"Finished saving images for item {item_id}.")
        
        self.logger.info("All image saving processes completed.")

