import re

from config import exchange_conf

import pandas as pd
from xbbg import blp

import win32com.client as win32


class Metrics:
    def __init__(self, ticker, us_group, us_cix, eu_cix):
        self.ticker = ticker
        self.us_group = us_group
        self.us_cix = us_cix
        self.eu_cix = eu_cix

    def get_us(self):
        group = blp.bdp(self.ticker, "GICS_INDUSTRY_GROUP_NAME").values[0][0]
        etf = self.us_group.loc[self.us_group['Level2Name'] == group, 'ETF'].iloc[0]
        idx = self.us_group.loc[self.us_group['Level2Name'] == group, 'Level2Index'].iloc[0] + " INDEX"
        val_metrics = self.us_group.loc[self.us_group['Level2Name'] == group, 'Valuation Metrics'].iloc[0]
        cix = self.us_cix.loc[self.us_cix["Ticker"] == self.ticker, "CIX"].iloc[0] + " index"
        return val_metrics, idx, etf, cix

    def get_emea(self):
        short_ticker = self.ticker.split(' ')[0] + " " + self.ticker.split(' ')[1]
        try:
            val_metrics = self.eu_cix.loc[self.eu_cix['Ticker'] == short_ticker, 'Valuation Metrics'].iloc[0]
        except IndexError:
            tar = exchange_conf.get(self.ticker.split(' ')[1])
            short_ticker = self.ticker.split(' ')[0] + ' ' + tar
            val_metrics = self.eu_cix.loc[self.eu_cix['Ticker'] == short_ticker, 'Valuation Metrics'].iloc[0]
        idx = self.eu_cix.loc[self.eu_cix['Ticker'] == short_ticker, 'Level2Index'].iloc[0] + " INDEX"
        etf = self.eu_cix.loc[self.eu_cix['Ticker'] == short_ticker, 'US ETF'].iloc[0]
        cix = self.eu_cix.loc[self.eu_cix["Ticker"] == short_ticker, "CIX"].iloc[0] + " index"
        return val_metrics, idx, etf, cix


def oss_ratio_calc(ticker, metrics_dict, e_data, i_data, metric_data, metric):
    e_individual = e_data[['Date', ticker]]
    relevant_index = metrics_dict.get(ticker).get('idx')
    i_individual = i_data[['Date', relevant_index]]
    eq_in = pd.merge(e_individual, i_individual, how='left', on=['Date'])
    eq_in['ratio'] = eq_in[ticker] / eq_in[relevant_index]
    oss_vol = ((eq_in[['ratio']].iloc[-1] - eq_in.loc[:, 'ratio'].mean()) / eq_in.loc[:, 'ratio'].std()).values[0]
    metric_data[ticker] = {'rel_hist': oss_vol, 'sector_avg': float(eq_in[['ratio']].values[-1])}
    return metric_data


def oss_val_calc(ticker, metrics_dict, e_data, i_data, metric_data, metric):
    e_individual = e_data[['Date', ticker]]
    abs_val = e_data[ticker].iloc[-1]
    relevant_index = metrics_dict.get(ticker).get(metric)
    i_individual = i_data[['Date', relevant_index]]
    eq_in = pd.merge(e_individual, i_individual, how='left', on=['Date'])
    eq_in['ratio'] = eq_in[ticker] / eq_in[relevant_index]
    oss_vol = ((eq_in[['ratio']].iloc[-1] - eq_in.loc[:, 'ratio'].mean()) / eq_in.loc[:, 'ratio'].std()).values[0]
    metric_data[ticker] = {'rel_hist': oss_vol, 'sector_avg': float(eq_in[['ratio']].values[-1]), 'abs_val': abs_val}
    return metric_data


def oss_vol_calc(ticker, metrics_dict, e_data, i_data, metric_data, metric):
    e_individual = e_data[['Date', ticker]]
    relevant_index = metrics_dict.get(ticker).get(metric)
    i_individual = i_data[['Date', relevant_index]]
    eq_in = pd.merge(e_individual, i_individual, how='left', on=['Date'])
    eq_in['ratio'] = eq_in[ticker] / eq_in[relevant_index]
    oss_vol = ((eq_in[['ratio']].iloc[-1] - eq_in.loc[:, 'ratio'].mean()) / eq_in.loc[:, 'ratio'].std()).values[0]
    metric_data[ticker] = oss_vol
    return metric_data


def get_ratio_calc(ticker, metrics_dict, e_data, i_data, metric_data, metric):
    e_individual = e_data[['Date', ticker]]
    relevant_index = metrics_dict.get(ticker).get(metric)
    i_individual = i_data[['Date', relevant_index]]
    eq_in = pd.merge(e_individual, i_individual, how='left', on=['Date'])
    eq_in['ratio'] = eq_in[ticker]/eq_in[relevant_index]
    oss_vol = ((eq_in[['ratio']].iloc[-1] - eq_in.loc[:, 'ratio'].mean())/eq_in.loc[:, 'ratio'].std()).values[0]
    metric_data[ticker] = oss_vol
    return metric_data


def oss_yield_calc(ticker, metrics_dict, e_data, i_data, metric_data, metric):
    e_individual = e_data[['Date', ticker]]
    relevant_index = metrics_dict.get(ticker).get('idx')
    i_individual = i_data[['Date', relevant_index]]
    eq_in = pd.merge(e_individual, i_individual, how='left', on=['Date'])
    eq_in['ratio'] = eq_in[ticker]/eq_in[relevant_index]
    oss_vol = ((eq_in[['ratio']].iloc[-1] - eq_in.loc[:, 'ratio'].mean())/eq_in.loc[:, 'ratio'].std()).values[0]
    metric_data[ticker] = oss_vol
    return metric_data


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_time_form(form, t):
    return t.strftime(form).replace('{S}', str(t.day) + suffix(t.day))


def get_eq_metric_history(metrics_df, metric, choice, p_start, p_end):
    tickers = metrics_df.loc[metrics_df[choice] == metric]['ticker'].to_list()
    val = blp.bdh(tickers, metric, p_start.strftime('%Y%m%d'), p_end.strftime('%Y%m%d'),
                  best_fperiod_override="bf")
    return val


def get_in_metric_history(metrics_df, metric, choice, p_start, p_end):
    idx = list(metrics_df.loc[metrics_df[choice] == metric].idx.unique())
    val = blp.bdh(idx, metric, p_start.strftime('%Y%m%d'), p_end.strftime('%Y%m%d'),
                  best_fperiod_override="bf")
    return val


def oss_perf_calc(ticker, oss_df, e_data, i_data, metric_data):
    e_individual = e_data[['Date', ticker]]
    relevant_index = oss_df[oss_df['ticker'] == ticker]['idx'].values[0]
    i_individual = i_data[['Date', relevant_index]]
    eq_in = pd.merge(e_individual, i_individual, how='left', on=['Date'])
    eq_in['ratio'] = eq_in[ticker]/eq_in[relevant_index]
    oss_vol = (((eq_in[['ratio']].iloc[-1] - eq_in.loc[:, 'ratio'].iloc[0]) * 100)/eq_in.loc[:, 'ratio'].iloc[0]).values[0]
    metric_data[ticker] = oss_vol
    return metric_data


def check_word_str(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search


def get_client_tickers_dict(care_data, care_data_path):
    client_tickers = {}
    for care in care_data.sheet_names:
        universe = pd.read_excel(care_data_path,
                                 sheet_name=care)
        ticker_list = universe['Ticker'].to_list()
        ticker_list = [item for item in ticker_list if not pd.isnull(item)]
        client_tickers[care] = ticker_list
    return client_tickers


def send_email(client_emails, cc_email, template, day):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = client_emails
    mail.CC = cc_email
    mail.Subject = f"Olivetree: OSS comments for names reporting {day.strftime('%A')}"
    mail.GetInspector
    mail.SentOnBehalfOfName = 'olivetree.europe@olivetreeglobal.com'
    body_start = re.search("<body.*?>", mail.HTMLBody)
    mail.HTMLbody = re.sub(body_start.group(), body_start.group() + template, mail.HTMLBody)
    mail.Send()


def get_multi_recipients(recipients):
    recipient_txt = ""
    for reci in recipients:
        recipient_txt += reci + ";"
    return recipient_txt


def get_equities_txt(text_file):
    text = open(text_file, "r")
    lines = text.read().split('\n')
    lines = [ticker for ticker in lines if ticker != '']
    lines_e = [ticker.replace(' Equity', '') for ticker in lines]
    return lines_e, lines

