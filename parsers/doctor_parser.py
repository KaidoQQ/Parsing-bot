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

URL = os.getenv("URL")

def run_selenium_parse(doctor_name,date,city):
  print(f"✳️ [SELENIUM] Starts...")
  chrome_option = Options()
  chrome_option.add_argument("--headless")
  chrome_option.add_argument("--window-size=1920,1080")
  chrome_option.add_argument("--no-sandbox")
  chrome_option.add_argument("--disable-dev-shm-usage")
  chrome_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service,options=chrome_option)

  wait = WebDriverWait(driver,5)
  driver.get(URL)
  name = None
  parsed_data = []

  try:
    cook = driver.find_element(By.CSS_SELECTOR, ".cookies-buttons #btnCookiesAll")
    cook.click()
    time.sleep(1)
    
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

    try:
      first_doctor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"[id^='wynik_lekarz_']")))

      if first_doctor:
        doctors = driver.find_elements(By.CSS_SELECTOR, "[id^='wynik_lekarz_']")


        for doctor in doctors:
          if doctor:
            name_el = doctor.find_element(By.CSS_SELECTOR, ".thd-name a")
            ph_number = "No phone number"
            new_date = "Unknown"
            try:
              phone_btn = doctor.find_element(By.XPATH, ".//button[contains(@onclick, 'pokazTelefon')]")
              driver.execute_script("arguments[0].click();", phone_btn)

              time.sleep(0.5)
              phone_link = doctor.find_element(By.XPATH, ".//a[contains(@href, 'tel:')]")

              ph_number = phone_link.get_attribute("textContent").strip()

              if not ph_number:
                href_val = phone_link.get_attribute("href")
                if href_val:
                  ph_number = href_val.replace("tel:", "").strip()

              print("✅ Phone number of doctor was added")
              print(ph_number)
            except:
              print("❌ No phone number was found")

            name = name_el.text
            n_date = date.lower()
            n_date = n_date.replace(" ","")

            if n_date == "nearest":
              try:
                near_date_el = doctor.find_element(By.CSS_SELECTOR, ".tb-data")
                near_date = near_date_el.text
                new_date = convert_polish_date(near_date)
              except:
                try:
                  near_date_el = doctor.find_element(By.CSS_SELECTOR, ".tb-none")
                  near_date = near_date_el.text
                  new_date = "This doctor didnt indicate an upcoming date"
                except:
                  new_date = "Date info not found"

            try:
              street_el = doctor.find_element(By.CSS_SELECTOR, "span.device-n")
              street = street_el.text

              url_link = doctor.find_element(By.CSS_SELECTOR, "a[id^=linkNazwaZasobu_]")
              url = url_link.get_attribute("href")
            except Exception as e:
              print(f"❌ [ERROR] Something wrong {e}")


            parsed_doc = {
              'name' : name,
              'ph_number' : ph_number,
              'near_date' : new_date,
              'street': street,
              'link': url
            }

            parsed_data.append(parsed_doc)
            print(f"✅  Doctor: {name} | Tel: {ph_number} | Date: {new_date} | Street: {street} | Link: {url}")
            print()
          else:
            print("❌ [ERROR] cant find a doctor card!")
    except Exception as e:
      print(f"❌ [ERROR] no doctors was found {e}")

  except Exception as e:
    print(f"⭕ [GLOBAL ERROR] longer than 5 sec or ERROR_NAME: {e}")
  finally:
    driver.quit()
    print(f"✴️ [SELENIUM] Finished")
  
  if len(parsed_data) > 0:
    return parsed_data
  else:
    return []
    


def convert_polish_date(date_str):
  months_mapping = {
    "stycznia": "01",
    "lutego": "02",
    "marca": "03",
    "kwietnia": "04",
    "maja": "05",
    "czerwca": "06",
    "lipca": "07",
    "sierpnia": "08",
    "września": "09",
    "października": "10",
    "listopada": "11",
    "grudnia": "12"
  }
  try:
    clean_date = date_str.strip().lower()
    
    parts = clean_date.split()
    
    if len(parts) != 3:
      return date_str 
        
    day, month_name, year = parts
    
    month_number = months_mapping.get(month_name)
    
    if not month_number:
      return date_str 
        
    day = day.zfill(2)
    
    return f"{year}-{month_number}-{day}"
    
  except Exception as e:
    print(f"❌ [ERROR] Conversion: {e}")
    return date_str



# Асинхронная обертка
# Aiogram работает асинхронно, а Selenium - синхронно.
# Чтобы бот не завис, мы запускаем Selenium в отдельном потоке через to_thread
async def search_doctors_func(doctor_name: str,date:str,city:str):
  result = await asyncio.to_thread(run_selenium_parse,doctor_name,date,city)
  return result