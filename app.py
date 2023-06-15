import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io
import numpy as np

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)

    # Display shape of dataframe
    nrows, ncols = df.shape
    st.write("Number of Rows:", nrows)
    st.write("Number of Columns:", ncols)

    # Calculate number of columns of each datatype
    column_types = df.dtypes
    categorical_count = 0
    quantitative_count = 0
    bool_count = 0

    for dtype in column_types:
      if np.issubdtype(dtype, np.number):  # Check if numeric
        quantitative_count += 1
      elif np.issubdtype(dtype, np.bool_):  # Check if boolean
        bool_count += 1
      else:
        categorical_count += 1
    

    st.write('Number of categorical variables: ', categorical_count)
    st.write('Number of quantitative variables: ', quantitative_count)
    st.write('Number of boolean variables: ', bool_count)

      

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)
      
      # 5 number summary
      summary = df[numerical_column].describe()
      minimum = summary['min']
      first_quartile = summary['25%']
      median = summary['50%']
      third_quartile = summary['75%']
      maximum = summary['max']

      st.write("Minimum:", minimum)
      st.write("First Quartile", first_quartile)
      st.write("Median:", median)
      st.write("Third Quartile:", third_quartile)
      st.write("Maximum:", maximum)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )
    elif column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object']).columns)  

      #proportion table
      value_counts = df[categorical_column].value_counts()
      proportions = value_counts / value_counts.sum()
      proportions_df = pd.DataFrame({'Category': proportions.index, 'Proportion': proportions.values})
      st.write(proportions_df)

      #bar graph
      bar_color = st.color_picker('Bar Color', "#69b3a2", key=1)
      edge_color = st.color_picker('Edge Color', "#69b3a2", key=2)
      bar_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, key=3)
      bar_title = st.text_input('Set Title', 'Bar Graph')
      bar_xtitle = st.text_input('Set x-axis Title', categorical_column)

      fig, ax = plt.subplots()
      ax.bar(value_counts.index, value_counts.values, alpha = bar_opacity, color = bar_color, edgecolor = edge_color)
      ax.set_title(bar_title)
      ax.set_ylabel("Counts")
      ax.set_xlabel(bar_xtitle)
      ax.set_xticklabels(value_counts.index, rotation=90)
      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )
    elif column_type == "Bool":
      bool_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['bool']).columns)  

      #proportion table
      value_counts = df[bool_column].value_counts()
      proportions = value_counts / value_counts.sum()
      proportions_df = pd.DataFrame({'Category': proportions.index, 'Proportion': proportions.values})
      st.write(proportions_df)

      #bar graph
      bar_color = st.color_picker('Bar Color', "#69b3a2", key=4)
      edge_color = st.color_picker('Edge Color', "#69b3a2", key=5)
      bar_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, key=6)
      bar_title = st.text_input('Set Title', 'Bar Graph')
      bar_xtitle = st.text_input('Set x-axis Title', bool_column)

      fig, ax = plt.subplots()
      ax.bar(value_counts.index, value_counts.values, alpha = bar_opacity, color = bar_color, edgecolor = edge_color)
      ax.set_title(bar_title)
      ax.set_ylabel("Counts")
      ax.set_xlabel(bar_xtitle)
      ax.set_xticks([0, 1])
      ax.set_xticklabels(labels = ["False", "True"], rotation=90)
      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )
