import streamlit as st
import pandas as pd
import os

# (Optional) Matplotlib for pie chart
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

# ---------- Data Setup ----------
DATA_FILE = "expenses.csv"
if "expenses" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state["expenses"] = pd.read_csv(DATA_FILE)
    else:
        st.session_state["expenses"] = pd.DataFrame(
            columns=["Date", "Description", "Amount", "Category"]
        )
df = st.session_state["expenses"]

# ---------- Page Config ----------
st.set_page_config(page_title="💸 Expense Tracker", layout="centered")

# ---------- Global Styles ----------
st.markdown(
    """
<style>
/* App base */
.stApp { background-color: #0d1117; color: #e6edf3; }

/* Title */
.title { font-size: 2.6rem; font-weight: 800; color: #58a6ff;
         text-align: center; margin: 10px 0 20px 0;
         text-shadow: 0 0 10px rgba(88,166,255,.75); }

/* Cards */
.card { background: #161b22; border: 1px solid #30363d;
        border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.5);
        padding: 18px; }

/* Labels */
.stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label {
  color: #58a6ff !important; font-weight: 700 !important;
}

/* Inputs */
input, select, textarea {
  background: #0d1117 !important; color: #e6edf3 !important;
  border: 1px solid #30363d !important; border-radius: 8px !important;
}

/* Dataframe */
.stDataFrame { background: #161b22 !important;
               border: 1px solid #30363d; border-radius: 12px; padding: 8px; }

/* Buttons */
.stButton button, .stDownloadButton button {
  background: linear-gradient(90deg, #238636, #2ea043);
  color: #fff; border: none; border-radius: 10px; padding: 10px 16px;
  font-weight: 700; transition: .25s;
}
.stButton button:hover, .stDownloadButton button:hover {
  background: linear-gradient(90deg, #2ea043, #3fb950);
}

/* Only form submit button -> dark */
div.stForm button {
  background: linear-gradient(90deg, #161b22, #21262d) !important;
  color: #f0f6fc !important; border: 1px solid #30363d !important;
  border-radius: 10px !important; font-weight: 800 !important;
}
div.stForm button:hover {
  background: linear-gradient(90deg, #2a3139, #3a424c) !important;
}

/* Sidebar dark */
section[data-testid="stSidebar"] {
  background: #161b22 !important; border-right: 1px solid #30363d;
}
section[data-testid="stSidebar"] * { color: #e6edf3 !important; }
.sidebar-title { font-size: 1.25rem; font-weight: 800; color: #ffa657 !important;
                 text-align: center; margin-bottom: 10px; }
.sidebar-box { background: #0d1117; border: 1px solid #30363d;
               border-radius: 12px; padding: 12px; margin-bottom: 12px; }
.sidebar-actions .stButton>button, .sidebar-actions .stDownloadButton>button {
  width: 100%;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="sidebar-title">📌 Dashboard</div>', unsafe_allow_html=True)

    total_spent = float(df["Amount"].sum()) if not df.empty else 0.0
    entry_count = int(len(df)) if not df.empty else 0
    st.markdown(
        f"""
        <div class="sidebar-box">
          <div><b>🔢 Entries:</b> {entry_count}</div>
          <div><b>💰 Total Spent:</b> ${total_spent:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-box"><b>🕒 Recent</b></div>', unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df.tail(5)[["Date", "Description", "Amount", "Category"]],
                     hide_index=True, use_container_width=True, height=200)
    else:
        st.caption("No expenses yet — add your first one!")

    st.markdown('<div class="sidebar-actions">', unsafe_allow_html=True)
    if st.button("🗑️ Clear All Data", key="clear_all"):
        st.session_state["expenses"] = pd.DataFrame(
            columns=["Date", "Description", "Amount", "Category"]
        )
        st.session_state["expenses"].to_csv(DATA_FILE, index=False)
        st.rerun()
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "expenses.csv")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="title">💸 Expense Tracker</div>', unsafe_allow_html=True)

# ---------- Add Expense Form ----------
with st.form("add_expense", clear_on_submit=True):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    date = st.date_input("📅 Date")
    desc = st.text_input("📝 Description")
    amount = st.number_input("💰 Amount", min_value=0.0, step=0.01)
    category = st.selectbox(
        "🏷️ Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]
    )
    submitted = st.form_submit_button("➕ Add Expense")
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        new_row = pd.DataFrame([[date, desc, amount, category]], columns=df.columns)
        st.session_state["expenses"] = pd.concat([df, new_row], ignore_index=True)
        st.session_state["expenses"].to_csv(DATA_FILE, index=False)
        st.success(f"✅ Added under '{category}'!")
        st.rerun()  # 🔥 Immediately refresh sidebar + dashboard

# ---------- Main Table ----------
st.subheader("📊 All Expenses")
st.dataframe(st.session_state["expenses"], use_container_width=True)

# ---------- Charts ----------
if not st.session_state["expenses"].empty:
    st.subheader("📈 Spending by Category")
    summary = st.session_state["expenses"].groupby("Category")["Amount"].sum()
    st.bar_chart(summary)

    if plt is not None:
        st.subheader("🥧 Category Share")
        fig, ax = plt.subplots(facecolor="#0d1117")
        ax.pie(summary, labels=summary.index, autopct="%1.1f%%",
               textprops={"color": "white"})
        ax.set_facecolor("#0d1117")
        st.pyplot(fig)










