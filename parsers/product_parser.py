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
from datetime import datetime

load_dotenv("tokens.env")

URL = os.getenv("URL_product")

def search_products_func(category: str,budget:str):
  print(f"✳️ [SELENIUM] Starts...")
  print(f"Query: {category}, Date: {budget}")

  chrome_option = Options()
  chrome_option.add_argument("--headless")
  chrome_option.add_argument("--window-size=1920,1080")
  chrome_option.add_argument("--no-sandbox")
  chrome_option.add_argument("--disable-dev-shm-usage")
  chrome_option.add_argument("--disable-blink-features=AutomationControlled") 
  chrome_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service,options=chrome_option)

  wait = WebDriverWait(driver,7)
  driver.get(URL)
  name = None
  parsed_data = []
  
  try:
    cook = wait.until(EC.presence_of_element_located((By.ID, "sp-cc-accept")))
    cook.click()

    time.sleep(1.5)


    try:
      container = driver.find_element(By.ID, "twotabsearchtextbox")
      container.click()
      container.clear()
      container.send_keys(category)
      time.sleep(0.5)

      container.send_keys(Keys.ENTER)

      try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-component-type='s-search-results']")))
        new_budget = int(budget)


        try:
          min = driver.find_element(By.ID, "p_36/dynamic-picker-0")
          min_text_el = min.find_element(By.CSS_SELECTOR, "span.a-size-base")

          text = min_text_el.text
          new_text = text.replace("Do","").replace("zł","").strip()
          new_text = new_text.replace("\u00A0","").replace(" ","")
          min_text = int(new_text)

          if new_budget <= min_text:
            button = min.find_element(By.TAG_NAME,"a")
            button.click()

            time.sleep(1)
        except Exception as e:
          print(f"❌ [ERROR] Cant find a button with start price")

        try:
          menu = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
          print("✅ MENU was found")
          if menu:
            first = menu[0]
            print(f"✅ Item was found{first.text[:50]}")
        except Exception as e:
          print(f"❌ [ERROR] No results found or XPath error: {e}")

      except Exception as e:
        driver.save_screenshot("error_screenshot.png")
        print(f"❌ [ERROR] No menu was found {e}")

    except Exception as e:
      print("❌ [ERROR] No search-box was found")

  except Exception as e:
    print(f"⭕ [GLOBAL ERROR] Longer than 7 sec or ERROR_NAME: {e}")

  finally:
    driver.quit()
    print(f"✴️ [SELENIUM] Finished")

  return parsed_data
    


async def product_func(category: str,budget:str):
  result = await asyncio.to_thread(search_products_func,category,budget)
  return result