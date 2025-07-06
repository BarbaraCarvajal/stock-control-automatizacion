from selenium import webdriver

def get_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver
