import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def df_remove_chars(df, rowsname, char_list):
    for rowname in rowsname:
        for char in char_list:
            df[rowname] = df[rowname].str.replace(char,'')
    return df

def taxes(df, rate_name, income_name, salary):
    tax_count = 0
    dfsize = len(df)
    for i in range(len(df)):
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
                    tax_count = ((tax_rate/100)*salary)

                case (_, 0, _):
                    tax_count = ((tax_rate/100)*df[income_name].iloc[i+1]-1)

        if salary > tax_range:
            tax_count = ((tax_rate/100)*(tax_range-df[income_name].iloc[i-1]))+tax_count
        
        else:
            #tax_count = ((tax_rate/100)*(salary-df[income_name].iloc[i-1]))+tax_count
            return tax_count, tax_rate, tax_range
    return tax_count, tax_rate, tax_range
