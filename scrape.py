# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape ():

    scraped_data={}

    # ------NASA MARS NEWS-----

    # Choose the executable path to driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)


    # Visit Nasa news url through splinter module
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)



    # HTML Object
    html_news = browser.html
    soup = bs(html_news, "html.parser")
    article = soup.find("div", class_='list_text')

    #Titles contained in <div class="content_title"
    scraped_data["title"] = article.find("div", class_ = "content_title").text

    #Pragraph text contained in <div class="article_teaser_body"
    scraped_data["paragraph"] = article.find("div", class_ = "article_teaser_body").text

    

    #------------JPL Mars Space Images - Featured Image---------------

    # Visit JPL Featured Space Image url through splinter module
    url_spaceimage = "https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(url_spaceimage)


    # HTML Object
    img_html = browser.html
    img_soup = bs(img_html, "html.parser")


    # Find image url to the full size
    scraped_data["featured_image"] = img_soup.find("img", class_="BaseImage object-contain")["data-src"]
  
   
    # -----------Mars Facts---------------

    # Visit the Mars Facts webpage and use Pandas to scrape the table
    url_facts = "https://space-facts.com/mars/"



    # Use Pandas - read_html - to scrape tabular data from a page
    mars_facts = pd.read_html(url_facts)
    

    mars_df = mars_facts[0]

    # Create Data Frame
    mars_df.columns = ["Description", "Value"]

    # Set index to Description
    mars_df.set_index("Description", inplace=True)

  
    # Save html code to folder Assets
    html_table = mars_df.to_html()
    scraped_data["html_table"] = html_table

    # Strip unwanted newlines to clean up the table
    html_table.replace("\n", '')

    # Save html code
    mars_df.to_html("mars_facts_data.html")


    # --------------Mars Hempispheres---------------
    # Visit the USGS Astrogeology Science Center url through splinter
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)


    # HTML Object
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, "html.parser")


    # Scrape all items that contain mars hemispheres information
    hemispheres = soup.find_all("div", class_="item")

    # Create empty list
    hemispheres_info = []

    # Sign main url for loop
    hemispheres_url = "https://astrogeology.usgs.gov"

    # Loop through the list of all hemispheres information
    for i in hemispheres:
        title = i.find("h3").text
        hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        web_info = bs(image_html, "html.parser")
        
        # Create full image url
        img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
        
        hemispheres_info.append({"title" : title, "img_url" : img_url})
    
    scraped_data["hemispheres_info"] = hemispheres_info

    print (scraped_data)
    
    return scraped_data

scrape()





