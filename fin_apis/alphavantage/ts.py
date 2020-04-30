from alpha_vantage.timeseries import TimeSeries

from fin_apis.utils import multicall
from fin_apis.auth import AuthKeys


class AVTimeSeries(TimeSeries):

    def __init__(self, key=None, output_format='pandas', treat_info_as_error=True, indexing_type='date', proxy=None,
                 rapidapi=False):
        if key is None:
            key = AuthKeys.alpha_vantage()
        super(AVTimeSeries, self).__init__(
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

    def get_daily_multi(self, symbols, output_size='compact'):
        return multicall(self.get_daily, symbols, output_size=output_size)

    def get_daily_adjusted_multi(self, symbols, output_size='compact'):
        return multicall(self.get_daily_adjusted, symbols, output_size=output_size)

    def get_intraday_multi(self, symbols, interval='15m', outputsize='compact'):
        return multicall(self.get_intraday, symbols, interval=interval, outputsize=outputsize)
