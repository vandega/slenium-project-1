import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv


options = Options()
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
options.add_argument('--headless')

service = Service(executable_path='driver/chromedriver')

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://www.jobs.ge')
    time.sleep(1)

    driver.find_element(by=By.NAME, value='has_salary').click()
    time.sleep(1)

    # can be changed to get some other info
    search = driver.find_element(by=By.NAME, value='q')
    target = str(input('search: '))
    search.send_keys(target, Keys.ENTER)
    time.sleep(1)

    scroll_duration = 5
    scroll_end = time.time() + scroll_duration

    # scrolling site
    while time.time() < scroll_end:
        driver.execute_script("window.scrollBy(0, 10000);")
        time.sleep(0.5)

    jobs = driver.find_elements(by=By.CLASS_NAME, value='vip')

    for i in jobs:
        title = i.text
        i.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        xpath = ['//*[@id="job"]/table/tbody/tr/td[1]/table[2]/tbody/tr[4]/td/b[3]', '//*[@id="job"]/table/tbody/tr/td[1]/table[2]/tbody/tr[4]/td/b[4]']

        for path in xpath:
            try:
                salary = driver.find_element(by=By.XPATH, value=f'{path}').text
                if int(salary[0]):
                    with open('collected_data.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow((
                            title,
                            salary
                        ))

            except:
                continue



        driver.close()
        driver.switch_to.window(driver.window_handles[0])

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()
