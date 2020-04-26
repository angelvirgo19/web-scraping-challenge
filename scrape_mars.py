from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='bottom_gradient').find('h3').text
    news_p = soup.find("div", class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image

    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)
    time.sleep(5)
    html1 = browser.html
    soup = bs(html1, 'html.parser')

    featured_image  = soup.find('article', class_="carousel_item")['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image

    # Mars Weather

    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    time.sleep(10)
    html2 = browser.html
    soup = bs(html2,"lxml")

    mars_weather = soup.find('article').find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[4].text

    # Mars Facts

    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    time.sleep(10)
    facts = pd.read_html(url3)
    facts_df = facts[0]
    mars_facts = facts_df.rename(columns={0 : "Features", 1 : "Value"}).set_index(["Features"])
    mars_table = mars_facts.to_html()
    mars_table.replace('\n','')
    

    # Mars Hemispheres

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(5)
    html4 = browser.html
    soup = bs(html4, 'html.parser')

    infos = soup.find('div', class_='collapsible results')
    hemispheres=infos.find_all('a')

    hemisphere_image_urls=[]

    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        if hemisphere.h3:
            title=hemisphere.h3.text
            link=hemisphere["href"]
            main_url="https://astrogeology.usgs.gov/"
            next_url=main_url+link
            browser.visit(next_url)
            time.sleep(5)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemisphere2=soup.find("div",class_= "downloads")
            img=hemisphere2.ul.a["href"]
            hemisphere_dict={}
            hemisphere_dict["Title"]=title
            hemisphere_dict["Image_URL"]=img
            hemisphere_image_urls.append(hemisphere_dict)
            browser.back()

    hemisphere_image_urls
        


    Mars={
        "Mars_news_title": news_title,
        "Mars_news_p": news_p,
        "Featured_mars_image": featured_image_url,
        "Mars_weather": mars_weather,
        "Mars_facts": mars_table,
        "Mars_hemispheres": hemisphere_image_urls
    }
    browser.quit()

    return Mars

# if __name__ == "__main__":
#     data = scrape()
#     print(data)