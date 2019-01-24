"""Various and sundry useful functions which handy for different types of
variable importance"""

import numpy as np
import pandas as pd

from src.error_handling import InvalidDataException

__all__ = ["convert_result_list_to_dict"]


def convert_result_list_to_dict(result, variable_names, scoring_strategy):
    """Takes a list of (var, score) and converts to a dictionary

    :param result: a list of (var_index, score)
    :param variable_names: a list of variable names
    :param scoring_strategy: a function to be used for determining optimal 
        variables. Should be of the form ([floats]) -> index
    """
    if len(result) == 0:
        return dict()

    result_dict = dict()
    rank = 0
    while len(result) > 1:
        best_index = scoring_strategy([res[1] for res in result])
        var, score = result.pop(best_index)
        result_dict[variable_names[var]] = (rank, score)
        rank += 1
    var, score = result[0]
    result_dict[variable_names[var]] = (rank, score)
    return result_dict


def get_data_subset(data, columns):
    """Returns a subset of the data corresponding to the desired columns

    :param data: either a pandas dataframe or a numpy array
    :param columns: a list of column indices
    :returns: data_subset (same type as data)
    """
    if isinstance(data, pd.DataFrame):
        return data.loc[:, data.columns.values[columns]]
    elif isinstance(data, np.ndarray):
        return data[:, columns]
    else:
        raise InvalidDataException(
            data, "Data must be a pandas dataframe or numpy array")