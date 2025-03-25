import streamlit as st
import random
import json
import os
import time

# --- Load Tweet Data from tweets.json file ---
def load_tweets(path="tweets.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("tweets.json not found. Please create it with a list of tweet pairs.")
        return []

tweet_data = load_tweets()

# --- Fake Twitter-style tweet card UI ---
def render_fake_tweet(tweet_text):
    st.markdown(f"""
    <div style="border:1px solid #ccc; padding:16px; border-radius:10px; max-width:600px; background-color:#fff;">
        <div style="display:flex; align-items:center;">
            <img src="https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_400x400.jpg" width="48" style="border-radius:50%; margin-right:10px;">
            <div>
                <strong>Donald J. Trump</strong><br>
                <span style="color:gray;">@realDonaldTrump</span>
            </div>
        </div>
        <div style="margin-top:12px; font-size:16px;">{tweet_text}</div>
        <div style="color:gray; font-size:13px; margin-top:8px;">8:08 AM · Jan 3, 2018 · Twitter for iPhone</div>
    </div>
    """, unsafe_allow_html=True)


# --- Page Config ---
st.set_page_config(page_title="Trump Tweet Game", page_icon="🇺🇸", layout="centered")
st.title("🇺🇸 Trump Tweet Game")
st.subheader("Can you guess which tweet is real?")

# --- State Management ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "result_time" not in st.session_state:
    st.session_state.result_time = None

# --- Game Logic ---
def get_random_pair():
    if not tweet_data:
        return ["No tweets loaded.", "Please check tweets.json"], 0
    pair = random.choice(tweet_data)
    mix = random.random() > 0.5
    tweets = [pair["real"], pair["fake"]] if mix else [pair["fake"], pair["real"]]
    correct_index = 0 if mix else 1
    return tweets, correct_index

# --- Check for game over ---
MAX_ROUNDS = 10
if st.session_state.round > MAX_ROUNDS:
    st.session_state.game_over = True

# --- Game Over Screen ---
if st.session_state.game_over:
    st.header("🏁 Game Over!")
    st.write(f"Your final Trump Score: **{st.session_state.score} / {MAX_ROUNDS}**")

    # --- Trump Score Rating ---
    accuracy = round((st.session_state.score / MAX_ROUNDS) * 100)

    if accuracy >= 90:
        title = "🧠 Trump Psychic!"
    elif accuracy >= 70:
        title = "🕵️‍♂️ Tweet Whisperer"
    elif accuracy >= 50:
        title = "🧐 Not Bad... But Suspicious"
    else:
        title = "🤡 Easily Fooled by Fake News"

    st.subheader(f"Your Accuracy: {accuracy}%")
    st.markdown(f"## {title}")

    # Play again button
    if st.button("🔄 Play Again"):
        st.session_state.score = 0
        st.session_state.round = 1
        st.session_state.last_result = ""
        st.session_state.result_time = None
        st.session_state.game_over = False
        st.rerun()

else:
    tweets, correct_index = get_random_pair()
    st.write(f"### Round {st.session_state.round} of {MAX_ROUNDS}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📝 Tweet 1"):
            if correct_index == 0:
                st.session_state.score += 1
                st.session_state.last_result = "✅ Correct! Tweet 1 was real."
            else:
                st.session_state.last_result = "❌ Nope. Tweet 1 was fake."
            st.session_state.round += 1
            st.session_state.result_time = time.time()
            st.rerun()

    with col2:
        if st.button("📝 Tweet 2"):
            if correct_index == 1:
                st.session_state.score += 1
                st.session_state.last_result = "✅ Correct! Tweet 2 was real."
            else:
                st.session_state.last_result = "❌ Nope. Tweet 2 was fake."
            st.session_state.round += 1
            st.session_state.result_time = time.time()
            st.rerun()

    # --- Display Tweets ---
    st.write("**Tweet 1:**")
    render_fake_tweet(tweets[0])
    st.write("**Tweet 2:**")
    render_fake_tweet(tweets[1])

    # --- Result Display (non-blocking) ---
    if st.session_state.last_result:
        st.success(st.session_state.last_result)
        if st.session_state.result_time:
            if time.time() - st.session_state.result_time > 1.5:
                st.session_state.last_result = ""
                st.session_state.result_time = None
                st.rerun()

    st.write(f"#### Score: {st.session_state.score}")
