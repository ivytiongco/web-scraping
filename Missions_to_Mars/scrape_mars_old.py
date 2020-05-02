from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "c:/webdrivers/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

# NASA Mars News
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    mars['news_title'] = news_title
    mars['news_p'] = news_p

# JPL Mars Space Images - Featured Image    
    # URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find('footer')
    link = image.find('a')
    image_url = link['data-fancybox-href']

    featured_image_url = jpl_url + image_url
    mars['featured_image_url'] = featured_image_url

# Mars Weather twitter account 
    # URL of page to be scraped

    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('span', text = re.compile('2020-04-29')).text
    mars['mars_weather'] = mars_weather

# Mars Facts webpage

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(1)

    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['measurement', 'value']
    html_table = df.to_html()
    html_table.replace('\n', '') 
    mars['html_table'] = html_table

# Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.

    hemisphere_image_urls = []

    # Cerberus Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    download = soup.find('div', class_='downloads')
    ul_list = download.find('ul')
    li_list = ul_list.find_all('li')[1]
    cer_image_url = li_list.a['href']

    container = soup.find('div', class_='container')
    content = container.find('div', class_='content')
    meta = content.find('section', class_='block metadata')
    cer_title = meta.h2.text
    cer_title = cer_title_enhanced.replace(" Enhanced", "") 

    cer = {"title": cer_title, "img_url": cer_image_url}
    hemisphere_img_urls.append(cer)

    # Schiaparelli Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    download = soup.find('div', class_='downloads')
    ul_list = download.find('ul')
    li_list = ul_list.find_all('li')[1]
    sch_image_url = li_list.a['href']

    container = soup.find('div', class_='container')
    content = container.find('div', class_='content')
    meta = content.find('section', class_='block metadata')
    sch_title = meta.h2.text
    sch_title = sch_title_enhanced.replace(" Enhanced", "") 

    sch = {"title": sch_title, "img_url": sch_image_url}
    hemisphere_img_urls.append(sch)

    # Syrtis Major Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    download = soup.find('div', class_='downloads')
    ul_list = download.find('ul')
    li_list = ul_list.find_all('li')[1]
    syr_image_url = li_list.a['href']

    container = soup.find('div', class_='container')
    content = container.find('div', class_='content')
    meta = content.find('section', class_='block metadata')
    syr_title = meta.h2.text
    syr_title = syr_title_enhanced.replace(" Enhanced", "")

    syr = {"title": syr_title, "img_url": syr_image_url}
    hemisphere_img_urls.append(syr)


    # Valles Marineris Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    download = soup.find('div', class_='downloads')
    ul_list = download.find('ul')
    li_list = ul_list.find_all('li')[1]
    val_image_url = li_list.a['href']

    container = soup.find('div', class_='container')
    content = container.find('div', class_='content')
    meta = content.find('section', class_='block metadata')
    val_title = meta.h2.text
    val_title = val_title_enhanced.replace(" Enhanced", "")

    val = {"title": val_title, "img_url": val_image_url}
    hemisphere_img_urls.append(val)

    # Dictionary to be inserted into MongoDB
    mars['hemisphere_image_urls'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data