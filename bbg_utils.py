from xbbg import blp


def get_bbg_tickers(index_import):
    """Take the index name and query data from Bloomberg,
    Return a list of tickers instead."""
    index_members = blp.bds(index_import, flds=["INDX_MEMBERS"])
    index_members["member_ticker_and_exchange_code"] = index_members["member_ticker_and_exchange_code"] + " Equity"
    ticker_list = index_members["member_ticker_and_exchange_code"].to_list()
    return ticker_list


def bbg_multiple_dates_data_format(bbg_data, txt_replace):
    """Take the bloomberg queried data with multiple dates (dataframe), and the type of data (str)
     return a dataframe with tickers and multiple dates without the name of the data."""
    bbg_data = bbg_data.reset_index()
    bbg_data.columns = ['_'.join(tuple(map(str, t))).rstrip('_') for t in bbg_data.columns.values]
    bbg_data.columns = [ticker.replace(txt_replace, '') for ticker in bbg_data.columns.values]
    bbg_data = bbg_data.rename({'index': 'Date'}, axis=1)
    return bbg_data


def get_price_chg(universe, data, start_date):
    """Take universe, data you wish to query on Bloomberg, and the start date.
    return a dictionary of security as key and price change as values. """
    q_result = blp.bdh(universe, data, start_date)
    q_result = bbg_multiple_dates_data_format(q_result, '_' + data)
    q_1d_chg = q_result.set_index('Date').pct_change().shift(-1).dropna()
    chg_dict = q_1d_chg.to_dict('index')
    chg_dict = {k.strftime('%Y-%m-%d'): v for k, v in chg_dict.items()}
    return chg_dict
