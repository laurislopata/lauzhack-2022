from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import platform
from webdriver_manager.chrome import ChromeDriverManager

import re

EMAIL = 'laurynas.lopata@epfl.ch'
PASS = 'VZqP%86QUoBph6*Zjv*'


def seleniumScript(filename):
    PLATFORM = 'https://chat.openai.com/'

    CODE = open(filename, mode='r').read()

    # CODE = "How much memory in bytes does this code allocate: " + code_from_file

    # print(CODE)

    # op = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    driver.get(PLATFORM)
    time.sleep(1)

    elem = driver.find_element("xpath", '/html/body/div/div/div/div[4]/button[1]')
    elem.click()
    time.sleep(3)

    elem = driver.find_element("xpath", '/html/body/main/section/div/div/div/form/div[1]/div/div/div/input')
    elem.send_keys(EMAIL)
    time.sleep(2)

    elem = driver.find_element("xpath", '/html/body/main/section/div/div/div/form/div[2]/button')
    elem.click()
    time.sleep(2)

    elem = driver.find_element("xpath", '/html/body/main/section/div/div/div/form/div[1]/div/div[2]/div/input')
    elem.send_keys(PASS)
    time.sleep(2)

    elem = driver.find_element("xpath", '/html/body/main/section/div/div/div/form/div[2]/button')
    elem.click()
    time.sleep(2)

    elem = driver.find_element("xpath", '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button')
    elem.click()
    time.sleep(2)

    elem = driver.find_element("xpath", ' /html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]')
    elem.click()
    time.sleep(2)

    elem = driver.find_element("xpath", '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]')
    elem.click()
    time.sleep(2)

    elem = driver.find_element("xpath", '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/textarea')
    elem.send_keys(CODE)
    time.sleep(5)

    elem = driver.find_element("xpath", '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button')
    elem.click()
    time.sleep(15)

    elem = driver.find_element("xpath", '/html/body/div/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/p')
    time.sleep(1)

    answer = elem.text
    temp_ls = [int(s) for s in re.findall(r'\b\d+\b', answer)]

    return temp_ls

            # elem.click()
    # return "Hello"
    # op.add_argument('headless') 

ls = []

for i in range(2):
    ls.append(seleniumScript("code.txt"))

flat_list = [item for sublist in ls for item in sublist]

if len(flat_list) > 0:
    print(max(flat_list))
else:
    print(128)

ls = []

for i in range(2):
    ls.append(seleniumScript("code2.txt"))

flat_list = [item for sublist in ls for item in sublist]

if 'constant' in flat_list:
    print("constant")
elif 'O(n)' in flat_list or 'linear' in flat_list:
    print("n")
elif 'O(n^2)' in flat_list or 'quadratic' in flat_list:
    print("n^2")
elif 'log' in flat_list:
    print("nlog")
else:
    print("log")

