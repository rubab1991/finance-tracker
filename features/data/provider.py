import csv
from collections import defaultdict
from datetime import datetime

TRANSACTION_FILE = "database/transactions.txt"
BUDGET_FILE = "database/budgets.txt"

def get_all_transactions():
    """Reads all transactions from the file."""
    transactions = []
    try:
        with open(TRANSACTION_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    transactions.append({
                        "date": row[0],
                        "type": row[1],
                        "category": row[2],
                        "description": row[3],
                        "amount": int(row[4])
                    })
    except FileNotFoundError:
        pass
    return transactions

def get_budgets():
    """Reads all set budgets."""
    budgets = {}
    try:
        with open(BUDGET_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    budgets[row[0]] = int(row[1])
    except FileNotFoundError:
        pass
    return budgets

def get_transactions_for_month(month_str):
    """Filters transactions for a specific month from all transactions."""
    all_transactions = get_all_transactions()
    return [t for t in all_transactions if t['date'].startswith(month_str)]

def get_monthly_spending():
    """Calculates spending per category for the current month."""
    spending = defaultdict(int)
    current_month_str = datetime.now().strftime("%Y-%m")
    current_month_transactions = get_transactions_for_month(current_month_str)
    
    for t in current_month_transactions:
        if t['type'] == "Expense":
            spending[t['category']] += t['amount']
            
    return spending

def calculate_monthly_summary(transactions):
    """Calculates total income and expenses for a list of transactions."""
    total_income = 0
    total_expense = 0
    spending_by_category = defaultdict(int)
    income_by_source = defaultdict(int)

    for t in transactions:
        if t["type"] == "Income":
            total_income += t["amount"]
            income_by_source[t["category"]] += t["amount"]
        elif t["type"] == "Expense":
            total_expense += t["amount"]
            spending_by_category[t["category"]] += t["amount"]

    return total_income, total_expense, spending_by_category, income_by_source
