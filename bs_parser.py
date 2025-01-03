import requests
from bs4 import BeautifulSoup


def search_google(query, num_results=5):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        link = g.find('a')['href']
        title = g.find('h3').text
        results.append({'title': title, 'link': link})
        if len(results) >= num_results:
            break
    return results


def search_yandex(query, num_results=5):
    url = f"https://yandex.ru/search/?text={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('li', class_='serp-item'):
        link = g.find('a', class_='link')['href']
        title = g.find('h2').text
        results.append({'title': title, 'link': link})
        if len(results) >= num_results:
            break
    return results
