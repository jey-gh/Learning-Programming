# Web scraping exercise inspired by FreeCodeCamp's YouTube video
# "Web Scraping with Python - Beautiful Soup Crash Course"

from bs4 import BeautifulSoup
import requests

# Context manager to ensure opened file is automatically closed after use.
with open('toscrapedotcom.txt', 'w', encoding='utf-8') as file:
    # Set url to start with. This will be updated with below while loop.
    url = 'http://books.toscrape.com/'
    
    #Write custom title.
    file.write('Books to Scrape - They Love Being Scraped \n')

    while True:
        # Get html text from url.
        res = requests.get(url) # This needs to be inside while loop.
        res.raise_for_status()

        # Open html text with BeautifulSoup.
        soup = BeautifulSoup(res.text, features='html.parser')

        # Scrape page number.
        cur_page = soup.find('li', class_='current').text
        page_num = ' '.join(cur_page.split()[:2])
        file.write(f'\n{page_num} \n\n')
        print(f'Writing {page_num.lower()} ...')

        # Scrap book titles.
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

        # Looping through books on each page to extract data.
        for book in books:
            book_name = book.h3.a['title']
            book_price = book.find('p', class_='price_color').text.replace('Â','')
                    
            file.write(f'{book_name} costs {book_price}. \n')

        # Update next page url. Break out of while loop on error.
        try:
            next_url = soup.find('li', class_='next').a['href'] # Access href attribute value with square brackets.

        # Catch error thrown by .a['href'] and break out of loop, when last page reached.
        except AttributeError:
            print('Done.')
            break
        
        # Dynamically update url.
        if next_url.startswith('catalogue'):
            url = 'http://books.toscrape.com/' + next_url
        else:
            url = 'http://books.toscrape.com/catalogue/' + next_url
