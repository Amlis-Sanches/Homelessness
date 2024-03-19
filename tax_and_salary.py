import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

def df_remove_chars(df, rowsname, char_list):
    for rowname in rowsname:
        for char in char_list:
            df[rowname] = df[rowname].str.replace(char,'')
    return df

def tax_rate():
    ...

