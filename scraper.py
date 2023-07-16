from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.ulta.com/shop/makeup/lips"

product_links = []
for num in range(1,9):
    new_url = url + f"?page={num}"
    page = requests.get(new_url)
    soup = BeautifulSoup(page.content, "lxml")
    product_list = soup.find_all("div", class_="ProductCard")
    for item in product_list:
        for link in item.find_all("a", href=True):
            product_links.append(link["href"])
            set(product_links)

lipstick_list = []
for link in product_links:
    r= requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        name = soup.find("div", class_="ProductInformation").text
    except:
        name = name = soup.find("h1", class_="Text-ds Text-ds--body-1 Text-ds--left").text
    finally:
        name = "No results"
    price = soup.find("div", class_="ProductPricing").text
    try:
        rating = soup.find("div", class_="ReviewStars__Content").text
    except:
        rating = "No results"
    try:
        reviews = soup.find("div", class_="ProductReviews__Content").text
    except:
        reviews = "No results"
    try:
        conscious = soup.find("div", class_="SummaryCard").text
    except:
        conscious = "No results"
    details = soup.find("div", class_="ProductDetail__Content").text
    lipstick_info = {
        "name":name,
        "price":price,
        "rating":rating,
        "details":details,
        "reviews":reviews,
        "conscious":conscious
    }
    lipstick_list.append(lipstick_info)

df = pd.DataFrame(lipstick_list)
df.to_csv("scraper.csv")
df.to_excel('lipgloss.xlsx')