import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_selenium_parse(doctor_name,date):
  print(f"--- [SELENIUM] Starts... ---")
  chrome_option = Options()
  chrome_option.add_argument("--headless")
  chrome_option.add_argument("--no-sandbox")
  chrome_option.add_argument("--disable-dev-shm-usage")

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service,options=chrome_option)
  url = "https://www.google.com"

  try:
    driver.get(url)

    print(f"Title: {driver.title}")
    print(f"Searching for {doctor_name}")

    import time
    time.sleep(5)

    result_text = f"Im on google! Title: {driver.title}"
  except Exception as e:
    print(f"Error, {e}")
    result_text = "Something goes wrong"
  finally:
    driver.quit()
    print("--- [SELENIUM] Finished ---")
  
  return result_text

# Асинхронная обертка
# Aiogram работает асинхронно, а Selenium - синхронно.
# Чтобы бот не завис, мы запускаем Selenium в отдельном потоке через to_thread
async def search_doctors_func(doctor_name: str,date:str):
  result = await asyncio.to_thread(run_selenium_parse,doctor_name,date)
  return result