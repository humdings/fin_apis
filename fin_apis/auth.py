import os


class AuthKeys(object):
    """
    Class to get API keys from environment variables.
    """
    _ALLOWED_VARS = [
        'EODDATA_API_KEY',
        'FINNHUB_API_KEY',
        'ALPHAVANTAGE_API_KEY',
        'TIINGO_API_KEY',
        'QUANDL_API_KEY'
    ]

    @staticmethod
    def lookup_var(var, env=None):
        if var not in AuthKeys._ALLOWED_VARS:
            raise ValueError(
                'Invalid API environment variable. Allowed values={}'.format(AuthKeys._ALLOWED_VARS)
            )
        if env is None:
            env = os.environ
        return env.get(var, None)

    @staticmethod
    def eod_data(env=None):
        return AuthKeys.lookup_var('EODDATA_API_KEY', env=env)

    @staticmethod
    def finnhub(env=None):
        return AuthKeys.lookup_var('FINNHUB_API_KEY', env=env)

    @staticmethod
    def alpha_vantage(env=None):
        return AuthKeys.lookup_var('ALPHAVANTAGE_API_KEY', env=env)

    @staticmethod
    def tiingo(env=None):
        return AuthKeys.lookup_var('TIINGO_API_KEY', env=env)

    @staticmethod
    def quandl(env=None):
        return AuthKeys.lookup_var('QUANDL_API_KEY', env=env)
