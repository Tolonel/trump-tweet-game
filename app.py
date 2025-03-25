import streamlit as st
import random
import json
import os
import time

# --- Load Tweet Data ---
def load_tweets(path="tweets.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("tweets.json not found.")
        return []

tweet_data = load_tweets()

# --- Page Config ---
st.set_page_config(page_title="Trump Tweet Game", page_icon="🇺🇸", layout="centered")
st.title("🇺🇸 Trump Tweet Game")
st.subheader("Can you guess which tweet is real?")

# --- Tweet Card Style ---
def render_tweet(tweet_text):
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

# --- Game Setup ---
MAX_ROUNDS = 10

if "score" not in st.session_state:
    st.session_state.score = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "round_pairs" not in st.session_state:
    pairs = tweet_data.copy()
    random.shuffle(pairs)
    st.session_state.round_pairs = pairs[:MAX_ROUNDS]
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "result_time" not in st.session_state:
    st.session_state.result_time = None
if "current_pair" not in st.session_state:
    st.session_state.current_pair = None
if "current_mix" not in st.session_state:
    st.session_state.current_mix = None
if "correct_index" not in st.session_state:
    st.session_state.correct_index = None

# --- Game Over ---
if st.session_state.round > MAX_ROUNDS:
    st.session_state.game_over = True

if st.session_state.game_over:
    st.header("🏁 Game Over!")
    st.write(f"Your final Trump Score: **{st.session_state.score} / {MAX_ROUNDS}**")

    accuracy = round((st.session_state.score / MAX_ROUNDS) * 100)
    if accuracy >= 90:
        label = "🧠 Trump Psychic!"
    elif accuracy >= 70:
        label = "🕵️‍♂️ Tweet Whisperer"
    elif accuracy >= 50:
        label = "🧐 Not Bad... But Suspicious"
    else:
        label = "🤡 Easily Fooled by Fake News"

    st.subheader(f"Your Accuracy: {accuracy}%")
    st.markdown(f"## {label}")

    if st.button("🔄 Play Again"):
        st.session_state.score = 0
        st.session_state.round = 1
        st.session_state.game_over = False
        st.session_state.round_pairs = random.sample(tweet_data, MAX_ROUNDS)
        st.session_state.last_result = ""
        st.session_state.result_time = None
        st.session_state.current_pair = None
        st.session_state.current_mix = None
        st.session_state.correct_index = None
        st.rerun()

else:
    # Load or set up the current pair
    if not st.session_state.current_pair:
        pair = st.session_state.round_pairs[st.session_state.round - 1]
        mix = random.random() > 0.5
        tweets = [pair["real"], pair["fake"]] if mix else [pair["fake"], pair["real"]]
        correct_index = 0 if mix else 1
        st.session_state.current_pair = tweets
        st.session_state.correct_index = correct_index

    tweets = st.session_state.current_pair
    correct_index = st.session_state.correct_index

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
            st.session_state.current_pair = None
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
            st.session_state.current_pair = None
            st.rerun()

    st.write("**Tweet 1:**")
    render_tweet(tweets[0])
    st.write("**Tweet 2:**")
    render_tweet(tweets[1])

    if st.session_state.last_result:
        st.success(st.session_state.last_result)
        if st.session_state.result_time and time.time() - st.session_state.result_time > 1.5:
            st.session_state.last_result = ""
            st.session_state.result_time = None
            st.rerun()

    st.write(f"#### Score: {st.session_state.score}")
