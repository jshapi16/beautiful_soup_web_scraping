#!/usr/bin/env python
# coding: utf-8

# In[27]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests


# In[28]:


#set up executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## Scrape news from redplanet website

# In[29]:


#setup beautiful soup for redplanetscience.com

#URL to be scraped
url = "https://www.redplanetscience.com"

#visit url
browser.visit(url)

#Grab the html 
news_html = browser.html

#create beautiful soup object with parser - parse in the html elements
soup = BeautifulSoup(news_html, "html.parser")


# In[30]:


#find most recent news title
news_title = soup.find('div', class_="content_title").text
news_title


# In[34]:


#find paragraph text
news_p = soup.find('div', class_="article_teaser_body").text
news_p


# In[35]:


#Make a dictionary with the values
redplanet_dict = {"news_title": "NASA's Perseverance Rover 100 Days Out", "news_p": "Mark your calendars: The agency's latest rover has only about 8,640,000 seconds to go before it touches down on the Red Planet, becoming history's next Mars car."}
redplanet_dict


# ## Scrape photo from mars space image website

# In[78]:


#set up url for. the browser to visit using splinter
url="https://spaceimages-mars.com/"
html = browser.visit(url)


# In[79]:


#locate the button and click it
image_element = browser.find_by_tag("button")[1]
image_element.click()


# In[80]:


#Parse with beautiful soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')


# In[83]:


#Select image src and add it to the url
image_anchor = img_soup.find("img", class_="fancybox-image").get('src')
featured_image_url = url + image_anchor
print(featured_image_url)
print(image_anchor)


# In[40]:


#Make a dictionary of space image
space_image_dict = {"featured_image": "https://spaceimages-mars.com/image/featured/mars3.jpg"}
space_image_dict


# ## Scrape hemisphere data from mars hemispheres

# In[22]:


#Visit mars hemispheres website
url = "https://www.marshemispheres.com"
browser.visit(url)


# In[23]:


#List which will hold the dictionaries
hemisphere_image_links = []


#get links for all hemispheres
links = browser.find_by_css('a.product-item img')

#click all links and get the href
for i in range(len(links)):
    hemisphere_dict = {}
    browser.find_by_css('a.product-item img')[i].click()
    thumb_img = browser.links.find_by_text('Sample').first
    print(thumb_img)
    
    #hemisphere href
    hemisphere_dict['img_url'] = thumb_img['href']
    
    #hemisphere title
    hemisphere_dict['title'] = browser.find_by_css('h2.title').text
    
    hemisphere_image_links.append(hemisphere_dict)
    
    browser.back()


# In[68]:


#checking the list and dict
hemisphere_image_links
hemisphere_dict


# # Combine all dicts

# In[91]:


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
    }
    browser.quit()
    return(data)

