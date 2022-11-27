# Web scraping exercise inspired by FreeCodeCamp's YouTube video
# "Web Scraping with Python - Beautiful Soup Crash Course"

from bs4 import BeautifulSoup
import requests, csv

# Context manager to ensure opened file is automatically closed after use.
with open('BooksToScrape.csv', 'w', newline='', encoding='utf-8') as f:

    writer = csv.writer(f)

    # Set url to start with. This will be updated with below while loop.
    url = 'http://books.toscrape.com/'
    
    while True:
        # Get html text from url.
        res = requests.get(url) # This needs to be inside while loop.
        res.raise_for_status()

        # Open html text with BeautifulSoup.
        soup = BeautifulSoup(res.text, features='html.parser')

        # Scrape page number.
        cur_page = soup.find('li', class_='current').text.strip()
        print(f'Writing {cur_page.lower()} ...')

        # Scrap book titles.
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

        # Create and write header of CSV file.
        header = ['Title', 'Price (GBP)']
        writer.writerow(header)

        # Looping through books on each page to extract data.
        for book in books:
            book_name = book.h3.a['title']
            book_price = book.find('p', class_='price_color').text[2:]
                    
            writer.writerow([book_name, book_price])

        # Update next page url. Break out of while loop on error.
        try:
            next_url = soup.find('li', class_='next').a['href'] # Access href attribute value with square brackets.

        # Catch error thrown by .a['href'] and break out of loop, when last page reached.
        except AttributeError:
            print('Done.')
            break
        
        # Dynamically update url.
        url_head = url.rsplit('/', 1)[0] # Split out url head. Next_url changes between page 1 and 2.
        url = url_head + '/' + next_url

