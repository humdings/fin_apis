import pandas as pd
import json


class FinnHubOptionChain(object):
    """
    Wrapper class for option chain data returned
    by FinnHubs api.
    """

    def __init__(self, data):
        self._data = data
        self.chain = data['data']
        self.expirations = [i['expirationDate'] for i in self.chain]
        self._frame = None

    @property
    def underlying_symbol(self):
        return self._data['code']

    @property
    def underlying_price(self):
        return self._data['lastTradePrice']

    @property
    def underlying_last_trade_date(self):
        return self._data['lastTradeDate']

    @property
    def exchange(self):
        return self._data['exchange']

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(data)

    def to_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self._data, f)

    def to_frame(self):
        if self._frame is None:
            self._frame = pd.DataFrame(self.to_list())
        return self._frame

    def to_list(self):
        options = (
            opts['options'][side]
            for side in ('CALL', 'PUT')
            for opts in self.chain
        )
        all_options = []
        map(all_options.extend, options)
        return all_options

    def get_expiry(self, expiry):
        for opts in self.chain:
            if opts['expirationDate'] == expiry:
                return opts['options']
        raise ValueError('Invalid expiry. valid dates = {}'.format(self.expirations))

    def _get_side(self, expiry, side):
        opts = self.get_expiry(expiry)
        return opts[side]

    def get_calls(self, expiry):
        """
        Get a dataframe of calls for an expiration.
        Dataframe is indexed by strike

        :param expiry: str, date
        :return: pandas.DataFrame
        """
        opts = self._get_side(expiry, 'CALL')
        df = pd.DataFrame(opts)
        df.index = df.strike
        return df

    def get_puts(self, expiry):
        """
        Get a dataframe of puts for an expiration.
        Dataframe is indexed by strike

        :param expiry: str, date
        :return: pandas.DataFrame
        """
        opts = self._get_side(expiry, 'PUT')
        df = pd.DataFrame(opts)
        df.index = df.strike
        return df

    def all_calls(self):
        """ DataFrame of all call options """
        gen = (
            opts['options']['CALL']
            for opts in self.chain
        )
        calls = []
        map(calls.extend, gen)
        return pd.DataFrame(calls)

    def all_puts(self):
        """ DataFrame of all put options """
        gen = (
            opts['options']['PUT']
            for opts in self.chain
        )
        puts = []
        map(puts.extend, gen)
        return pd.DataFrame(puts)

    def get_option(self, expiry, side, strike):
        """ Get a single option row """
        if side.upper() == 'CALL':
            opts = self.get_calls(expiry)
        elif side.upper() == 'PUT':
            opts = self.get_puts(expiry)
        else:
            raise ValueError('Invalid Option Side: {}'.format(side))
        return opts.loc[strike]
