# platform_data_processors/dabang/dabang_data_saver.py
import pandas as pd
import logging
import os
from common_utils.logger_setup import setup_logger

class DabangDataSaver:
    def __init__(self, output_filename, log_level="INFO", log_file=None):
        self.output_filename = output_filename
        self.logger = setup_logger(self.__class__.__name__, log_level, log_file)
        self.logger.info("DabangDataSaver initialized.")

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
            self.logger.info(f"Successfully saved {len(dataframe)} records to {self.output_filename}")
        except Exception as e:
            self.logger.error(f"Failed to save data to {self.output_filename}: {e}")

