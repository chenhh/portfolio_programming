# -*- coding: utf-8 -*-
"""
Author: Hung-Hsin Chen <chenhh@par.cse.nsysu.edu.tw>
License: GPL v3
"""

import platform
import os
import datetime as dt

# data storage
node_name = platform.node()

if node_name == 'X220':
    # windows 10
    PROJECT_DIR = r'C:\Users\chen1\Documents\workspace_pycharm\portfolio_programming'
    TMP_DIR = r'e:'
else:
    # ubuntu linux 16.04
    PROJECT_DIR = r'/home/chenhh/workspace_pycharm/portfolio_programming'
    TMP_DIR = r'/tmp'

DATA_DIR = os.path.join(PROJECT_DIR, 'data')

TAIEX_SYMBOL_JSON = os.path.join(DATA_DIR,
                                 'TAIEX_20050103_50largest_listed_market_cap.json')

TAIEX_PANEL_PKL = os.path.join(TMP_DIR,
                             'TAIEX_20050103_50largest_listed_market_cap_panel.pkl')

SCENARIO_SET_DIR = TMP_DIR

# solver
PROG_SOLVER = 'cplex'

# simulation
EXP_START_DATE = dt.date(2005, 1, 3)
EXP_END_DATE = dt.date(2014, 12, 31)
SCENARIO_START_DATE = EXP_START_DATE
SCENARIO_END_DATE = EXP_END_DATE
BUY_TRANS_FEE = 0.001425
SELL_TRANS_FEE = 0.001425