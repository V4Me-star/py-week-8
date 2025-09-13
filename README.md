# py-week-8COVID-19 Research Analysis App
This is a Streamlit application for analyzing a subset of the CORD-19 (COVID-19 Open Research Dataset) to explore key research trends and publication patterns.

The application performs the following tasks:

Data Loading & Exploration: Downloads a sample of the metadata.csv file from the CORD-19 dataset, loads it into a pandas DataFrame, and provides a basic overview of the data structure, dimensions, and missing values.

Data Cleaning & Preparation: Cleans the data by handling missing values, converting date columns to the correct format, and extracting the publication year for time-series analysis.

Data Analysis & Visualization:

Counts papers published per year to show publication trends over time.

Identifies and visualizes the top 10 journals.

Analyzes the most frequent words in paper titles and displays them in a dataframe and a word cloud.

Presents a pie chart showing the distribution of papers by their source.

Interactive Dashboard: A simple Streamlit dashboard allows users to filter the data by year using a slider, dynamically updating the charts and data display.
#
