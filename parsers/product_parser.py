import asyncio

async def search_products_func(category: str,budget:str):
  print(f"--- [LOG] Product Parser Started ---")
  print(f"Query: {category}, Date: {budget}")

  await asyncio.sleep(3)

  print(f"--- [LOG] Product Parser Finished ---")
  return "products_result.xlsx"