import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

s = Service(r"C:\Users\Enot\PycharmProjects\seleniumproject\chromedriver.exe")
driver = webdriver.Chrome(service=s)
chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = r"C:\Users\Enot\PycharmProjects\seleniumproject\chromedriver.exe"
driver.maximize_window()

def test_pf():
    driver.get("https://petfriends.skillfactory.ru/")

    btn_newuser = driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()
    time.sleep(2)

    btn_exist_acc = driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт")
    btn_exist_acc.click()
    time.sleep(2)

    field_email = driver.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("cosmicship@yandex.ru")
    time.sleep(2)

    field_pass = driver.find_element(By.ID,"pass")
    field_pass.clear()
    field_pass.send_keys("Petf19833891")
    time.sleep(2)

    btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()


def test_show_my_pets():
    # Тест проверяет, что открывается страница "Мои питомцы"
    # Нажимаем на кнопку "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()

    if driver.current_url == 'https://petfriends.skillfactory.ru/my_pets':
        # Делаем скриншот:
        driver.save_screenshot('result_petfriends.png')
    else:
        raise Exception("login error")

# Проверяем что мы оказались на странице "Мои питомцы"
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'


def test_number_of_my_pets():
    #Тест проверяет, что на странице "Мои питомцы" отображаются все карточки животных

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

    # Сохраняем в переменную элементы поля статистики
    pets_statistics = driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    # Сохраняем в переменную элементы карточек питомцев
    pets_table = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Получаем количество питомцев из данных статистики
    number_of_pets = pets_statistics[0].text.split('\n')
    number_of_pets = number_of_pets[1].split(' ')
    number_of_pets = int(number_of_pets[1])

    #Получаем количество карточек питомцев
    pets_amount = len(pets_table)

    # Неявные ожидания:
    driver.implicitly_wait(10)

    #Проверяем, что количество питомцев из статистики совпадает с количеством карточек питомцев
    assert number_of_pets == pets_amount


def test_half_pets_with_photo():
    #Тест проверяет, что хотя бы половина карточек животных имеют фото

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))

    # Сохраняем в переменную элементы поля статистики
    pets_statistics = driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # Сохраняем в переменную элементы с атрибутом img
    photos = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # Получаем количество питомцев из данных статистики
    number_of_pets = pets_statistics[0].text.split('\n')
    number_of_pets = number_of_pets[1].split(' ')
    number_of_pets = int(number_of_pets[1])

    # Находим половину от количества питомцев
    half_of_pets = number_of_pets // 2

    # Неявные ожидания:
    driver.implicitly_wait(10)

    # Находим количество питомцев с фотографией
    number_of_photos = 0
    for i in range(len(photos)):
        if photos[i].get_attribute('src') != '':
            number_of_photos += 1

    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert half_of_pets <= number_of_photos


def test_pets_name_age_type():
    # Тест проверяет, что у всех животных имеется имя, возраст, порода

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную элементы с данными о животных
    pets_data = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Явное ожидание:
    wait = WebDriverWait(driver, 5)

    # Ожидаем, что данные всех животных отображаются на странице:
    for i in range(len(pets_data)):
        assert wait.until(EC.visibility_of(pets_data[i]))

    # Ожидаем, что найденные имена животных отображаются странице:
    names_of_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(names_of_pets)):
        assert wait.until(EC.visibility_of(names_of_pets[i]))

    # Ожидаем, что найденные породы животных отображаются на странице:
    types_of_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    for i in range(len(types_of_pets)):
        assert wait.until(EC.visibility_of(types_of_pets[i]))

    # Ожидаем, что данные возраста питомцев отображаются на странице:
    age_of_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_of_pets)):
        assert wait.until(EC.visibility_of(age_of_pets[i]))


def test_all_pets_with_different_names():
    # Тест проверяет, что все животные имеют разные имена

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную элементы с данными о питомцах
    names_of_pets = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Неявные ожидания:
    driver.implicitly_wait(10)

    # Проверяем, что у всех питомцев разные имена:
    names_list = []
    for i in range(len(names_of_pets)):
        names_list.append(names_of_pets[i].text)
    set_pet_data = set(names_list)
    assert len(names_list) == len(set_pet_data)


def test_all_pets_unique():
    # Тест проверяет, что нет повторяющихся животных

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    # Сохраняем в переменную элементы с данными о питомцах
    pets = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Неявные ожидания:
    driver.implicitly_wait(10)

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_pets = []
    for i in range(len(pets)):
        list_data = pets[i].text.split("\n")
        list_pets.append(list_data[0])
    set_pets = set(list_pets)

    #Проверяем, что длина списка и массива совпадают

    assert len(list_pets) == len(set_pets)
