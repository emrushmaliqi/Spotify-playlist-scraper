from classes.Scraper import Scraper


s = Scraper()

try:
    csv_file = s.get_input_csv_file()
    urls = s.get_urls_from_csv_file(csv_file)
    playlists = s.scrape(urls)
    s.store_to_json(playlists)
except Exception as e:
    print(e)
