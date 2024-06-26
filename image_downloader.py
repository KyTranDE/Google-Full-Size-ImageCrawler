from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import time
import urllib.request
import os
from selenium.webdriver.common.by import By
import ssl
import yaml
from Utils.logger import logger

def google_scroll(SCROLL_PAUSE_TIME,search,cssScronto):
    elem = driver.find_element(By.NAME, "q")
    elem.send_keys(search)
    elem.send_keys(Keys.RETURN)
   
    SCROLL_PAUSE_TIME = SCROLL_PAUSE_TIME

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, cssScronto).click()
            except:
                break
        last_height = new_height
def check_url(url,search):
    if search in url:
        return True
    else:
        return False
    
def url_retrieve(total_image_count,next_addlink,imgUrlCrawl):
    images = driver.find_elements(By.XPATH,next_addlink)
    print(f'{"*"*60}Crawlling started.{"*"*60}')
    count = 1
    TIME_LIMIT = 1
    for image in images:
       
        try:
            try:
                image.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", image)
                except:
                    pass
            # time.sleep(TIME_LIMIT)
            imgUrl = driver.find_element(By.XPATH,imgUrlCrawl).get_attribute('src')
            altUrl = driver.find_element(By.XPATH,imgUrlCrawl).get_attribute('alt')
            if check_url(altUrl.lower(),search):
                urllib.request.urlretrieve(url=imgUrl, filename=f"image/{search}/" + altUrl + "_" + str(count) + ".jpg")            
                logger(f'logs/{search}.log',f'{altUrl}_{count}')
                if (count == total_image_count):
                    break
                else:
                    count+=1
            else:
                pass
        except Exception as e:
            pass
    print(f'{"*"*60}Crawlling Completed.{"*"*60}')
    driver.close()

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == '__main__':
    # ssl._create_default_https_context = ssl._create_unverified_context

    search = "áo dài"
    total_image_count = 1000
    config_path = 'configs/config.yml'
    config = load_config(config_path)
    
    next_addlink = config['xpath']['next_addlink']
    imgUrlCrawl = config['xpath']['imgUrlCrawl']
    copied_xpath = config['xpath']['copied_xpath']
    urlGoogleSearch = config['url']['urlGoogleSearch']
    cssScronto = config['css']['cssScronto']
    urlGoogleSearch = config['url']['urlGoogleSearch']
    options = Options()
    # options.add_argument("--headless")

    
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    driver.get(urlGoogleSearch)
    
    if not os.path.isdir(f"image/{search}/"):
        os.makedirs(f"image/{search}/")

    google_scroll(SCROLL_PAUSE_TIME=1, search=search, cssScronto=cssScronto)
    url_retrieve(total_image_count=total_image_count,next_addlink=next_addlink,imgUrlCrawl=imgUrlCrawl)