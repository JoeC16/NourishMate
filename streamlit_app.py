import streamlit as st
from firebase_config import db
import openai

st.set_page_config(page_title="Nourish Mate", layout="centered")

st.title("🍽️ Nourish Mate")
st.subheader("Meal Planning & Dysphagia Support")

# User input
name = st.text_input("Your name")
iddsi_level = st.selectbox("Select IDDSI Level", ["Level 3", "Level 4", "Level 5", "Level 6"])
preferences = st.text_area("Dietary preferences or restrictions")

# Generate meal plan
if st.button("Generate Meal Plan"):
    with st.spinner("Thinking..."):
        prompt = f"Create a meal plan for someone with {preferences} at {iddsi_level} texture level."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        plan = response.choices[0].message.content
        st.success("Here's your meal plan:")
        st.write(plan)

        # Save to Firebase
        db.collection("mealPlans").add({
            "name": name,
            "iddsi_level": iddsi_level,
            "preferences": preferences,
            "plan": plan
        })
