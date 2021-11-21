"""
Functions:
    list_files()
    read_data()

Author:
    Mélina Verger - Oct. 2021
"""

import zipfile
import pandas as pd


DATA_PATH = '/Users/melina/Documents/work/2021_Internship/Work/OLC_tracking/' \
            'project/data/open_olc/anonymised_data/'

files = ['assessments.csv', 'courses.csv', 'studentAssessment.csv',
         'studentInfo.csv', 'studentRegistration.csv', 'studentVle.csv',
         'vle.csv']


def list_files():
    """
    Print the names of the files (or data tables) constituting the OULAD.
    """
    print(*files, sep='\n')
    print('\nTotal:', len(files))


def read_data(file_name):
    """
    Return a data table in csv format as a pandas DataFrame.

    Parameters
    ----------
    file_name : str
        The name of the csv file

    Returns
    ----------
    pd.DataFrame
        The data table as pd.DataFrame

    Raises
    ------
    NameError
        If file_name is not in files List
    """
    if file_name in files:
        zf = zipfile.ZipFile(DATA_PATH + file_name + '.zip')
        data = pd.read_csv(zf.open(file_name))
        return data
    else:
        raise NameError("file_name argument must be included in:"
                        " {}".format(', '.join(files)))
