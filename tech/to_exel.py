import asyncio
import pandas as pd
import os

def creator_excel(data,filename="doctors_list.xlsx"):
  if not data:
    print("❌ [ERROR] NO DATA FOR EXCEL")
    return None
  try:
    if isinstance(data,dict):
      data = [data]

    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
      os.makedirs(directory)
      print(f"📁 Created directory: {directory}")

      
    df = pd.DataFrame(data)
    df.rename(columns={
      'name': 'Name',
      'ph_number': 'Phone number',
      'near_date': 'Nearest date', 
      'street' : 'Street',
      'link': 'URL'
    }, inplace=True)

    df.to_excel(filename,index=False)
    print("✅  Excel file was created!")

    return os.path.abspath(filename)
  except Exception as e:
    print(f"❌ [ERROR] while creating Excel: {e}")
    return None
  

async def excel_file(data,filename="doctors_list.xlsx"):
  result = await asyncio.to_thread(creator_excel,data,filename)
  return result