# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "c:/webdrivers/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Dictionary to be inserted into MongoDB
    mars = {}

    # Scrape the NASA Mars News Site
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    mars['news_title'] = news_title
    mars['news_p'] = news_p

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string
    # to a variable called featured_image_url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('footer')
    link = image.find('a')
    image_url = link['data-fancybox-href']

    featured_image_url = 'https://www.jpl.nasa.gov' + image_url
    mars['featured_image_url'] = featured_image_url

    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('span', text = re.compile('2020-04-30')).text
#    mars_weather = soup.find_all('span', text = re.compile(r'\d{4}-\d{2}-\d{2}'))[0].text
    mars['mars_weather'] = mars_weather

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    # including Diameter, Mass, etc.
    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['measurement', 'value']
    html_table = df.to_html()
    html_table.replace('\n', '') 

    mars['html_table'] = html_table

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.

    # Create list to add image_url and title for each hemisphere
    hemisphere_image_urls = []

    # Cerberus Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find image url
    wrapper = soup.find('div', class_='wide-image-wrapper')
    img = wrapper.find('img', class_='wide-image')['src']
    cer_image_url = 'https://astrogeology.usgs.gov' + img
    
    # Find image title
    cer_title_enhanced = soup.find('section', class_='block metadata').h2.text
    cer_title = cer_title_enhanced.replace(" Enhanced", "") 

    # Add image url and title to hemisphere_image_urls
    cer = {"title": cer_title, "img_url": cer_image_url}
    hemisphere_image_urls.append(cer)

    # Schiaparelli Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find image url
    wrapper = soup.find('div', class_='wide-image-wrapper')
    img = wrapper.find('img', class_='wide-image')['src']
    sch_image_url = 'https://astrogeology.usgs.gov' + img

    # Find image title
    sch_title_enhanced = soup.find('section', class_='block metadata').h2.text
    sch_title = sch_title_enhanced.replace(" Enhanced", "") 

    # Add image url and title to hemisphere_image_urls
    sch = {"title": sch_title, "img_url": sch_image_url}
    hemisphere_image_urls.append(sch)

    # Syrtis Major Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find image url
    wrapper = soup.find('div', class_='wide-image-wrapper')
    img = wrapper.find('img', class_='wide-image')['src']
    syr_image_url = 'https://astrogeology.usgs.gov' + img

    # Find image title
    syr_title_enhanced = soup.find('section', class_='block metadata').h2.text
    syr_title = syr_title_enhanced.replace(" Enhanced", "") 

    # Add image url and title to hemisphere_image_urls
    syr = {"title": syr_title, "img_url": syr_image_url}
    hemisphere_image_urls.append(syr)

    # Valles Marineris Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find image url
    wrapper = soup.find('div', class_='wide-image-wrapper')
    img = wrapper.find('img', class_='wide-image')['src']
    val_image_url = 'https://astrogeology.usgs.gov' + img

    # Find image title
    val_title_enhanced = soup.find('section', class_='block metadata').h2.text
    val_title = val_title_enhanced.replace(" Enhanced", "") 

    # Add image url and title to hemisphere_image_urls
    val = {"title": val_title, "img_url": val_image_url}
    hemisphere_image_urls.append(val)

    # Dictionary to be inserted into MongoDB
    mars['hemisphere_image_urls'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars