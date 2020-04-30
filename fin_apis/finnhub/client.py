import pandas as pd

from fin_apis.finnhub.base import FinnHubBase
from fin_apis.finnhub.options import FinnHubOptionChain
from fin_apis.utils import multicall
from fin_apis.auth import AuthKeys


class FinnHubClient(FinnHubBase):

    def __init__(self, api_key=None):
        if api_key is None:
            api_key = AuthKeys.finnhub()
        super(FinnHubClient, self).__init__(api_key=api_key)

    def get_stock_option_chain(self, symbol):
        opts = super(FinnHubClient, self).get_stock_option_chain(symbol)
        return FinnHubOptionChain(opts)

    def get_stock_option_chain_multi(self, symbols):
        return multicall(
            self.get_stock_option_chain,
            symbols
        )

    def get_stock_earnings(self, symbol):
        earnings = super(FinnHubClient, self).get_stock_earnings(symbol)
        df = pd.DataFrame(earnings)
        df.index = df.pop('period')
        return df.sort_index()

    def get_stock_earnings_multi(self, symbols):
        return multicall(
            self.get_stock_earnings,
            symbols
        )

    def get_stock_candles(self, symbol, resolution='D', count=250, utc=True):
        bars = super(FinnHubClient, self).get_stock_candles(symbol, resolution, count)
        df = pd.DataFrame(bars)
        df.index = df.pop('t').apply(pd.Timestamp.fromtimestamp)
        if utc:
            df = df.tz_localize('utc')
        return df

    def get_stock_candles_multi(self, symbols, resolution='D', count=250, utc=True):
        return multicall(
            self.get_stock_candles,
            symbols,
            resolution=resolution,
            count=count,
            utc=utc
        )
