import streamlit as st
import feedparser
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
# =========================
# Gemini API
# =========================
genai.configure(api_key="AIzaSyBrlKzsb_XeSdFdp_veQ9ArIkkZKgmWTn4")

# =========================
# Google Sheets connection
# =========================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("AI Content Engine").sheet1


# =========================
# Streamlit UI
# =========================

st.title("🤖 AI Content Research & Idea Engine")

st.markdown(
"""
This tool automatically:
- Finds trending AI content
- Generates viral hooks
- Creates short content scripts
- Scores content virality
"""
)

rss_feeds = [
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"
]
st.set_page_config(
    page_title="AI Content Research Engine",
    page_icon="🤖",
    layout="wide"
)



def analyze_content(title):

    prompt = f"""
    Analyze this topic and generate viral content insights.

    Topic: {title}

    Return in this format:

    Hook: <short viral hook>
    Script: <2-3 sentence script>
    ViralScore: <number between 1 and 10>
    """

    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            st.error("⚠️ API quota exceeded (20 requests/day free tier). Try again tomorrow or upgrade to a paid plan.")
            return "[Demo] Trending AI topic", "[Demo] Short script about the topic", "8"
        else:
            st.error(f"API Error: {error_msg}")
            return "Error", "API Error", "0"

    hook = ""
    script = ""
    score = ""

    lines = text.split("\n")

    for line in lines:

        if "Hook:" in line:
            hook = line.replace("Hook:", "").strip()

        elif "Script:" in line:
            script = line.replace("Script:", "").strip()

        elif "ViralScore:" in line:
            score = line.replace("ViralScore:", "").strip()

    return hook, script, score


# =========================
# Button
# =========================

if st.button("Generate Content Ideas"):

    processed_titles = set()

    for feed_url in rss_feeds:

        feed = feedparser.parse(feed_url)

        for post in feed.entries[:20]:

            title = post.title
            link = post.link

            if title in processed_titles:
                continue

            processed_titles.add(title)

            hook, script, score = analyze_content(title)

            # Show in Streamlit
            st.subheader(title)
            st.write("Link:", link)
            st.write("Hook:", hook)
            st.write("Script:", script)
            st.write("Viral Score:", score)

            st.divider()

            # Save to Google Sheet
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                title,
                link,
                hook,
                script,
                score

            ])
