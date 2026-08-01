import streamlit as st
import pandas as pd
import json
import os

# --- 1. SETUP SIMPLE DATABASE ---
DB_FILE = "live_votes.json"

# Define the blind pitches and the big reveal!
CASES = {
    "Pitch 1: The Menu Scanner": {
        "pitch": """**The Pitch:**
"I am the founder. I have built a website that scans the physical, paper menus of local neighborhood restaurants and puts them online. Right now, there is no delivery, no live tracking, just scanned menus so people can look at prices before they walk in. I need money to scan more menus in different cities.

Who wants to invest? Let's say I am asking for ₹5 Crores. Here are the 4 deals you could offer me as a VC." """,
        "options": [
            "A: Expand aggressively into 10 new Tier-1 cities",
            "B: Build an in-house food delivery fleet",
            "C: Invest heavily in restaurant B2B software/POS",
            "D: Launch massive discount campaigns for user acquisition"
        ],
        "reveal_company": "Zomato (formerly Foodiebay) 🍅",
        "reveal_action": "**The Actual VC Decision: Option A** \n\nEarly investors like Info Edge didn't fund delivery. They funded the aggressive expansion of the restaurant directory. By becoming the absolute monopoly in restaurant search across new cities first, they owned the customer traffic. Only years later did they pivot that massive user base into food delivery."
    },
    "Pitch 2: The Bill Payer": {
        "pitch": """**The Pitch:**
"I am a founder, and I want to build an app where people can pay their credit card bills. But here is the catch: We will not charge the users any fees. In fact, we will give them expensive rewards, free coffee, and cashback just for paying the bills they already have to pay anyway.

Also, we will reject 99% of people who try to sign up. Only people with extremely high credit scores are allowed in. I have zero revenue model on Day 1. I just need money to give away free stuff to wealthy people and run TV ads with 90s Bollywood stars and cricketers." """,
        "options": [
            "A: Launch a lending product (Cash) for high-trust users",
            "B: Build a premium e-commerce marketplace (Store)",
            "C: Acquire a payment gateway",
            "D: Expand internationally"
        ],
        "reveal_company": "CRED 💳",
        "reveal_action": "**The Actual VC Decision: Options A & B** \n\nVCs backed Kunal Shah not to process bills, but to capture the trust and data of India's top 1% most affluent consumers. Once they had the most premium user base in India, they monetized through high-margin consumer lending (CRED Cash) and a curated D2C luxury marketplace (CRED Store)."
    }
}

def load_votes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "Pitch 1: The Menu Scanner": {opt: 0 for opt in CASES["Pitch 1: The Menu Scanner"]["options"]},
            "Pitch 2: The Bill Payer": {opt: 0 for opt in CASES["Pitch 2: The Bill Payer"]["options"]}
        }

def save_vote(case, option):
    votes = load_votes()
    votes[case][option] += 1
    with open(DB_FILE, "w") as f:
        json.dump(votes, f)

# --- 2. STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="Mini Shark Tank", layout="centered")

st.title("🦈 Mini Shark Tank: The VC Decision")

# Sidebar navigation
view_mode = st.sidebar.radio("Select View:", ["Student (Vote Here)", "Host (Board View)"])

# --- 3. STUDENT VIEW (PHONES) ---
if view_mode == "Student (Vote Here)":
    st.subheader("Evaluate the Pitch")
    
    selected_case = st.selectbox("Which Pitch are we evaluating?", list(CASES.keys()))
    
    st.markdown("---")
    st.markdown(CASES[selected_case]["pitch"])
    st.markdown("---")
    
    st.write("### 💼 Your Offer:")
    selected_option = st.radio("Where do you force the founder to deploy your capital?", CASES[selected_case]["options"])
    
    if st.button("Submit My Vote!"):
        save_vote(selected_case, selected_option)
        st.success("✅ Vote registered! Look at the main projector for live results.")

# --- 4. HOST VIEW (PROJECTOR) ---
elif view_mode == "Host (Board View)":
    st.subheader("Live Boardroom Results")
    
    selected_case = st.selectbox("Select Pitch to Display:", list(CASES.keys()))
    
    st.button("🔄 Refresh Live Votes")
    
    current_votes = load_votes()
    case_data = current_votes[selected_case]
    
    df = pd.DataFrame({
        "Options": list(case_data.keys()),
        "Votes": list(case_data.values())
    })
    
    df["Short Labels"] = df["Options"].apply(lambda x: x.split(":")[1].strip())
    df.set_index("Short Labels", inplace=True)
    
    if df["Votes"].sum() == 0:
        st.info("Waiting for the board to cast their votes...")
    else:
        st.bar_chart(df["Votes"])
        
    st.write(f"**Total Capital Deployed (Votes Cast):** {df['Votes'].sum()}")
    
    # --- THE BIG REVEAL (Only visible to the Host) ---
    st.markdown("---")
    with st.expander("🚨 CLICK TO REVEAL THE ACTUAL COMPANY & VC DECISION"):
        st.header(f"The Company was... {CASES[selected_case]['reveal_company']}!")
        st.info(CASES[selected_case]['reveal_action'])
