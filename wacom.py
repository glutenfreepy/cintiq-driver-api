from bs4 import BeautifulSoup
from decouple import config
import requests


DRIVERS_URL = 'https://www.wacom.com/en-us/support/product-support/drivers'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
TRUST_STORE = config('TRUST_STORE')


def get_soup():
    getpage = requests.get(url=DRIVERS_URL, headers=HEADERS, verify=TRUST_STORE)
    page_contents = getpage.text
    soup = BeautifulSoup(page_contents, 'html.parser')
    return soup


def get_driver_page():
    driver_page = get_soup()
    return driver_page.find_all('a', attrs={'class': 'modal__drivers-btn'})


def get_latest_drivers():
    result = get_driver_page()
    # TODO: loop this to get 0(latest), 1(next latest, and 2
    mac_driver = result[0]
    mac_download_link = mac_driver.get('data-download-link')
    print(mac_download_link)
    return mac_download_link


if __name__ == "__main__":
    get_latest_drivers()
