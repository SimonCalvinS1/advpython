import requests, os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("url_api")
response = requests.get(url)

if response.status_code == 200:
    print("Connected successfully\n")
    
    data = response.json()
    
    total_calories = 0
    recipe_count = 0
    
    for recipe in data['recipes']:
        name = recipe['name']
        calories = recipe['caloriesPerServing']
        cuisine = recipe['cuisine']
        
        print(f"Recipe: {name} ({cuisine}) =>> {calories} kcal/serving")
        
        total_calories += calories
        recipe_count += 1

    print("-" * 40)
    print(f"Total recipes processed: {recipe_count}")
    print(f"Total combined calories: {total_calories} kcal")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")