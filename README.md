# 🤖 Async Parsing Bot

A modular Telegram bot built with **Python 3.10+**, **Aiogram 3.x**, and **Selenium**. Designed to automate the search for doctor appointments and monitor product prices.

## 🚀 Features

### 1. 👨‍⚕️ Doctor Appointment Finder
* **Search by Name/Specialty:** User inputs a doctor's name or medical specialty.
* **Date Filtering:** User specifies a preferred date or time range.
* **Automated Parsing:** The bot scans medical aggregator websites for available slots.
* **Report Generation:** Exports a list of available appointments to an **Excel file**.

### 2. 🛍 Product Price Tracker
* **Category & Budget:** User selects a product category and sets a maximum budget.
* **Deal Hunting:** The bot parses e-commerce sites to find items within the budget.
* **Results:** Returns a structured list of products with prices and links.

### 3. 🏗 Core Architecture
* **Asynchronous:** Uses `aiogram`'s async capabilities to handle multiple users simultaneously without blocking.
* **FSM (Finite State Machine):** Implements guided user dialogs to collect necessary search criteria.
* **Background Processing:** Runs heavy Selenium tasks in separate threads (`asyncio.to_thread`) to keep the bot responsive.

---

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Bot Framework:** [Aiogram 3.x](https://docs.aiogram.dev/en/latest/)
* **Web Scraping:** [Selenium WebDriver](https://www.selenium.dev/)
* **Browser Manager:** `webdriver-manager`
* **Data Handling:** `pandas`, `openpyxl` (Planned for Excel export)
* **Database:** SQLite (Planned for storing user preferences)

---

## ⚙️ Installation & Setup

## 1. **Clone the repository:**
  (Cloning into a shorter folder name 'parsing-bot' for convenience)
  ```bash
  git clone [https://github.com/KaidoQQ/Async-Telegram-Bot-for-Data-Parsing-Doctors-Products-.git](https://github.com/KaidoQQ/Async-Telegram-Bot-for-Data-Parsing-Doctors-Products-.git) parsing-bot
  cd parsing-bot
  ```

## 2. **Create a virtual environment (optional but recommended):**
  * python -m venv venv
    # Windows:
  * venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate

## 3. **Install dependencies:**
  ```bash
    pip install aiogram selenium webdriver-manager pandas openpyxl
  ```

## 4. **Configure the Bot:**
  1. Open main.py
  2. Replace TOKEN = "YOUR_TOKEN_HERE" with your actual Telegram Bot Token from @BotFather.

## 5. **Run the Bot:**
  ```bash
    python bot.py
  ```

## 📂 Project Structure
```text
Parsing-bot/
├── bot.py                  # Entry point (Handlers, FSM, Menu)
├── tech/                   # Folder for system files
│   ├── database.py         # Data base creating file
│   └── to_exel.py           #Converter to exel file
├── parsers/                 # Logic for web scraping
│   ├── __init__.py
│   ├── doctor_parser.py     # Selenium logic for doctors
│   └── product_parser.py    # Selenium logic for products
└── README.md                # Project documentation
```

## 📝 Roadmap

* [x] Basic Bot Structure (Menu, Commands)

* [x] FSM Implementation (Dialog logic)

* [x] Selenium Integration (Headless browser setup)

* [ ] Real-time parsing logic for target websites

* [x] Excel report generation

* [ ] SQLite Database integration

*Created by [KaidoQQ](https://github.com/KaidoQQ)*
