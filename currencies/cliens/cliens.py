from requests import request


class GetCurrencyBaseClient:
    base_url = None

    def _request(self, method: str,
                 params: dict = None,
                 headers: dict = None,
                 data: dict = None):
        try:
            response = request(
                url=self.base_url,
                method=method,
                params=params or {},
                data=data or {},
                headers=headers or {}
            )
        except Exception:
            # todo logging errors and success results
            ...
        else:
            return response.json()


class PrivatBankAPI(GetCurrencyBaseClient):
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
        return self._request(
            'get',
            params={'exchange': '', 'coursid': 5, 'json': ''}
        )


privat_currency_client = PrivatBankAPI()
