from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os
from selenium.webdriver.common.by import By
import yaml
from Utils.logger import logger
import ssl

def google_scroll(SCROLL_PAUSE_TIME,search,cssScronto,driver):
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
    
def url_retrieve(total_image_count,next_addlink,imgUrlCrawl,driver,search):
    images = driver.find_elements(By.XPATH,next_addlink)
    print(f'{"*"*60}Crawlling started.{"*"*60}')
    count = 1
    print(len(images))
    for image in images:
        try:
            try:
                image.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", image)
                except:
                    pass
            imgUrl = driver.find_element(By.XPATH,imgUrlCrawl).get_attribute('src')
            altUrl = driver.find_element(By.XPATH,imgUrlCrawl).get_attribute('alt')
            if check_url(altUrl.lower(),"minion"):
                urllib.request.urlretrieve(url=imgUrl, filename=f"image/{search}/" + altUrl + "_" + str(count) + ".jpg")            
                logger(f'logs/{search}.log',f'{altUrl}_{count}')
                count+=1
            else:
                pass
            if count > total_image_count:
                break
        except Exception as e:
            pass
    print(f'{"*"*60}Crawlling Completed.{"*"*60}')

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    search = "minion" #input image name
    total_image_count = 10 #input image count
    config_path = 'configs/config.yml'
    config = load_config(config_path)
    
    next_addlink = config['xpath']['next_addlink']
    imgUrlCrawl = config['xpath']['imgUrlCrawl']
    urlGoogleSearch = config['url']['urlGoogleSearch']
    cssScronto = config['css']['cssScronto']
    urlGoogleSearch = config['url']['urlGoogleSearch']
    
    ssl._create_default_https_context = ssl._create_unverified_context
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--password-store=basic")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--enable-automation")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-software-rasterizer")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(urlGoogleSearch)
    
    if not os.path.isdir(f"image/{search}/"):
        os.makedirs(f"image/{search}/")

    google_scroll(SCROLL_PAUSE_TIME=5, search=search, cssScronto=cssScronto,driver=driver)
    url_retrieve(total_image_count=total_image_count,next_addlink=next_addlink,imgUrlCrawl=imgUrlCrawl,driver=driver,search=search)
    driver.quit()

if __name__ == '__main__':
    main()