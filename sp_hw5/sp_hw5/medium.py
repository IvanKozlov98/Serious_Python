from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from aiomisc import threaded
import itertools
import json


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    items = soup.find_all("div", {"data-marker": "item"})

    entry_items = []
    # Print the text content of the matched elements
    for item in items:
        # get price
        price_element = [el for el in item.find_all("meta", itemprop="price")][0]
        price = price_element.get("content")
        # get name
        name_element = [el for el in item.find_all("h3", itemprop="name")][0]
        name = name_element.string
        # location
        geo_element = [el for el in item.find_all("div", class_="geo-root-zPwRk iva-item-geo-_Owyg")][0]
        city_name = geo_element.find('span').string
        # get description
        description_element = [el for el in item.find_all("div", class_="iva-item-descriptionStep-C0ty1")][0]
        description = description_element.string
        # url
        part_ref = [a_tag.get("href") for a_tag in item.select('a[href]')][0]
        ref = f"https://www.avito.ru{part_ref}"

        entry_items.append(dict(price=price, location=city_name, name=name, description=description, url=ref))
    return entry_items


@threaded
def task(link):
    driver = webdriver.Chrome(chrome_options=webdriver.ChromeOptions())  # В этот раз будем запускать браузер с опциями)
    driver.get(link)
    return parse_html(driver.page_source)


def save_results(all_entries, filtered_func):
    with open("../artifacts/medium/all_entries.json", "w", encoding="utf-8") as file:
        json.dump(all_entries, file, ensure_ascii=False, indent=2)
    filtered_entries = list(filter(filtered_func, all_entries))
    with open("../artifacts/medium/filtered_entries.json", "w", encoding="utf-8") as file:
        json.dump(filtered_entries, file, ensure_ascii=False, indent=2)


async def main_medium_impl(query, filtered_func):
    driver = webdriver.Chrome(chrome_options=webdriver.ChromeOptions())  # В этот раз будем запускать браузер с опциями)
    driver.get("https://www.avito.ru/")

    element = driver.find_element(by=By.XPATH, value="//*[@id=\"app\"]/div/div[3]/div/div[1]/div/div[3]/div[2]/div[1]/div/div/div/label[1]/input")
    element.send_keys(query)
    time.sleep(2)

    element = driver.find_element(by=By.XPATH, value="//*[@id=\"app\"]/div/div[3]/div/div[1]/div/div[3]/div[2]/div[2]/button")
    element.click()
    time.sleep(2)

    first_entries = parse_html(driver.page_source)

    element = driver.find_element(by=By.XPATH, value="//*[@id=\"app\"]/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/nav/ul/li[3]/a")
    element.click()
    time.sleep(2)

    total_results = await asyncio.gather(*[task(str(driver.current_url).replace("p=2", f"p={i + 2}")) for i in range(5)])
    all_entries = first_entries + list(itertools.chain(*total_results))
    save_results(all_entries, filtered_func)


def main_medium(query, filtered_function):
    loop = asyncio.get_event_loop()
    thread_pool = ThreadPoolExecutor(10)
    loop.set_default_executor(thread_pool)
    loop.run_until_complete(main_medium_impl(query, filtered_function))
