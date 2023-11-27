# useful libraries
import streamlit as st
from textblob import TextBlob
import psycopg2
from psycopg2 import sql
import pandas as pd

# app configuration
st.set_page_config(page_title="sentiment analysis", layout="wide", page_icon=":chart:")

# create PostgresSQL connection
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="password",
    database="sentimentDB"
)

# create cursor for executing SQL queries
conn_cursor = conn.cursor()

# page title
st.title('Sentimental Analysis Tool')
st.markdown("---", unsafe_allow_html=True)


# function to analyze sentiment
def sentiment_analysis(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"

    else:
        return "Neutral"


# Perform sentiment analysis and store in PostgresSQL when the user clicks the button
with st.form("sentiment_one", clear_on_submit=False):
    # Text area for user input
    sentiment_text = st.text_area("Enter text for Sentimental Analysis:")
    on_click = st.form_submit_button("Analyze the sentiment and store into the database")
    if on_click:
        if sentiment_text:
            sentiment = sentiment_analysis(sentiment_text)

            # Store the input and sentiment analysis result in the database
            insert_query = sql.SQL(
                "INSERT INTO sentiment_table(sentiment_text,sentiment_response_polarity) VALUES(%s,%s);")
            conn_cursor.execute(insert_query, (sentiment_text, sentiment))
            conn.commit()
            st.success(f"The sentiment of the text is {sentiment}.")
            st.success("Data saved into the database  successfully!")
    else:
        st.warning("Please enter some text for analysis!")
st.markdown("---", unsafe_allow_html=True)
# Display recent entries from the database
st.header(" A display of  some recent entries into the database:")
select_query = sql.SQL("SELECT sentiment_text,sentiment_response_polarity FROM sentiment_table ORDER BY id;")
conn_cursor.execute(select_query)
recent_entries = conn_cursor.fetchall()

for sentiment_entry in recent_entries:
    st.write(f"Input Text: {sentiment_entry[0]} | Sentiment: {sentiment_entry[1]}")

# close database connect
conn_cursor.close()
conn.close()
