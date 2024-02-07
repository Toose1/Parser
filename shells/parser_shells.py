from bs4 import BeautifulSoup
import requests
import csv

from typing import List
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    brand: str
    price: str
    image: str
    link: str


def parser(pages: int) -> List[Product]:
    list_products: List[Product] = []

    for i in range(1, pages+1):
        url = f"https://glavsnab.net/santehnika/rakoviny-i-komplektuyushchiye/rakoviny.html?p={i}"
        resp = requests.get(url=url)
        soup = BeautifulSoup(resp.text, "lxml")
        products = soup.find_all("div", class_="product-card oneclick-enabled")

        for product in products:
            image = product.get("data-product-image")
            name = product.get("data-product-name")
            brand = product.get("data-product-brand")
            link = product.find("a", itemprop="url").get("href")
            price_el = product.find("span", class_="num")
            if price_el:
                price = price_el.get("content")
            else:
                price = "По запросу"

            list_products.append(Product(name=name, brand=brand, price=price, image=image, link=link))

    return list_products

    
        
def create_csv() -> None:
    with open(r"data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "brand", "price", "image", "link"])
        

def write_csv(products: List[Product]) -> None:
    with open(r"data.csv", "a", encoding="UTF-8") as file:
        writer = csv.writer(file)
        
        for product in products:
            writer.writerow([product.name, product.brand, product.price, product.image, product.link])



def main() -> None:
    products = parser(21)
    create_csv()
    write_csv(products=products)