from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
data = open('data.csv', 'r', encoding='UTF8')
reader = csv.reader(data)
header = next(reader)
rows = []
for row in reader:
    rows.append(row)
results = open('results.csv', 'w', encoding='UTF8')
writer = csv.writer(results)
writer.writerow(["title", "amount", "status", "comment", "balance"])
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("http://127.0.0.1:5501")
for data in rows:
    browser.execute_script('window.localStorage.clear();')
    browser.get("http://127.0.0.1:5501")
    title = browser.find_element_by_id("text")
    amount = browser.find_element_by_id("amount")
    title.send_keys(data[0])
    amount.send_keys(data[1])
    browser.find_element_by_xpath('//*[@id="form"]/button').click()
    try:
        WebDriverWait(browser, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
        alert = browser.switch_to.alert
        alert.accept()
        data.extend(["failed", "got an alert"])
        writer.writerow(data)
    except TimeoutException:
        balance = browser.find_element_by_id("balance")
        ul = browser.find_element_by_id("list")
        if(not ul.find_elements_by_xpath("*")):
            data.extend(
                ["failed", "no alert, not added in history, wrong balance", balance.get_attribute('innerHTML')])
            writer.writerow(data)
        elif(balance.get_attribute('innerHTML') == "$"+str("{:.2f}".format(float(data[1])))):
            data.extend(["success", "no alert,added in history , right balance",
                        balance.get_attribute('innerHTML')])
            writer.writerow(data)
        else:
            print(balance.get_attribute('innerHTML'))
            print("$"+str(float(data[1])))
            data.extend(["failed", "no alert,added in history, but wrong balance",
                        balance.get_attribute('innerHTML')])
            writer.writerow(data)

browser.close()
