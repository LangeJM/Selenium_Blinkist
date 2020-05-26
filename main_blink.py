'''script to scrapes all books in library of service blinkist.com
and arrange and save them as docs in provided directory.
'''
#import msvcrt
import time
import random
#from datetime import datetime
from os import path
import logging

import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from helper_blink import set_geckodriver_path
from helper_blink import setup_geckodriver
from helper_blink import blinkist_login
from helper_blink import skip_already_processed_read_urls
from helper_blink import get_book_urls
from helper_blink import get_read_urls_lib
from helper_blink import get_save_dir
from helper_blink import get_book_info
from helper_blink import get_book_headers_and_chapters
from helper_blink import file_name
from helper_blink import create_doc
from helper_blink import usr_selection_books
from helper_blink import convert_docx_to_pdf
import get_all_blinkist_books


# Ask for save directory of blinkist book summaries
save_dir = get_save_dir()

# Get geckodriver path from user dialogue
geckodriver_path = set_geckodriver_path()

# Set up Firefox profile to run private session
firefox_profile = setup_geckodriver()

# Start automated Firefox session on right screen (if multi screen setup) and maxed window
driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=geckodriver_path)
driver.set_window_position(2000, 0)
driver.maximize_window()

# Login to blinkist (needs manual reCaptcha resolution!!!)
blinkist_login(driver)

# Query user for selection of books to retrieve and get list of book reader urls
all_books = usr_selection_books()
if all_books == 1:
    read_urls = get_read_urls_lib(driver)
elif all_books == 0:
    if path.exists('blinkist_all_books.csv'):
        read_urls = (pd.read_csv('blinkist_all_books.csv')).Read_Url.tolist()
        read_urls = read_urls[1:]
        # convert list to dict to list removes duplicates within list and respects the original order
        read_urls = list(dict.fromkeys(read_urls))
    else:
        get_all_blinkist_books.all_books_to_csv()
        read_urls = (pd.read_csv('blinkist_all_books.csv')).Read_Url.tolist()
        read_urls = read_urls[1:]
        read_urls = list(dict.fromkeys(read_urls))


# Check if books have already been retrieved and delete from list if so
read_urls, skipped_urls = skip_already_processed_read_urls(read_urls, save_dir)

# Get book urls from book reader urls
book_urls = get_book_urls(read_urls)

def get_and_save_books(read_urls):
    '''Main function to actually scrape the books and save them to docx. Includes expection handling and log.
    '''
    pass_counter = 1
    log = 'exception_log.log'
    logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    def empty_line(log):
        new_empty_line = open(log, 'a+')
        new_empty_line.write('\n')
        new_empty_line.close()

    empty_line(log)
    logging.info('New Scrape Session Started.')
    logging.info('%s urls have been skipped because the respective documents already exist in the provided directory.\n Remaining urls: %s.', skipped_urls, len(read_urls))
    index_start = 0

    while True:
        try:
            logging.info('Pass #: %s.', pass_counter)

            for index in range(index_start, len(book_urls)):
                book_url = book_urls[index]

                header_title, header_subtitle, header_author, read_time, book_info, amazon_link = get_book_info(book_url, driver)

                read_url = read_urls[index]
                chapter_headers, chapter_bodies, num_of_chapters = get_book_headers_and_chapters(read_url, driver)


                book_fn = file_name(header_title, header_author)

                create_doc(header_title, header_subtitle, header_author, read_time, book_info, amazon_link, chapter_headers, chapter_bodies, num_of_chapters, save_dir, book_fn, read_url)
                index_start += 1
                time.sleep(random.uniform(2, 3.5))

        except (NoSuchElementException, StaleElementReferenceException, UnboundLocalError) as exception:

            logging.info('%s after %s iterations.', exception, index_start)
            if 'referenced before assignment' in str(exception):
                waiting_time = 120
            else:
                waiting_time = 120

            print(str(exception) + ' This indicates that you have reached the maximum iterations for the current IP in the given time frame. The session will continue after a break of ' + str(waiting_time/60) + ' minutes.\n')


            if pass_counter <= 200:
                time.sleep(waiting_time)
                logging.info('Session continued after break.')
                pass_counter += 1
                index_start -= 1
                continue

            break
        break

    driver.quit()

    convert_docx_to_pdf(save_dir)

if __name__ == "__main__":
    get_and_save_books(read_urls)
