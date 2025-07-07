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

HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HF_HEADERS = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}

def generate_ai_advice(prompt):
    try:
        response = requests.post(
            HF_API_URL,
            headers=HF_HEADERS,
            json={"inputs": prompt},
            timeout=40  # Allow for large models to respond
        )

        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"

        result = response.json()

        # Check for correct output structure
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            return f"❌ API Error: {result['error']}"
        else:
            return "⚠️ Unexpected response. Please try again later."
    except Exception as e:
        return f"❌ Error generating advice: {e}"

# ---------------------- AI Advice Trigger ----------------------

if st.button("🤖 Get Smart AI Advice"):
    expense_list = "\n".join([f"- {cat}: ₹{amt}" for cat, amt in expenses.items()])
    ai_prompt = f"""
    I'm a helpful personal finance assistant.
    The user has spent the following this week:
    {expense_list}
    Weekly Budget: ₹{weekly_budget}

    Please provide 3–5 friendly, practical financial tips to help them budget better.
    """

    ai_reply = generate_ai_advice(ai_prompt)
    st.markdown("### 🧠 AI-Powered Financial Advice")
    st.success(ai_reply)
