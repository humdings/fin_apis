from alpha_vantage.cryptocurrencies import CryptoCurrencies

from fin_apis.auth import AuthKeys


class AVCryptoCurrencies(CryptoCurrencies):

    def __init__(self, key=None, output_format='pandas', treat_info_as_error=True, indexing_type='date', proxy=None,
                 rapidapi=False):
        if key is None:
            key = AuthKeys.alpha_vantage()
        super(AVCryptoCurrencies, self).__init__(
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