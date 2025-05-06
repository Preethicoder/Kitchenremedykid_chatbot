import streamlit as st
import pandas as pd
import json
from collections import Counter
import re

# Load your JSON
with open("relevance_scores.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
rows = []
for item in data:
    rows.append({
        "User Message": item["last_user_message:::"],
        "AI Response": item["last_ai_message:::"],
        "Relevant": item["Relevance score:::"],
        "Explanation": item["Explanation:::"]
    })
df = pd.DataFrame(rows)

# Dashboard
st.title("KitchenRemedy Chatbot - Relevance Dashboard")

# 1. Overall Relevance
relevant_pct = df["Relevant"].mean() * 100
st.metric("Relevant Responses", f"{relevant_pct:.2f}%")

# 2. Symptoms / Topics with most irrelevant responses
def extract_symptom(text):
    return text.lower().split()[0]  # crude fallback

df["Symptom"] = df["User Message"].apply(extract_symptom)
irrelevant_df = df[df["Relevant"] == False]
symptom_counts = Counter(irrelevant_df["Symptom"])
top_irrelevant = pd.DataFrame(symptom_counts.items(), columns=["Symptom/Topic", "Count"]).sort_values("Count", ascending=False)

st.subheader("Most Common Topics with Irrelevant Responses")
st.dataframe(top_irrelevant)
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# 3. Word Cloud of failing message types (Optional)
# 3. Word Cloud of failing message types
if not irrelevant_df.empty:
    all_text = " ".join(irrelevant_df["User Message"].tolist())
    wc = WordCloud(background_color="white", width=800, height=400).generate(all_text)

    st.subheader("Common Words in Irrelevant Requests")

    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")

    st.pyplot(fig)
else:
    st.info("No irrelevant responses to generate a word cloud.")
    st.info("Install wordcloud and matplotlib for visual analysis: `pip install wordcloud matplotlib`")

# 4. Search or filter
st.subheader("Explore Responses")
selected_symptom = st.selectbox("Filter by symptom/topic", ["All"] + list(df["Symptom"].unique()))
if selected_symptom != "All":
    filtered_df = df[df["Symptom"] == selected_symptom]
else:
    filtered_df = df
st.dataframe(filtered_df[["User Message", "AI Response", "Relevant"]])
