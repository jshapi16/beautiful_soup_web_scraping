from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    #Redplanetscience
    #URL to be scraped
    url = "https://www.redplanetscience.com"
    #visit url
    browser.visit(url)
    #Grab the html 
    news_html = browser.html
    #create beautiful soup object with parser - parse in the html elements
    soup = BeautifulSoup(news_html, "html.parser")
    #find most recent news title
    news_title = soup.find('div', class_="content_title").text
    #find paragraph text
    news_p = soup.find('div', class_="article_teaser_body").text
    
    
    #Space images, featured image 
    url="https://spaceimages-mars.com/"
    html = browser.visit(url)
    #locate the button and click it
    image_element = browser.find_by_tag("button")[1]
    image_element.click()
    #Parse with beautiful soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    #Select image src and add it to the url
    image_anchor = img_soup.find("img", class_="fancybox-image").get('src')
    featured_image_url = url + image_anchor
    
    def mars_facts():
        mars_table = pd.read_html('https://galaxyfacts-mars.com')[0]
        mars_table.columns = ['description', 'mars', 'earth']
        mars_table.set_index('description', inplace=True)
        mars_df = mars_table.to_html()
        return mars_df

    #mars hemispheres information
    def mars_hemispheres():
        #Visit mars hemispheres website
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        hemisphere_image_links = []

        #get links for all hemispheres
        links = browser.find_by_css('a.product-item img')
        hemisphere_dict = {}
        #click all links and get the href
        for i in range(len(links)):
            browser.find_by_css('a.product-item img')[i].click()
            thumb_img = browser.links.find_by_text('Sample').first
            print(thumb_img)
            #hemisphere href
            hemisphere_dict['img_url'] = thumb_img['href']
            #hemisphere title
            hemisphere_dict['title'] = browser.find_by_css('h2.title').text
            hemisphere_image_links.append(hemisphere_dict)
            browser.back()
        return hemisphere_image_links

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "mars_facts": mars_facts(),
        "hemispheres": mars_hemispheres(),
    }
    browser.quit()
    return(mars_data)

if __name__ == "__main__":
    print(scrape_all())