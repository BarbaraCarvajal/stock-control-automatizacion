from config_rutas import SCREENSHOTS_DIR, PDFS_DIR
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def enmarcar_elemento(driver, elemento, color="#8E44AD", grosor=5):
    """Aplica un borde al elemento para resaltarlo visualmente"""
    driver.execute_script(
        "arguments[0].style.border='%spx solid %s'" % (grosor, color),
        elemento
    )

def desmarcar_elemento(driver, elemento):
    """Quita el borde del elemento resaltado"""
    driver.execute_script(
        "arguments[0].style.border=''", elemento
    )
