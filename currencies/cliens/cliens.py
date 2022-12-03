from shop.api_clients import BaseClient


class PrivatBankAPI(BaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def get_currency(self) -> dict:
        """
        [
            {
            "ccy":"EUR",
            "base_ccy":"UAH",
            "buy":"19.20000",
            "sale":"20.00000"
            },
            {
            "ccy":"USD",
            "base_ccy":"UAH",
            "buy":"15.50000",
            "sale":"15.85000"
            }
            ]
        :return: dict
        """
        return self.get_request(
            'get',
            params={'exchange': '', 'coursid': 5, 'json': ''}
        )


privat_currency_client = PrivatBankAPI()
