import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import w3w_macro
import zipfile
from streamlit import legacy_caching

st.title("W3W Cleaner")

csv_file = st.file_uploader("Upload CSV", type=["csv"])

if csv_file is not None:
    st.write(type(csv_file))
    ### st.write(csv_file.name)
    df = pd.read_csv(csv_file)
    st.dataframe(df)

    if st.button('Continue'):
        df = w3w_macro.cleaner(df)
        df = w3w_macro.df_NAN_dropper(df)
        df = w3w_macro.df_COUNTIF(df)
        df = w3w_macro.df_WORD_dropper(df)
        df = df[(df['ColumnCount'] == 1) | (df['ColumnCount'] == 2) | (df['ColumnCount'] == 3) | (df['ColumnCount'] == 4)]
        df = df.reset_index().drop(columns="index")
        df = w3w_macro.df_snippet_adder(df)
        df_main = df.drop(columns="ColumnCount", axis=1)
        st.write("Number of Emails:", df.shape[0])
        st.dataframe(df_main)
            
        df1 = df[df['ColumnCount'] == 1].drop(columns="ColumnCount", axis=1)
        df2 = df[df['ColumnCount'] == 2].drop(columns="ColumnCount", axis=1)
        df3 = df[df['ColumnCount'] == 3].drop(columns="ColumnCount", axis=1)
        df4 = df[df['ColumnCount'] == 4].drop(columns="ColumnCount", axis=1)
            
        csvname = csv_file.name
        csvname1 = csvname.split("_")[0] + "_" + csvname.split("_")[1] + "_" + csvname.split("_")[2] + "_"
        csvname2 = "_" + csvname.split("_")[-3] + "_" + csvname.split("_")[-2] + "_" + csvname.split("_")[-1]
            
            
        with zipfile.ZipFile('file.zip', 'w') as csv_zip:
            csv_zip.writestr(csvname1 + "1" + csvname2 +'.csv', pd.DataFrame(df1).to_csv(index=False))
            csv_zip.writestr(csvname1 + "2" + csvname2 +'.csv', pd.DataFrame(df2).to_csv(index=False))
            csv_zip.writestr(csvname1 + "3" + csvname2 +'.csv', pd.DataFrame(df3).to_csv(index=False))
            csv_zip.writestr(csvname1 + "4" + csvname2 +'.csv', pd.DataFrame(df4).to_csv(index=False))
                #csv_zip.writestr("data2.csv", pd.DataFrame(data2).to_csv())
        with open('file.zip', 'rb') as f:
            st.download_button('Download Zip', f, file_name= csvname1 + "1" + csvname2 +'.zip')


        
        


    