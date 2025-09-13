import streamlit as st
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --- Part 1: Data Loading and Basic Exploration ---

@st.cache_data
def load_data(url):
    """
    Downloads and loads the metadata.csv file into a pandas DataFrame.
    """
    st.write("Downloading data... this may take a moment.")
    try:
        df = pd.read_csv(url)
        st.success("Data loaded successfully!")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# URL for a subset of the CORD-19 metadata.csv
DATA_URL = 'https://zenodo.org/records/3715506/files/all_sources_metadata_2020-03-13.csv?download=1'
df = load_data(DATA_URL)

st.title("CORD-19 Research Analysis Dashboard")
st.write("This application analyzes a subset of the COVID-19 Open Research Dataset (CORD-19) to explore publication trends and key topics.")

st.header("1. Data Exploration")
st.write("Examing the first 5 rows of the dataset:")
st.dataframe(df.head())

st.write("Data dimensions (rows, columns):", df.shape)
st.write("Data types:")
st.dataframe(df.dtypes.to_frame(name='Data Type'))

st.write("Missing values check for key columns:")
missing_data = df[['publish_time', 'abstract', 'journal']].isnull().sum().to_frame(name='Missing Values')
st.dataframe(missing_data)

st.header("2. Data Cleaning and Preparation")

# Drop rows with missing values in key columns
df_cleaned = df.dropna(subset=['publish_time', 'abstract', 'title'])
st.write(f"After cleaning, the dataset has {df_cleaned.shape[0]} rows.")

# Convert 'publish_time' to datetime and extract year
df_cleaned['publish_time'] = pd.to_datetime(df_cleaned['publish_time'], errors='coerce')
df_cleaned.dropna(subset=['publish_time'], inplace=True)
df_cleaned['year'] = df_cleaned['publish_time'].dt.year

# Create new columns
df_cleaned['abstract_word_count'] = df_cleaned['abstract'].apply(lambda x: len(str(x).split()))

st.write("Date columns converted and new 'year' and 'abstract_word_count' columns added.")
st.dataframe(df_cleaned.head())

# --- Part 3: Data Analysis and Visualization ---

st.header("3. Data Analysis and Visualizations")

# Analysis: Publications over time
papers_by_year = df_cleaned['year'].value_counts().sort_index()
st.subheader("Publications Over Time")
st.line_chart(papers_by_year)

# Analysis: Top journals
st.subheader("Top 10 Journals Publishing Research")
top_journals = df_cleaned['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# Analysis: Most frequent words in titles
def get_top_words(text_series, num_words=50):
    stop_words = set(
        "the, a, an, in, for, of, on, with, to, and, or, is, are, from, by, as, it, that, its, was, were, been, have, had, has"
        .split(', ')
    )
    all_words = []
    for text in text_series.dropna():
        words = re.findall(r'\b\w+\b', text.lower())
        all_words.extend([word for word in words if word not in stop_words and len(word) > 2])
    return Counter(all_words).most_common(num_words)

# Display top words in a data frame
top_title_words = get_top_words(df_cleaned['title'], 20)
st.subheader("Most Frequent Words in Paper Titles")
st.dataframe(pd.DataFrame(top_title_words, columns=['Word', 'Frequency']))

# Create a word cloud
st.subheader("Word Cloud of Paper Titles")
all_title_text = ' '.join(df_cleaned['title'].dropna().str.lower())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_title_text)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Plot distribution of paper counts by source
st.subheader("Distribution of Papers by Source")
source_counts = df_cleaned['source_x'].value_counts()
fig, ax = plt.subplots()
ax.pie(source_counts, labels=source_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Ensures the pie chart is circular.
st.pyplot(fig)

# --- Part 4: Streamlit Interactive Features ---

st.sidebar.header("Interactive Filters")

min_year = int(df_cleaned['year'].min())
max_year = int(df_cleaned['year'].max())

year_range = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = df_cleaned[(df_cleaned['year'] >= year_range[0]) & (df_cleaned['year'] <= year_range[1])]

st.header(f"Filtered Results ({year_range[0]} - {year_range[1]})")
st.write(f"Displaying data for {filtered_df.shape[0]} papers.")

# Display filtered charts
st.subheader("Filtered Publications Over Time")
filtered_papers_by_year = filtered_df['year'].value_counts().sort_index()
st.line_chart(filtered_papers_by_year)

st.subheader("Filtered Top 10 Journals")
filtered_top_journals = filtered_df['journal'].value_counts().head(10)
st.bar_chart(filtered_top_journals)

# Show a sample of the filtered data
st.subheader("Sample of Filtered Data")
st.dataframe(filtered_df[['title', 'journal', 'publish_time', 'abstract_word_count']].sample(n=min(10, len(filtered_df))))
