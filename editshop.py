from ast import Index
import sys
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
import time
import random
import json
from cleantext import clean
mail = input("Enter your google email: ")
password = input("Enter your google password: ")
product_id = input("Enter product ID of Shopify: ")
amazon_id = input("Enter product ID of Amazon: ")






driver = uc.Chrome(use_subprocess=True)
driver.get('Link to reviews in your apps to edit them')
time.sleep(0.7)
email = driver.find_element(By.XPATH, '//input [@type="email"]')
email.send_keys(mail) 
while True:
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button [@type="submit"]')))
    except TimeoutException:
        exit()
            
    email.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div [@id="identifierNext"]')))
    driver.find_element(By.XPATH, '//div [@id="identifierNext"]').click()   
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input [@type="password"]')))
    clickpass = driver.find_element(By.XPATH, '//input [@type="password"]')
    clickpass.send_keys(password)
    time.sleep(0.5)
    clickpass.send_keys(Keys.ENTER)

    #Switches to iframe & searches for a product
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//iframe [@name="app-iframe"]')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe [@name="app-iframe"]'))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//iframe [@name="internal-api-iframe"]')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe [@name="internal-api-iframe"]'))
    searchbar = driver.find_element(By.XPATH, '//input [@type="search"]')
    time.sleep(0.5)
    searchbar.send_keys(product_id)
    searchbar.send_keys(Keys.ENTER)
    time.sleep(3)
    #Edits reviews
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span [@class="btn btn-xs btn-raised btn-default ali-reviews-edit-btn"]')))
    btn = driver.find_elements(By.XPATH, '//span [contains(text(), "Edit")]')
    loop_num = 0
    while True:
        for i in range((len(btn))):
            print(i)
            try: 
                WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'dynatable-processing')))
                driver.find_elements(By.XPATH, '//span [contains(text(), "Edit")]')[i].click()
            except IndexError:
                print("Done!")
                time.sleep(2)
                driver.close()
                sys.exit()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span [@class="btn btn-primary btn-raised review-editor__submit-btn"]')))
            submit_btn = driver.find_element(By.XPATH, '//span [@class="btn btn-primary btn-raised review-editor__submit-btn"]')
            review_body = driver.find_element(By.XPATH, '//textarea [@class="review-edit-form__body-input review-edit-form__form-control"]')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//textarea [@class="review-edit-form__body-input review-edit-form__form-control"]')))
            f = open(amazon_id + "-reviews.json", "r")
            data = json.load(f)
            review_body.clear()
            print(data[loop_num]['body'])
            review_body.send_keys(data[loop_num]['body'])
            loop_num += 1
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(0.5)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span [contains(text(), "Edit")]')))
            WebDriverWait(driver, 10).until(EC.invisibility_of_element(((By.XPATH, 'div[@class="css-loading-bar__bar"]'))))
            time.sleep(3)
            if i == (len(btn)-1):
                    driver.find_element(By.XPATH, '//a [@class="dynatable-page-link dynatable-page-next"]').click()
                    WebDriverWait(driver, 10).until(EC.invisibility_of_element(((By.XPATH, '//a [@class="dynatable-page-link dynatable-page-next"]'))))
                    time.sleep(3)  
        continue
    


