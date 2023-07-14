import uproot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyarrow

file_name = ['pwp8_pp_hh_lambda000_5f_hhbbaa', 'pwp8_pp_hh_lambda100_5f_hhbbaa', 'pwp8_pp_hh_lambda240_5f_hhbbaa','pwp8_pp_hh_lambda300_5f_hhbbaa', 'mgp8_pp_tth01j_5f','mgp8_pp_h012j_5f','mgp8_pp_jjaa_5f', 'mgp8_pp_vh012j_5f','mgp8_pp_vbf_h01j_5f', 'mgp8_pp_tt012j_5f']

file_ = uproot.open("./"+file_name[0]+".root")
tree = file_["events"]
print(tree.keys())
lists = tree.keys()
lists.append('process')
print("LIST: ",lists)

df = pd.DataFrame(columns = lists)

for name in file_name:

    file_ = uproot.open("./"+name+".root")

    #print(file_.keys())

    tree = file_["events"]
    df_ = tree.arrays(expressions = tree.keys(),library="pd")
    #df_ = df_[:100000]
    df_['process'] = name
    df = df.append(df_,ignore_index = True)
    print("df: ",df)
    print("df_: ",df_)
    print("df_col:", df_.columns)

#print(df)
print(df.shape)
print(df.columns)

df.to_parquet('df_Sel_All.parquet')

