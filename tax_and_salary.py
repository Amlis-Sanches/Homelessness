import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

def df_remove_chars(df, rowname, char_list, numeric='n'):
    for char in char_list:
        df[rowname] = df[rowname].str.replace(char,'')


def df_remove_na(df, ccolumns):
    for column in ccolumns:
        df = df.dropna(subset=[column])

def tax_rate():
    

