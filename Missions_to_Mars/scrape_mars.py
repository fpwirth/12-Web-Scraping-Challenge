#Load Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    executable_path={'executable_path':'chromedriver.exe'}
    return Browser('chrome',**executable_path,headless=False)

def scrape():
    browser=init_browser()
    data={}
    #Setup urls to be scraped
    marsnewsurl='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    marsimageurl='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    marsweatherurl='https://twitter.com/marswxreport?lang=en'
    marsfactsurl='https://space-facts.com/mars/'
    hemisphereurl='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Create BeautifulSoup object in order to get latest Mars news
    browser.visit(marsnewsurl)
    marsnews=bs(browser.html,'html5lib')
    browser.quit

    #Create variable for latest Mars news title
    data['news_title']=marsnews.find_all('div',class_='content_title')[0].text

    #Create variable for latest Mars news text
    data['news_p']=marsnews.find_all('div',class_='article_teaser_body')[0].text

    #Create BeautifulSoup object in order to get featured space image from JPL
    browser.visit(marsimageurl)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    marsimage=bs(browser.html,'html5lib')
    browser.quit

    #Create variable for featured image
    data['featured_image_url']='https://www.jpl.nasa.gov'+marsimage.find('figure',class_='lede').a['href']

    #Create BeautifulSoup object in order to get featured space image from JPL
    browser.visit(marsimageurl)
    marsimage2=bs(browser.html,'html5lib')
    browser.quit

    #Create variable for Mars image
    data['featured_image_url2']='https://www.jpl.nasa.gov'+marsimage2.find('li',class_='slide').a['data-fancybox-href']

    #Create BeautifulSoup object in order to get latest Mars weather
    browser.visit(marsweatherurl)
    marsweather=bs(browser.html,'html5lib')
    browser.quit

    #Create variable for Mars weather
    data['mars_weather']=((marsweather.find('p',class_='TweetTextSize').text).split('pic.twitter.com',1)[0]).replace('\n',' ')

    #Generate html table code of Mars facts
    table=pd.read_html(marsfactsurl)[0]
    data['mars_facts']=table.to_html(index=False,header=False)

    #Create BeautifulSoup objects in order to get Mars hemisphere images
    hemisphere_image=[]
    browser.visit(hemisphereurl)
    hemis=bs(browser.html,'html5lib')
    hemispheres=hemis.find_all('div',class_='description')
    for h in hemispheres:
        hemisphere={}
        hemisphere['title']=((h.find('h3').text).split(' Enhanced',1)[0])
        nextpage=h.find('a')['href']
        browser.visit('https://astrogeology.usgs.gov'+nextpage)
        hemiimage=bs(browser.html,'html5lib')
        hemisphere['img_url']='https://astrogeology.usgs.gov'+hemiimage.find('img',class_='wide-image')['src']
        browser.back()
        hemisphere_image.append(hemisphere)
    browser.quit
    data['hemisphere_image_urls']=hemisphere_image
    return data