import streamlit as st
import pandas as pd
import json
import os

# --- 1. SETUP SIMPLE DATABASE ---
# Streamlit Cloud needs a way to save votes across different phones. 
# We use a simple temporary JSON file which is perfect for a 15-minute presentation.
DB_FILE = "live_votes.json"

# Define the cases and the four VC options for each
CASES = {
    "Zomato (formerly Foodiebay)": [
        "A: Expand aggressively into 10 new Tier-1 cities",
        "B: Build an in-house food delivery fleet",
        "C: Invest heavily in restaurant B2B software/POS",
        "D: Launch massive discount campaigns for user acquisition"
    ],
    "CRED": [
        "A: Launch a lending product (CRED Cash) for high-trust users",
        "B: Build a premium e-commerce marketplace (CRED Store)",
        "C: Acquire a payment gateway to control infrastructure",
        "D: Expand the app internationally to US/UK markets"
    ]
}

def load_votes():
    # If the file exists, read it. If not, create a fresh scorecard.
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "Zomato (formerly Foodiebay)": {opt: 0 for opt in CASES["Zomato (formerly Foodiebay)"]},
            "CRED": {opt: 0 for opt in CASES["CRED"]}
        }

def save_vote(case, option):
    votes = load_votes()
    votes[case][option] += 1
    with open(DB_FILE, "w") as f:
        json.dump(votes, f)

# --- 2. STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="VC Shark Tank", layout="centered")

st.title("🦈 Mini Shark Tank: The VC Decision")

# Sidebar navigation
view_mode = st.sidebar.radio("Select View:", ["Student (Vote Here)", "Host (Board View)"])

# --- 3. STUDENT VIEW (PHONES) ---
if view_mode == "Student (Vote Here)":
    st.subheader("Cast Your Investment Vote")
    st.write("Select a startup case and vote on where you would deploy your VC capital.")
    
    selected_case = st.selectbox("Which Case are we discussing?", list(CASES.keys()))
    
    st.write("### Your Options:")
    selected_option = st.radio("Where should the money go?", CASES[selected_case])
    
    if st.button("Submit My Vote!"):
        save_vote(selected_case, selected_option)
        st.success("✅ Vote registered! Look at the main screen for live results.")

# --- 4. HOST VIEW (PROJECTOR) ---
elif view_mode == "Host (Board View)":
    st.subheader("Live Boardroom Results")
    
    selected_case = st.selectbox("Select Case to Display:", list(CASES.keys()))
    
    # Add a refresh button for the presenter
    st.button("🔄 Refresh Live Votes")
    
    # Load and display the data
    current_votes = load_votes()
    case_data = current_votes[selected_case]
    
    # Convert to a Pandas DataFrame for the chart
    df = pd.DataFrame({
        "Options": list(case_data.keys()),
        "Votes": list(case_data.values())
    })
    
    # Clean up option names for the chart display (removes the A: B: C: D:)
    df["Short Labels"] = df["Options"].apply(lambda x: x.split(":")[1].strip())
    df.set_index("Short Labels", inplace=True)
    
    # Display the chart
    if df["Votes"].sum() == 0:
        st.info("Waiting for the board to cast their votes...")
    else:
        st.bar_chart(df["Votes"])
        
    st.write(f"**Total Capital Deployed (Votes):** {df['Votes'].sum()}")
