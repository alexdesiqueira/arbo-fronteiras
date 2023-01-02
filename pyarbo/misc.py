from dbfread import DBF

import pandas as pd


def fill_missing_dates(data, format="%Y-%m-%d"):
    """Fills missing dates from a pandas dataframe.

    Parameters
    ----------
    data : pandas.DataFrame
        Data whose index is a datetime column.

    Returns
    -------
    data : pandas.DataFrame
        Data reindexed with filled missing data.

    Notes
    -----
    The dataframe column to be filled should be in data.index.
    """
    try:
        data.index = pd.to_datetime(data.index, format=format)
    except ParserError:
        raise

    date_min_max = pd.date_range(data.index.min(), data.index.max())
    data = data.reindex(date_min_max, fill_value=0)

    return data


def classify_dengue_cases(data):
    """Return dengue cases, classified in notified, probable, and lab
       confirmed.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame.

    Returns
    -------

    Notes
    -----
    Expected columns: "dt_sin_pri", "classi_fin", "criterio"
    """
    data = data.assign(type="notified")

    class_not_5 = data["classi_fin"] != 5
    criterio_is_1 = data["criterio"] == 1

    data.loc[:, (class_not_5, "type")] = "probable"

    class_mask = class_not_5 & criterio_is_1
    data[class_mask]["type"] = "lab_confirmed"

    return data


def _read_data_mosquito_dbf(filename=FILENAME_ARMADILHAS_DBF):
    """
    Helping function. Reads and returns DBF mosquito data.
    """
    data_dbf = DBF(filename)
    data = pd.DataFrame(iter(data_dbf))

    return data
