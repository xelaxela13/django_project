import logging

from bs4 import BeautifulSoup

from shop.api_clients import BaseClient

logger = logging.getLogger(__name__)


class Parser(BaseClient):
    base_url = 'https://prom.ua/ua/Kovanye-stulya-i-taburety'

    def parse(self) -> list:
        response = self.get_request(
            method='get',
        )
        soup = BeautifulSoup(response)
        try:
            category_name = soup.find_all(
                'li', attrs={'data-qaid': 'breadcrumbs_seo_item'}
            )[-1].find('span').text
        except (AssertionError, IndexError) as err:
            logger.error(err)
        else:
            products_list = []
            for element in soup.find_all('div',
                                         attrs={'class': 'js-productad'}):
                try:
                    name = element.find(
                        'span',
                        attrs={'data-qaid': "product_name"}
                    ).text
                    price = element.find(
                        'span', attrs={'data-qaid': "product_price"}
                    ).find('span').text
                    image_url = element.find(
                        'picture', attrs={'data-qaid': "image_link"}
                    ).find('img').attrs['src']
                    products_list.append(
                        {
                            'name': name,
                            'description': name,
                            'price': price,
                            'category': category_name,
                            'image': image_url,
                            'sku': element.attrs['data-product-id'],
                        }
                    )
                except (AssertionError, KeyError) as err:
                    logger.error(err)
            return products_list


products_parser = Parser()
