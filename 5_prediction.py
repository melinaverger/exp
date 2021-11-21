"""
Author:
    Mélina Verger - Oct. 2021
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, recall_score, precision_score,
                             confusion_matrix)


###############################################################################
def rf_model():
    return RandomForestClassifier(random_state=0)


def train(model, X_train, y_train):
    return model.fit(X_train, y_train)


def pred(model, X_test):
    return model.predict(X_test)


def pred_proba(model, X_test):
    return model.predict_proba(X_test)


###############################################################################
def accuracy(Y, Ypred):
    return accuracy_score(Y, Ypred)


def recall(Y, Ypred):
    return recall_score(Y, Ypred, average='binary')


def precision(Y, Ypred):
    return precision_score(Y, Ypred, average='binary')


def demographic_parity(Y, Ypred):
    tn, fp, fn, tp = confusion_matrix(Y, Ypred).ravel()
    return (tp + fp) / (tn + fp + fn + tp)


###############################################################################
def metric_group(func, ind_group, Y, Ypred):
    y_ind = list(Y.index)
    Y, Ypred = list(Y), list(Ypred)
    new_Y, new_Ypred = [], []
    for i in range(len(y_ind)):
        if y_ind[i] in ind_group:
            new_Y.append(Y[i])
            new_Ypred.append(Ypred[i])
    return func(new_Y, new_Ypred)


def accuracy_per_group(ind_group, Y, Ypred):
    return metric_group(accuracy, ind_group, Y, Ypred)


def recall_per_group(ind_group, Y, Ypred):
    return metric_group(recall, ind_group, Y, Ypred)


def precision_per_group(ind_group, Y, Ypred):
    return metric_group(precision, ind_group, Y, Ypred)


def demog_parity_per_group(ind_group, Y, Ypred):
    return metric_group(demographic_parity, ind_group, Y, Ypred)


# formulas
# from sklearn.metrics import confusion_matrix
# tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
# # accuracy
# (tp + tn) / (tn + fp + fn + tp)
# # precision
# tp / (tp + fp)
# # recall
# tp / (tp + fn)
# # demographic parity (TP + FP) (absolute number)
# tp + fp
# # proportional parity (https://cran.r-project.org/web/packages/fairness/vignettes/fairness.html)
# (tp + fp) / (tn + fp + fn + tp)
###############################################################################


def predicted_proba_success(Ytest, Yproba):
    """
    Return the predicted probabilites of success (1) with the
    corresponding indices of test instances.

    Parameters
    ----------
    Ytest : pd.Series
        The target variable of the test set with instance indices
    Yproba : np.array of shape (n_instances, n_classes)
        The array of probabilites for all classes

    Returns
    ----------
    pd.DataFrame
        The 2-column dataframe (indices, probabilities of success)
    """
    pred_proba_success = Yproba[:, 1]  # as we have binary classes
    df_pps = pd.DataFrame(pred_proba_success, columns=["proba_success"])
    df_pps.insert(0, "ind", Ytest.index)
    return df_pps


# unused
# def group_predicted_proba_success(ind_group, df_pps):
#     """
#     """
#     group_proba = []
#     for i in range(len(df_pps)):
#         if df_pps.loc[i, "ind"] in ind_group:
#             group_proba.append(df_pps.loc[i, "proba_success"])
#     return group_proba


def group_outcome_predicted_proba_success(ind_group, ind_outcome, df_pps):
    """
    Return filtered predicted probabilites of success (1) according to the
    chosen protected attribute and the chosen true outcome.

    Parameters
    ----------
    ind_group : list
        Indices of the instances of the protected group
    ind_outcome : list
        Indices of the instances of the true outcome
    df_pps : pd.DataFrame
        The 2-column dataframe (indices, probabilities of success)

    Returns
    ----------
    list
        The filtered probabilities of success
    """
    group_proba = []
    for i in range(len(df_pps)):
        if (df_pps.loc[i, "ind"] in ind_group) and (df_pps.loc[i, "ind"] in ind_outcome):
            group_proba.append(df_pps.loc[i, "proba_success"])
    return group_proba
