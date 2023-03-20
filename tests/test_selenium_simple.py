from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

s = Service(r"C:\Users\Enot\PycharmProjects\seleniumproject\chromedriver.exe")
driver = webdriver.Chrome(service=s)
chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = r"C:\Users\Enot\PycharmProjects\seleniumproject\chromedriver.exe"


def test_search_example():
    driver.get('https://google.com')
    time.sleep(2)
    search_input = driver.find_element(By.NAME, 'q')
    search_input.clear()
    search_input.send_keys('first test')
    time.sleep(2)
    search_button = driver.find_element(By.NAME, 'btnK')
    search_button.submit()  # метод click() не сработает (так как кнопка скрыта другим элементом)
    time.sleep(2)
    driver.save_screenshot('result.png')



def test_petfriends():
    # Open PetFriends base page:
    driver.get("https://petfriends.skillfactory.ru/")

    time.sleep(2)  # just for demo purposes, do NOT repeat it on real projects!

    # click on the new user button
    btn_newuser = driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()
    time.sleep(2)

    # click existing user button
    btn_exist_acc = driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт")  # u
    btn_exist_acc.click()

    time.sleep(2)
    # add email
    field_email = driver.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("api@api")

    time.sleep(2)
    # add password
    field_pass = driver.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("api@api")

    # click submit button
    btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    time.sleep(3)  # just for demo purposes, do NOT repeat it on real projects!
    if driver.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        # Make the screenshot of browser window:
        driver.save_screenshot('result_petfriends.png')
    else:
        raise Exception("login error")