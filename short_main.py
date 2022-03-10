import datetime as dt
from datetime import datetime
import time
import numpy as np
import pandas as pd
from scipy import stats
from xbbg import blp
from dxclient.Query import *
from dxclient.DxOpenClient import DxOpenClient
from htmldocx import HtmlToDocx

from bbg_utils import get_bbg_tickers, bbg_multiple_dates_data_format
from commentary_template import eps_chg_temp, eps_summary, short_summary, adj_price_pct, valuation_start, \
    val_sector_summary, val_hist_summary, oss_summary, get_bear, get_bull, \
    get_short_base, get_valuation_flag, empty_to_none, brief_options, brief_rsi_summary, brief_sector_rsi_summary, \
    price_pct_brief, brief_anr_rating, brief_anr_summary, brief_dy_commentary, brief_dy_start, price_pct_start
from config import tdy, this_mon, this_fri, twenty_biz_f_tdy, eu_cix_map, us_grp_map, us_cix_map, metrics_conf, \
    two_y_f_tdy, one_m_f_tdy, today_day, comp_ending, next_mon, next_fri, exchange_conf, idx_err, sel_tics_e, si_err
from oss_utils import anr_assignment, hold_pt_assignment, sell_pt_assignment, buy_pt_assignment, sector_rsi_assignment, \
    price_score_assignment, performance_score_assignment, rsi_score_assignment, eps_score_assignment, \
    cds_score_assignment, si_score_assignment, vol_score_assignment, valn_score_assignment, yield_score_assignment
from utils import custom_time_form, Metrics, oss_ratio_calc, oss_vol_calc, get_eq_metric_history, \
    get_in_metric_history, oss_val_calc, oss_perf_calc, get_ratio_calc, oss_yield_calc

import warnings

warnings.filterwarnings("ignore")

start = time.time()

# dates
mon_date = custom_time_form('{S} %B', this_mon)
fri_date = custom_time_form('{S} %B', this_fri)
n_mon_date = custom_time_form('{S} %B', next_mon)
n_fri_date = custom_time_form('{S} %B', next_fri)
# pandas visualisation for pycharm , non essentials
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 20)

purpose = input('Type s for selected universe, f for universe based on earnings calendar')
q_date_str = input('What date do you want to generate data on?(DDMMYYYY)')
q_date_dt = datetime.strptime(q_date_str, "%d%m%Y")
if purpose == 's':
    tics_e = [ticker for ticker in sel_tics_e if type(ticker) == str]
elif purpose == 'f':
    # earnings calendar
    if today_day not in ['Friday', 'Saturday', 'Sunday']:
        er_cal = pd.read_excel(f'//otsukfs02/Users/Matt.Worby/Matt Worby Documents/Directional Group/Screens/Earnings '
                               f'Calendars/Europe Earnings Calendar/Europe Earnings Calendar {mon_date} - {fri_date}.xlsm',
                               sheet_name='week')
    else:
        er_cal = pd.read_excel(f'//otsukfs02/Users/Matt.Worby/Matt Worby Documents/Directional Group/Screens/Earnings '
                               f'Calendars/Europe Earnings Calendar/Europe Earnings Calendar {n_mon_date} - {n_fri_date}.xlsm',
                               sheet_name='week')
    er_cal = er_cal.dropna(how='all')
    er_cal.columns = er_cal.iloc[1]
    er_cal = er_cal.iloc[2:]
    er_cal['Date'] = er_cal['Date'].astype(str).str[:10]
    tdy_er = er_cal[er_cal['Date'] == q_date_dt.strftime("%Y-%m-%d")]  # companies reporting today
    tics_l = tdy_er.Ticker.unique()
    tics_l = [ticker for ticker in tics_l if type(ticker) == str]
    tics_e = [ticker + ' Equity' for ticker in tics_l]
# tics_e = ['1COV GR Equity', 'VOD LN Equity']
problems = {}
for idx_e in tics_e:
    short_ticker = idx_e.split(' ')[0] + " " + idx_e.split(' ')[1]
    try:
        try:
            eu_cix_map.loc[eu_cix_map['Ticker'] == short_ticker, 'Valuation Metrics'].iloc[0]
        except IndexError:
            for original, target in exchange_conf.items():
                if idx_e.split(' ')[1] == original:
                    short_ticker = idx_e.split(' ')[0] + ' ' + target
            eu_cix_map.loc[eu_cix_map['Ticker'] == short_ticker, 'Valuation Metrics'].iloc[0]
    except IndexError:
        print(f"{idx_e} does not have a cix.")
        problems[idx_e] = 'no cix in database'

exclusion = list(problems.keys())
tics_e = list(set(tics_e) - set(exclusion))
# To exclude bbg cix mismatch
cix_excl = list(set(tics_e).intersection(idx_err))
si_excl = list(set(tics_e).intersection(si_err))
for item in cix_excl:
    print(f'{item} has a Bloomberg cix mismatch issue.')
tics_e = list(set(tics_e) - set(idx_err))
tics_e = list(set(tics_e) - set(si_err))
eu_cix_map['ticker'] = eu_cix_map['Ticker'] + ' Equity'
metrics_dict = {}
# storing the missing ticker
m_tics = exclusion + cix_excl + si_excl
m_tics_w = open(r'S:\New World 2021\Earnings Comments\automated_tickers\missing_tickers.txt', 'w')
for tic in m_tics:
    m_tics_w.write(tic + "\n")
m_tics_w.close()
for tic in tics_e:
    get_metrics = Metrics(tic, us_grp_map, us_cix_map, eu_cix_map)
    if len(tic) == 1 or (tic.split()[1] in ['US', 'UN', 'UW']):
        val_metric, idx, etf, cix = get_metrics.get_us()

    else:
        val_metric, idx, etf, cix = get_metrics.get_emea()

    val_eq_metric = metrics_conf.get(val_metric).get('eq')
    val_in_metric = metrics_conf.get(val_metric).get('in')
    metrics_dict[tic] = {'val_metric': val_metric, 'idx': idx, 'etf': etf, 'cix': cix,
                         'eq_metric': val_eq_metric, 'in_metric': val_in_metric}

metrics_df = pd.DataFrame.from_dict(metrics_dict).transpose()
etf_list = list(metrics_df.etf.unique())
cix_list = metrics_df.cix.to_list()
idx_list = list(metrics_df.idx.unique())
# print(metrics_dict)
# index universe
idx_l = []
for k, v in metrics_dict.items():
    idx_l.append(metrics_dict.get(k).get('idx'))

# bbg starter query
bbg_df = blp.bdp(
    tics_e,
    flds=["SHORT_NAME", "SECURITY_NAME", "GICS_SECTOR_NAME", "GICS_INDUSTRY_GROUP_NAME", "GICS_INDUSTRY_NAME",
          "CUR_MKT_CAP", "PX_LAST", "INTERVAL_PERCENT_CHANGE", "5Y_MID_CDS_SPREAD", "SHORT_INTEREST_RATIO",
          "VOLUME_AVG_30D", "EQY_FLOAT", "best_analyst_rating", "best_target_median", "EU_COMPOSITE_TICKER",
          "RSI_14D", "CHG_PCT_1M"],
    best_fperiod_override="1bf",
    market_data_override="best eps",
    start_date_override=twenty_biz_f_tdy.strftime('%Y%m%d'),
    end_date_override=tdy.strftime('%Y%m%d'))

# Technicals
# Primary data for price score and rsi score
rel_cix = blp.bdp(cix_list, flds=["chg_pct_1m", "chg_pct_3m", "rsi_14d"]).reset_index().rename({'ticker': 'cix'},
                                                                                               axis='columns')
rel_cix = rel_cix.rename({'chg_pct_1m': 'p_cix',
                          'rsi_14d': 'rsi_cix',
                          'chg_pct_3m': 'rsi_3m'}, axis=1)
met_for_df = metrics_df.reset_index().rename({'index': 'ticker'}, axis='columns')
bbg_df = bbg_df.reset_index().rename({'index':'ticker'}, axis='columns')
temp1_df = pd.merge(bbg_df, met_for_df, how='left', on=['ticker'])
rel_cix = rel_cix.rename({'index':'cix'}, axis=1)
tec_df = pd.merge(temp1_df, rel_cix, how='left', on=['cix'])
# renaming the columns
equity_p = blp.bdh(tics_e, "PX_LAST", one_m_f_tdy, tdy)
index_p = blp.bdh(idx_list, "PX_LAST", one_m_f_tdy, tdy)
eq_per = bbg_multiple_dates_data_format(equity_p, "_PX_LAST")
idx_per = bbg_multiple_dates_data_format(index_p, "_PX_LAST")
per_dict = {}
for ticker in tics_e:
    per_dict = oss_perf_calc(ticker, tec_df, eq_per, idx_per, per_dict)

# additional calculation
bbg_df['anr'] = bbg_df.apply(lambda x: anr_assignment(x['best_analyst_rating']), axis=1)
bbg_df['street_%_pt'] = (bbg_df['best_target_median'] / bbg_df['px_last']) - 1

# Dividend Yield
idx_l = list(set(idx_l))
equity_dy = blp.bdh(tics_e, "BEST_DIV_YLD", two_y_f_tdy, tdy, best_fperiod_override="bf")
idx_dy = blp.bdh(idx_l, "BEST_DIV_YLD", two_y_f_tdy, tdy, best_fperiod_override="bf")
e_yield = bbg_multiple_dates_data_format(equity_dy, '_BEST_DIV_YLD')
i_yield = bbg_multiple_dates_data_format(idx_dy, '_BEST_DIV_YLD')
yield_dict = {}
oss_yield = {}

if not e_yield.empty:
    for tic in e_yield.transpose().index.to_list()[1:]:
        dy_dict = oss_ratio_calc(tic, metrics_dict, e_yield, i_yield, yield_dict, 'Level2Index')
        oss_yield = oss_yield_calc(tic, metrics_dict, e_yield, i_yield, oss_yield, 'Level2Index')
else:
    dy_dict = {}
    oss_yield = {}
# Volatility Ratio
equity_vol = blp.bdh(tics_e, "3MTH_IMPVOL_100.0%MNY_DF", two_y_f_tdy.strftime('%Y%m%d'), tdy.strftime('%Y%m%d'))
idx_vol = blp.bdh(idx_l, "3MTH_IMPVOL_100.0%MNY_DF", two_y_f_tdy.strftime('%Y%m%d'), tdy.strftime('%Y%m%d'))
e_vol = bbg_multiple_dates_data_format(equity_vol, '_3MTH_IMPVOL_100.0%MNY_DF')
i_vol = bbg_multiple_dates_data_format(idx_vol, '_3MTH_IMPVOL_100.0%MNY_DF')
m_idx_vol = []
for k, v in metrics_dict.items():
    if v.get('idx') in ['SX86P INDEX', 'SXRP INDEX', 'SX4P INDEX', 'SX8P INDEX']:
        m_idx_vol.append(k)

vol_dict = {}
vol_tickers = e_vol.transpose().index.to_list()[1:]
vol_tickers = [ticker for ticker in vol_tickers if ticker not in m_idx_vol]
for ticker in vol_tickers:
    vol_dict = oss_vol_calc(ticker, metrics_dict, e_vol, i_vol, vol_dict, 'idx')
# oss_df['oss_vol_ratio'] = oss_df['ticker'].map(vol_dict)

m_idx_vol = [ticker for ticker in m_idx_vol if ticker in e_vol.columns[1:]]
etf_vol = blp.bdh(etf_list, "3MTH_IMPVOL_100.0%MNY_DF", two_y_f_tdy.strftime('%Y%m%d'), tdy.strftime('%Y%m%d'))
f_vol = bbg_multiple_dates_data_format(etf_vol, '_3MTH_IMPVOL_100.0%MNY_DF')
for ticker in m_idx_vol:
    vol_dict = oss_vol_calc(ticker, metrics_dict, e_vol, f_vol, vol_dict, 'etf')

for k, v in vol_dict.items():
    if np.isnan(v):
        vol_dict[k] = -1000
val_dict = {}
val_oss = {}
# For Evaluation Metric that's P/Book
if 'P/Book' in metrics_df.val_metric.to_list():
    p_book_eq = get_eq_metric_history(met_for_df, 'BEST_PX_BPS_RATIO', 'eq_metric', two_y_f_tdy, tdy)  # equity_valn
    p_book_eq = bbg_multiple_dates_data_format(p_book_eq, '_BEST_PX_BPS_RATIO')
    p_book_in = get_in_metric_history(met_for_df, 'BEST_PX_BPS_RATIO', 'in_metric', two_y_f_tdy, tdy)
    p_book_in = bbg_multiple_dates_data_format(p_book_in, '_BEST_PX_BPS_RATIO')

    for ticker in p_book_eq.transpose().index.to_list()[1:]:
        val_dict = oss_val_calc(ticker, metrics_dict, p_book_eq, p_book_in, val_dict, 'idx')
        val_oss = get_ratio_calc(ticker, metrics_dict, p_book_eq, p_book_in, val_oss, 'idx')

# For Evaluation that's P/E
if 'P/E' in metrics_df.val_metric.to_list():
    pe_eq = get_eq_metric_history(met_for_df, 'BEST_PE_RATIO', 'eq_metric', two_y_f_tdy, tdy)  # equity_valn
    pe_eq = bbg_multiple_dates_data_format(pe_eq, '_BEST_PE_RATIO')
    pe_in = get_in_metric_history(met_for_df, 'BEST_PE_RATIO', 'in_metric', two_y_f_tdy, tdy)
    pe_in = bbg_multiple_dates_data_format(pe_in, '_BEST_PE_RATIO')
    for ticker in pe_eq.transpose().index.to_list()[1:]:
        val_dict = oss_val_calc(ticker, metrics_dict, pe_eq, pe_in, val_dict, 'idx')
        val_oss = get_ratio_calc(ticker, metrics_dict, pe_eq, pe_in, val_oss, 'idx')

# For Evaluation that's EV/EBITDA
if 'EV/EBITDA' in metrics_df.val_metric.to_list():
    ev_eq = get_eq_metric_history(met_for_df, 'BEST_EV_TO_BEST_EBITDA', 'eq_metric', two_y_f_tdy, tdy)
    ev_eq = bbg_multiple_dates_data_format(ev_eq, '_BEST_EV_TO_BEST_EBITDA')
    ev_in = get_in_metric_history(met_for_df, 'IDX_EST_EV_EBITDA', 'in_metric', two_y_f_tdy, tdy)
    ev_in = bbg_multiple_dates_data_format(ev_in, '_IDX_EST_EV_EBITDA')
    for ticker in ev_eq.transpose().index.to_list()[1:]:
        val_dict = oss_val_calc(ticker, metrics_dict, ev_eq, ev_in, val_dict, 'idx')
        val_oss = get_ratio_calc(ticker, metrics_dict, ev_eq, ev_in, val_oss, 'idx')

    # Index
    if ev_in['Date'].iloc[0] != tdy.strftime('%Y-%m-%d'):  # To deal with the one day delay
        ev_eq = ev_eq[:-1]

    for ticker in ev_eq.transpose().index.to_list()[1:]:
        val_dict = oss_val_calc(ticker, metrics_dict, ev_eq, ev_in, val_dict, 'idx')
        val_oss = get_ratio_calc(ticker, metrics_dict, ev_eq, ev_in, val_oss, 'idx')
print(val_dict)
# Short Interest
client = DxOpenClient("https://sf.ihsmarkit.com/dxopen")
client.setCredentials("christina.liu@olivetreeglobal.com", "hb95qG#vI5")
si_dict = {}
isin = blp.bdp(tics_e, "id_isin")
isin_dict = dict(isin.reset_index().values)
for ticker, isin in isin_dict.items():
    query = DxlSFQuery()
    query.setSource('SF.Instrument')
    query.addIdentifier('ISIN', isin)
    query.addFields(['ShortLoanQuantity'])
    marketData = client.getSF(query)
    data = marketData.get_Instrument() if marketData is not None else None
    try:
        borrow_vol = int(data[0].get_DataDate()[0].MarketColour.ShortLoanQuantity)
    except TypeError:
        print('No Borrow volume data')
        borrow_vol = None
    if borrow_vol is not None:
        si_dict[ticker] = borrow_vol
client.logout()

bbg_df['shortside'] = bbg_df.index.map(si_dict)
bbg_df = bbg_df.reset_index()
bbg_df['eu_composite_ticker'] = bbg_df['eu_composite_ticker'].fillna(bbg_df['ticker'])
eu_comp = bbg_df.eu_composite_ticker.to_list()
eu_vol = blp.bdp(eu_comp, "VOLUME_AVG_30D").reset_index().rename({'ticker': 'eu_composite_ticker',
                                                                  'volume_avg_30d': 'eu_volume_avg_30d',
                                                                  'index':'eu_composite_ticker'}, axis=1)  #
oss_df = pd.merge(bbg_df, eu_vol, how='left', on='eu_composite_ticker')
dtc_dict = {}
for mb in tics_e:
    dtc = oss_df[oss_df.ticker == mb]['shortside'].values[0] / max(
        oss_df[oss_df.ticker == mb]['eu_volume_avg_30d'].values[0],
        oss_df[oss_df.ticker == mb]['volume_avg_30d'].values[0])
    dtc_dict[mb] = dtc

# oss_score calculation
score_df = tec_df[['ticker', 'security_name', 'p_cix', 'rsi_cix', 'interval_percent_change', '5y_mid_cds_spread']]
score_df['price_score'] = score_df.apply(lambda x: price_score_assignment(x['p_cix']), axis=1)
score_df['oss_per'] = score_df.ticker.map(per_dict)
score_df['performance_score'] = score_df.apply(lambda x: performance_score_assignment(x['oss_per']), axis=1)
score_df['price_score'] = score_df['price_score'].fillna(score_df['performance_score'])
score_df['rsi_score'] = score_df.apply(lambda x: rsi_score_assignment(x['rsi_cix']), axis=1)
score_df['eps_score'] = score_df.apply(lambda x: eps_score_assignment(x['interval_percent_change']), axis=1)
score_df['cds_score'] = score_df.apply(lambda x: cds_score_assignment(x['5y_mid_cds_spread']), axis=1)
score_df['dtc'] = score_df['ticker'].map(dtc_dict)
score_df['si_score'] = score_df.apply(lambda x: si_score_assignment(x['dtc']), axis=1)
score_df['oss_vol_ratio'] = score_df.ticker.map(vol_dict)
score_df['vol_score'] = score_df.apply(lambda x: vol_score_assignment(x['oss_vol_ratio']), axis=1)
score_df['oss_val_ratio'] = score_df['ticker'].map(val_oss)
score_df['val_score'] = score_df.apply(lambda x: valn_score_assignment(x['oss_val_ratio']), axis=1)
score_df['oss_yield_ratio'] = score_df['ticker'].map(oss_yield)
score_df['yield_score'] = score_df.apply(lambda x: yield_score_assignment(x['oss_yield_ratio']), axis=1)
score_df['sum_score'] = score_df['price_score'] + score_df['rsi_score'] + score_df['eps_score'] + score_df[
    'cds_score'] + \
                        score_df['si_score'] + score_df['vol_score'] + score_df['val_score'] + score_df['yield_score']

score_df['oss_score'] = score_df['sum_score'] * 100 / 32

template_dict = {}
sector_map = {}
ffs_dict = {}
# The template starts here

industry_l = bbg_df['gics_industry_name'].unique()
for industry in industry_l:
    industry_df = bbg_df[bbg_df['gics_industry_name'] == industry].reset_index()
    industry_tics = industry_df.ticker.unique()
    for idx_pos, tic in enumerate(industry_tics):
        comp_name = industry_df[industry_df.ticker == tic]['security_name'].iloc[0]  # get company name
        shorter_comp_name = [
            " ".join(comp_name.split()[:-1]) if comp_name.split()[-1] in comp_ending else " ".join(
                comp_name.split())][0]
        # Analyst Rating
        if not np.isnan(industry_df[industry_df.ticker == tic]['best_analyst_rating'].iloc[0]):
            anr_txt = industry_df[industry_df.ticker == tic]['anr'].iloc[0]
            if not np.isnan(industry_df[industry_df.ticker == tic]['street_%_pt'].iloc[0]):
                pt_chg = round(industry_df[industry_df.ticker == tic]['street_%_pt'].iloc[0] * 100)
                if anr_txt == 'Strong Sell':
                    pt_score = sell_pt_assignment(pt_chg)
                elif anr_txt == 'Sell':
                    pt_score = sell_pt_assignment(pt_chg)
                elif anr_txt == 'Hold':
                    pt_score = hold_pt_assignment(pt_chg)
                elif anr_txt == 'Buy':
                    pt_score = buy_pt_assignment(pt_chg)
                elif anr_txt == 'Strong Buy':
                    pt_score = buy_pt_assignment(pt_chg)
                anr_rat_sum = brief_anr_rating(anr_txt) + brief_anr_summary(abs(pt_chg)).get(anr_txt).get(
                    pt_score) + ' '
            else:
                anr_rat_sum = ''
        else:
            anr_rat_sum = ''

        # EPS chg
        fwd_eps = round(industry_df[industry_df.ticker == tic]['interval_percent_change'].iloc[0], 1)
        idx_dict = {}
        for k, v in metrics_dict.items():
            idx_dict[k] = metrics_dict.get(k).get('idx')
        industry_df['Level2Index'] = industry_df.ticker.map(idx_dict)
        eps_idx = {}
        eps_rank_dict = {}
        for idx in industry_df['Level2Index'].unique():
            idx_mbs = get_bbg_tickers(idx)
            eps_m = blp.bdp(idx_mbs, "INTERVAL_PERCENT_CHANGE", best_fperiod_override="1bf",
                            market_data_override="best eps", start_date_override=twenty_biz_f_tdy.strftime('%Y%m%d'),
                            end_date_override=tdy.strftime('%Y%m%d'))
            eps_idx[idx] = eps_m
        idx = industry_df[industry_df['ticker'] == tic]['Level2Index'].iloc[0]
        eps_sec = eps_idx.get(idx)
        try:
            eps_tic = eps_sec.at[tic, 'interval_percent_change']
            if not np.isnan(eps_tic):
                eps_rank = stats.percentileofscore(eps_sec, eps_tic, kind='strict')
                eps_rank_dict[tic] = round(eps_rank)
                per_sec = eps_rank_dict.get(tic)
                if eps_tic < 100:
                    eps_sum = eps_chg_temp(round(eps_tic, 1)) + eps_summary(round(per_sec)) + ' '
                else:
                    eps_sum = ""
            else:
                eps_sum = ""
        except KeyError:
            try:
                eps_tic = \
                    blp.bdp(tic, 'interval_percent_change', best_fperiod_override='1bf',
                            market_data_override='best eps',
                            start_date_override=twenty_biz_f_tdy.strftime('%Y%m%d'),
                            end_date_override=tdy.strftime('%Y%m%d')).iloc[0][0]
                eps_rank = stats.percentileofscore(eps_sec, eps_tic, kind='strict')
                eps_rank_dict[tic] = round(eps_rank)
                per_sec = eps_rank_dict.get(tic)
                if eps_tic < 100:
                    eps_sum = eps_chg_temp(round(eps_tic, 1)) + eps_summary(round(per_sec)) + ' '
                else:
                    eps_sum = ""
            except IndexError:
                eps_sum = ""
        # Dividend yield
        if tic in list(dy_dict.keys()):
            dy_rel_hist = dy_dict.get(tic).get('rel_hist')
            dy_sec_avg = dy_dict.get(tic).get('sector_avg')
            eq_dy = float(e_yield[[tic]].iloc[-1])
            dy_one = brief_dy_start(eq_dy, dy_sec_avg)
            dy_two = brief_dy_commentary(dy_rel_hist)
            if dy_one and dy_two is not None:
                dvd_sum = dy_one + dy_two + ' '
            else:
                dvd_sum = ''
        else:
            dvd_sum = ''
        if vol_dict.get(tic) is not None:
            opt_sum = brief_options(vol_dict.get(tic))
        else:
            opt_sum = ''
        # short interest
        share = si_dict.get(tic)
        dtc = dtc_dict.get(tic)
        eqy_float = float(industry_df[industry_df['ticker'] == tic]['eqy_float'].iloc[0])
        try:
            ffs = (share / 1000000) / eqy_float * 100
            si_sum = short_summary(round(ffs, 1), round(dtc, 1)) + ' '
        except TypeError:
            si_sum = ""
        ffs_dict[shorter_comp_name] = ffs
        # eqy_flt = industry_df[industry_df['ticker'] == tic]['eqy_float'].iloc[0]
        # Technicals
        rsi_p = float(tec_df[tec_df['ticker'] == tic]['rsi_14d'].iloc[0])
        rsi_cix = float(tec_df[tec_df['ticker'] == tic]['rsi_cix'].iloc[0])
        daily_rsi_rating, technicals_one = brief_rsi_summary(round(rsi_p))
        technicals_dictionary = brief_sector_rsi_summary(rsi_cix)
        sector_rsi_rating = sector_rsi_assignment(round(rsi_cix))
        technicals_two = technicals_dictionary.get(daily_rsi_rating).get(sector_rsi_rating)
        if technicals_one != "" and technicals_two == "":
            tecs_summary = technicals_one + ". "
        else:
            tecs_summary = technicals_one + technicals_two
        # Adjusted Price
        try:
            perf_1m = tec_df[tec_df['ticker'] == tic]['p_cix'].iloc[0]
            perf_3m = tec_df[tec_df['ticker'] == tic]['rsi_3m'].iloc[0]
            sec_perf_1m = price_pct_start(round(perf_1m, 1)) + ' 1M'
            sec_perf_3m = adj_price_pct(round(perf_3m, 1)) + ' 3M both vs sector, '
            if sec_perf_1m.lower()[0] == sec_perf_3m.lower()[0]:
                sec_perf_con = ' and '
            else:
                sec_perf_con = ' though '
            sec_perf_1m = sec_perf_1m + sec_perf_con
            abs_perf_1m = tec_df[tec_df['ticker'] == tic]['chg_pct_1m'].iloc[0]
            # print(f'The absolute performance for a month is {round(abs_perf_1m, 1)}')
            abs_temp = price_pct_brief(round(abs_perf_1m, 1)) + ' 1M absolute. '
            adj_price_summary = sec_perf_1m + sec_perf_3m + abs_temp
        except TypeError:
            adj_price_summary = ""
        tic_val_metric = metrics_dict.get(tic).get('val_metric')
        if tic in list(val_dict.keys()):
            if not np.isnan(val_dict.get(tic).get('rel_hist')):
                val_rel_hist = val_dict.get(tic).get('rel_hist')
                val_sec_avg = val_dict.get(tic).get('sector_avg')
                val_abs_val = val_dict.get(tic).get('abs_val')
                val_one = ' '.join(tic.split(' ')[:-2]) + ' trades ' + valuation_start(tic_val_metric,
                                                                                       round(val_abs_val, 1))
                val_two = val_sector_summary(val_sec_avg)
                val_three = ', ' + val_hist_summary(val_rel_hist) + ' '
                if round(val_abs_val, 1) >= metrics_conf.get(tic_val_metric).get("exclusion"):
                    val_summary = ''
                else:
                    val_summary = val_one + val_two + val_three
            else:
                val_summary = ''
        else:
            val_summary = ''

        # oss score

        oss_score = score_df[score_df['ticker'] == tic]['oss_score'].iloc[0]
        oss_template = f'{oss_summary(oss_score, shorter_comp_name)}'
        template = f'<li>{oss_template + adj_price_summary + tecs_summary + anr_rat_sum + eps_sum + val_summary + dvd_sum + opt_sum + si_sum}</li>'
        template_dict[tic] = template

        # sector_map[industry] = tic
        # template

oss_dict = dict(score_df[['security_name', 'oss_score']].values)
oss_dict = {" ".join(k.split()[:-1]) if k.split()[-1] in comp_ending else " ".join(
    k.split()): v for k, v in oss_dict.items()}
oss_desc = {k: v for k, v in sorted(oss_dict.items(), key=lambda item: item[1], reverse=True)}
oss_asc = {k: v for k, v in sorted(oss_dict.items(), key=lambda item: item[1])}
ffs_desc = {k: v for k, v in sorted(ffs_dict.items(), key=lambda item: item[1], reverse=True)}
bear_intro = get_bear(oss_asc)
bull_intro = get_bull(oss_desc)
bear = empty_to_none(bear_intro)
bull = empty_to_none(bull_intro)

bear_positioning = f'Bearish Positioning: {bear}'
bull_positioning = f'Bullish Positioning: {bull}'
high_short_base = get_short_base(ffs_desc)
high_short = empty_to_none(high_short_base)
hsb_sum = 'High Short Base: ' + high_short
val_hist = {}
for k, v in val_dict.items():
    val_hist[k] = v.get('rel_hist')

ticker_security = dict(bbg_df[['ticker', 'security_name']].values)
ticker_security = {k: " ".join(v.split()[:-1]) if v.split()[-1] in comp_ending else " ".join(
    v.split()) for k, v in ticker_security.items()}

comp_val_hist = {}
for key, name in ticker_security.items():
    try:
        comp_val_hist[name] = val_hist[key]
    except KeyError:
        pass
val_flags = get_valuation_flag(comp_val_hist)
val_flags = empty_to_none(val_flags)
val_flag_sum = 'Relative Valuation Flags: ' + val_flags
template = f'<li>{bear_positioning}</li><li>{bull_positioning}</li><li>{hsb_sum}</li><li>{val_flag_sum}</li>'
industry_ticker = dict(bbg_df[['ticker', 'gics_sector_name']].values)
ind_tic = {}
completed_ticker = []
tics_order = []
for k, v in industry_ticker.items():
    ind_tic[v] = ind_tic.get(v, []) + [k]
for industry, v in ind_tic.items():
    template += f'<br><br><b><dt>{industry}</b><br></dt>'
    for idx_pos, ticker in enumerate(v):
        tics_order.append(ticker)
        if idx_pos == 0:
            template += f'{template_dict.get(ticker)}</p>'
        else:
            template += f'<br>{template_dict.get(ticker)}</p>'
        completed_ticker.append(ticker)

intro = f'<img src="olivetree.jpg"><img src="ot_line.jpg">' \
        f'Please see below details on positioning in selected stocks that report on {q_date_dt.strftime("%A")}: '
# Getting the names that are reporting in this report
name_order = blp.bdp(tics_order, 'SECURITY_NAME')
short_name = name_order['security_name'].to_list()
completed_ticker = [" ".join(ticker.split()[:-1]) if ticker.split()[-1] in comp_ending else " ".join(ticker.split())
                    for ticker in short_name]
intro_comp = ", ".join(completed_ticker[:-1]) + f" and {completed_ticker[-1]}."
template = intro + intro_comp + template
# print(list(set(tics_e) - (set(completed_ticker))))
# Generate the tickers universe
tics_uni = open(r"./tickers_universe.txt", "w")
for ticker in tics_e:
    tics_uni.write(ticker + "\n")
tics_uni.close()

# Missing tickers
template = template.replace('.0', '')
with open("file.html", 'w') as file:
    file.write(template)

new_parser = HtmlToDocx()
if purpose == 's':
    new_parser.parse_html_file("file.html", f"./output/selected_earnings_comment_{tdy.strftime('%d%m%Y')}")
elif purpose == 'f':
    new_parser.parse_html_file("file.html",
                               f"./output/full_earnings_comment_{tdy.strftime('%d%m%Y')}")

end = time.time()
print(
    'Elapsed time for ' + str(len(tics_e)) + ' Tickers is ' + str(dt.timedelta(seconds=(round(end - start)))))
if m_tics:
    print(f'The missing tickers are: ')
    print(m_tics)
