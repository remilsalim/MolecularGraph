import streamlit as st
import joblib
import pandas as pd
import numpy as np
import re
from collections import defaultdict
import os

# Set page config
st.set_page_config(page_title="Molecular Side Effect Predictor", page_icon="💊", layout="wide")

# Custom CSS for spacing
st.markdown("""
    <style>
    .stContainer {
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)


# Funny Molecular Quotes
CHEST_PUNS = [
    "I'm a chemist. I have all the solutions. 🧪",
    "Organic chemistry is difficult. Those who study it have alkynes of trouble. ⌬",
    "Never trust an atom. They make up everything! ⚛️",
    "I was going to tell a joke about sodium... but Na. 🧂",
    "Chemistry jokes are always better in the lab. They have the best reaction. ⚗️",
    "Oxygen, Hydrogen, Sulfur, Sodium, and Phosphorus walked into a bar. 'OH SNaP!' 🍺",
    "Why are chemists great at solving problems? Because they have all the solutions! 💡",
    "What do you do with a dead chemist? We barium. ⚰️"
]

# Funny Science Facts
CHEMISTRY_FACTS = [
    "Fact: The human body contains enough carbon to lead about 9,000 pencils! ✏️",
    "Fact: Oxygen is actually a pale blue gas in its liquid and solid states! ❄️",
    "Fact: Bananas are radioactive because they contain Potassium-40! 🍌",
    "Fact: Gallium is a metal that melts in your hand because its melting point is 29.7°C! 🖐️",
    "Fact: There is enough gold in Earth's core to cover the surface knee-deep! 💰",
    "Fact: Helium is the only element that cannot be solidified by cooling alone! 🎈",
    "Fact: Hydrofluoric acid is so corrosive it will actually dissolve glass! 🧪",
    "Fact: If you pour a handful of salt into a glass of water, the water level actually goes down! 🧂"
]

# Helper functions for parsing MF

def parse_mf(mf):
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', mf)
    counts = defaultdict(int)
    for (elem, count) in elements:
        counts[elem] += int(count) if count else 1
    return counts

def mf_to_vector(mf, element_list):
    counts = parse_mf(mf)
    return [counts.get(el, 0) for el in element_list]

# Load models and metadata
@st.cache_resource
def load_assets():
    base_path = "my_pickles_extracted"
    model = joblib.load(os.path.join(base_path, 'model.joblib'))
    mlb = joblib.load(os.path.join(base_path, 'mlb.joblib'))
    element_list = joblib.load(os.path.join(base_path, 'element_list.joblib'))
    result_df = joblib.load(os.path.join(base_path, 'result_df.joblib'))
    return model, mlb, element_list, result_df

try:
    with st.spinner("Analyzing your molecules... " + np.random.choice(CHEST_PUNS)):
        model, mlb, element_list, result_df = load_assets()
    
    # Branded Header
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <h1 style="margin: 0;">💊 Molecular Side Effect Predictor™</h1>
            <a href="https://github.com/remilsalim" target="_blank" style="text-decoration: none;">
                <img src="https://img.shields.io/badge/GitHub-remilsalim-black?style=for-the-badge&logo=github" alt="GitHub">
            </a>
        </div>
        <hr style="margin-top: 10px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)

    st.markdown("""
        Predict the potential side effects of a drug molecule based on its **Molecular Formula**.
        This tool uses a Random Forest model trained on PubChem data.
    """)

    # Sidebar
    st.sidebar.title("Molecular Graph™")
    st.sidebar.markdown("""
        ---
        **Author:** [remilsalim](https://github.com/remilsalim)
        
        **Product ID:** MG-PRD-2026
        
        *This is a proprietary product. All rights reserved.*
        ---
    """)
    st.sidebar.info("""
        This application uses a Random Forest classifier to predict multi-label side effects.
        Input a molecular formula to see predicted side effects and matched drug names.
    """)


    # Main UI
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Search Molecular Formula")
        
        # Get unique formulas for autocomplete
        all_formulas = sorted(result_df['mf'].unique())
        
        user_input = st.selectbox(
            "Type to search (e.g., c6h12o6, h3n)",
            options=all_formulas,
            index=None,
            placeholder="Search for a formula...",
            help="Autocomplete enabled! Just start typing letters to match."
        )

        if user_input:
            import time
            import random


            
            # Show a funny quote while "predicting"
            with st.status(f"✨ {random.choice(CHEST_PUNS)}", expanded=True) as status:
                st.write(f"💡 **Random Fact:** {random.choice(CHEMISTRY_FACTS)}")
                st.write("🔍 Extracting atomic features...")
                time.sleep(0.6)
                st.write("🧠 Running Random Forest inference...")
                time.sleep(0.6)
                st.write("💊 Mapping side effects...")
                
                # Predict
                vector = mf_to_vector(user_input, element_list)
                vector = np.array(vector).reshape(1, -1)
                
                y_pred = model.predict(vector)
                predicted_labels = mlb.inverse_transform(y_pred)[0]
                
                # Match drug name
                match = result_df[result_df['mf'].str.strip() == user_input]
                drug_name = match.iloc[0]['drug_name'] if not match.empty else "Unknown / New Compound"
                
                status.update(label="✅ Prediction Complete!", state="complete", expanded=False)


            # Display results in a container
            with st.container(border=True):
                st.markdown(f'### 📌 Drug: {drug_name}')
                
                if predicted_labels:
                    st.write("**💊 Predicted Side Effects:**")
                    
                    # Display in multi-column list
                    cols = st.columns(3)
                    for i, se in enumerate(predicted_labels):
                        cols[i % 3].markdown(f"• **{se}**")
                else:
                    st.warning("No side effects predicted for this compound.")


    with col2:
        st.subheader("Reference Data")
        if user_input:
            st.write("**Molecular Formula Details:**")
            st.json(parse_mf(user_input))
            st.write(f"**Selected Formula:** `{user_input}`")
            match_ref = result_df[result_df['mf'].str.strip() == user_input]
            if not match_ref.empty:
                 st.write(f"**Database Match:** Yes")
            else:
                 st.write(f"**Database Match:** No (New Discovery!)")


except Exception as e:
    st.error(f"Error loading models or running prediction: {e}")
    st.info("Ensure that 'my_pickles_extracted' folder contains the required .joblib files.")

# Persistent Footer
st.markdown("""
    <br><br>
    <hr>
    <div style="text-align: center; color: #7f8c8d; font-size: 14px;">
        © 2026 Molecular Graph™ by <a href="https://github.com/remilsalim" target="_blank" style="color: #7f8c8d; text-decoration: none; font-weight: bold;">remilsalim</a>. 
        All rights reserved. 
    </div>
""", unsafe_allow_html=True)


