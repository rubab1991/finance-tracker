import questionary
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
import csv
from features.data.provider import get_all_transactions, calculate_monthly_summary, get_transactions_for_month

# Categories
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]
TRANSACTION_FILE = "database/transactions.txt"

console = Console()

def add_expense():
    """Adds a new expense transaction."""
    try:
        amount_str = questionary.text("Enter amount (e.g., 12.50):").ask()
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return

        category = questionary.select("Select category:", choices=EXPENSE_CATEGORIES).ask()
        description = questionary.text("Enter description:").ask()
        date_str = questionary.text("Enter date (YYYY-MM-DD, default: today):").ask()
        date = datetime.now().strftime("%Y-%m-%d") if not date_str else date_str

        with open(TRANSACTION_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, "Expense", category, description, amount])
        console.print("[bold green]Expense added successfully![/bold green]")

    except (ValueError, TypeError):
        console.print("[bold red]Invalid amount. Please enter a valid number.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")


def add_expense_from_streamlit(amount, category, description, date):
    """Adds a new expense transaction from Streamlit."""
    try:
        amount_in_cents = int(float(amount) * 100)
        if amount_in_cents <= 0:
            return "Amount must be a positive number."

        date_str = date.strftime("%Y-%m-%d")

        with open(TRANSACTION_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date_str, "Expense", category, description, amount_in_cents])
        return "Expense added successfully!"

    except (ValueError, TypeError):
        return "Invalid amount. Please enter a valid number."
    except Exception as e:
        return f"An error occurred: {e}"


def add_income_from_streamlit(amount, category, description, date):
    """Adds a new income transaction from Streamlit."""
    try:
        amount_in_cents = int(float(amount) * 100)
        if amount_in_cents <= 0:
            return "Amount must be a positive number."

        date_str = date.strftime("%Y-%m-%d")

        with open(TRANSACTION_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date_str, "Income", category, description, amount_in_cents])
        return "Income added successfully!"

    except (ValueError, TypeError):
        return "Invalid amount. Please enter a valid number."
    except Exception as e:
        return f"An error occurred: {e}"


def add_income():
    """Adds a new income transaction."""
    try:
        amount_str = questionary.text("Enter amount (e.g., 1000.00):").ask()
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return

        category = questionary.select("Select source:", choices=INCOME_CATEGORIES).ask()
        description = questionary.text("Enter description:").ask()
        date_str = questionary.text("Enter date (YYYY-MM-DD, default: today):").ask()
        date = datetime.now().strftime("%Y-%m-%d") if not date_str else date_str

        with open(TRANSACTION_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, "Income", category, description, amount])
        console.print("[bold green]Income added successfully![/bold green]")

    except (ValueError, TypeError):
        console.print("[bold red]Invalid amount. Please enter a valid number.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def list_transactions(filter_days=None, filter_type=None):
    """Lists all transactions."""
    transactions = get_all_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    # Sort by date (newest first)
    transactions.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=True)

    # Apply filters
    if filter_days:
        cutoff_date = datetime.now() - timedelta(days=int(filter_days))
        transactions = [t for t in transactions if datetime.strptime(t['date'], "%Y-%m-%d") >= cutoff_date]

    if filter_type:
        transactions = [t for t in transactions if t['type'].lower() == filter_type.lower()]


    table = Table(title="Transactions")
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Amount", justify="right")

    for row in transactions:
        amount = float(row['amount']) / 100
        color = "red" if row['type'] == "Expense" else "green"
        table.add_row(row['date'], row['type'], row['category'], row['description'], f"[{color}]{amount:.2f}[/{color}]")

    console.print(table)


def get_balance():
    """Calculates and displays the current balance for the month."""
    current_month = datetime.now().strftime("%Y-%m")
    transactions = get_transactions_for_month(current_month)
    
    total_income, total_expense, _, _ = calculate_monthly_summary(transactions)

    balance = total_income - total_expense
    balance_color = "green" if balance >= 0 else "red"

    console.print(f"Total Income: [green]{total_income / 100:.2f}[/green]")
    console.print(f"Total Expenses: [red]{total_expense / 100:.2f}[/red]")
    console.print(f"Current Balance: [{balance_color}]{balance / 100:.2f}[/{balance_color}]")