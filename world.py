from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


# Opening the connection and grabbing the page
my_url = 'https://yandex.ru/covid19/stat'
option = Options()
option.headless = False
driver = webdriver.Chrome(options=option)
driver.get(my_url)
driver.maximize_window()


world_button = WebDriverWait(driver,  20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div/button[3]')))

world_button.click()

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[2]')))
loc = element.location
size = element.size


print(loc)
print(size)

action = webdriver.ActionChains(driver)
action.move_to_element_with_offset(element, -1, 0).perform()

infected = [driver.find_element_by_xpath('/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[22]/div[1]/span[1]').text]
death = [driver.find_element_by_xpath('/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[22]/div[2]/span').text]
date = [driver.find_element_by_xpath('/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[22]/div[4]/span').text]


pace = -1

action.reset_actions()

while True:
    action.move_to_element_with_offset(element, -1, 0)
    action.move_by_offset(pace, 0)
    action.perform()
    action.reset_actions()
    infected_ = driver.find_element_by_xpath(
        '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[22]/div[1]/span[1]').text
    death_ = driver.find_element_by_xpath(
        '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[22]/div[2]/span').text
    date_ = driver.find_element_by_xpath(
        '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[22]/div[4]/span').text


    if (infected_ == '5 790') and (death_ == '307') and (date_ == '12 МАР'):
        infected.append(infected_)
        death.append(death_)
        date.append(date_)
        break

    if (date_ == date[-1]) and (death_ == death[-1]) and (infected_ == infected[-1]):
        pace -= 1
        pass
    else:
        infected.append(infected_)
        death.append(death_)
        date.append(date_)
        pace -= 1

dictionary = {"date": date, "infected": infected, "death": death}

driver.quit()

df = pd.DataFrame.from_dict(dictionary)

df.to_csv("corona_yan_world.csv")