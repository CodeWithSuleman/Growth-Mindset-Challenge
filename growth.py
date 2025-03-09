import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title ="Data Sweeper", layout="wide")

st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
)

st.title("DataSweeper Sterling integrator by Muhammad Suleman")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization Creating the project.")

uploaded_file = st.file_uploader("Upload your files (accept CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_exe = os.path.splitext(file.name)[-1].lower()
        
        if file_exe == ".csv":
            df = pd.read_csv(file)
        elif file_exe == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_exe}")
            continue

        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())
        
        st.subheader("Data Cleaning")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed")
            
            with col2:
               if st.button(f"fill missing values with 0:{file.name}"):
                   numeric_cols = df.select_dtypes(include=["number"]).columns
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing values has been filled")
        
        st.subheader("Select Columns to keep")
        columns = st.multiselect(f"Choose Columns: {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualize for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])   
        
        st.subheader(" Conversion Options")
        conversion_type = st.radio(f"Convert {file.name}", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_exe, ".csv")
                mime_type = "text/csv"
                
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_exe, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            st.download_button(
                label = f"Download {file_name} as {conversion_type}",
                data = buffer,
                file_name=file_name,
                mime=mime_type
                )
st.success("All Files Processed Successfully")
