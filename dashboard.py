import streamlit as st
import pandas as pd
from datetime import datetime
from features.data.provider import get_all_transactions, get_budgets, get_monthly_spending
from features.transactions.transactions import add_expense_from_streamlit, EXPENSE_CATEGORIES, add_income_from_streamlit, INCOME_CATEGORIES


# --- Streamlit App ---

st.set_page_config(layout="centered", page_title="Finance Dashboard")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        border: 1px solid #e1e1e1;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    .st-emotion-cache-1jicfl2 {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


# --- Header ---
st.title("Financial Dashboard")
st.markdown(f"_Report for {datetime.now().strftime('%B %Y')}_")


# --- Data Preparation ---
transactions = get_all_transactions()
budgets = get_budgets()
monthly_spending = get_monthly_spending()

current_month_str = datetime.now().strftime("%Y-%m")
current_month_transactions = [t for t in transactions if t['date'].startswith(current_month_str)]

total_income = sum(t['amount'] for t in current_month_transactions if t['type'] == 'Income') / 100
total_expense = sum(t['amount'] for t in current_month_transactions if t['type'] == 'Expense') / 100
current_balance = total_income - total_expense


# --- Balance Section ---
st.header("Current Month's Balance")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}", delta_color="normal")
col2.metric("Total Expenses", f"${total_expense:,.2f}", delta_color="inverse")
col3.metric("Current Balance", f"${current_balance:,.2f}")


# --- Budget Status Section ---
st.header("Budget Status")
if not budgets:
    st.info("No budgets set. Use the CLI to set a budget.")
else:
    for category, budget_cents in budgets.items():
        budget_amount = budget_cents / 100
        spent_cents = monthly_spending.get(category, 0)
        spent_amount = spent_cents / 100
        
        utilization = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
        
        st.markdown(f"**{category}**")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(min(int(utilization), 100))
        with col2:
            st.markdown(f"`{spent_amount:,.2f} / {budget_amount:,.2f}`")

# --- Add New Expense Section ---
st.header("Add New Expense")
with st.form("new_expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.now())
        category = st.selectbox("Category", EXPENSE_CATEGORIES)
    with col2:
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
    
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        message = add_expense_from_streamlit(amount, category, description, date)
        st.success(message)
        st.rerun()



# --- Add New Income Section ---
st.header("Add New Income")
with st.form("new_income_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date_income = st.date_input("Income Date", datetime.now(), key="income_date")
        category_income = st.selectbox("Income Source", INCOME_CATEGORIES, key="income_category")
    with col2:
        description_income = st.text_input("Income Description", key="income_description")
        amount_income = st.number_input("Income Amount", min_value=0.01, step=0.01, format="%.2f", key="income_amount")
    
    submitted_income = st.form_submit_button("Add Income")
    if submitted_income:
        message_income = add_income_from_streamlit(amount_income, category_income, description_income, date_income)
        st.success(message_income)
        st.rerun()

# --- Recent Transactions Table ---
st.header("Recent Transactions")
if not transactions:
    st.info("No transactions found.")
else:
    # Sort transactions by date (newest first) and take the last 10
    recent_transactions = sorted(transactions, key=lambda t: t['date'], reverse=True)[:10]
    
    # Prepare data for display
    display_data = []
    for t in recent_transactions:
        amount_display = f"${t['amount'] / 100:,.2f}"
        display_data.append({
            "Date": t['date'],
            "Type": t['type'],
            "Category": t['category'],
            "Description": t['description'],
            "Amount": amount_display
        })

    # Convert to DataFrame for styling
    df = pd.DataFrame(display_data)

    def style_rows(row):
        color = 'green' if row.Type == 'Income' else 'red'
        return [f'color: {color}']*len(row)

    st.dataframe(df.style.apply(style_rows, axis=1), use_container_width=True, hide_index=True)
