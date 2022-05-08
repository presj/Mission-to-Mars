# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment, create dictionary, end the webdriver and return the scraped data
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # create new dictionary to hold list of dictionaries with URL string and title of each hemisphere image
    #data = {'img_url': 'https://marshemispheres.com/images/full.jpg',
    #'title': 'Cerberus Hemisphere Enhanced',
    #'img_url': 'https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg',
    #'title': 'Schiaparelli Hemisphere Enhanced',
    #'img_url': 'https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg',
    #'title': 'Syrtis Major Hemisphere Enhanced',
    #'img_url': 'https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg',
    #'title': 'Valles Marineris Hemisphere Enhanced'}

    data = {'titles':['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced'],
    'urls':['https://marshemispheres.com/images/full.jpg', 'https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg', 'https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg'
    'https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg']}
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
    
        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
        
    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
      
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        #create a function that will scrape the hemisphere data by using your code from the Mission_to_Mars_Challenge.py file.
        df = pd.read_html('https://galaxyfacts-mars.com')[0]        

    except BaseException:
        #return the scraped data as a list of dictionaries with the URL string and title of each hemisphere image.
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")  
   
def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item img")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data['img_url'] = url + hemi_data['img_url']
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    # parse html text
    hemi_soup = soup(html_text, "html.parser")

    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres








if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    

