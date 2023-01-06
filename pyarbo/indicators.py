

def cummul_infestation_index(n_mosquito, n_traps):
    """Calculates the cummulative infestation index.
    
    Parameters
    ----------
    n_mosquito : scalar or array_like
        Number, or time series, of total mosquitoes captured (dead or alive).
    n_traps : scalar or array_like
        Number, or time series, of traps checked.
    
    Notes
    -----
    The cummulative infestation index is calculated as the ratio between total
    mosquitoes captured and the number of traps.

    Example
    -------
    >>> data_aaeg_traps = data.total_mosquitos_traps()
    >>> m_aaeg_f_total = data_aaeg_traps["m_aaeg_f_v"] + data_aaeg_traps["m_aaeg_f_m"]
    >>> cuminf_ind = cummul_infestation_index(m_aaeg_f_total,
    ...                                       data_aaeg_traps["n_traps"])
    """
    return n_mosquito / n_traps 


def pos_deposit_index(n_deposit_pos, n_deposit):
    """Calculates the deposit positivity index.
    
    Parameters
    ----------
    n_deposit_pos : scalar or array_like
        Number, or time series, of deposits containing mosquitoes.
    n_traps : scalar or array_like
        Number, or time series, of deposits checked.
    
    Notes
    -----
    The deposit positivity index is calculated as the ratio between deposits
    containing mosquitoes and deposits checked.

    Example
    -------
    >>> data_aaeg_traps = data.total_mosquitos_traps()
    >>> pos_ind = pos_deposit_index(data_aaeg_traps["tt_dep_aa_pos"],
    ...                             data_aaeg_traps["tt_dep_aa"])
    """
    return n_deposit_pos / n_deposit


def positivity_index(n_traps_pos, n_traps):
    """Calculates the positivity index.
    
    Parameters
    ----------
    n_traps_pos : scalar or array_like
        Number, or time series, of traps containing mosquitoes.
    n_traps : scalar or array_like
        Number, or time series, of traps checked.
    
    Notes
    -----
    The positivity index is calculated as the ratio between traps containing
    mosquitoes and the total number of traps.

    Example
    -------
    >>> data_aaeg_traps = data.total_mosquitos_traps()
    >>> mask_traps_w_mosquitos = (data_aaeg_traps["m_aaeg_f_v"] > 0) |
    ...                          (data_aaeg_traps["m_aaeg_f_m"] > 0) |
    ...                          (data_aaeg_traps["m_aaeg_m_v"] > 0) |
    ...                          (data_aaeg_traps["m_aaeg_m_m"] > 0)
    # [TODO] Example is likely wrong. Check the right definition first to fix it
    >>> traps_pos = data[mask_traps_w_mosquitos]
    >>> pos_ind = positivity_index(traps_pos,
    ...                            data_aaeg_traps["n_traps"])
    """
    # [TODO] Check what is right: recent_infestation_index or positivity_index
    return n_traps_pos / n_traps


def recent_infestation_index(n_mosquito_alive, n_traps):
    """Calculates the recent infestation index.
    
    Parameters
    ----------
    n_mosquito_alive : scalar or array_like
        Number, or time series, of mosquitoes captured alive.
    n_traps : scalar or array_like
        Number, or time series, of traps checked.
    
    Notes
    -----
    The recent infestation index is calculated as the ratio between total
    mosquitoes captured alive and the number of traps.

    Example
    -------
    >>> data_aaeg_traps = data.total_mosquitos_traps()
    >>> recinf_ind = recent_infestation_index(data_aaeg_traps["m_aaeg_f_v"],
    ...                                       data_aaeg_traps["n_traps"])
    """
    # [TODO] Check what is right: recent_infestation_index or positivity_index
    return n_mosquito_alive / n_traps
