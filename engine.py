import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
import requests

# Read API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use a widely available Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI Content Research Engine", layout="wide")

st.title("🤖 AI Content Research & Idea Engine")

st.write(
    "This tool finds trending AI news and generates viral hooks, scripts, and scores using AI."
)

rss_feeds = [
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "https://venturebeat.com/category/ai/feed/"
]



def analyze_content(title):

    api_key = st.secrets["GEMINI_API_KEY"]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    prompt = f"""
    Analyze this topic and generate social media content insights.

    Topic: {title}

    Return in this format:

    Hook: <short viral hook>
    Script: <2 sentence script>
    ViralScore: <number between 1 and 10>
    """

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        text = result["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return "AI unavailable", "AI unavailable", "0"

    hook, script, score = "", "", ""

    for line in text.split("\n"):
        if "Hook:" in line:
            hook = line.replace("Hook:", "").strip()

        elif "Script:" in line:
            script = line.replace("Script:", "").strip()

        elif "ViralScore:" in line:
            score = line.replace("ViralScore:", "").strip()

    return hook, script, score

if st.button("Generate Content Ideas"):

    results = []

    for feed_url in rss_feeds:

        feed = feedparser.parse(feed_url)

        for post in feed.entries[:5]:

            title = post.title
            link = post.link

            hook, script, score = analyze_content(title)

            results.append({
                "Title": title,
                "Hook": hook,
                "Script": script,
                "Viral Score": score,
                "Link": link
            })

    df = pd.DataFrame(results)

    st.dataframe(df)





