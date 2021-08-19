from bs4 import BeautifulSoup
from decouple import config
from deta import Deta
import requests


DRIVERS_URL = 'https://www.wacom.com/en-us/support/product-support/drivers'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
# TRUST_STORE = 'my-trust-store.pem'
DETA_PROJECT_KEY = config('DETA_PROJECT_KEY')
DB_NAME = config('DB_NAME')

deta = Deta(DETA_PROJECT_KEY)
db = deta.Base(DB_NAME)


def get_soup():
    getpage = requests.get(url=DRIVERS_URL, headers=HEADERS, verify='my-trust-store.pem')
    page_contents = getpage.text
    soup = BeautifulSoup(page_contents, 'html.parser')
    return soup


def get_driver_page():
    driver_page = get_soup()
    return driver_page.find_all('a', attrs={'class': 'modal__drivers-btn'})


def get_latest_driver():
    versions = [0, 1, 2]
    result = get_driver_page()
    for version in versions:
        mac_driver = result[version]
        mac_download_link = mac_driver.get('data-download-link')
        db.put({
            "link": mac_download_link,
            "key": f"{version + 1}"
        })


if __name__ == "__main__":
    get_latest_driver()
