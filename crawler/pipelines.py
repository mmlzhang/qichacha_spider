
import os
import csv
import datetime

from .settings import DATA_PATH


class BigdataCrawlerPipeline(object):

    @staticmethod
    def process_item(item, spider):

        spider_data_path = os.path.join(DATA_PATH, spider.name)
        if not os.path.exists(spider_data_path):
            os.mkdir(spider_data_path)

        date_str = datetime.datetime.now().strftime("%Y%m%d")
        data_path = os.path.join(spider_data_path, date_str)
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        filename = item.get("filename")
        headers = item.get("headers")
        data = item.get("data")

        file_path = os.path.join(data_path, filename) + ".csv"
        delimiter = spider.CSV_DELIMITER
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerow(headers)

        with open(file_path, "a", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=delimiter)
            if isinstance(data, dict):
                row = [data.get(k) for k in headers]
                writer.writerow(row)
            if isinstance(data, list):
                rows = []
                for d in data:
                    row = [d.get(k) for k in headers]
                    rows.append(row)
                writer.writerows(rows)
        return item
