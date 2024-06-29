import os
import asyncio
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup


def rhymes(data):
    text = data['additional']['text']
    url = f"https://rifme.net/r/{quote(text.lower())}/0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    word_list = soup.find_all("li", class_="riLi", limit=20)
    header = soup.find("h2", class_="rifmypervye")

    new_word_list = []
    for word_item in word_list:
        word_data_w = word_item.get("data-w")
        new_word_list.append(word_data_w)

    if new_word_list:
        rhymes = '\n'.join(new_word_list)
        if header is not None:
            rhymes_message = f"<b>{header.text}\n\n</b>{rhymes}"
        else:
            rhymes_message = f"{rhymes}"
    else:
        rhymes_message = None

    return {'text': rhymes_message}
