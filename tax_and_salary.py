import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def df_remove_chars(df, rowsname, char_list):
    for rowname in rowsname:
        for char in char_list:
            df[rowname] = df[rowname].str.replace(char, "")
    return df


def taxes(df, rate_name, income_name, salary):
    tax_count = 0
    dfsize = len(df)
    for i in range(dfsize):
        tax_rate = df[rate_name].iloc[i]
        tax_range = df[income_name].iloc[i]

        if i == 1:
            match (tax_rate, tax_range, dfsize):
                case (0, 0, 1):
                    tax_count = 0
                    return tax_count, tax_rate, tax_range

                case (0, _, _):
                    tax_count = 0

                case (_, 0, 1):
                    tax_count = (tax_rate / 100) * salary

                case (_, 0, _):
                    tax_count = (tax_rate / 100) * df[income_name].iloc[i + 1] - 1

        if salary > tax_range:
            tax_count = (
                (tax_rate / 100) * (tax_range - df[income_name].iloc[i - 1])
            ) + tax_count

        else:
            # tax_count = ((tax_rate/100)*(salary-df[income_name].iloc[i-1]))+tax_count
            return tax_count, tax_rate, tax_range
    return tax_count, tax_rate, tax_range


def statetaxes(df, rate_name, income_name, salary):
    dfsize = len(df)
    tax_count = 0
    if dfsize == 1:
        tax_rate = df[rate_name].iloc[0] 
        tax_range = df[income_name].iloc[0]

        if tax_range == 0 and tax_rate == 0:
            return 0, tax_rate, tax_range

        elif tax_rate == 0:
            return 0, tax_rate, tax_range

        else:
            tax_count = (tax_rate / 100) * salary
            return tax_count, tax_rate, tax_range
    else:
        for i in range(dfsize):
            try:
                tax_range = df[income_name].iloc[i + 1] - df[income_name].iloc[i]
            except IndexError:
                tax_range = df[income_name].iloc[i]

            tax_rate = df[rate_name].iloc[i]

            if tax_rate == 0:
                tax_count = 0

            elif i == dfsize - 1: #Subtract 1 because i starts at 0 and will be one less than the dfsize. therefore they will never equil without -1. 
                tax_count = ((tax_rate / 100) * (salary)) + tax_count
                return tax_count, tax_rate, tax_range

            elif salary >= tax_range:
                tax_count = ((tax_rate / 100) * (tax_range)) + tax_count
                salary = salary - tax_count

            else:
                tax_count = ((tax_rate / 100) * (salary)) + tax_count
                return tax_count, tax_rate, tax_range
