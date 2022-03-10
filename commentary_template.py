# Analyst rating + PT
import random

import numpy as np

from config import today_day


def anr_pt_temp(anr_txt):
    anr_start = f'The Sell Side has a consensus {anr_txt} rating, '
    return anr_start


def brief_anr_rating(anr_txt):
    return f'Sell Side cons "{anr_txt}" rating, '


def brief_anr_summary(pt_chg):
    return {'Hold': {0: f'{pt_chg}% downside to median street PT.',
                     1: f'{pt_chg}% downside to median street PT.',
                     2: 'stock trading close to median street PT.',
                     3: f'{pt_chg}% upside to street PT.',
                     4: f'{pt_chg}% upside to street PT.'
                     },
            'Strong Sell': {0: f'{pt_chg}% downside to median street PT.',
                            1: f'{pt_chg}% downside to median street PT.',
                            2: 'stock trading broadly in line with median street PT.',
                            3: f'{pt_chg}% upside to street PT.',
                            },
            'Sell': {0: f'{pt_chg}% downside to median street PT.',
                     1: f'{pt_chg}% downside to median street PT.',
                     2: 'stock trading broadly in line with median street PT.',
                     3: f'{pt_chg}% upside to street PT.',
                     },
            'Buy': {0: f'{pt_chg}% downside to median street PT.',
                    1: 'stock trading close to median street PT',
                    2: f'{pt_chg}% upside to street PT.',
                    3: f'{pt_chg}% upside to street PT.',
                    },
            'Strong Buy': {0: f'{pt_chg}% downside to median street PT.',
                           1: 'stock trading broadly in line with median street PT',
                           2: f'{pt_chg}% upside to street PT.',
                           3: f'{pt_chg}% upside to street PT.',
                           },

            }


def anr_summary(pt_chg):
    return {'Hold': {0: f'despite {pt_chg}% downside to median street PT.',
                     1: f'with a modest {pt_chg}% downside to median street PT.',
                     2: 'with the stock trading close to median street PT',
                     3: f'with a modest {pt_chg}% upside to street PT.',
                     4: f'despite {pt_chg}% upside to street PT.'
                     },
            'Strong Sell': {0: f'with {pt_chg}% downside to median street PT.',
                            1: f'despite a modest {pt_chg}% downside to median street PT.',
                            2: 'despite the stock trading broadly in line with median street PT.',
                            3: f'despite {pt_chg}% upside to street PT.',
                            },
            'Sell': {0: f'with {pt_chg}% downside to median street PT.',
                     1: f'with a modest {pt_chg}% downside to median street PT.',
                     2: 'despite the stock trading broadly in line with median street PT.',
                     3: f'despite {pt_chg}% upside to street PT.',
                     },
            'Buy': {0: f'despite {pt_chg}% downside to median street PT.',
                    1: 'despite the stock trading close to median PT',
                    2: f'with a modest {pt_chg}% upside to street PT.',
                    3: f'with {pt_chg}% upside to street PT.',
                    },
            'Strong Buy': {0: f'despite {pt_chg}% downside to median street PT.',
                           1: 'despite the stock trading broadly in line with median street PT.',
                           2: f'with only a modest {pt_chg}% upside to street PT.',
                           3: f'with {pt_chg}% upside to street PT.',
                           }
            }


def eps_chg_temp(fwd_eps):
    if round(fwd_eps, 1) == 0:
        return f"12M blended fwd EPS estimates flat 1M are "
    elif 100 > fwd_eps > 0:
        return f"12M blended fwd EPS estimates +{str(round(fwd_eps, 1))}% 1M are "
    elif fwd_eps < 0:
        return f"12M blended fwd EPS estimates {str(round(fwd_eps, 1))}% 1M are "
    elif fwd_eps >= 100:
        return ""
    elif fwd_eps <= -100:
        return ""


def eps_summary(per_sec):
    if per_sec > 96:
        return 'best in class.'
    elif 96 >= per_sec >= 90:
        return 'amongst the best in class.'
    elif 89 >= per_sec >= 80:
        return 'top quintile of sector.'
    elif 79 >= per_sec >= 75:
        return 'top 1/4 in class.'
    elif 74 >= per_sec >= 67:
        return 'top 1/3 in class.'
    elif 66 >= per_sec >= 60:
        return 'slightly above class avg.'
    elif 59 >= per_sec >= 41:
        return 'in line with class avg.'
    elif 40 >= per_sec >= 34:
        return 'slightly below class avg.'
    elif 33 >= per_sec >= 26:
        return 'bottom 1/3 in class.'
    elif 25 >= per_sec >= 21:
        return 'bottom 1/4 in class.'
    elif 20 >= per_sec >= 11:
        return 'bottom quintile of sector.'
    elif 10 >= per_sec >= 4:
        return 'amongst the worst in class.'
    elif 3 >= per_sec >= 0:
        return 'worst in class.'


def dy_start(dy, dy_sec_avg):
    if dy >= 3.5:
        return f'The stock is expected to yield {round(dy, 1)}% the next 12M, which at {round(dy_sec_avg, 1)}x '


def dy_commentary(dy_rel_hist):
    if -2 >= dy_rel_hist:
        return 'the sector average is over 2 SDs below historical relative avg.'
    elif -1 >= dy_rel_hist > -2:
        return 'the sector average is more than 1SD below historical relative avg.'
    elif -0.5 >= dy_rel_hist > -1:
        return 'the sector average is a touch below historical relative avg.'
    elif 0.5 > dy_rel_hist > -0.5:
        return 'the sector average is in line with historical relative avg.'
    elif 1 > dy_rel_hist >= 0.5:
        return 'the sector average is a touch above historical relative avg.'
    elif 2 > dy_rel_hist >= 1:
        return 'the sector average is more than 1 SD above historical relative avg.'
    elif dy_rel_hist >= 2:
        return 'the sector average is over 2 SD above historical relative avg.'


def brief_dy_start(dy, dy_sec_avg):
    if dy >= 3.5:
        return f'12m fwd yield is {round(dy, 1)}%, {round(dy_sec_avg, 1)}x the sector avg which is '


def brief_dy_commentary(dy_rel_hist):
    if -2 >= dy_rel_hist:
        return '>2 SDs below 2yr rel avg.'
    elif -1 >= dy_rel_hist > -2:
        return '>1 SD below 2yr rel avg.'
    elif -0.5 >= dy_rel_hist > -1:
        return 'a touch below 2yr rel avg.'
    elif 0.5 > dy_rel_hist > -0.5:
        return 'in line with 2yr rel avg.'
    elif 1 > dy_rel_hist >= 0.5:
        return 'a touch above 2yr rel avg.'
    elif 2 > dy_rel_hist >= 1:
        return '>1 SD above 2yr rel avg.'
    elif dy_rel_hist >= 2:
        return '>2 SD above 2yr rel avg.'


def options_summary(vol_ratio):
    if vol_ratio is None:
        pass
    elif -2 >= vol_ratio:
        return 'a lot less risk vs the sector with relative implied volatility over 2 SDs below historical avg. '
    elif -1 >= vol_ratio > -2:
        return 'less risk than usual on a relative basis with implied vol vs the sector more than 1 SD below ' \
               'historical avg. '
    elif -0.5 >= vol_ratio > -1:
        return 'broadly normal amounts of risk vs the sector with rel IV a touch below historical avg. '
    elif 0.5 > vol_ratio > -0.5:
        return 'usual amounts of risk vs the sector with relative implied vol in line with historical avg. '
    elif 1 > vol_ratio >= 0.5:
        return 'broadly normal amounts of relative risk with IV vs the sector, a touch above historical avg. '
    elif 2 > vol_ratio >= 1:
        return 'more than the usual amount of risk vs the sector with relative implied vol more than 1 SD above ' \
               'historical avg. '
    elif vol_ratio >= 2:
        return 'well above the usual amounts of risk vs the sector with relative implied volatility over 2 SD' \
               'above historical avg. '


def brief_options(vol_ratio):
    if vol_ratio is None:
        pass
    elif -2 >= vol_ratio:
        return 'Options market pricing a lot less risk vs sector, rel IV over 2 SDs below hist avg. '
    elif -1 >= vol_ratio > -2:
        return 'Options market pricing less risk than usual, IV vs sector more than 1 SD below hist avg. '
    elif -0.5 >= vol_ratio > -1:
        return 'Options market pricing broadly normal risk vs sector, rel IV a touch below hist avg. '
    elif 0.5 > vol_ratio > -0.5:
        return 'Options neutral. '
    elif 1 > vol_ratio >= 0.5:
        return 'Options market pricing broadly normal relative risk with IV vs sector a touch above hist avg. '
    elif 2 > vol_ratio >= 1:
        return 'Options market pricing more than usual risk vs sector, rel IV more than 1 SD above hist avg. '
    elif vol_ratio >= 2:
        return 'Options market pricing well above the usual relative risk, implied vol vs sector over 2 SD above hist ' \
               'avg. '


def short_summary(ffs, dtc):
    if 0.1 > ffs:
        return f"There is no short base."
    elif np.isnan(ffs):
        return ""
    else:
        return f"Short interest is {str(round(ffs, 1))}% FFS, {str(round(dtc, 1))} DTC."


def daily_rsi_summary(rsi_p):
    if rsi_p >= 80:
        daily_rsi = 80
        rsi_summary = f'Technically heavily overbought on a daily abs RSI of {str(round(rsi_p, 1))} '
        return daily_rsi, rsi_summary
    elif 79 >= rsi_p >= 70:
        daily_rsi = 70
        rsi_summary = f'Technically overbought on a daily abs RSI of {str(round(rsi_p, 1))} '
        return daily_rsi, rsi_summary
    elif 69 >= rsi_p >= 60:
        daily_rsi = 60
        rsi_summary = f'Towards technically overbought territory on daily abs RSI of {str(round(rsi_p, 1))} '
        return daily_rsi, rsi_summary
    elif 59 >= rsi_p >= 41:
        daily_rsi = 41
        rsi_summary = f'Neither overbought nor oversold on a daily abs RSI of {str(round(rsi_p, 1))} '
        return daily_rsi, rsi_summary
    elif 40 >= rsi_p >= 31:
        daily_rsi = 31
        rsi_summary = f'Towards technically oversold territory on daily abs RSI of {str(round(rsi_p, 1))} '
        return daily_rsi, rsi_summary
    elif 30 >= rsi_p >= 21:
        daily_rsi = 21
        rsi_summary = f'Technically oversold on a daily abs RSI of {str(round(rsi_p, 1))} '
        return daily_rsi, rsi_summary
    elif 20 >= rsi_p:
        daily_rsi = 20
        rsi_summary = f'Technically heavily oversold on a daily abs RSI of {str(round(rsi_p, 1))}'
        return daily_rsi, rsi_summary


def brief_rsi_summary(rsi_p):
    if rsi_p >= 80:
        daily_rsi = 80
        rsi_summary = f'Heavily overbought abs (RSI {str(round(rsi_p))})'
        return daily_rsi, rsi_summary
    elif 80 > rsi_p >= 70:
        daily_rsi = 70
        rsi_summary = f'Overbought abs (RSI {str(round(rsi_p))})'
        return daily_rsi, rsi_summary
    elif 70 > rsi_p >= 60:
        daily_rsi = 60
        rsi_summary = f'Towards overbought abs (RSI {str(round(rsi_p))})'
        return daily_rsi, rsi_summary
    elif 60 > rsi_p >= 40:
        daily_rsi = 41
        rsi_summary = f''
        return daily_rsi, rsi_summary
    elif 40 > rsi_p >= 30:
        daily_rsi = 31
        rsi_summary = f'Towards oversold abs (RSI {str(round(rsi_p))})'
        return daily_rsi, rsi_summary
    elif 30 > rsi_p >= 20:
        daily_rsi = 21
        rsi_summary = f'Oversold abs (RSI {str(round(rsi_p))})'
        return daily_rsi, rsi_summary
    elif 20 > rsi_p:
        daily_rsi = 20
        rsi_summary = f'Heavily oversold abs (RSI {str(round(rsi_p))})'
        return daily_rsi, rsi_summary


def brief_sector_rsi_summary(rsi_cix):
    return {80: {0: f' and vs sector (RSI {str(round(rsi_cix))}). ',
                 1: f' and overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 2: f', towards overbought relative (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f' tho towards oversold rel (RSI {str(round(rsi_cix))}). ',
                 5: f' tho oversold relative (RSI {str(round(rsi_cix))}). ',
                 6: f' tho heavily oversold vs sector (RSI {str(round(rsi_cix))}). '
                 },
            70: {0: f' and massively overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 1: f' and rel (RSI {str(round(rsi_cix))}). ',
                 2: f', near overbought rel (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f' tho near oversold rel (RSI {str(round(rsi_cix))}). ',
                 5: f' tho oversold rel (RSI {str(round(rsi_cix))}). ',
                 6: f' tho heavily oversold vs sector (RSI {str(round(rsi_cix))}). '
                 },
            60: {0: f', tho massively overbought rel (RSI {str(round(rsi_cix))}). ',
                 1: f' and overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 2: f' and rel (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f' tho close to oversold rel (RSI {str(round(rsi_cix))}). ',
                 5: f' tho oversold vs sector (RSI {str(round(rsi_cix))}). ',
                 6: f' but massively oversold rel (RSI {str(round(rsi_cix))}). '
                 },
            41: {0: f'Massively overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 1: f'Overbought relative (RSI {str(round(rsi_cix))}). ',
                 2: f'Close to overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f'Towards oversold rel (RSI {str(round(rsi_cix))}). ',
                 5: f'Oversold relative (RSI {str(round(rsi_cix))}). ',
                 6: f'Massively oversold rel (RSI{str(round(rsi_cix))}). '
                 },
            31: {0: f' but heavily overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 1: f' tho overbought rel (RSI {str(round(rsi_cix))}). ',
                 2: f' but near to overbought rel (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f' and rel (RSI {str(round(rsi_cix))}). ',
                 5: f' and oversold rel (RSI {str(round(rsi_cix))}). ',
                 6: f', massively oversold rel (RSI {str(round(rsi_cix))}). '
                 },
            21: {0: f' tho massively overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 1: f' tho overbought rel (RSI {str(round(rsi_cix))}). ',
                 2: f' tho close to overbought rel (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f', towards oversold vs sector (RSI {str(round(rsi_cix))}). ',
                 5: f' and rel (RSI {str(round(rsi_cix))}). ',
                 6: f' and heavily so rel (RSI {str(round(rsi_cix))}). '
                 },
            20: {0: f' tho massively overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 1: f' tho overbought vs sector (RSI {str(round(rsi_cix))}). ',
                 2: f' but towards overbought rel, (RSI {str(round(rsi_cix))}). ',
                 3: f'',
                 4: f' tho just towards oversold rel (RSI {str(round(rsi_cix))}). ',
                 5: f' and oversold rel (RSI {str(round(rsi_cix))}). ',
                 6: f' and rel (RSI {str(round(rsi_cix))}). '
                 },
            }


def sector_rsi_summary(rsi_cix):
    return {80: {0: f'and sector rel RSI of {str(round(rsi_cix, 1))}',
                 1: f'and overbought vs the sector on rel RSI of {str(round(rsi_cix, 1))}',
                 2: f'though only towards overbought territory vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 3: f'though not vs the sector with a rel RSI of {str(round(rsi_cix, 1))}',
                 4: f'though closer to technically oversold territory on a relative basis with an \
                     RSI of {str(round(rsi_cix, 1))}',
                 5: f'though oversold vs the sector on a rel RSI of {str(round(rsi_cix, 1))}',
                 6: f'though heavily oversold on a rel RSI of {str(round(rsi_cix, 1))}'
                 },
            70: {0: f'and massively overbought vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 1: f'and vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 2: f'and near to overbought territory on a relative RSI of {str(round(rsi_cix, 1))}',
                 3: f'though not close to overbought levels vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 4: f'though towards oversold territory vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 5: f'though technically oversold on a relative RSI of {str(round(rsi_cix, 1))}',
                 6: f'though well into oversold territory with an RSI vs the sector of {str(round(rsi_cix, 1))}'
                 },
            60: {0: f'though massively overbought vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 1: f'and is overbought vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 2: f'and on a relative RSI of {str(round(rsi_cix, 1))}',
                 3: f'though not near in relative terms, RSI {str(round(rsi_cix, 1))}',
                 4: f'however is close to oversold territory on a relative basis with an RSI of {str(round(rsi_cix, 1))}',
                 5: f'though technically oversold vs the sector, RSI {str(round(rsi_cix, 1))}',
                 6: f'but massively oversold vs the sector on an RSI of {str(round(rsi_cix, 1))}'
                 },
            41: {0: f'however well into technically overbought territory on a relative RSI of {str(round(rsi_cix, 1))}',
                 1: f'though technically overbought vs the sector, RSI {str(round(rsi_cix, 1))}',
                 2: f'though is towards overbought territory in relative terms on an RSI of {str(round(rsi_cix, 1))}',
                 3: f'and a relative RSI of {str(round(rsi_cix, 1))}',
                 4: f'though closer to technically oversold territory vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 5: f'though technically oversold on a relative RSI of {str(round(rsi_cix, 1))}',
                 6: f'however is massively oversold vs the sector on an RSI of {str(round(rsi_cix, 1))}'
                 },
            31: {0: f'but heavily overbought vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 1: f'though technically overbought on a relative basis with an RSI of {str(round(rsi_cix, 1))}',
                 2: f'but closer to technically overbought territory on a relative RSI of {str(round(rsi_cix, 1))}',
                 3: f'though technically neither overbought nor oversold on a rel RSI of {str(round(rsi_cix, 1))}',
                 4: f'and on a relative RSI of {str(round(rsi_cix, 1))}',
                 5: f'and oversold on a relative RSI of {str(round(rsi_cix, 1))}',
                 6: f'though massively oversold vs the sector on a rel RSI of {str(round(rsi_cix, 1))}'
                 },
            21: {0: f'however is massively overbought vs the sector on a rel RSI of {str(round(rsi_cix, 1))}',
                 1: f'though technically overbought vs the sector, RSI {str(round(rsi_cix, 1))}',
                 2: f'though close to overbought levels on a relative basis, RSI {str(round(rsi_cix, 1))}',
                 3: f'though not near on a relative basis with an RSI of {str(round(rsi_cix, 1))}',
                 4: f'and towards oversold territory vs the sector, RSI {str(round(rsi_cix, 1))}',
                 5: f'and on a relative RSI of {str(round(rsi_cix, 1))}',
                 6: f'and massively so on a relative basis with an RSI of {str(round(rsi_cix, 1))}'
                 },
            20: {0: f'though is massively overbought on relative RSI of {str(round(rsi_cix, 1))}',
                 1: f'though is technically overbought vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 2: f'but is near to technically overbought territory vs the sector, RSI {str(round(rsi_cix, 1))}',
                 3: f'but neither overbought nor oversold vs the sector, RSI {str(round(rsi_cix, 1))}',
                 4: f'though just near to oversold territory on a relative RSI of {str(round(rsi_cix, 1))}',
                 5: f'and also oversold vs the sector on an RSI of {str(round(rsi_cix, 1))}',
                 6: f'and vs the sector on an RSI of {str(round(rsi_cix, 1))}'
                 },
            }


def adj_price_start(perf_1m, perf_3m):
    if perf_1m <= -8 and perf_3m <= -8:
        return ' has materially underperformed, '
    elif perf_1m >= 8 and perf_3m >= 8:
        return ' has materially outperformed, '
    else:
        return ' is '


def price_pct_start(perf):
    if -8 >= perf:
        return f'Down {str(abs(perf))}%'
    elif -1 >= perf > -8:
        return f'Down {str(abs(perf))}%'
    elif -0.3 >= perf > -1:
        return f'Down {str(round(abs(perf * 100), 1))}bps'
    elif 0.3 > perf > -0.3:
        return f'Flat'
    elif 1 > perf >= 0.3:
        return f'Up {str(round(perf * 100, 1))}bps'
    elif 8 > perf >= 1:
        return f'Up {str(perf)}%'
    elif perf >= 8:
        return f'Up {str(perf)}%'


def adj_price_pct(perf):
    if -8 >= perf:
        return f'down {str(abs(perf))}%'
    elif -1 >= perf > -8:
        return f'down {str(abs(perf))}%'
    elif -0.3 >= perf > -1:
        return f'down {str(round(abs(perf * 100), 1))}bps'
    elif 0.3 > perf > -0.3:
        return f'flat'
    elif 1 > perf >= 0.3:
        return f'up {str(round(perf * 100, 1))}bps'
    elif 8 > perf >= 1:
        return f'up {str(perf)}%'
    elif perf >= 8:
        return f'up {str(perf)}%'


def brief_price_pct(perf):
    if -8 >= perf > -1:
        return f'down '
    elif 0.3 > perf > -0.3:
        return f'flat '
    elif perf >= 0.3:
        return f'up '


def abs_price_pct(perf):
    perf = round(perf, 1)
    if -8 >= perf:
        return f'has been weak, {str(perf)}%'
    elif -1 >= perf > -8:
        return f'is down {str(abs(perf))}%'
    elif -0.3 >= perf > -1:
        return f'is down {str(abs(round(perf * 100, 1)))}bps'
    elif 0.21 >= perf >= -0.21:
        return f'is flat'
    elif 1 > perf >= 0.3:
        return f'is up {str(round(perf * 100, 1))}bps'
    elif 8 > perf >= 1:
        return f'is up {str(perf)}%'
    elif perf >= 8:
        return f'has been strong, {str(perf)}%'


def price_pct_brief(perf):
    perf = round(perf, 1)
    if -8 >= perf:
        return f'down {str(abs(perf))}%'
    elif -1 >= perf > -8:
        return f'down {str(abs(perf))}%'
    elif -0.3 >= perf > -1:
        return f'down {str(abs(round(perf * 100, 1)))}bps'
    elif 0.21 >= perf >= -0.21:
        return f'flat'
    elif 1 > perf >= 0.3:
        return f'up {str(round(perf * 100, 1))}bps'
    elif 8 > perf >= 1:
        return f'up {str(perf)}%'
    elif perf >= 8:
        return f'up {str(perf)}%'


def valuation_start(val_metric, val_abs_val):
    if val_metric == 'EV/EBITDA':
        return f'on {val_abs_val}x 12m fwd EV/EBITDA, '
    elif val_metric == 'P/E':
        return f'on {val_abs_val}x 12m fwd earnings, '
    elif val_metric == 'P/Book':
        return f'on {val_abs_val}x P/Book, '


def val_hist_summary(val_rel_hist):
    if -3 >= val_rel_hist:
        return '>3 SDs below 2yr rel avg.'
    elif -2 >= val_rel_hist > -3:
        return '>2 SDs below 2yr rel avg.'
    elif -1 >= val_rel_hist > -2:
        return '>1 SD below 2yr rel avg.'
    elif -0.5 >= val_rel_hist > -1:
        return 'shade below 2yr rel avg.'
    elif 0.5 > val_rel_hist > -0.5:
        return 'in line with 2yr rel avg.'
    elif 1 > val_rel_hist >= 0.5:
        return 'shade above 2yr rel avg.'
    elif 2 > val_rel_hist >= 1:
        return '>1 SD above 2yr rel avg.'
    elif 3 > val_rel_hist >= 2:
        return '>2 SD above 2yr rel avg.'
    elif val_rel_hist >= 3:
        return '>3 SD above 2yr rel avg.'


def val_sector_summary(val_sector_avg):
    if 1.025 >= val_sector_avg > 0.975:
        return ' parity to the sector'
    elif 0.1 >= val_sector_avg >= 0:
        return ' > 90% discount to the sector avg multiple'
    elif 0.125 >= val_sector_avg > 0.1:
        return ' a 90% discount to the sector avg multiple'
    elif 0.175 >= val_sector_avg > 0.125:
        return ' a 85% discount to the sector avg multiple'
    elif 0.225 >= val_sector_avg > 0.175:
        return ' a 80% discount to the sector avg multiple'
    elif 0.275 >= val_sector_avg > 0.225:
        return ' a 75% discount to the sector avg multiple'
    elif 0.325 >= val_sector_avg > 0.275:
        return ' a 70% discount to the sector avg multiple'
    elif 0.375 >= val_sector_avg > 0.325:
        return ' a 65% discount to the sector avg multiple'
    elif 0.425 >= val_sector_avg > 0.375:
        return ' a 60% discount to the sector avg multiple'
    elif 0.475 >= val_sector_avg > 0.425:
        return ' a 55% discount to the sector avg multiple'
    elif 0.525 >= val_sector_avg > 0.475:
        return ' a 50% discount to the sector avg multiple'
    elif 0.575 >= val_sector_avg > 0.525:
        return ' a 45% discount to the sector avg multiple'
    elif 0.625 >= val_sector_avg > 0.575:
        return ' a 40% discount to the sector avg multiple'
    elif 0.675 >= val_sector_avg > 0.625:
        return ' a 35% discount to the sector avg multiple'
    elif 0.725 >= val_sector_avg > 0.675:
        return ' a 30% discount to the sector avg multiple'
    elif 0.775 >= val_sector_avg > 0.725:
        return ' a 25% discount to the sector avg multiple'
    elif 0.825 >= val_sector_avg > 0.775:
        return ' a 20% discount to the sector avg multiple'
    elif 0.875 >= val_sector_avg > 0.825:
        return ' a 15% discount to the sector avg multiple'
    elif 0.925 >= val_sector_avg > 0.875:
        return ' a 10% discount to the sector avg multiple'
    elif 0.975 >= val_sector_avg > 0.925:
        return ' a 5% discount to the sector avg multiple'
    elif 1.075 >= val_sector_avg > 1.025:
        return ' a 5% premium to the sector avg multiple'
    elif 1.125 >= val_sector_avg > 1.075:
        return ' a 10% premium to the sector avg multiple'
    elif 1.175 >= val_sector_avg > 1.125:
        return ' a 15% premium to the sector avg multiple'
    elif 1.225 >= val_sector_avg > 1.175:
        return ' a 20% premium to the sector avg multiple'
    elif 1.275 >= val_sector_avg > 1.225:
        return ' a 25% premium to the sector avg multiple'
    elif 1.325 >= val_sector_avg > 1.275:
        return ' a 30% premium to the sector avg multiple'
    elif 1.375 >= val_sector_avg > 1.325:
        return ' a 35% premium to the sector avg multiple'
    elif 1.425 >= val_sector_avg > 1.375:
        return ' a 40% premium to the sector avg multiple'
    elif 1.475 >= val_sector_avg > 1.425:
        return ' a 45% premium to the sector avg multiple'
    elif 1.525 >= val_sector_avg > 1.475:
        return ' a 50% premium to the sector avg multiple'
    elif 1.575 >= val_sector_avg > 1.525:
        return ' a 55% premium to the sector avg multiple'
    elif 1.625 >= val_sector_avg > 1.575:
        return ' a 60% premium to the sector avg multiple'
    elif 1.675 >= val_sector_avg > 1.625:
        return ' a 65% premium to the sector avg multiple'
    elif 1.725 >= val_sector_avg > 1.675:
        return ' a 70% premium to the sector avg multiple'
    elif 1.775 >= val_sector_avg > 1.725:
        return ' a 75% premium to the sector avg multiple'
    elif 1.825 >= val_sector_avg > 1.775:
        return ' a 80% premium to the sector avg multiple'
    elif 1.875 >= val_sector_avg > 1.825:
        return ' a 85% premium to the sector avg multiple'
    elif 1.9 >= val_sector_avg > 1.875:
        return ' a 90% premium to the sector avg multiple'
    elif 2 >= val_sector_avg > 1.9:
        return ' > 90% premium to the sector avg multiple'
    elif val_sector_avg > 2:
        return f' {round(val_sector_avg, 1)}x the sector avg'


def oss_summary(score, comp_name):
    if score < 27.4:
        return f"<u><b>{comp_name}: OSS {round(score)}% - Extreme Bearish sentiment. </b></u>"
    if 27.4 <= score <= 33:
        return f"<u><b>{comp_name}: OSS {round(score)}% - Bearish sentiment. </b></u>"
    if 33 < score < 67:
        return f"<u><b>{comp_name}: OSS {round(score)}% - Neutral sentiment. </b></u>"
    if 67 <= score < 72.6:
        return f"<u><b>{comp_name}: OSS {round(score)}% - Bullish sentiment. </b></u>"
    if 72.6 <= score:
        return f"<u><b>{comp_name}: OSS {round(score)}% - Extreme Bullish sentiment. </b></u>"


def get_bear(oss_asc):
    intro = ''
    for ticker, oss in oss_asc.items():
        if 27.4 > oss:
            intro += f'<b>{ticker}</b> (OSS: {round(oss)}% - Extreme), '
        if 33 >= oss >= 27.4:
            intro += f'<b>{ticker}</b> (OSS: {round(oss)}%), '
    return intro[:-2]


def get_bull(oss_desc):
    intro = ''
    for ticker, oss in oss_desc.items():
        if 72.6 <= oss:
            intro += f'<b>{ticker}</b> (OSS: {round(oss)}% - Extreme), '
        if 67 <= oss < 72.6:
            intro += f'<b>{ticker}</b> (OSS: {round(oss)}%), '
    return intro[:-2]


def get_short_base(ffs_dict):
    intro = ''
    for ticker, ffs in ffs_dict.items():
        if ffs >= 5:
            intro += f'<b>{ticker}</b> (SI: {round(ffs, 1)}% FFS), '
    return intro[:-2]


def get_valuation_flag(val_hist):
    flag = ''
    for ticker, val_hist in val_hist.items():
        if -2 >= val_hist:
            flag += f'<b>{ticker}</b> ({round(val_hist, 1)} SD), '
        elif val_hist >= 2:
            flag += f'<b>{ticker}</b> ({round(val_hist, 1)} SD), '
    return flag[:-2]


def empty_to_none(original):
    if original == '':
        return 'None'
    else:
        return original


intro = f'Please see below details on positioning in selected stocks that report on {today_day} '
product_notes = f'<br><HTML><BODY style="font-size:9pt;font-family:Calibri"> <b>Product Notes:</b><br>' \
                ' The above OSS comments, utilising data from 3rd party vendors including Bloomberg and IHS Markit,' \
                ' are driven by the Olivetree European Reporting and Positioning Calendar. This covers stocks in ' \
                'Europe with Mkt Cap >€1bn and ADV >€1m. Names due to report but that have insufficient data' \
                ' to generate an OSS score or are outside of the OSS universe will be noted below the main' \
                ' body of this summary. <br><br> <b>Terminology:</b><br>The Olivetree Sentiment Score (OSS) is a ' \
                'measure of sentiment and market positioning based on proprietary analysis of a variety of different' \
                ' metrics. We classify scores below 27.4% as Extreme Bearish and above 72.6% as Extreme Bullish.<br>' \
                'Our ‘High Short Base’ hurdle is set at 5% of free-float, whilst our ‘Relative Valuation Flag‘ is' \
                ' triggered by Z scores ≥ 2 and ≤-2 standard deviations from the stock’s avg multiple vs its sector ' \
                'over the prior 2yrs. ‘Rel RSI’ is the relative strength of the stock against its closest sector ' \
                'index, ‘Fwd yield’ is the 12m blended fwd dividend yield and ‘Rel IV’ is the 3M Implied Volatility' \
                ' versus sector. Short Interest ‘FFS’ is Free Float Shares, and ‘DTC’ is Days to Cover based using 30' \
                ' Day Average Daily Volume of the greater of EU Composite Ticker or Primary Exchange Ticker.' \

