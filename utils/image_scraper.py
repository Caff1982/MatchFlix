import csv
import requests
import time

from config import TMDB_API_KEY

from tmdbv3api import TMDb, Movie, TV

def scrape_images(filepath, save_to='media/images/'):
    """
    Takes path to a csv file as argument and uses
    TMDB API to download images by searching
    for title
    """
    BASE_IMG_URL = 'https://image.tmdb.org/t/p/w500'

    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tmdb.language = 'en'
    tmdb.debug = True

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        movie = Movie()
        tv = TV()
        for i, row in enumerate(reader):
            title = row['title']
            print(f'{i} Title: {title}')
            if row['type'] == 'TV Show':
                res = tv.search(title)
            else:
                res = movie.search(title)
            if len(res) == 0:
                print('No results found')
                continue
            elif len(res) > 1:
                print('Length of results: ', len(res))
                print(res)
            # Check to see if image is available
            try:
                image_url = BASE_IMG_URL + res[0].poster_path
            except TypeError as e:
                print('No image available')
                continue
            
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(save_to + row['show_id'] + '.jpg', 'wb') as f:
                    f.write(image_response.content)
            else:
                print(f'Error retreiving image for: {title}')
                print(f'Status code: {image_response.status_code}')


            time.sleep(0.1)


if __name__ == '__main__':
    filepath = 'netflix_data.csv'
    scrape_images(filepath)