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
    for i in range(len(df)):
        tax_range = df[income_name].iloc[i]

        if i == 1:
            choice = df[rate_name].iloc[i]

            match choice:
                case 0:
                    tax_count = 0

                case _:
                    tax_count = (((df[rate_name].iloc[i])/100)*(df[income_name].iloc[i]))

        if salary > tax_range:
            tax_count = ((df[rate_name].iloc[i]/100)*(df[income_name].iloc[i]-df[income_name].iloc[i-1]))+tax_count
        
        else:
            tax_count = ((df[rate_name].iloc[i]/100)*(salary-df[income_name].iloc[i-1]))+tax_count
            return tax_count, df[rate_name].iloc[i], df[income_name].iloc[i]
    return tax_count, df[rate_name].iloc[i], df[income_name].iloc[i]
