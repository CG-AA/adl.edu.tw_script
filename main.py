from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import threading
import json

def focus_window(driver: webdriver.Chrome):
    # alert the window and accept
    script = "alert('focus')"
    driver.execute_script(script)
    driver.switch_to.alert.accept()

def fake_focus_window(driver: webdriver.Chrome):
    script = "window.focus();"
    driver.execute_script(script)

def create_driver():
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService(executable_path = '/media/cg/D/WorkSpace/adl.edu.tw_script/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# click mission(multiple times)
def click_mission(driver: webdriver.Chrome, mission_name, times = 1):
    driver.find_element(By.XPATH, "//*[contains(text(), '" + mission_name + "')]").click()
    driver.implicitly_wait(10)
    for i in range(times):
        driver.find_element(By.XPATH, "//*[contains(text(), '前往任務')]").click()

def close_news(driver: webdriver.Chrome):
    driver.find_element(By.CLASS_NAME, "btn.defaultBtn.closeNews").click()

def handle_login(driver: webdriver.Chrome):
    focus_window(driver)
    # Open a URL
    driver.get("https://adl.edu.tw/login.php")

    with open("senstive.json", "r") as f:
        j = json.load(f)
        # Selet dropdown
        select = Select(driver.find_element(By.NAME, "school[0]"))
        select.select_by_visible_text(j["city"])
        select = Select(driver.find_element(By.NAME, "school[1]"))
        select.select_by_visible_text(j["district"])
        select = Select(driver.find_element(By.NAME, "school[2]"))
        select.select_by_visible_text(j["school"])

        # Input username and password
        driver.find_element(By.NAME, "username").send_keys(j["account"])
        driver.find_element(By.NAME, "password").send_keys(j["password"])

    # let user input the captcha
    captcha = driver.find_element(By.NAME, "captcha_code")
    captcha.click()

    # wait untill the url changed
    while driver.current_url == "https://adl.edu.tw/login.php":
        time.sleep(1)
    time.sleep(20)

def driverScript(driver: webdriver.Chrome):
    while 1:
        time.sleep(5)
        fake_focus_window(driver)
        # if has 確定 and a spec class and is button, click it
        if len(driver.find_elements(By.XPATH, "//*[contains(text(), '確定') and @class='swal2-confirm swal2-styled']")) > 0:
            driver.find_element(By.XPATH, "//*[contains(text(), '確定') and @class='swal2-confirm swal2-styled']").click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "fas.fa-play").click()

    # ### quiz
    # # back to main tab
    # driver.switch_to.window(handles[0])

    # # refresh
    # driver.refresh()
    # close_news(driver)
    # # select mission by visible text
    # click_mission(driver, "Ib-Ⅳ-5臺灣的災變現象包括颱風、梅雨、寒潮、乾旱等現象", 10)

if __name__ == "__main__":
    driver_count = 10

    drivers = [create_driver() for i in range(driver_count)]

    threads = []
    for driver in drivers:
        handle_login(driver)
        thread = threading.Thread(target=driverScript, args=(driver,))
        threads.append(thread)
        thread.start()

    # wait
    input("Wait for finish...")

    for thread in threads:
        thread.join()
    
