# Code for Crawling Google Playstore Reviews

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException


def scroll_down(browser):
    # Get scroll height.
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height.
        new_height = browser.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


def click_more_button(browser):
    see_more_button = browser.find_element_by_xpath(
        '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span')
    see_more_button.click()


reviews = []
dates = []
ratings = []

driver = webdriver.Chrome('/Users/SeoyeonHong/Downloads/chromedriver')
time.sleep(1)
driver.get("https://play.google.com/store/apps/details?id=com.prestigeworldwide.myfast&hl=en&showAllReviews=true")
time.sleep(1)

driver.execute_script("window.scrollTo(0, 150);")

# Order by Recent
relevance_button = driver.find_element_by_xpath(
    '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/c-wiz/div[1]/div/div[1]/div[1]/div[3]')
relevance_button.click()
time.sleep(1)

recent_button = driver.find_element_by_xpath(
    '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]')
recent_button.click()
time.sleep(2)

# Scrolling down to the bottom of the page
scroll_down(driver)

j = 0
while True:
    try:
        driver.find_element_by_xpath(
            '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div').click()
        time.sleep(3)
        scroll_down(driver)
        time.sleep(3)
    except NoSuchElementException:
        j += 1
    if j >= 10:
        break

# Retrieving Source
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

# driver.close()

all_reviews = soup.find_all('div', class_='UD7Dzf')
all_dates = soup.find_all('div', class_='bAhLNe kx8XBd')
print("Ratings: ", len(all_reviews))

for all_review in all_reviews:
    review = all_review.get_text()  # Getting Reviews
    reviews.append(review)

for all_date in all_dates:
    date = all_date.find('span', class_='p2TkOb').get_text()  # Getting Dates
    dates.append(date)
    rating = all_date.find('div', class_='pf5lIe').div.attrs['aria-label'].split(" ")[1]  # Getting Ratings
    ratings.append(int(rating))

df = pd.DataFrame(list(zip(dates, reviews, ratings)), columns=['dates', 'reviews', 'ratings'])
df.to_excel('/Users/SeoyeonHong/Desktop/MyFast_ps_reviews.xlsx', index=False)
