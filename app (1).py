import streamlit as st
import requests
import os
# ---------------------- UI & Input Section ----------------------
st.set_page_config(page_title="FinanceBuddy", page_icon="💸")
st.title("💸 FinanceBuddy – Your Personal Expense Advisor")
st.caption("Smart, real-time financial advice using AI 💡")

st.subheader("📝 Enter your weekly expenses")

categories = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
expenses = {}

for category in categories:
    amount = st.number_input(f"{category} expense (₹)", min_value=0, step=100, key=category)
    expenses[category] = amount

weekly_budget = st.slider("📊 Set your weekly budget (₹)", min_value=1000, max_value=20000, step=500, value=5000)

total_spent = sum(expenses.values())
st.markdown(f"### 💰 **Total Spent:** ₹{total_spent}")
st.markdown(f"### 📊 **Weekly Budget:** ₹{weekly_budget}")

# ---------------------- HuggingFace Integration ----------------------

# Replace this with your actual HuggingFace token
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_HEADERS = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}
def generate_ai_advice(prompt):
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": prompt})
        return response.json()[0]['generated_text']
    except Exception as e:
        return f"❌ Error generating advice: {e}"

# ---------------------- AI Advice Trigger ----------------------

if st.button("🤖 Get Smart AI Advice"):
    expense_list = "\n".join([f"- {cat}: ₹{amt}" for cat, amt in expenses.items()])
    ai_prompt = f"""
    I'm a helpful financial assistant. Here is the user's weekly spending:
    {expense_list}
    Weekly Budget: ₹{weekly_budget}
    Please give clear, friendly, financial advice in 3–5 bullet points.
    """

    ai_reply = generate_ai_advice(ai_prompt)
    st.markdown("### 🧠 AI-Powered Financial Advice")
    st.success(ai_reply)
