"""
Functions:
    prepare_dataset()
    add_protected_imd()     (encode_imd)
    add_protected_gender()  (encode_gender)
    filter_final_result()
    encode_variables()      (encode_final_result, encode_disability,
                             encode_education, encode_age, encode_region)
    split()

Author:
    Mélina Verger - Oct. 2021
"""

import pandas as pd
from sklearn.model_selection import train_test_split

pd.options.mode.chained_assignment = None  # default='warn'


###############################################################################
def prepare_dataset(dataframe0):
    """
    Return a new dataframe with all columns except 'id_student', 'code_module'
    and 'code_presentation' and with distinct students' information only.

    Parameters
    ----------
    dataframe0 : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    pd.DataFrame
        The final dataframe
    """
    columns = ['id_student', 'gender', 'region', 'highest_education',
               'imd_band', 'age_band', 'num_of_prev_attempts',
               'studied_credits', 'disability', 'final_result']
    dataframe = dataframe0[columns]
    # drop rows when same students' id (redundant students' info)
    dataframe = dataframe.drop_duplicates(subset=['id_student'], keep='first')

    return dataframe.drop(columns=['id_student'])


###############################################################################
def encode_imd(x):
    if x in ['0-10%', '10-20', '20-30%', '30-40%', '40-50%']:
        return 1
    elif x in ['50-60%', '60-70%', '70-80%', '80-90%', '90-100%']:
        return 0
    else:
        raise ValueError("missing values should have been removed")


def encode_gender(x):
    if x == 'M':
        return 1
    else:
        return 0


def add_protected_imd(dataframe):
    """
    Apply encoding for IMD protected attribute.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    pd.DataFrame
        The final dataframe
    """
    # remove when IMD missing
    new_dataframe = dataframe.dropna(subset=['imd_band'])

    new_dataframe.loc[:, 'imd_band'] = new_dataframe.imd_band.apply(encode_imd)  # specific syntax to avoid SettingWithCopyWarning
    return new_dataframe


def add_protected_gender(dataframe):
    """
    Apply encoding for gender protected attribute.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    pd.DataFrame
        The final dataframe
    """
    dataframe.loc[:, 'gender'] = dataframe.gender.apply(encode_gender)  # specific syntax to avoid SettingWithCopyWarning
    return dataframe


###############################################################################
def filter_final_result(dataframe):
    """
    Return the dataframe filtered on final_result column.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The initial pd.DataFrame

    Returns
    ----------
    pd.DataFrame
        The final pd.DataFrame
    """
    column = 'final_result'
    options = ['Pass', 'Fail']
    return dataframe[dataframe[column].isin(options)]  # keep associated rows


###############################################################################
def encode_final_result(x):
    if x == "Pass":
        return 1
    else:  # "Fail"
        return 0


def encode_disability(x):
    if x == "Y":
        return 1
    else:  # "N"
        return 0


def encode_education(x):
    if x == "No Formal quals":
        return 0
    elif x == "Lower Than A Level":
        return 1
    elif x == "A Level or Equivalent":
        return 2
    elif x == "HE Qualification":
        return 3
    else:  # "Post Graduate Qualification"
        return 4


def encode_age(x):
    if x == "0-35":
        return 0
    elif x == "35-55":
        return 1
    else:  # "55<="
        return 2


def encode_region(dataframe):
    dict_region = {'East Anglian Region': 0,
                   'Scotland': 1,
                   'North Western Region': 2,
                   'South East Region': 3,
                   'West Midlands Region': 4,
                   "Wales": 5,
                   "North Region": 6,
                   "South Region": 7,
                   "Ireland": 8,
                   "South West Region": 9,
                   "East Midlands Region": 10,
                   "Yorkshire Region": 11,
                   "London Region": 12}
    dataframe['region'] = dataframe.region.map(dict_region)
    return dataframe


def encode_variables(dataframe):
    """
    Apply encoding for all variables except protected attributes and numerical
    variables.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    pd.DataFrame
        The final dataframe
    """
    dataframe.loc[:, 'final_result'] = dataframe.final_result.apply(encode_final_result)  # specific syntax to avoid SettingWithCopyWarning
    dataframe.loc[:, 'disability'] = dataframe.disability.apply(encode_disability)
    dataframe.loc[:, 'highest_education'] = dataframe.highest_education.apply(encode_education)
    dataframe.loc[:, 'age_band'] = dataframe.age_band.apply(encode_age)
    dataframe = encode_region(dataframe)
    return dataframe


###############################################################################
def split(dataframe, test_=0.3):
    """
    Apply encoding for all variables except protected attributes and numerical
    variables.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    X_train : pd.DataFrame
    y_train : pd.Series
    X_test : pd.DataFrame
    y_test : pd.Series
    """
    return train_test_split(dataframe.drop(columns=['final_result']),  # X
                            dataframe['final_result'],  # y
                            test_size=test_,
                            random_state=0)
