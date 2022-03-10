import datetime as dt
from datetime import date

import pandas as pd
from pandas.tseries.offsets import BDay
from dateutil.relativedelta import relativedelta

# dates
tdy = dt.date.today()
one_biz_f_tdy = date.today() + BDay(1)
this_mon = tdy - dt.timedelta(days=tdy.weekday())
this_fri = tdy - dt.timedelta(days=tdy.weekday() - 4)
one_m_f_tdy = date.today() - relativedelta(months=1)
twenty_biz_f_tdy = date.today() - BDay(20)
two_y_f_tdy = date.today() - relativedelta(days=2 * 365)
today_day = dt.datetime.now().strftime("%A")
next_mon = tdy + dt.timedelta(days=(7 - tdy.weekday()))
next_fri = tdy + dt.timedelta(days=(7 - tdy.weekday()) + 4)

# files
eu_cix_map = pd.read_csv(r'S:\US\NOTAS - US Office\Non-US Stock Sectors.csv')
us_cix_map = pd.read_csv(r'S:\US\NOTAS - US Office\CIX_Dataset.csv')
us_cix_map = us_cix_map.drop_duplicates(subset='Ticker', keep="last")
us_grp_map = pd.read_csv(r'S:\US\NOTAS - US Office\GroupNameToIndex.csv').dropna(how='all', axis=0)
us_grp_map.dropna(how='all', axis=1, inplace=True)

# tickers exclusion due to bbg cix mismatch
idx_err = pd.read_csv(r'S:\US\NOTAS - US Office\bbg_cix_miss.csv')
idx_err = idx_err.ticker.to_list()
idx_err = [ticker + ' Equity' for ticker in idx_err]

# Short Interest exclusion
si_err = pd.read_csv(r'S:\US\NOTAS - US Office\bbg_si_miss.csv')
si_err = si_err.ticker.to_list()
si_err = [ticker + ' Equity' for ticker in si_err]

# tickers
selected = pd.read_csv(r'./data/selected_universe.csv')
sel_tics = selected.ticker.to_list()
sel_tics_e = [ticker + ' Equity' for ticker in sel_tics]

# exchange dictionary
exchange_conf = {"SE": "SW", "SW": "SE",
                 "GY": "GR", "GR": "GY",
                 "ID": "LN", "LN": "ID",
                 "SQ": "SM", "SM": "SQ",
                 "US": "UN", "UN": "US",
                 "SF": "SS", "SS": "SF",
                 "UW": "US", "US": "UW"
                 }

# Metrics configuration
metrics_conf = {"P/E": {"eq": "BEST_PE_RATIO",
                        "in": "BEST_PE_RATIO",
                        "exclusion": 75},
                "P/Book": {"eq": "BEST_PX_BPS_RATIO",
                           "in": "BEST_PX_BPS_RATIO",
                           "exclusion": 10},
                "EV/EBITDA": {"eq": "BEST_EV_TO_BEST_EBITDA",
                              "in": "IDX_EST_EV_EBITDA",
                              "exclusion": 50}
                }

# Unwanted companies ending
comp_ending = ['NV', 'Plc', 'PLC', 'AG', 'SA', 'AB', 'ASA', 'Ltd', 'ltd', 'SE']

# fake tap
fake_tap = '<pre>-&nbsp;&nbsp;&nbsp;&nbsp;</pre>'

cc_recipients = ['linus.ng@olivetreeglobal.com', 'alex.bowden@olivetreeglobal.com', 'matt.worby@olivetreeglobal.com']
testing_cc = ['linus.ng@olivetreeglobal.com', 'alex.bowden@olivetreeglobal.com']

# email_distribution = {'Olivetree Focus': {'client': [],
#                                           'ot': ['Matthew.Thomas@olivetreeglobal.com'] + cc_recipients},
#                       'MattT OT Swiss': {'client': ['Matthew.Thomas@olivetreeglobal.com'],
#                                          'ot': cc_recipients},
#                       'SDickgieser Point 72': {'client': ['Adrian.Ahmadi@Point72.com',
#                                                           'daniel.collin@point72.com',
#                                                           'nadine.nieuwstad@point72.com',
#                                                           'Kim.Chatall@Point72.com',
#                                                           'Andrew.Line@Point72.com',
#                                                           'sebastian.dickgiesser@point72.com'],
#                                                'ot': ['Matthew.Thomas@olivetreeglobal.com'] + cc_recipients},
#                       'Corto Pictet': {'client': ['psarreau@pictet.com',
#                                                   'ddufour@pictet.com',
#                                                   'fnassauer@pictet.com'],
#                                        'ot': ['Matthew.Thomas@olivetreeglobal.com'] + cc_recipients},
#                       'Phil Turner': {'client': ['emmh@capgroup.com',
#                                                  'pt@capgroup.com'],
#                                       'ot': ['Matthew.Thomas@olivetreeglobal.com'] + cc_recipients},
#                       'EU Balyasny': {'client': ['emmh@capgroup.com',
#                                                  'pt@capgroup.com'],
#                                       'ot': ['Matthew.Thomas@olivetreeglobal.com'] + cc_recipients},
#                       'Benoit': {'client': ['Benoit.genevier@man.com', 'gareth.davies@man.com'],
#                                  'ot': ['tim.emmott@olivetreeglobal.com'] + cc_recipients},
#                       'GLG Pickard': {'client': ['Neil.pickard@glgpartners.com'],
#                                       'ot': ['tim.emmott@olivetreeglobal.com',
#                                              'Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Capital Gary': {'client': ['gary_carson@capgroup.com', 'NEESHA.PATEL@CAPITALINTERNATIONAL.COM',
#                                                   'daniel.walters@capgroup.com'],
#                                        'ot': ['Tim.Emmott@olivetreeglobal.com'] + cc_recipients},
#                       'Capital Danny': {'client': ['daniel.walters@capgroup.com', 'gary_carson@capgroup.com',
#                                                    'NEESHA.PATEL@CAPITALINTERNATIONAL.COM'],
#                                         'ot': ['Tim.Emmott@olivetreeglobal.com'] + cc_recipients},
#                       'Tim Capital': {'client': ['tim.southwell-sander@capitalworld.com'],
#                                       'ot': ['tim.emmott@olivetreeglobal.com',
#                                              'matthew.thomas@olivetreeglobal.com'] + cc_recipients},
#                       'Richard Pinnington': {'client': ['richard_pinnington@troweprice.com'],
#                                              'ot': ['Tim.Emmott@olivetreeglobal.com'] + cc_recipients},
#                       'Adelio': {'client': ['gilles@adelio.com'],
#                                  'ot': ['Tim.Emmott@olivetreeglobal.com'] + cc_recipients},
#                       'White Momentum': {'client': ['Greg.White@Momentum.co.uk'],
#                                          'ot': ['Tim.Emmott@olivetreeglobal.com'] + cc_recipients},
#                       'Chris Silfverling Covalis': {'client': ['csilfverling@covaliscapital.com'],
#                                                     'ot': ['Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Davidson Kempner': {'client': ['dyates@dkp.com'],
#                                            'ot': ['Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Carlson': {'client': ['fig@cclp.com'],
#                                   'ot': ['Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Moore Cap': {'client': ['simone.arbib@moorecap.co.uk'],
#                                     'ot': ['Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Millenium': {'client': ['amit.sohal@domineum.uk.com', 'nmcgarry8@bloomberg.net'],
#                                     'ot': ['Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Caxton': {'client': ['jdouglas@caxton.com'],
#                                  'ot': ['Mark.Edwards@olivetreeglobal.com'] + cc_recipients},
#                       'Hermes': {'client': [],
#                                  'ot': ['James.Crammond@olivetreeglobal.com'] + cc_recipients},
#                       'SEB': {'client': [],
#                               'ot': ['James.Crammond@olivetreeglobal.com'] + cc_recipients},
#                       'Liontrust': {'client': [],
#                                     'ot': ['James.Crammond@olivetreeglobal.com'] + cc_recipients}
#                       }
email_distribution = {'Olivetree Focus': {'client': [],
                                            'ot': cc_recipients}}
testing_distribution = {'Olivetree Focus': {'client': [],
                                            'ot': testing_cc},
                        'MattT OT Swiss': {'client': [],
                                           'ot': testing_cc},
                        'SDickgieser Point 72': {'client': [],
                                                 'ot': testing_cc},
                        'Corto Pictet': {'client': [],
                                         'ot': testing_cc},
                        'Phil Turner': {'client': [],
                                        'ot': testing_cc},
                        'EU Balyasny': {'client': [],
                                        'ot': testing_cc}
                        }
