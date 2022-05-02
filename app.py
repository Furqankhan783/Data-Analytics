###  Imports
import os
import streamlit as st

import pandas as pd

####  Visualization Imports
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')
import seaborn as sns


def main():
    html_temp = """
	<div style="background-color:DimGrey;"><p style="color:white;font-size:50px;padding:10px">Happy Exploring</p></div>
	"""
    st.subheader("A Tool which helps to do Exploratory Data Analysis.")

    st.markdown(html_temp, unsafe_allow_html=True)

    #### First add dataset in "datasets" folder to view in the app.

    def file_selector(folder_path='./datasets'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select A file", filenames)
        return os.path.join(folder_path, selected_filename)

    filename = file_selector()

    #### Read Dataset
    df = pd.read_csv(filename)

    #### Show Dataset

    if st.checkbox("Show Dataset"):
        st.dataframe(df.head(10))

    #### Show Columns
    if st.button("Column Names"):
        st.write(df.columns)

    #### Show Shape
    if st.checkbox("Shape of Dataset"):
        data_dim = st.radio("Show Dimension By ", ("Rows", "Columns"))
        if data_dim == 'Rows':
            st.text("Number of Rows")
            st.write(df.shape[0])
        elif data_dim == 'Columns':
            st.text("Number of Columns")
            st.write(df.shape[1])
        else:
            st.write(df.shape)

    #### Select Columns
    if st.checkbox("Select Columns To Show"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select", all_columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)

    #### Show Values
    if st.button("Value Counts"):
        st.text("Value Counts By Target/Class")
        st.write(df.iloc[:, -1].value_counts())

    #### Show Datatypes
    if st.button("Data Types"):
        st.write(df.dtypes)

    #### Show Summary
    if st.checkbox("Summary"):
        st.write(df.describe().T)

    if st.button("Missing Values"):
        st.write(df.apply(lambda x: sum(x.isnull()), axis=0))

    if st.checkbox("List Numerical Columns"):
        num_vars = [var for var in df.columns if df[var].dtypes != 'O']
        st.write(num_vars)

    if st.checkbox("List String Columns"):
        cat_vars = [var for var in df.columns if df[var].dtypes == 'O']
        st.write(cat_vars)

    ### Plot and Visualization

    st.subheader("Data Visualization")
    ### Correlation
    ### Seaborn Plot
    if st.checkbox("Correlation Plot[Seaborn]"):
        st.write(sns.heatmap(df.corr(), annot=True))
        st.pyplot()

    ### Pie Chart
    if st.checkbox("Pie Plot"):
        all_columns_names = df.columns.tolist()
        if st.button("Generate Pie Plot"):
            st.success("Generating A Pie Plot")
            st.write(df.iloc[:, -1].value_counts().plot.pie(autopct="%1.1f%%"))
            st.pyplot()

    ### Count Plot
    if st.checkbox("Plot of Value Counts"):
        st.text("Value Counts By Target")
        all_columns_names = df.columns.tolist()
        primary_col = st.selectbox("Primary Columm to GroupBy", all_columns_names)
        selected_columns_names = st.multiselect("Select Columns", all_columns_names)
        if st.button("Plot"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].count()
            else:
                vc_plot = df.iloc[:, -1].value_counts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()

    ### Customizable Plot

    st.subheader("Customizable Plot")
    all_columns_names = df.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
    selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

    if st.button("Generate Plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

        # Plot By Streamlit
        if type_of_plot == 'area':
            cust_data = df[selected_columns_names]
            st.area_chart(cust_data)

        elif type_of_plot == 'bar':
            cust_data = df[selected_columns_names]
            st.bar_chart(cust_data)

        elif type_of_plot == 'line':
            cust_data = df[selected_columns_names]
            st.line_chart(cust_data)

        #### Custom Plot
        elif type_of_plot:
            cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()

    st.sidebar.header("Developed By")
    st.sidebar.info("Mohammad Furqan Khan")
    st.sidebar.markdown("[Follow on LinkedIn](https://www.linkedin.com/in/muhammad-furqan-khan-5614ba183/)")
    st.sidebar.markdown("[Check Github](https://github.com/Furqankhan783)")

    st.sidebar.header("Application Info")
    st.sidebar.text("Built using Streamlit")
    st.sidebar.markdown("[Want to use it? Click here](https://github.com/Furqankhan783/Data-Analytics/)")


if __name__ == '__main__':
    main()