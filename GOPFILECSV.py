import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Step 2 read the cvs file and create pandas dataframes
MAL1= pd.read_csv("Malware_infor_1.csv")
MAL2 = pd.read_csv("Malware_infor_2.csv")


df_MAL = pd.concat([MAL1, MAL2], axis=0)
df_MAL['label'] = 1
df_MAL.to_csv("Malware_infor.csv", index=False)



BE1 = pd.read_csv("Begin_infor_1.csv")
BE2 = pd.read_csv("Begin_infor_2.csv")

df_BE = pd.concat([BE1, BE2], axis=0)
df_BE.to_csv("Begin_infor.csv", index=False)
df_BE['label'] = 0
df_BE.to_csv("Begin_infor.csv", index=False)

# ộp file và xóa các dòng có ội dung trùng lặp
DATA1= pd.read_csv("Malware_infor.csv")
DATA2 = pd.read_csv("Begin_infor.csv")
data = pd.concat([DATA1, DATA2],axis=0)
data = data.drop_duplicates()

# tạo cột cho dataset
data.columns=["APIcall","permission","intent","label"]
data.to_csv("dataset.csv", index=False)



