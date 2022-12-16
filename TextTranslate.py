from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def creatURL(start_lng = "en", final_lng="ru", text=""):
    url = "https://www.deepl.com/ru/translator#"
    url += start_lng + "/" + final_lng + "/"+text.replace(" ", "%20").replace("\n", " %0A")
    return url


def translate(text="", start_lng = "en", final_lng="ru"):
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")

    driver = webdriver.Chrome(
            executable_path="C:\\Users\\123\\Desktop\\progs\\Python\\Projects\\Text_recognition\\RELISE\\drivers\\chromedriver.exe",
            options=options
            )
    url = creatURL(start_lng=start_lng, final_lng=final_lng, text=text)
    try:
        driver.get(url=url)
        time.sleep(7)
        element = driver.find_element(By.ID, "target-dummydiv")
        answ = element.get_attribute("textContent")
    except Exception as ex:
        return ex
    finally:
        driver.close()
        driver.quit()
        return answ

