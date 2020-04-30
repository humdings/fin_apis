from alpha_vantage.foreignexchange import ForeignExchange

from fin_apis.utils import multicall
from fin_apis.auth import AuthKeys


class AVForeignExchange(ForeignExchange):

    def __init__(self, key=None, output_format='pandas', treat_info_as_error=True, indexing_type='date', proxy=None,
                 rapidapi=False):
        if key is None:
            key = AuthKeys.alpha_vantage()
        super(AVForeignExchange, self).__init__(
            key=key,
            output_format=output_format,
            treat_info_as_error=treat_info_as_error,
            indexing_type=indexing_type,
            proxy=proxy,
            rapidapi=rapidapi
        )
        # For some reason the output format is not being set in the superclass
        if self.output_format != output_format:
            self.output_format = output_format

    def get_currency_exchange_rate_multi(self, from_currencies, to_currency):
        """
        Get multiple fx quotes for one 'to currency.'

        :param from_currencies: list of FX symbols
        :param to_currency: base currency
        :return: dict {symbol: api result}
        """
        return multicall(
            self.get_currency_exchange_rate,
            from_currencies,
            to_currency=to_currency
        )