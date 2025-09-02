import streamlit as st
import pandas as pd
import os

# ---------- Data Setup ----------
DATA_FILE = "expenses.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])

# ---------- Page Config ----------
st.set_page_config(page_title="💸 Expense Tracker", layout="centered")

# ---------- Custom Dark CSS ----------
st.markdown("""
<style>
/* Set main background */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Title */
.title {
    font-size: 2.5em;
    font-weight: bold;
    color: #58a6ff;
    text-align: center;
    margin-bottom: 25px;
    text-shadow: 0px 0px 8px rgba(88,166,255,0.8);
}

/* Expense Form Card */
.expense-form {
    background: #161b22;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    border: 1px solid #30363d;
}

/* Form Labels */
label, .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label {
    color: #58a6ff !important;
    font-weight: bold !important;
}

/* DataFrame styling */
.stDataFrame {
    background: #161b22 !important;
    border-radius: 12px;
    border: 1px solid #30363d;
    padding: 10px;
    color: #e6edf3 !important;
}

/* Buttons */
.stButton button, .stDownloadButton button {
    background: linear-gradient(90deg, #238636, #2ea043);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: linear-gradient(90deg, #2ea043, #3fb950);
}

/* Danger (Clear All Data) Button */
.stButton > button:first-child {
    background: linear-gradient(90deg, #d73a49, #f85149);
}
.stButton > button:first-child:hover {
    background: linear-gradient(90deg, #f85149, #ff7b72);
}

/* Input fields */
input, select, textarea {
    background: #0d1117 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px;
    padding: 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="title">💸 Expense Tracker</div>', unsafe_allow_html=True)

# ---------- Add Expense Form ----------
with st.form("add_expense", clear_on_submit=True):
    st.markdown('<div class="expense-form">', unsafe_allow_html=True)

    date = st.date_input("📅 Date")
    desc = st.text_input("📝 Description")
    amount = st.number_input("💰 Amount", min_value=0.0, step=0.01)
    category = st.selectbox("🏷️ Category", ["Food", "Transport", "Shopping", "Bills", "Other"])

    submitted = st.form_submit_button("➕ Add Expense")
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        new_row = pd.DataFrame([[date, desc, amount, category]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"✅ Expense added under '{category}'!")

# ---------- Display Table ----------
st.subheader("📊 All Expenses")
st.dataframe(df, use_container_width=True)

# ---------- Clear Data Option ----------
if not df.empty:
    if st.button("🗑️ Clear All Data"):
        df = pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("⚠️ All expenses cleared!")

# ---------- Charts ----------
if not df.empty:
    st.subheader("📈 Spending by Category")
    summary = df.groupby("Category")["Amount"].sum()
    st.bar_chart(summary)

# ---------- Download ----------
if not df.empty:
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "expenses.csv")









