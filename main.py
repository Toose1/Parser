import requests
import json
import csv

from fake_useragent import UserAgent
from pydantic import BaseModel
from bs4 import BeautifulSoup
from typing import Dict, Any



class Product(BaseModel):
    product: str
    calories: str
    proteins: str
    fats: str
    carbohydrates: str
    

def get_all_categories() -> Dict[str, str]:
    headers = { "Accept": "*/*",
                "User-Agent": f"{UserAgent().random}" }
    resp = requests.get("http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie", headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    
    all_categories: Dict[str, str] = {}
    categories = soup.find_all("a", class_="mzr-tc-group-item-href")
    
    for category in categories:
        title = category.text
        link = category.get("href")
        full_link = f"http://health-diet.ru{link}"
        all_categories[title] = full_link
    
    return all_categories




def get_info_category(name_category: str, link: str) -> None:
    headers = { "Accept": "*/*",
                "User-Agent": f"{UserAgent().random}" }
    resp = requests.get(link, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")

    
    products: list[dict[str, str]] = []
    category_table = soup.find("table", class_="mzr-tc-group-table").find("thead").find("tr").find_all("th")
    titles = (category_table[0].text, category_table[1].text, category_table[2].text, category_table[3].text, category_table[4].text)

    chars = [' ', ',', '-', '\'']
    for char in chars:
        if char in name_category:
            name_category = name_category.replace(char, '_')
    
    csv_creater(name_category, titles)

    category_products = soup.find("table", class_="mzr-tc-group-table").find("tbody").find_all("tr")
    for product_td in category_products:
        product = product_td.find_all("td")
        obj = Product(product=product[0].text[:-1], calories=product[1].text,
                                proteins=product[2].text, fats=product[3].text,
                                carbohydrates=product[4].text)
        csv_writer(name_category, obj)
        products.append(obj.model_dump())

    json_writer(name_category, products)
    
    
    



def json_writer(name_file: str, products: list[dict[str, str]]) -> None:
    with open(f"products_calories/{name_file}.json", "a", encoding="UTF-8") as file:
        json.dump(products, file, indent=4, ensure_ascii=False)


def csv_creater(name_file: str, titles: tuple) -> None:
    with open(f"products_calories/{name_file}.csv", "w", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(titles)



def csv_writer(name_file: str, product: Product) -> None:
    with open(f"products_calories/{name_file}.csv", "a", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow((product.product, product.calories,
                         product.proteins, product.fats, product.carbohydrates))


def main() -> None:
    
    #get_info_category("Баранина и дичь", "http://health-diet.ru/base_of_food/food_24507/")
    pass



if __name__ == "__main__":
    main()