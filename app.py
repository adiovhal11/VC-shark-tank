import streamlit as st
import sqlite3
import pandas as pd

# 1. Setup a lightweight database to store live votes
conn = sqlite3.connect('shark_tank_votes.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS votes (name TEXT, case_study TEXT, offer TEXT)')
conn.commit()

# 2. Configure the page
st.set_page_config(page_title="VC Shark Tank", page_icon="🦈", layout="wide")
st.title("🦈 Mini Shark Tank: VC Edition")

# 3. Sidebar to separate the Host (You) from the Students
role = st.sidebar.radio("Select your view:", ["Student (Vote Here)", "Host (Board View)"])

# ==========================================
# STUDENT VIEW (What they see on their phones)
# ==========================================
if role == "Student (Vote Here)":
    st.header("Cast Your Investment Vote!")
    
    name = st.text_input("Enter your name (e.g., Shark Rahul):")
    
    case = st.radio("Which startup pitch are we evaluating?", 
                    ["Case 1: The Scanned Menus", "Case 2: The Exclusive Club"])
    
    st.markdown("---")
    st.subheader("Select your offer:")
    
    # Show context based on the case
    if "Case 1" in case:
        offer = st.radio("Options for Case 1:", 
                         ["Offer A: ₹5 Crores for 1%", 
                          "Offer B: ₹5 Crores for 15%", 
                          "Offer C: ₹5 Crores for 30%", 
                          "Offer D: ₹4.7 Crores for maximum control"])
    else:
        offer = st.radio("Options for Case 2:", 
                         ["Offer A: ₹10 Crores for 20%", 
                          "Offer B: ₹50 Crores for 30%", 
                          "Offer C: ₹220 Crores before the app even launches", 
                          "Offer D: ZERO. I'm out."])
    
    if st.button("Submit My Offer 💸"):
        if name:
            c.execute("INSERT INTO votes (name, case_study, offer) VALUES (?, ?, ?)", 
                      (name, case, offer.split(":")[0])) 
            conn.commit()
            st.success(f"Deal logged, {name}! Look at the board to see how everyone else voted.")
        else:
            st.error("Please enter your name first!")

# ==========================================
# HOST VIEW (What you project on the board)
# ==========================================
elif role == "Host (Board View)":
    st.header("Live Investment Board")
    
    case = st.selectbox("Select pitch to track:", ["Case 1: The Scanned Menus", "Case 2: The Exclusive Club"])
    
    df = pd.read_sql_query(f"SELECT * FROM votes WHERE case_study='{case}'", conn)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Market Sentiment (Live Votes)")
        if not df.empty:
            vote_counts = df['offer'].value_counts().reset_index()
            vote_counts.columns = ['Offer', 'Votes']
            st.bar_chart(vote_counts.set_index('Offer'))
            
            with st.expander("See who invested"):
                st.dataframe(df, use_container_width=True)
        else:
            st.info("Waiting for the sharks to make their offers...")
            
    with col2:
        st.subheader("The Big Reveal")
        st.write("Wait for everyone to vote before clicking!")
        
        if st.button("Reveal the Startup & The Real Deal 🚨"):
            st.balloons()
            if "Case 1" in case:
                st.success("**Startup: ZOMATO (Foodiebay)**")
                st.markdown("""
                **The Real Deal:** A mix of **Offer C & D**. 
                
                In 2010, Sanjeev Bikhchandani invested roughly ₹4.7 Crores but took a massive **~30% stake** because the risk was so high!
                """)
            else:
                st.success("**Startup: CRED**")
                st.markdown("""
                **The Real Deal: Offer C**. 
                
                In 2018, Kunal Shah raised roughly **$30 Million (₹220 Crores)** in seed funding before the app was even fully launched. VCs wanted access to India's top 1% wealthiest consumers!
                """)
                
    st.markdown("---")
    if st.button("Clear All Data (Reset for next class)"):
        c.execute("DELETE FROM votes")
        conn.commit()
        st.rerun()
