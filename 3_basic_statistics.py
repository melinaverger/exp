"""
Functions:
    dataset_population()
    how_many()          (_students, _modules, _presentations, _genders)
    ratio()             (_gender, _region, _education, _imd, _age, _disability)
    disability_per_gender()
    imd_per_region()
    ed_per_age()

Author:
    Mélina Verger - Oct. 2021
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

plt.rcParams['axes.facecolor'] = 'white'


###############################################################################
def dataset_population(dataframe0):
    """
    Return a new dataframe with students' information only (distinct students).

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
               'imd_band', 'age_band', 'disability']
    dataframe = dataframe0[columns]
    # drop rows when same students' id (redundant students' info)
    return dataframe.drop_duplicates(subset=['id_student'], keep='first')


###############################################################################
def how_many(col_name, dataframe):
    """
    Return the number of (unique) instances asked in input.

    Parameters
    ----------
    col_name : str
        The name of the relative column
    dataframe : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    int
        The relative counts

    Raises
    ------
    TypeError
        If dataframe type is not pandas.DataFrame
    NameError
        If col_name is not in the list names
    """
    names = ['id_student', 'code_module', 'code_presentation', 'gender']
    if isinstance(dataframe, pd.DataFrame):
        if col_name in names:
            column = col_name
            elems = pd.Series(dataframe[column].unique())
            return len(elems) - elems.isna().sum()  # substract 0 or 1 if NaN value in elems
        else:
            raise NameError("col_name argument must be included in:"
                             " {}".format(', '.join(names)))
    else:
        raise TypeError('dataframe type must be pandas.DataFrame')


def how_many_students(dataframe):
    """
    Return the number of (unique) students in a dataframe.
    """
    return how_many('id_student', dataframe)


def how_many_modules(dataframe):
    """
    Return the number of (unique) modules/courses in a dataframe.
    """
    return how_many('code_module', dataframe)


def how_many_presentations(dataframe):
    """
    Return the number of (unique) modules' presentations in a dataframe.
    """
    return how_many('code_presentation', dataframe)


def how_many_genders(dataframe):
    """
    Return the number of (unique) gender types a dataframe.
    """
    return how_many('gender', dataframe)


###############################################################################
def ratio(col_name, dataframe0):
    """
    Display a table and a plot of the ratios of the information asked among the
    population of distinct students.

    Parameters
    ----------
    col_name : str
        The name of the relative column
    dataframe0 : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    None

    Raises
    ------
    TypeError
        If dataframe type is not pandas.DataFrame
    ValueError
        If col_name is not in the list names
    """
    names = ['gender', 'region', 'highest_education', 'imd_band', 'age_band',
             'disability']
    if isinstance(dataframe0, pd.DataFrame):
        if col_name in names:
            # new dataset
            dataframe = dataset_population(dataframe0)

            column = col_name
            ind = list(dataframe[column].value_counts().index)
            counts = list(dataframe[column].value_counts())
            percentages = [round(x/sum(counts)*100, 2) for x in counts]
            table = np.stack((ind, counts, percentages), axis=1)
            print(tabulate(table, headers=[column, "# distinct students",
                                           "percentage (%)"]))

            dataframe[column].value_counts().plot(kind='bar', color='b')
            plt.ylabel('# distinct students')
        else:
            raise ValueError("col_name argument must be included in:"
                             " {}".format(', '.join(names)))
    else:
        raise TypeError('dataframe type must be pandas.DataFrame')


def ratio_gender(dataframe):
    """
    Return the gender ratio among the population of distinct students.
    """
    return ratio('gender', dataframe)


def ratio_region(dataframe):
    """
    Return the region ratio among the population of distinct students.
    """
    return ratio('region', dataframe)


def ratio_education(dataframe):
    """
    Return the education ratio among the population of distinct students.
    """
    return ratio('highest_education', dataframe)


def ratio_imd(dataframe):
    """
    Return the IMD ratio among the population of distinct students.
    """
    return ratio('imd_band', dataframe)


def ratio_age(dataframe):
    """
    Return the age ratio among the population of distinct students.
    """
    return ratio('age_band', dataframe)


def ratio_disability(dataframe):
    """
    Return the disability ratio among the population of distinct students.
    """
    return ratio('disability', dataframe)


###############################################################################
def disability_per_gender(dataframe0):
    """
    Display a table of the disability ratio within the M and F populations.

    Parameters
    ----------
    dataframe0 : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    None

    Raises
    ------
    TypeError
        If dataframe type is not pandas.DataFrame
    """
    if isinstance(dataframe0, pd.DataFrame):
        # new dataset
        dataframe = dataset_population(dataframe0)

        Y_male = len(dataframe[(dataframe.gender == 'M') &
                               (dataframe.disability == "Y")])
        Y_female = len(dataframe[(dataframe.gender == 'F') &
                                 (dataframe.disability == "Y")])
        print(f"M: {Y_male} ({round(Y_male/(Y_male+Y_female)*100, 2)}%)")
        print(f"F: {Y_female} ({round(Y_female/(Y_male+Y_female)*100, 2)}%)")
    else:
        raise TypeError('dataframe type must be pandas.DataFrame')


###############################################################################
def imd_per_region(dataframe0):
    """
    Display a plot of the distribution of the students among the IMD indices
    per region.

    Parameters
    ----------
    dataframe0 : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    None

    Raises
    ------
    TypeError
        If dataframe type is not pandas.DataFrame
    """
    if isinstance(dataframe0, pd.DataFrame):
        # new dataset
        dataframe = dataset_population(dataframe0)
        # reduce new dataset
        df = dataframe[['region', 'imd_band']]

        i = 1
        fig = plt.figure(figsize=(10, 7))
        #fig.patch.set_facecolor('white')
        for region in df['region'].unique():
            if i <= 10:
                df[df['region'] == region]['imd_band'].value_counts().sort_index().plot(linestyle='-', marker='o', label=region)
            else:
                df[df['region'] == region]['imd_band'].value_counts().sort_index().plot(linestyle='--', marker='o', label=region)
            i += 1
        plt.legend(bbox_to_anchor=(1, 0.75))
        plt.ylabel('# distinct students')
        plt.xlabel('IMD')
        plt.xticks()
        plt.show()
    else:
        raise TypeError('dataframe type must be pandas.DataFrame')


###############################################################################
def ed_per_age(dataframe0):
    """
    Display a plot of the distribution of the students among the age intervals
    per education.

    Parameters
    ----------
    dataframe0 : pd.DataFrame
        The initial dataframe

    Returns
    ----------
    None

    Raises
    ------
    TypeError
        If dataframe type is not pandas.DataFrame
    """
    if isinstance(dataframe0, pd.DataFrame):
        # new dataset
        dataframe = dataset_population(dataframe0)
        # reduce new dataset
        df = dataframe[['highest_education', 'age_band']]

        for ed in df['highest_education'].unique():
            df[df['highest_education'] == ed]['age_band'].value_counts().sort_index().plot(linestyle='-', marker='o', label=ed)
        plt.legend(bbox_to_anchor=(1, 0.75))
        plt.ylabel('# distinct students')
        plt.xlabel('Age')
        plt.xticks()
        plt.show()
    else:
        raise TypeError('dataframe type must be pandas.DataFrame')
