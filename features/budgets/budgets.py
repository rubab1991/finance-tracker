import questionary
from rich.console import Console
from rich.table import Table
from rich.progress_bar import ProgressBar
import csv
from features.data.provider import get_budgets, get_monthly_spending

BUDGET_FILE = "database/budgets.txt"
BUDGET_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health"]

console = Console()

def set_budget():
    """Sets a monthly budget for a category."""
    try:
        category = questionary.select("Select category to budget:", choices=BUDGET_CATEGORIES).ask()
        if not category:
            return

        amount_str = questionary.text(f"Enter monthly budget for {category} (e.g., 500.00):").ask()
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            console.print("[bold red]Budget amount must be a positive number.[/bold red]")
            return

        # Read existing budgets
        budgets = get_budgets()

        # Update or add new budget
        budgets[category] = amount

        # Write all budgets back to file
        with open(BUDGET_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for cat, amt in budgets.items():
                writer.writerow([cat, amt])

        console.print(f"[bold green]Budget for {category} set to {amount / 100:.2f}[/bold green]")

    except (ValueError, TypeError):
        console.print("[bold red]Invalid amount. Please enter a valid number.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")


def view_budgets():
    """Displays budget status."""
    budgets = get_budgets()
    if not budgets:
        console.print("[bold yellow]No budgets set. Please set a budget first.[/bold yellow]")
        return

    spending = get_monthly_spending()

    table = Table(title="Budget Status")
    table.add_column("Category", style="cyan")
    table.add_column("Budget", justify="right", style="green")
    table.add_column("Spent", justify="right", style="yellow")
    table.add_column("Remaining", justify="right")
    table.add_column("Utilization", width=20)
    table.add_column("Status", justify="center")

    total_budget = 0
    total_spent = 0

    for category, budget_cents in budgets.items():
        budget = budget_cents / 100
        spent_cents = spending.get(category, 0)
        spent = spent_cents / 100
        remaining = budget - spent
        utilization = (spent / budget) * 100 if budget > 0 else 0

        status = ""
        color = ""
        if utilization < 70:
            status = "OK"
            color = "green"
        elif 70 <= utilization <= 100:
            status = "Warning"
            color = "yellow"
        else:
            status = "Over"
            color = "red"
            
        progress_bar = ProgressBar(total=100, completed=min(utilization, 100), width=15)

        table.add_row(
            category,
            f"{budget:.2f}",
            f"{spent:.2f}",
            f"[{'red' if remaining < 0 else 'green'}]{remaining:.2f}[/]",
            progress_bar,
            f"[{color}]{status}[/]",
        )
        total_budget += budget_cents
        total_spent += spent_cents
    
    console.print(table)

    total_remaining = total_budget - total_spent
    total_utilization = (total_spent / total_budget) * 100 if total_budget > 0 else 0
    
    console.print("\n[bold]Overall Budget Summary[/bold]")
    console.print(f"Total Budget: [green]{total_budget / 100:.2f}[/green]")
    console.print(f"Total Spent: [yellow]{total_spent / 100:.2f}[/yellow]")
    console.print(f"Total Remaining: {total_remaining / 100:.2f}")
    console.print(f"Overall Utilization: {total_utilization:.2f}%")
