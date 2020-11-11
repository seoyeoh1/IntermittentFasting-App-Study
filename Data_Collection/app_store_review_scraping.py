life_url = 'https://apps.apple.com/us/app/life-fasting-tracker/id1319306064#see-all/reviews'
bodyfast_url = 'https://apps.apple.com/us/app/bodyfast-intermittent-fasting/id1189568780#see-all/reviews'
dofasting_url = 'https://apps.apple.com/us/app/dofasting-fasting-tracker/id1456288628#see-all/reviews' #12903
simple_url = 'https://apps.apple.com/us/app/simple-fasting-meal-tracker/id1467720176#see-all/reviews'
myfast_url = 'https://apps.apple.com/us/app/intermittent-fasting-diet-app/id1218416683#see-all/reviews' #96

urls = {'life': life_url, 'bodyfast': bodyfast_url, 'dofasting': dofasting_url, 'simple': simple_url, 'myfast': myfast_url}

def app_store_review_scraper(app_name, url):
    import re
    import xlrd
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    from random import uniform

    from bs4 import BeautifulSoup

    reviews = []
    dates = []
    ratings = []
    titles = []
    dev_responses = []

    stars = re.compile(r"\d out of \d")

    driver = webdriver.Chrome('/Users/angieryu2202/Downloads/chromedriver')
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    time.sleep(1)

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(uniform(1.2, 4.2))
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".we-customer-review")))
    time.sleep(1)

    for elem in elements:
        s = BeautifulSoup(elem.get_attribute("innerHTML"), "html.parser")
        review_date = s.find("time").text
        review_body = s.find("p").text
        review_title = s.find("h3", {"data-test-customer-review-title": ""}).text.strip()
        review_stars = ''.join(re.findall(stars, str(s.find("figure"))))
        dev_response = s.find_all("p", {"data-test-bidi": ""})
        #print(f"{review_title} | {review_date} | {review_stars}")
        #print(review_body)
        #print(dev_response[1].text if len(dev_response) > 1 else "")
        #print("-" * 80)
        reviews.append(review_body)
        dates.append(review_date)
        ratings.append(review_stars)
        titles.append(review_title)
        dev_responses.append(dev_response)
    
    driver.quit()
    
    print(app_name)
    print(len(reviews))
    print("-" * 80)
    
    df = pd.DataFrame(list(zip(dates, titles, reviews, dev_responses, ratings)), columns = ['dates', 'titles', 'reviews', 'dev_responses', 'ratings'])
    df['app_name'] = str(app_name)
    df = df.reset_index(drop = True)
    df.to_excel('/Users/angieryu2202/Desktop/IF_App_Study/'+str(app_name)+'_app_store_reviews_'+str(len(reviews))+'.xlsx', index = False)

app_store_review_scraper('life', life_url)
#app_store_review_scraper('myfast', myfast_url)
#app_store_review_scraper('bodyfast', bodyfast_url)
#app_store_review_scraper('simple', simple_url)
# app_store_review_scraper('dofasting', dofasting_url)
