import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv 
import os

load_dotenv("tokens.env")

URL = os.getenv("URL")

def run_selenium_parse(doctor_name,date,city):
  print(f"--- [SELENIUM] Starts... ---")
  chrome_option = Options()
  chrome_option.add_argument("--headless")
  chrome_option.add_argument("--no-sandbox")
  chrome_option.add_argument("--disable-dev-shm-usage")
  chrome_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service,options=chrome_option)

  wait = WebDriverWait(driver,5)
  driver.get(URL)
  name = None

  try:
    cook = driver.find_element(By.CSS_SELECTOR, ".cookies-buttons #btnCookiesAll")
    cook.click()
    
    container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class='pos:r m-b:xl']")))

    town_ent = container.find_element(By.CSS_SELECTOR, "#lokalizacja input")
    town_ent.clear()
    town_ent.send_keys(city)
    time.sleep(0.5)
    town_ent.send_keys(Keys.ENTER)

    doctor_ent = container.find_element(By.CSS_SELECTOR, "#specjalizacja input")
    doctor_ent.clear()
    doctor_ent.send_keys(doctor_name)
    time.sleep(0.5)

    doctor_ent.send_keys(Keys.ENTER)

    first_dictor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"[id^='wynik_lekarz_']")))

    name_el = first_dictor.find_element(By.CSS_SELECTOR, ".thd-name a")
    name = name_el.text

    print(f"Name: {name}")

  except Exception as e:
    print(f"====== Error longer than 5 sec or ERROR_NAME: {e} ====== ")
  finally:
    driver.quit()
    print(f"--- [SELENIUM] Finished ---")
  
  return name
    


# Асинхронная обертка
# Aiogram работает асинхронно, а Selenium - синхронно.
# Чтобы бот не завис, мы запускаем Selenium в отдельном потоке через to_thread
async def search_doctors_func(doctor_name: str,date:str,city:str):
  result = await asyncio.to_thread(run_selenium_parse,doctor_name,date,city)
  return result