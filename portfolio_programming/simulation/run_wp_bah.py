# -*- coding: utf-8 -*-
"""
Author: Hung-Hsin Chen <chen1116@gmail.com>
"""

import logging
import sys
import os
import csv
import pandas as pd
import xarray as xr
import numpy as np
import datetime as dt

import portfolio_programming as pp
from portfolio_programming.simulation.wp_bah import BAHPortfolio


def run_bah(exp_name, group_name, exp_start_date, exp_end_date):
    group_symbols = pp.GROUP_SYMBOLS
    if group_name not in group_symbols.keys():
        raise ValueError('Unknown group name:{}'.format(group_name))
    symbols = group_symbols[group_name]
    n_symbol = len(symbols)

    market = group_name[:2]
    if market == "TW":
        roi_xarr = xr.open_dataarray(pp.TAIEX_2005_MKT_CAP_NC)
    elif market == "US":
        roi_xarr = xr.open_dataarray(pp.DJIA_2005_NC)

    rois = roi_xarr.loc[exp_start_date:exp_end_date, symbols, 'simple_roi']

    initial_wealth = 1e6
    initial_weights = xr.DataArray(
        np.ones(n_symbol) / n_symbol,
        dims=('symbol',),
        coords=(symbols,)
    )
    obj = BAHPortfolio(
        group_name,
        symbols,
        rois,
        initial_weights,
        initial_wealth,
        start_date=exp_start_date,
        end_date=exp_end_date
    )
    obj.run()


def get_bah_report(report_dir=pp.WEIGHT_PORTFOLIO_REPORT_DIR):

    group_names = pp.GROUP_SYMBOLS.keys()
    with open(os.path.join(pp.TMP_DIR,"BAH_stat.csv"), "w",) as csv_file:
        fields = [
            "simulation_name",
            "group_name",
            "start_date",
            "end_date",
            "n_data",
            "cum_roi",
            "annual_roi",
            "roi_mu",
            "std",
            "skew",
            "ex_kurt",
            "Sharpe",
            "Sortino_full",
            "Sortino_partial",
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for gdx, group_name in enumerate(group_names):
            report_name = "report_BAH_{}_20050103_20181228.pkl".format(
                group_name)

            rp = pd.read_pickle(os.path.join(pp.WEIGHT_PORTFOLIO_REPORT_DIR,
                report_name))
            writer.writerow(
                {
                    "simulation_name": rp["simulation_name"],
                    "group_name": group_name,
                    "start_date": rp['exp_start_date'].strftime("%Y-%m-%d"),
                    "end_date": rp['exp_end_date'].strftime("%Y-%m-%d"),
                    "n_data": rp['n_exp_period'],
                    "cum_roi": rp['cum_roi'],
                    "annual_roi": rp['annual_roi'],
                    "roi_mu": rp['daily_mean_roi'],
                    "std": rp['daily_std_roi'],
                    "skew": rp['daily_skew_roi'],
                    "ex_kurt": rp['daily_ex-kurt_roi'],
                    "Sharpe": rp['Sharpe'],
                    "Sortino_full": rp['Sortino_full'],
                    "Sortino_partial": rp['Sortino_partial']
                }
            )
            print(
                "[{}/{}] {}, cum_roi:{:.2%}".format(
                    gdx + 1, len(group_names), group_name,  rp['cum_roi']
                )
            )


if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        format='%(filename)15s %(levelname)10s %(asctime)s\n'
               '%(message)s',
        datefmt='%Y%m%d-%H:%M:%S',
        level=logging.INFO)

    for group_name in pp.GROUP_SYMBOLS.keys():
        run_bah('dissertation', group_name,
                dt.date(2005, 1, 1), dt.date(2018, 12, 28))
    # get_bah_report()