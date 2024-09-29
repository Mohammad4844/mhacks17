import streamlit as st
from streamlit_lottie import st_lottie
import requests
import random
import time
import requests
import os
from groq import Groq
import datetime
from db_config import init_authenticator

# Set page config
st.set_page_config(layout="wide", page_title="RecycleBuddy", page_icon="♻️")

# Initialize authenticator from `db_config.py`
authenticator = init_authenticator()

# Create a login widget
name, authenticator_status, username = authenticator.login('Login', 'main')

def main():
    client = Groq(
        api_key = os.environ.get("GROQ_KEY")
    )

    # for groq; this gives it an idea of who it is
    system_prompt = {
        "role": "system",
        "content":
        "You are a helpful assistant. You reply concisely, and you only reply if \
        the prompt is related to recycling. If not, then kindly redirect the \
        conversation to recycling. Try to use less than 40 words and no numbered \
        lists."
        }

    chat_history = [system_prompt]

    # Load Lottie animation
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_recycle = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")

    # Custom CSS for styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        .stApp {
            font-family: 'Poppins', sans-serif;
        }
        .main-title {
            font-size: 3rem;
            font-weight: 600;
            color: #4CAF50;
        }
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .our-features{
                font-size: 1.2rem;
            font-weight: 600;
                }
    </style>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown('<p class="main-title">RecycleBuddy</p>', unsafe_allow_html=True)
    st.subheader("Your AI-powered companion for smarter recycling")

    # Hero section with Lottie animation
    col1, col2 = st.columns([1, 1])
    with col1:
        st_lottie(lottie_recycle, height=400)
    with col2:
        st.header(":green[Join the Green Revolution]")
        st.write("""
        RecycleBuddy uses cutting-edge AI to help you recycle more effectively. 
        Scan any item, and we'll tell you exactly how to recycle it. You can also chat our AI to clear up any confusions you may have!
        """)
        if st.button("Take a Picture", key="take_picture"):
            st.success("Welcome to RecycleBuddy! Let's start your recycling journey.")
            
        user_input = st.text_area("Ask our AI", placeholder="Ex: How should I dispose of batteries?")
        if st.button("Submit"):
            chat_history.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(model="llama3-70b-8192",
            messages = chat_history,
            max_tokens = 100,
            temperature = 0.2)
            chat_history.append({"role": "assistant", \
            "content": response.choices[0].message.content})
            st.write("Assistant: ", response.choices[0].message.content)

    # Features section
    st.header(":green[Our Features]")
    col1, col2, col3 = st.columns(3)

    with col1:
        #st.markdown('<div class="feature-icon">📱</div>', unsafe_allow_html=True)
        #st.subheader("Smart Scanning")
        st.markdown('<p class="our-features">Smart Scanning</p>', unsafe_allow_html=True)
        st.write("Use your camera to instantly identify and learn how to recycle any item.")
        st.markdown('<div class="feature-icon">📱</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<p class="our-features">Chat With Recycle Buddy</p>', unsafe_allow_html=True)
        st.write("Chat with RecycleBuddy if you are unsure on what to do with a specific item!")
        st.markdown('<div class="feature-icon">🗣️</div>', unsafe_allow_html=True)

    with col3:
        #st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<p class="our-features">Impact Tracker</p>', unsafe_allow_html=True)
        st.write("Monitor your recycling efforts and see your positive impact on the environment by gaining gems each time you use us!")
        st.markdown('<div class = "feature-icon">💎</div>', unsafe_allow_html=True)

    # Interactive recycling guide
    st.header(":green[Interactive Recycling Guide]")

    item = st.selectbox("Select an item to recycle:", ["Plastic Bottle", "Cardboard Box", "Glass Jar", "Aluminum Can"])

    if item:
        if item == "Plastic Bottle":
            st.info("♻️ Rinse the bottle and remove the cap. Place the bottle in your recycling bin. Check if your local facility accepts the cap separately.")
        elif item == "Cardboard Box":
            st.info("♻️ Break down the box to save space. Remove any tape or labels. Place in your recycling bin or take to a local recycling center.")
        elif item == "Glass Jar":
            st.info("♻️ Rinse the jar and remove the lid. Place the jar in your glass recycling bin. Metal lids can often be recycled separately.")
        elif item == "Aluminum Can":
            st.info("♻️ Rinse the can and place it in your recycling bin. No need to remove the label. Crush the can to save space if desired.")

    # Dynamic stats
    st.header("Our Impact")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Items Recycled", "1M+")

    with col2:
        st.metric("Active Users", "500K")

    with col3:
        st.metric("Trees Saved", "10K")

    # Call to action
    st.header("Ready to Make a Difference?")
    st.write("Join RecycleBuddy today and start your journey towards a greener future.")
    if st.button("Download RecycleBuddy"):
        st.success("Thank you for your interest! Download link coming soon.")

    # Fun fact
    fun_facts = [
        "Recycling one aluminum can saves enough energy to power a TV for three hours.",
        "Plastic bottles take 700 years to decompose in landfills.",
        "Recycling one ton of paper saves 17 trees and 7,000 gallons of water.",
        "The average person generates over 4 pounds of trash every day and about 1.5 tons of solid waste per year.",
        "It takes just 60 days for an aluminum can to be recycled, refilled, and back on the shelf.",
        "Every glass bottle recycled saves enough energy to light a 100-watt bulb for four hours.",
        "Only 9% of all plastic ever produced has been recycled.",
        "Recycling a stack of newspapers 3 feet high saves one tree.",
        "The energy saved from recycling one glass bottle can power a computer for 25 minutes.",
        "Americans throw away 2.5 million plastic bottles every hour.",
        "Over 80% of items in landfills could have been recycled.",
        "Each year, enough plastic is thrown away to circle the Earth four times.",
        "Recycling steel saves 75% of the energy used to make new steel from raw materials.",
        "The U.S. produces 70% of the world’s solid waste.",
        "It takes 24 trees to make one ton of newspaper.",
        "Recycling 1 ton of plastic can save up to 2,000 gallons of gasoline.",
        "Recycling 1 ton of glass saves over 1,300 pounds of sand and 410 pounds of soda ash.",
        "Americans use 100 billion plastic bags a year, and only 1% are recycled.",
        "Recycling just 1 ton of cardboard saves 46 gallons of oil.",
        "An estimated 1 million sea creatures are killed annually by plastic waste in the ocean."
    ]

    st.sidebar.title("Menu")
    if st.sidebar.button("Profile"):
        st.sidebar.write("Profile details coming soon!")
    if st.sidebar.button("History"):
        st.sidebar.write("No history available yet.")

    # Token tracker
    tokens = 0
    st.sidebar.write(f"Tokens: 💎 {tokens}")

    # Display fun facts with auto-change every n seconds
    placeholder = st.sidebar.empty()

    # Loop to change fun facts every 10 seconds
    for i in range(len(fun_facts)):
        placeholder.write(f"Fun Fact: {fun_facts[i]}")
        time.sleep(6)

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    main()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')