import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import csv

st.set_page_config(page_title="SpendWise | Expense Tracker", page_icon="💸", layout="wide")

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "transactions.csv"
COLUMNS = ["id", "date", "type", "category", "description", "amount", "payment_method"]

st.markdown("""
<style>
.block-container{max-width:1150px;padding-top:2rem}
.hero{padding:1.5rem 1.7rem;border:1px solid #e5e9ef;border-radius:20px;background:linear-gradient(120deg,#f0f5ff,#effaf4)}
.hero h1{margin:0;color:#172b3b;font-size:2.3rem}
.hero p{margin:.45rem 0 0;color:#536779}
div[data-testid="stMetric"]{background:white;border:1px solid #e6eaf0;padding:13px;border-radius:14px}
</style>
""", unsafe_allow_html=True)

def load_data():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            return df[COLUMNS]
        except Exception:
            st.error("Your saved transaction file could not be read. Download a backup if you have one, then check data/transactions.csv.")
    return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    df[COLUMNS].to_csv(DATA_FILE, index=False)

if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()

df = st.session_state.transactions.copy()
if not df.empty:
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

st.markdown("""
<div class="hero">
<h1>💸 SpendWise</h1>
<p>A simple personal expense tracker — record spending, monitor your budget and understand where your money goes.</p>
</div>
""", unsafe_allow_html=True)
st.write("")

currency = st.sidebar.selectbox("Currency", ["₹ INR", "$ USD", "€ EUR", "£ GBP"], index=0)
symbol = {"₹ INR":"₹", "$ USD":"$", "€ EUR":"€", "£ GBP":"£"}[currency]
st.sidebar.caption("Your transactions are saved locally in this project's data folder.")
st.sidebar.info("This is a local personal tracker. It does not connect to your bank.")

def money(value):
    return f"{symbol}{value:,.2f}"

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "➕ Add Transaction", "📋 Transactions", "🎯 Budget"])

with tab1:
    st.subheader("Your financial overview")
    if df.empty:
        income = expenses = balance = 0.0
    else:
        income = df.loc[df["type"] == "Income", "amount"].sum()
        expenses = df.loc[df["type"] == "Expense", "amount"].sum()
        balance = income - expenses
    c1,c2,c3 = st.columns(3)
    c1.metric("Total income", money(income))
    c2.metric("Total expenses", money(expenses))
    c3.metric("Remaining balance", money(balance), delta_color="normal")
    st.divider()
    if df.empty:
        st.info("No transactions yet. Open Add Transaction to record your first income or expense.")
    else:
        left, right = st.columns(2)
        with left:
            st.markdown("#### Expenses by category")
            expense_df = df[df["type"] == "Expense"]
            if not expense_df.empty:
                category_totals = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
                st.bar_chart(category_totals)
            else:
                st.caption("No expenses recorded yet.")
        with right:
            st.markdown("#### Income vs expenses")
            comparison = pd.Series({"Income": income, "Expenses": expenses})
            st.bar_chart(comparison)
        st.markdown("#### Recent transactions")
        recent = df.sort_values("date", ascending=False).head(5)
        st.dataframe(recent[["date","type","category","description","amount"]], use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Add a transaction")
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tx_type = st.selectbox("Transaction type", ["Expense", "Income"])
            tx_date = st.date_input("Date", value=date.today())
            category_options = (
                ["Food", "Transport", "Education", "Shopping", "Bills", "Health", "Entertainment", "Rent", "Travel", "Other"]
                if tx_type == "Expense" else
                ["Salary", "Allowance", "Scholarship", "Freelance", "Gift", "Other Income"]
            )
            category = st.selectbox("Category", category_options)
        with col2:
            amount = st.number_input("Amount", min_value=0.01, value=100.0, step=10.0)
            description = st.text_input("Description", placeholder="Example: Lunch, bus pass, monthly allowance")
            payment = st.selectbox("Payment method", ["Cash", "UPI", "Debit card", "Credit card", "Bank transfer", "Other"])
        submitted = st.form_submit_button("Save transaction", type="primary", use_container_width=True)
        if submitted:
            next_id = int(pd.to_numeric(df["id"], errors="coerce").max() + 1) if not df.empty else 1
            new_row = pd.DataFrame([{
                "id": next_id, "date": tx_date.isoformat(), "type": tx_type,
                "category": category, "description": description.strip(),
                "amount": float(amount), "payment_method": payment
            }])
            updated = pd.concat([df, new_row], ignore_index=True)
            save_data(updated)
            st.session_state.transactions = load_data()
            st.success("Transaction saved successfully.")
            st.rerun()

with tab3:
    st.subheader("All transactions")
    df = st.session_state.transactions.copy()
    if df.empty:
        st.info("Your transaction list is empty.")
    else:
        f1, f2 = st.columns(2)
        with f1:
            type_filter = st.selectbox("Filter by type", ["All", "Income", "Expense"])
        with f2:
            category_filter = st.selectbox("Filter by category", ["All"] + sorted(df["category"].dropna().astype(str).unique().tolist()))
        view = df.copy()
        if type_filter != "All":
            view = view[view["type"] == type_filter]
        if category_filter != "All":
            view = view[view["category"] == category_filter]
        st.dataframe(view[["date","type","category","description","amount","payment_method"]], use_container_width=True, hide_index=True)
        csv_data = view.to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered transactions (CSV)", csv_data, "spendwise_transactions.csv", "text/csv")
        st.divider()
        st.markdown("#### Delete a transaction")
        id_options = view["id"].tolist()
        if id_options:
            selected_id = st.selectbox("Select transaction ID", id_options)
            if st.button("Delete selected transaction", type="secondary"):
                updated = st.session_state.transactions[st.session_state.transactions["id"] != selected_id].copy()
                save_data(updated)
                st.session_state.transactions = load_data()
                st.success("Transaction deleted.")
                st.rerun()
        st.caption("Keep downloaded CSV backups if you want an extra copy of your records.")

with tab4:
    st.subheader("Monthly expense budget")
    default_budget = float(st.session_state.get("monthly_budget", 10000.0))
    budget = st.number_input(f"Set monthly budget ({symbol})", min_value=0.0, value=default_budget, step=500.0)
    st.session_state.monthly_budget = budget
    selected_month = st.date_input("Choose any date in the month", value=date.today(), key="budget_month")
    if not df.empty:
        dates = pd.to_datetime(df["date"], errors="coerce")
        month_mask = (dates.dt.year == selected_month.year) & (dates.dt.month == selected_month.month)
        month_expenses = df[(df["type"] == "Expense") & month_mask]["amount"].sum()
    else:
        month_expenses = 0.0
    remaining = budget - month_expenses
    b1,b2 = st.columns(2)
    b1.metric("Expenses this month", money(month_expenses))
    b2.metric("Budget remaining", money(remaining), delta_color="normal")
    if budget > 0:
        st.progress(min(month_expenses / budget, 1.0), text=f"{(month_expenses / budget * 100):.1f}% of monthly budget used")
    if month_expenses > budget and budget > 0:
        st.warning("You have exceeded your monthly budget.")
    elif budget > 0:
        st.success("You are within your budget.")

st.divider()
st.caption("SpendWise is a student project for personal record-keeping. It is not financial advice. Your data is stored locally in data/transactions.csv.")
