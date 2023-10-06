from instagram_scrape import InstaScraper, DataSaver

if __name__ == "__main__":
    scraper = InstaScraper()
    data = scraper.scrape_data()
    DataSaver.save(data)
