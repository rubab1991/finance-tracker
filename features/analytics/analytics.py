from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from features.data.provider import get_transactions_for_month, get_budgets, calculate_monthly_summary

console = Console()


def create_pie_chart(data, title="Distribution"):
    """Generates an ASCII art pie chart."""
    if not data:
        return f"[bold yellow]No data for {title} pie chart.[/bold yellow]"

    total = sum(data.values())
    if total == 0:
        return f"[bold yellow]No data for {title} pie chart.[/bold yellow]"

    chart = []
    chart.append(f"[bold]{title}:[/bold]")
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)

    for item, amount in sorted_data:
        percentage = (amount / total) * 100
        # Scale to 20 characters for the bar
        bar_length = int(percentage / 5)
        bar = "█" * bar_length
        chart.append(f"{item.ljust(15)} {bar.ljust(20)} {percentage:.1f}%")
    return "\n".join(chart)


def generate_financial_report():
    """Generates a comprehensive financial report for the current month."""
    current_month_str = datetime.now().strftime("%Y-%m")
    previous_month_str = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    # Get data
    current_month_transactions = get_transactions_for_month(current_month_str)
    previous_month_transactions = get_transactions_for_month(previous_month_str)
    budgets = get_budgets()

    (current_income, current_expense, current_spending_by_category,
     current_income_by_source) = calculate_monthly_summary(current_month_transactions)

    (prev_income, prev_expense, prev_spending_by_category,
     prev_income_by_source) = calculate_monthly_summary(previous_month_transactions)

    console.print(Panel(f"[bold green]Financial Report for {datetime.now().strftime('%B %Y')}[/bold green]",
                        expand=False))

    # --- Income Summary ---
    console.print(Panel("[bold cyan]Income Summary[/bold cyan]", expand=False))
    console.print(f"Total Income this month: [green]{current_income / 100:.2f}[/green]")
    income_diff = current_income - prev_income
    income_trend = "[green]Up[/green]" if income_diff >= 0 else "[red]Down[/red]"
    console.print(f"Vs last month ({previous_month_str}): {income_diff / 100:.2f} ({income_trend})")
    
    if current_income_by_source:
        table = Table("Source", "Amount")
        for source, amount in current_income_by_source.items():
            table.add_row(source, f"{amount / 100:.2f}")
        console.print(table)


    # --- Expense Summary ---
    console.print(Panel("[bold cyan]Expense Summary[/bold cyan]", expand=False))
    console.print(f"Total Expenses this month: [red]{current_expense / 100:.2f}[/red]")
    expense_diff = current_expense - prev_expense
    expense_trend = "[red]Up[/red]" if expense_diff >= 0 else "[green]Down[/green]"
    console.print(f"Vs last month ({previous_month_str}): {expense_diff / 100:.2f} ({expense_trend})")

    avg_daily_expense = current_expense / datetime.now().day if datetime.now().day > 0 else 0
    console.print(f"Average daily expense: [yellow]{avg_daily_expense / 100:.2f}[/yellow]")
    
    console.print(create_pie_chart(current_spending_by_category, "Spending by Category"))

    # Top 3 spending categories
    if current_spending_by_category:
        top_spending = sorted(current_spending_by_category.items(), key=lambda item: item[1], reverse=True)[:3]
        console.print("\n[bold]Top 3 Spending Categories:[/bold]")
        for category, amount in top_spending:
            console.print(f"- {category}: {amount / 100:.2f}")

    # --- Budget Adherence ---
    console.print(Panel("[bold cyan]Budget Adherence[/bold cyan]", expand=False))
    budget_adherence_score_factor = 0
    over_budget_categories = []
    if budgets:
        for category, budgeted_amount in budgets.items():
            spent = current_spending_by_category.get(category, 0)
            if spent > budgeted_amount:
                over_budget_categories.append(category)
            
        if not over_budget_categories:
            console.print("[green]Excellent! You are within all your budgets.[/green]")
            budget_adherence_score_factor = 1 # Full points
        else:
            console.print(f"[red]Warning! You are over budget in: {', '.join(over_budget_categories)}[/red]")
            budget_adherence_score_factor = 0.5 # Partial points for being over in some

        console.print("[yellow]Review 'View Budgets' for detailed breakdown.[/yellow]")
    else:
        console.print("[yellow]No budgets set. Set budgets to track adherence.[/yellow]")


    # --- Savings Analysis ---
    console.print(Panel("[bold cyan]Savings Analysis[/bold cyan]", expand=False))
    monthly_savings = current_income - current_expense
    console.print(f"Monthly Savings: {monthly_savings / 100:.2f}")

    savings_rate = (monthly_savings / current_income) * 100 if current_income > 0 else 0
    console.print(f"Savings Rate: [green]{savings_rate:.2f}%[/green]")


    # --- Financial Health Score ---
    console.print(Panel("[bold cyan]Financial Health Score[/bold cyan]", expand=False))
    score = 0
    recommendations = []

    # Savings rate (30 points)
    if savings_rate >= 20:
        score += 30
    elif savings_rate >= 10:
        score += 15
    else:
        recommendations.append("Increase your savings rate. Aim for at least 10-20% of your income.")

    # Budget adherence (25 points)
    budget_adherence_points = budget_adherence_score_factor * 25
    score += budget_adherence_points
    if budget_adherence_score_factor < 1 and budgets:
        recommendations.append("Review your budget adherence and try to stick to your spending limits.")

    # Income vs expenses (25 points)
    if current_income > current_expense:
        score += 25
    else:
        recommendations.append("Your expenses are matching or exceeding your income. Look for ways to reduce spending or increase income.")

    console.print(f"[bold]Overall Financial Health Score: [cyan]{score:.0f}/100[/cyan][/bold]")
    
    if score >= 80:
        console.print("[green]Excellent! You have a strong financial standing.[/green]")
    elif score >= 50:
        console.print("[yellow]Good. There are areas for improvement, but you're on the right track.[/yellow]")
    else:
        console.print("[red]Needs Attention. Focus on the recommendations below to improve your financial health.[/red]")

    if recommendations:
        console.print("\n[bold]Recommendations:[/bold]")
        for rec in recommendations:
            console.print(f"- {rec}")
    else:
        console.print("\n[green]No specific recommendations at this time. Keep up the good work![/green]")