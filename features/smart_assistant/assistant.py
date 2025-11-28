import questionary
from rich.console import Console
from datetime import datetime

# Import existing functions to be called by the assistant
from features.transactions.transactions import list_transactions
from features.budgets.budgets import view_budgets
from features.analytics.analytics import generate_financial_report
from features.data.provider import get_transactions_for_month, calculate_monthly_summary

console = Console()

# --- 1. Hardcoded Financial Q&A ---
FINANCIAL_QA = {
    "what is inflation?": "Inflation is the rate at which the general level of prices for goods and services is rising, and subsequently, purchasing power is falling.",
    "what is compound interest?": "Compound interest is the interest on a loan or deposit calculated based on both the initial principal and the accumulated interest from previous periods.",
    "what is a good savings rate?": "A common rule of thumb is to save at least 20% of your income. However, the right amount for you depends on your financial goals and circumstances.",
    "how can i save money?": "You can save money by creating a budget, cutting unnecessary expenses, setting savings goals, and automating your savings.",
}


def handle_query(query: str):
    """Parses user query and routes to the correct function."""
    query = query.lower().strip()

    if "how much did i spend" in query or "spending on" in query:
        # Example: "how much did i spend on food?"
        parts = query.split(" on ")
        if len(parts) > 1:
            category_query = parts[1].replace("?", "").strip()
            # This is a simple implementation. A more robust solution would be to match to existing categories.
            console.print(f"Looking for spending on '{category_query}'...")
            list_transactions(filter_type="expense") # For now, just show all expenses
        else:
            list_transactions(filter_type="expense")

    elif "list my transactions" in query:
        list_transactions()

    elif "show my budget" in query or "view budget" in query:
        view_budgets()

    elif "am i overspending" in query:
        # A simple rule-based advice
        current_month_str = datetime.now().strftime("%Y-%m")
        transactions = get_transactions_for_month(current_month_str)
        income, expense, _, _ = calculate_monthly_summary(transactions)

        if expense > income:
            console.print(f"[bold red]Alert![/bold red] You've spent {expense/100:.2f} but only earned {income/100:.2f} this month. You are overspending.")
        else:
            console.print(f"[bold green]Good job![/bold green] Your spending ({expense/100:.2f}) is within your income ({income/100:.2f}) this month.")

    elif "give me tips" in query or "advice" in query:
        console.print("[bold cyan]Financial Tip:[/bold cyan] Create a budget and track your spending for a month. You'll be surprised where your money is going!")

    elif query in FINANCIAL_QA:
        console.print(f"[bold cyan]Answer:[/bold cyan] {FINANCIAL_QA[query]}")

    elif "report" in query:
        generate_financial_report()

    else:
        console.print("[yellow]Sorry, I didn't understand that. Please try asking in a different way.[/yellow]")
        console.print("You can ask things like: 'Show my budget', 'Am I overspending?', 'What is inflation?'.")


def run_assistant():
    """Main function to run the smart assistant chat interface."""
    console.print("[bold magenta]Welcome to your Smart Financial Assistant![/bold magenta]")
    console.print("You can ask me questions about your finances. Type 'exit' to quit.")

    while True:
        try:
            query = questionary.text("Ask me something:").ask()

            if query is None or query.lower() == 'exit':
                console.print("[bold magenta]Goodbye![/bold magenta]")
                break
            
            if not query:
                continue

            handle_query(query)

        except KeyboardInterrupt:
            console.print("\n[bold magenta]Goodbye![/bold magenta]")
            break
