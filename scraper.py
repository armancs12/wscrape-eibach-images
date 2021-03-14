from bs4 import BeautifulSoup
import requests

WEBSITE_URL = "https://eibach.com/us/search.html?q="

LIST_ID = "wsm-prod-list-view"
LIST_ITEM_CLASS = "wsm-cat-list-item"
CONTAINER_CLASS = "wsm-cat-image wsm-cat-image-nobrand"

IMAGE_CONTAINER_ID = "wsm-prod-rotate-image"
ONE_IMAGE_CLASS = "productRotateImage"
MULTIPLE_IMAGE_ID = "productImageBar"


def get_image(image_code: str) -> str:
    def get_image_page_url(image_code: str) -> str:
        search_page = requests.get(WEBSITE_URL + image_code)
        soup = BeautifulSoup(search_page.content, 'html.parser')
        items_list = soup.find('div', id=LIST_ID)
        first_item = items_list.find_all('div', class_=LIST_ITEM_CLASS)[0]
        link = first_item.find('div', class_=CONTAINER_CLASS).a
        return link.get('href')

    def get_image_url_from_page(page_url: str) -> str:
        image_page = requests.get(page_url)
        soup = BeautifulSoup(image_page.content, 'html.parser')
        image_container = soup.find('div', id=IMAGE_CONTAINER_ID)

        one_image = image_container.find('div', class_=ONE_IMAGE_CLASS)
        if one_image is not None:
            return get_one_image(one_image)

        multiple_image = image_container.find('ul', id=MULTIPLE_IMAGE_ID)
        return get_image_from_multiple_images(multiple_image)

    def get_one_image(image) -> str:
        return image.a.get('href')

    def get_image_from_multiple_images(multiple_image) -> str:
        return multiple_image.li.a.get('href')

    image_page_url = get_image_page_url(image_code)
    image_url = get_image_url_from_page(image_page_url)

    return image_url
