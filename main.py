from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

def perform_actions(action):
    """ Perform and reset actions """
    action.perform()
    action.reset_actions()
    for device in action.w3c_actions.devices:
        device.clear_actions()


def main():
    # Opening the connection and grabbing the page
    my_url = 'https://yandex.ru/covid19/stat'
    option = Options()
    option.headless = False
    driver = webdriver.Chrome(options=option)
    driver.get(my_url)
    driver.maximize_window()


    action = webdriver.ActionChains(driver)

    element = WebDriverWait(driver,
                                  20).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[3]')))
    loc = element.location
    size = element.size


    #print(loc)
    #print(size)


    action.move_to_element_with_offset(element, 1, 0).perform()

    infected = [driver.find_element_by_xpath('/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]/div[1]/span[1]').text]
    death = [driver.find_element_by_xpath('/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]/div[2]/span').text]
    date = [driver.find_element_by_xpath('/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]/div[4]/span').text]


    pace = -1


    while True:
        action.move_to_element_with_offset(element, 1, 0)
        action.move_by_offset(pace, 0)
        perform_actions(action)
        infected_ = driver.find_element_by_xpath(
            '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]/div[1]/span[1]').text
        death_ = driver.find_element_by_xpath(
            '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]/div[2]/span').text
        date_ = driver.find_element_by_xpath(
            '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]/div[4]/span').text

        element = WebDriverWait(driver,
                                20).until(EC.presence_of_element_located((By.XPATH,
                                                                          '/html/body/main/section/div/section[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[3]/div/div[20]')))




        if infected_ == "32" and death_ == "0" and date_ == "12 МАР":
            infected.append(infected_)
            death.append(death_)
            date.append(date_)
            break

        if (date_ in date) and (death_ in death) and (infected_ in infected):
            pass
        else:
            infected.append(infected_)
            death.append(death_)
            date.append(date_)

    dictionary = {"date": date, "infected": infected, "death": death}

    driver.quit()

    df = pd.DataFrame.from_dict(dictionary)

    df.to_csv("corona_yan.csv")


if __name__ == '__main__':
    main()