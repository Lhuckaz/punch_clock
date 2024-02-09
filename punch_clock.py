import os, time, random, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from workalendar.america import BrazilSaoPauloCity

def is_workday():
    cal = BrazilSaoPauloCity()
    today = datetime.datetime.now().date()
    return cal.is_working_day(today) and not cal.is_holiday(today)

def is_vacation():
    vacation_path = "vacation/date.txt"
    if not os.path.exists(vacation_path):
        return False
    else:
        with open(vacation_path, "r") as file:
            datas_especificas = [datetime.datetime.strptime(data.strip(), "%d/%m/%Y").date() for data in file]
        if datetime.datetime.now().date() in datas_especificas:
            return True
        else:
            return False
    
def punch_clock():
    if not is_workday():
        print("Not a workday. Exiting...")
        return

    if is_vacation():
        print("Is vacation. Exiting...")
        return

    url = os.environ.get("URL", "http://site.com")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    description = os.environ.get("DESCRIPTION")

    if not user or not password:
        print("Credentials not found in environment variables.")
        return

    delay = random.randint(1, 1200)  # 1200 seconds = 20 minutes
    print(f"Waiting for {delay} seconds before opening the browser.")
    time.sleep(delay)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote("http://chrome:4444/wd/hub", options=chrome_options)

    driver.get(url)

    input_user = driver.find_element("name", "login")
    input_user.send_keys(user)
    input_user.send_keys(Keys.TAB)

    input_password = driver.find_element("name", "password")
    input_password.send_keys(password)
    input_password.send_keys(Keys.RETURN)

    current_time = datetime.datetime.now().time()
    refer_time = datetime.time(11, 0, 0)
    if current_time < refer_time:
        input_description = driver.find_element("id", "descricao")
        input_description.send_keys(description)
    else:
        print("Do not insert description")

    button = driver.find_element("id", "submitponto")
    button.click()

    time.sleep(5)

    driver.quit()

punch_clock()

