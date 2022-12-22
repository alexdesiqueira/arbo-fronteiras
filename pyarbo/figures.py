"""
FIGURES.PY


Notes
-----

Please add the private data to `../data`, or change the value of `BASE_PATH`.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path
from scipy import interpolate

import misc

# Setting up the figures appearance.
plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.size"] = 30
plt.rcParams["axes.labelsize"] = plt.rcParams["font.size"]
plt.rcParams["axes.titlesize"] = 1.2 * plt.rcParams["font.size"]
plt.rcParams["legend.fontsize"] = 0.6 * plt.rcParams["font.size"]
plt.rcParams["xtick.labelsize"] = plt.rcParams["font.size"]
plt.rcParams["ytick.labelsize"] = plt.rcParams["font.size"]

BASE_PATH = Path("../data")

FILENAME_DENGUE = BASE_PATH / "dengue_cases-2010_2022.csv"
FILENAME_MOSQUITO = BASE_PATH / "mosq_aaeg_trap_pos-2017_2022.csv"
FILENAME_WEATHER = BASE_PATH / "weather-2010_2022.csv"

data_dengue = pd.read_csv(io=FILENAME_DENGUE)
data_mosquito = pd.read_excel(io=FILENAME_MOSQUITO)

# In `FILENAME_WEATHER`, NULL elements are represented as `'     '`
data_weather = pd.read_excel(io=FILENAME_WEATHER, na_values="     ")


def figure_01():
    """ """
    notified_cases = (
        data_dengue["notified"]
        + data_dengue["probable"]
        + data_dengue["lab_confirmed"]
    )
    probable_cases = data_dengue["probable"] + data_dengue["lab_confirmed"]

    _, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 25))
    axes[0].plot(data_dengue.index, notified_cases, c="red")
    axes[0].set_xlabel("notified")

    axes[1].plot(data_dengue.index, probable_cases, c="blue")
    axes[1].set_xlabel("probable")
    axes[2].plot(data_dengue.index, data_dengue["lab_confirmed"], c="green")
    axes[2].set_xlabel("lab_confirmed")

    for ax in axes:
        ax._plot_temp(axis=ax, start="2010-01-01", stop="2010-01-01")
    return None


def figure_02():
    """ """
    plt.figure(figsize=(15, 10))
    plt.stem(
        data_mosquito_fill.index,
        data_mosquito_fill["mosq_aed_aeg_f_vivo"]
        + data_mosquito_fill["mosq_aed_aeg_f_morto"],
    )
    plt.title(
        "Aedes aegypti fêmeas capturadas (vivas ou mortas)\n por bimestre em Foz"
    )

    plt.plot(
        data_weather["date"],
        data_weather["temp_max-celsius"],
        "--",
        color="black",
        alpha=0.7,
    )

    return None


def _check_date(date):
    """Helping function. Will check if input date is complete, and fill it
    with not.
    """
    len_date = len(date.split("-"))
    if len_date == 3:
        # date has YYYY-MM-DD
        return pd.to_datetime(date)
    elif len_date == 2:  # date has YYYY-MM; will consider DD = "01"
        return pd.to_datetime(date + "-01")
    elif len_date == 1:  # date has YYYY; will consider MM-DD = "01-01"
        return pd.to_datetime(date + "-01-01")


def _return_data_interval(data, start, stop):
    """ """
    start = _check_date(start)
    stop = _check_date(stop)

    data_eq_before = data.Data >= stop
    data_eq_after = data.Data >= start

    data_in_interval = data[(data_eq_before) & (data_eq_after)]

    return data_in_interval


def _plot_pluv(axis, start, stop, num=40):
    """ """
    data = data_weather
    data_in_interval = _return_data_interval(data, start, stop)

    data_int_step = data_in_interval["daily_precipitation-mm"][::num]

    x_axis = np.linspace(
        start=start, stop=stop, num=len(data_int_step), endpoint=True
    )

    func_interp = interpolate.interp1d(x_axis, data_int_step, kind="cubic")
    axis.plot(
        data_in_interval["Data"][::num], func_interp(x_axis), color="blue"
    )

    return axis


def _plot_temp(axis, start, stop):
    """Auxiliary function. Will return an axis with min, mean and max
    temperatures between `start` and `stop` dates.
    """
    data = data_weather
    data_in_interval = _return_data_interval(data, start, stop)

    axis.plot(
        data_in_interval["date"],
        data_in_interval["temp_min-celsius"],
        "--",
        color="black",
        alpha=0.7,
    )
    axis.plot(
        data_in_interval["date"],
        data_in_interval["temp_mean-celsius"],
        "--",
        color="black",
        alpha=0.7,
    )
    axis.plot(
        data_in_interval["date"],
        data_in_interval["temp_max-celsius"],
        "--",
        color="black",
        alpha=0.7,
    )

    # filling area between min and max temperature.
    axis.fill_between(
        data_in_interval["date"],
        data_in_interval["temp_min-celsius"],
        data_in_interval["temp_max-celsius"],
        facecolor="gray",
        alpha=0.2,
    )

    return axis
