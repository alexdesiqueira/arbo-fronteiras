"""
DATA.PY

Functions to generate the data frames within `arbo-fronteiras`'s repository.

Notes
-----

Please add the private data to `../data`, or change the value of BASE_PATH.
"""

import misc
import pandas as pd

from dbfread import DBF
from pathlib import Path


BASE_PATH = Path("../data")

FILENAME_SINAN_DENGUE = BASE_PATH / "sinan_dengue_2010_2022.xlsx"
FILENAME_MOSQUITO_POS = BASE_PATH / "mosquitos positivos 2017 a 2022.xlsx"
FILENAME_ARMADILHAS_DBF = BASE_PATH / "armadilhas_liraa_XY.dbf"
FILENAME_PTUV = (
    BASE_PATH
    / "Precipitação - Temperatura - Umidade - Vento - 2010 a 2022.xlsx"
)

data_dengue = pd.read_excel(io=FILENAME_SINAN_DENGUE)
data_mosquito = _read_data_mosquito_dbf(filename=FILENAME_ARMADILHAS_DBF)
data_mosquito_pos = pd.read_excel(io=FILENAME_MOSQUITO_POS)
data_ptuv = pd.read_excel(io=FILENAME_PTUV, na_values="     ")


def data_ptuv(filename="data_ptuv.csv"):
    """ """

    return data


def data_dengue_cases(filename="data_dengue.csv"):
    """ """

    data = data.dropna()

    data = data_dengue[["dt_sin_pri", "classi_fin", "criterio"]]

    data["dt_sin_pri"] = pd.to_datetime(
        data["dt_sin_pri"]
    )

    data = data[
        data["dt_sin_pri"] >= "2010-01-01"
    ]

    data = misc.classify_dengue_cases(data)

    # adding three more columns: "notified", "probable", "lab_confirmed", with their values
    dummy_data = pd.get_dummies(data["type"])
    data = pd.concat([data, dummy_data], axis=1)

    # aggregating data according to "DT_SIN_PRI"
    data = data.groupby(["dt_sin_pri"], as_index=True)[
        ["notified",
         "probable",
         "lab_confirmed"]].sum()

    data = misc.fill_missing_dates(data,
                                   format="%Y-%m-%d")

    return data


def data_mosquito(filename="mosq_aaeg_trap_pos-2017_2022.csv"):
    """

    Notes
    -----
    If `filename` is provided, the data will be stored in disk with that
    file name.
    """
    # start adding columns of positive mosquitos, by date.
    data_mosquito_group = data_mosquito_pos.groupby(
        ["data_atividade"], as_index=True
    )[
        [
            "total_dep_aed_aeg",
            "mosq_aed_aeg_m_morto",
            "mosq_aed_aeg_m_vivo",
            "mosq_aed_aeg_f_morto",
            "mosq_aed_aeg_f_vivo",
        ]
    ].sum()

    # filling their missing dates.
    data_mosquito_fill = misc.fill_missing_dates(data_mosquito_group)

    # counting different traps, by id.
    data_trap = data_mosquito.groupby(["data_atividade"], as_index=True)[
        ["id_armadilha"]
    ].count()

    # filling dates.
    data_trap_fill = misc.fill_missing_dates(data_trap)
    # joining mosquitos and traps.
    data_mosq_arm_pos_fill = data_mosquito_fill.join(data_trap_fill)

    # renaming columns for consistency.
    data_mosq_arm_pos_fill.rename(
        columns={
            "total_dep_aed_aeg": "tt_dep_aa_pos",
            "mosq_aed_aeg_m_morto": "m_aaeg_m_m_pos",
            "mosq_aed_aeg_m_vivo": "m_aaeg_m_v_pos",
            "mosq_aed_aeg_f_morto": "m_aaeg_f_m_pos",
            "mosq_aed_aeg_f_vivo": "m_aaeg_f_v_pos",
            "id_armadilha": "id_armadil_pos",
        },
        inplace=True,
    )

    # repeating the process for all mosquitos.
    data_mosquito_dbf_group = data_mosquito.groupby(
        ["data_ativi"], as_index=True
    )[
        ["tt_dep_aa", "m_aaeg_m_m", "m_aaeg_m_v", "m_aaeg_f_m", "m_aaeg_f_v"]
    ].sum()

    data_trap_dbf = data_mosquito.groupby(["data_ativi"], as_index=True)[
        ["id_armadil"]
    ].count()

    # filling mosquitos and trap dates.
    data_mosquito_dbf_fill = misc.fill_missing_dates(data_mosquito_dbf_group)
    data_trap_dbf_fill = misc.fill_missing_dates(data_trap_dbf)

    # joining mosquitos and traps.
    data_mosq_arm_dbf_fill = data_mosquito_dbf_fill.join(data_trap_dbf_fill)

    # finally joining all data together.
    data = data_mosq_arm_dbf_fill.join(data_mosq_arm_pos_fill)

    if filename is not None:
        data.to_csv(filename)
    return data


def _read_data_mosquito_dbf(filename=FILENAME_ARMADILHAS_DBF):
    """
    Helping function. Reads and returns DBF mosquito data.
    """
    data_dbf = DBF(filename)
    data = pd.DataFrame(iter(data_dbf))

    return data
