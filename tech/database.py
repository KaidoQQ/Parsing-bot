import sqlite3

class DataBase:
  def __init__(self,db_file):
    self.connection = sqlite3.connect(db_file)
    self.cursor = self.connection.cursor()
    self.create_tables()

  def create_tables(self):
    # Таблица пользователей
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    """)
    
    # Таблица истории поиска (логов)
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        search_type TEXT, 
        query_data TEXT,
        file_path TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    """)
    self.connection.commit()
  
  def add_user(self,user_id, username):
    with self.connection:
      self.cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
  
  def add_search_log(self, user_id, search_type, query_data, file_path):
    with self.connection:
      self.cursor.execute(
        "INSERT INTO search_history (user_id, search_type, query_data, file_path) VALUES (?, ?, ?, ?)",
        (user_id, search_type, query_data, file_path)
    )
      
  def get_cached_file(self, query_data):
    with self.connection:
      result = self.cursor.execute(
        "SELECT file_path FROM search_history WHERE query_data = ? ORDER BY date DESC LIMIT 1",
        (query_data,)
    ).fetchone()
      
      if result:
        return result[0]
      return None
  
  def close(self):
    self.connection.close()