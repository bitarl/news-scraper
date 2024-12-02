class NewsPipelineExecutor:
    def __init__(self, scrapers, preprocessor, output_path):
        self.scrapers = scrapers
        self.preprocessor = preprocessor
        self.output_path = output_path

    def execute(self):
        for source, scraper_info in self.scrapers.items():
            scraper, schema_mapping = scraper_info['scraper'], scraper_info['schema_mapping']
            search_term = scraper.config['search_term']
            print(f"Fetching news from {source}")
            data = scraper.fetch_news()
            processed_data = self.preprocessor.process_data(data, schema_mapping)
            self.preprocessor.write_data(processed_data, source, search_term)
