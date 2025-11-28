import questionary
from rich.console import Console
import os

from features.transactions.transactions import add_expense, add_income, list_transactions, get_balance
from features.budgets.budgets import set_budget, view_budgets
from features.analytics.analytics import generate_financial_report
from features.smart_assistant.assistant import run_assistant
from features.data_management.data_manager import export_data, import_data, backup_data, reset_data

console = Console()

def main():
    """Main function to run the Personal Finance Tracker CLI."""
    console.print("[bold cyan]Welcome to your Personal Finance Tracker![/bold cyan]")

    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Expense",
                "Add Income",
                "List Transactions",
                "View Balance",
                "Set Budget",
                "View Budgets",
                "Generate Financial Report",
                "Smart Assistant",
                "Data Management",
                "Launch Web Dashboard",
                "Exit",
            ],
        ).ask()

        if choice == "Add Expense":
            add_expense()
        elif choice == "Add Income":
            add_income()
        elif choice == "List Transactions":
            filter_choice = questionary.select(
                "Filter transactions?",
                choices=["All", "Last 7 days", "Expenses only", "Income only", "Back"],
            ).ask()

            if filter_choice == "All":
                list_transactions()
            elif filter_choice == "Last 7 days":
                list_transactions(filter_days=7)
            elif filter_choice == "Expenses only":
                list_transactions(filter_type="expense")
            elif filter_choice == "Income only":
                list_transactions(filter_type="income")
            elif filter_choice == "Back":
                continue

        elif choice == "View Balance":
            get_balance()
        elif choice == "Set Budget":
            set_budget()
        elif choice == "View Budgets":
            view_budgets()
        elif choice == "Generate Financial Report":
            generate_financial_report()
        elif choice == "Smart Assistant":
            run_assistant()
        elif choice == "Data Management":
            data_choice = questionary.select(
                "Data Management Options:",
                choices=["Export Data", "Import Data", "Backup Data", "Reset Data", "Back"],
            ).ask()

            if data_choice == "Export Data":
                export_data()
            elif data_choice == "Import Data":
                import_data()
            elif data_choice == "Backup Data":
                backup_data()
            elif data_choice == "Reset Data":
                reset_data()
            elif data_choice == "Back":
                continue
        elif choice == "Launch Web Dashboard":
            console.print("[bold green]Launching dashboard...[/bold green]")
            os.system("streamlit run dashboard.py")
        elif choice == "Exit":
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break

if __name__ == "__main__":
    main()
