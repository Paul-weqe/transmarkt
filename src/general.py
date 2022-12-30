import requests
from bs4 import BeautifulSoup
import random

BASE_URL = "https://www.transfermarkt.co.uk"


# For pages with paginators, we will need links to all the pages
# that will need to be paginated across. This will give us how to do that.
def get_all_paginator_links(page_link: str) -> list:
    user_agent = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz1234567890@') for i in range(10)))

    response = requests.get(page_link, headers={'User-Agent': user_agent})
    soup = BeautifulSoup(response.content, 'html.parser')

    list_links =  soup.select(
        ".tm-pagination__list-item:not(.tm-pagination__list-item--icon-first-page)"
        ":not(.tm-pagination__list-item--icon-previous-page)"
        ":not(.tm-pagination__list-item--icon-next-page)"
        ":not(.tm-pagination__list-item--icon-last-page)"
    )

    links = []
    if len(list_links) == 0:
        return [page_link]

    for link in list_links:
        l = link.find_all('a')[0].get('href')
        links.append(f"{BASE_URL}{l}")

    return links
