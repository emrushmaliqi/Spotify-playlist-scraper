import sys
import csv
import json
import requests
from bs4 import BeautifulSoup


class Scraper:
    def get_input_csv_file(self):
        if (len(sys.argv) <= 1):
            raise Exception("Please provide a file name as an argument")
        return sys.argv[1]

    def get_urls_from_csv_file(self, csv_file):
        urls = []
        if (not csv_file.endswith('.csv')):
            raise Exception("Please provide a valid csv file")
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                urls.append(row[0])
        return urls

    def scrape(self, urls):
        playlists = []

        if len(urls) == 0:
            raise Exception("CSV file is empty")

        for i in range(len(urls)):
            print(f"Scraping playlist {i+1} of {len(urls)}")
            response = requests.get(urls[i])
            playlist_html = response.text

            soup = BeautifulSoup(playlist_html, 'html.parser')
            title = soup.find('h1').text
            description = soup.find(
                'meta', attrs={'property': 'og:description'}).attrs['content']

            songs_html = soup.find_all('meta', attrs={'name': 'music:song'})
            songs = []

            for song in songs_html:
                song_url = song.attrs['content']
                song_response = requests.get(song_url)
                song_html = song_response.text
                song_soup = BeautifulSoup(song_html, 'html.parser')

                song_title = song_soup.find(
                    'meta', attrs={'property': 'og:title'}).attrs['content']
                song_description = song_soup.find(
                    'meta', attrs={'property': 'og:description'}).attrs['content']
                song_image_url = song_soup.find(
                    'meta', attrs={'property': 'og:image'}).attrs['content']
                song_preview_url = song_soup.find(
                    'meta', attrs={'property': 'og:audio'}).attrs['content']

                songs.append({'title': song_title, 'description': song_description, 'url': song_url,
                             'image_url': song_image_url, 'preview_url': song_preview_url, })

            playlists.append(
                {"title": title, "description": description, "songs": songs})

        return playlists

    def store_to_json(self, playlists):
        if len(playlists) == 0:
            raise Exception("Playlists list is empty")

        playlists_json = json.dumps(playlists, indent=4)

        with open('playlists/playlists.json', 'w') as f:
            f.write(playlists_json)
            print("Saved!")
