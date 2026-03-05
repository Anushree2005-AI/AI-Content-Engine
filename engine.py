import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd

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

    prompt = f"""
    Analyze this topic and create social media content insights.

    Topic: {title}

    Return in this format:

    Hook: <short viral hook>
    Script: <2 sentence script>
    ViralScore: <number between 1 and 10>
    """

    try:
        response = model.generate_content(prompt)

        text = response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "AI unavailable", "AI unavailable", "0"

    hook = ""
    script = ""
    score = ""

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




