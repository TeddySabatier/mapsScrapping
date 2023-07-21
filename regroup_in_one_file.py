from warnings import catch_warnings
import pandas as pd
import os
import tkinter
from tkinter import filedialog

path=filedialog.askdirectory()
dir_list = os.listdir(path)
df=pd.DataFrame()
for fname in dir_list:
    try:
        df1=pd.read_excel(path+"/"+fname)
        df=pd.concat([df,df1])
    except:
        pass
pd.DataFrame(df).to_excel('Regrouped.xlsx')
