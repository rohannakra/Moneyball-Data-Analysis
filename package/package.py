# Import sklearn/tensorflow modules.
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score

# Import other modules.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import pickle
import math
import os
from time import sleep
from sportsipy.mlb.teams import Teams
from IPython.display import clear_output
get_ipython().run_line_magic('matplotlib', 'inline')


dataset = pd.read_csv('data management/data_all.csv')
