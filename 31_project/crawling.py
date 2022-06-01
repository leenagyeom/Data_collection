from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from urllib.request import (urlopen, urlparse, urlretrieve)

chrome_path = "./chromedriver.exe"
base_url = "https://www.google.co.kr/imghp"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("lang=ko_kr") # 한국어
chrome_options.add_argument("window-size=1920x1080") # 윈도우 사이즈 조절 = 크롤링 뜨는 창의 크기


def selenium_scroll_option():
    SCROLL_PAUSE_SEC = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

a = ["망고", "용과", "리치", "두리안"]

for i in a :
    if i == "망고":
        image_name = "mango"
    elif i == "용과":
        image_name = "dragon_fruit"
    elif i == "리치":
        image_name = "lychee"
    elif i == "두리안":
        image_name = "durian"
    driver = webdriver.Chrome(chrome_path)
    driver.get("http://www.google.co.kr/imghp?hl=ko")
    browser = driver.find_element_by_name('q')
    browser.send_keys(i)
    browser.send_keys(Keys.RETURN)


    selenium_scroll_option()
    driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
    selenium_scroll_option()

    image = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

    image_url = []
    for i in image:
        if i.get_attribute("src") != None:
            image_url.append(i.get_attribute("src"))
        else:
            image_url.append(i.get_attribute("data-src"))

    image_url = pd.DataFrame(image_url)[0].unique()

    os.makedirs(f"./tropical_fruit/{image_name}", exist_ok=True)
    dirname = f"./tropical_fruit/{image_name}"
    print(f"{image_name} 전체 >>", len(image_url))
    for t, url in enumerate(image_url, 0):
        urlretrieve(url, dirname + "\\" + image_name + "_" + str(t) + ".png")

driver.close()
print("완료")