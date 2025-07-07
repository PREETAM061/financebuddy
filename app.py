import streamlit as st
import requests
import os

# ---------------------- UI & Input Section ----------------------
st.set_page_config(page_title="FinanceBuddy", page_icon="💸", layout="wide")
st.title("💸 FinanceBuddy – Your Personal Expense Advisor")
st.caption("Smart, real-time financial advice using AI, with offline fallback 🛡️")

st.subheader("📝 Enter your weekly expenses")
categories = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
expenses = {cat: st.number_input(f"{cat} expense (₹)", min_value=0, step=100, key=cat) for cat in categories}

weekly_budget = st.slider("📊 Set your weekly budget (₹)", 1000, 20000, 5000, 500)
total_spent = sum(expenses.values())

st.markdown(f"### 💰 **Total Spent:** ₹{total_spent}")
st.markdown(f"### 📊 **Weekly Budget:** ₹{weekly_budget}")

# ---------------------- Offline Advice Engine ----------------------
def offline_advice(expenses, budget):
    tips = []
    total = sum(expenses.values())

    if total > budget:
        tips.append("🚨 You're over budget! Review your spending categories.")
    else:
        tips.append("✅ Great! You’re within budget.")

    # Category-wise suggestions
    for cat, amt in expenses.items():
        pct = amt / (budget or 1)
        if pct > 0.4:
            tips.append(f"💡 High spending on **{cat}** ({amt}₹). Try reducing this next week.")
        elif pct < 0.1 and amt > 0:
            tips.append(f"🌟 Low spending on **{cat}**—you might allocate more wisely.")

    # General advice
    saving = budget - total
    if saving > budget * 0.2:
        tips.append(f"💰 Nice savings! Consider putting ₹{saving} into an emergency fund.")
    tips.append("🗓️ Tip: Track and review your budget every Sunday.")

    return "\n".join(tips)

# ---------------------- Hugging Face Integration ----------------------
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_HEADERS = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}

def ai_advice(prompt):
    try:
        resp = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": prompt}, timeout=30)
        if resp.status_code != 200:
            raise Exception(f"API {resp.status_code}")
        data = resp.json()
        return data[0]["generated_text"].strip()
    except Exception:
        # On any failure, fall back to offline advice
        return offline_advice(expenses, weekly_budget)

# ---------------------- Advice Trigger ----------------------
if st.button("🤖 Get Advice"):
    # Build prompt
    expense_lines = "\n".join(f"- {cat}: ₹{amt}" for cat, amt in expenses.items())
    prompt = (
        "You are a friendly finance assistant.\n"
        f"User's weekly expenses:\n{expense_lines}\n"
        f"Budget: ₹{weekly_budget}\n\n"
        "Give 3–5 bullet tips to manage their budget."
    )

    # Get advice (AI or fallback)
    advice = ai_advice(prompt)
    st.markdown("### 🧠 Financial Advice")
    st.write(advice)
