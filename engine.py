import streamlit as st
import feedparser
import pandas as pd
import random

st.set_page_config(page_title="AI Content Research Engine", layout="wide")

st.title("🤖 AI Content Research & Idea Engine")

st.write(
    "This tool collects trending AI news and generates content hooks and scripts automatically."
)

rss_feeds = [
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "https://venturebeat.com/category/ai/feed/"
]


def generate_content(title):
    hooks = [
        f"Why everyone is talking about: {title}",
        f"The surprising truth behind: {title}",
        f"This AI story could change everything: {title}",
        f"Here’s what you need to know about: {title}",
    ]

    scripts = [
        f"Let’s break down why this topic matters: {title}. This development could reshape the AI landscape.",
        f"This story highlights an important shift happening in AI right now: {title}. Here’s what it means.",
        f"AI innovation is moving fast, and this example shows why: {title}. Let’s understand the impact.",
    ]

    hook = random.choice(hooks)
    script = random.choice(scripts)
    score = random.randint(6, 9)

    return hook, script, score


if st.button("Generate Content Ideas"):

    results = []

    for feed_url in rss_feeds:

        feed = feedparser.parse(feed_url)

        for post in feed.entries[:10]:

            title = post.title
            link = post.link

            hook, script, score = generate_content(title)

            results.append({
                "Title": title,
                "Hook": hook,
                "Script": script,
                "Viral Score": score,
                "Link": link
            })

    df = pd.DataFrame(results)

    st.dataframe(df)
