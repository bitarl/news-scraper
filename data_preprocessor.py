import json
import os
from datetime import datetime

class DataPreprocessor:
    def __init__(self, target_schema):
        self.target_schema = target_schema

    def process_data(self, data, schema_mapping):
        print(f"Data: {data}")
        processed_data = []
        for item in data:
            processed_item = {}
            for target, source in schema_mapping.items():
                processed_item[target] = item.get(source, 'unknown')
            processed_data.append(processed_item)

        return processed_data

    # def write_data(self, data, base_path, source):
    #     for item in data:
    #         date = item.get('date', datetime.now().strftime("%Y-%m-%d"))
    #         directory = os.path.join(base_path, source, date)
    #         os.makedirs(directory, exist_ok=True)
    #         filename = os.path.join(directory, f"{datetime.now().strftime('%H%M%S')}.json")
    #         with open(filename, 'w') as f:
    #             json.dump(item, f, indent=4)

    def write_data(self, news_data, source, search_term):
        if not news_data:
            print(f"No data available for {source}")
            return
        
        base_dir = "/Users/leen/Downloads/news_data"
        source_dir = os.path.join(base_dir, source)
        search_term_dir = os.path.join(source_dir, search_term)
        os.makedirs(search_term_dir, exist_ok=True)

        for item in news_data:
            date = item.get("date", "Unknown")
            date_dir = os.path.join(search_term_dir, date)
            os.makedirs(date_dir, exist_ok=True)

            filename = os.path.join(date_dir, f"{source}_{date}.json")
            with open(filename, "w") as f:
                json.dump(item, f, indent=4)
                print(f"Data written to {filename}")