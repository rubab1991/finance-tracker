import questionary
from rich.console import Console
import csv
import json
import os
import shutil
from datetime import datetime

console = Console()
TRANSACTION_FILE = "database/transactions.txt"
BUDGET_FILE = "database/budgets.txt"
BACKUP_DIR = "backups"

def export_data():
    """Exports financial data to user-specified format and location."""
    export_format = questionary.select(
        "Select export format:",
        choices=["CSV", "JSON"]
    ).ask()

    export_type = questionary.select(
        "What do you want to export?",
        choices=["Transactions", "Budgets", "Both"]
    ).ask()

    destination_folder = questionary.text(
        "Enter destination folder path (default: current directory):"
    ).ask()

    if not destination_folder:
        destination_folder = "."

    if not os.path.exists(destination_folder):
        console.print(f"[bold red]Error: Destination folder '{destination_folder}' does not exist.[/bold red]")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")

    def export_transactions(folder, fmt):
        try:
            with open(TRANSACTION_FILE, "r") as f_in:
                reader = csv.reader(f_in)
                transactions = list(reader)
            
            if not transactions:
                console.print("[yellow]No transactions to export.[/yellow]")
                return

            filename = os.path.join(folder, f"transactions_{date_str}.{fmt.lower()}")
            
            if fmt == "CSV":
                with open(filename, "w", newline="") as f_out:
                    writer = csv.writer(f_out)
                    writer.writerows(transactions)
            elif fmt == "JSON":
                json_data = []
                for t in transactions:
                    json_data.append({
                        "date": t[0], "type": t[1], "category": t[2],
                        "description": t[3], "amount": int(t[4])
                    })
                with open(filename, "w") as f_out:
                    json.dump(json_data, f_out, indent=4)

            console.print(f"[green]Transactions successfully exported to {filename}[/green]")
        except FileNotFoundError:
            console.print("[yellow]No transactions file found to export.[/yellow]")
        except Exception as e:
            console.print(f"[bold red]An error occurred during transaction export: {e}[/bold red]")


    def export_budgets(folder, fmt):
        try:
            with open(BUDGET_FILE, "r") as f_in:
                reader = csv.reader(f_in)
                budgets = list(reader)

            if not budgets:
                console.print("[yellow]No budgets to export.[/yellow]")
                return
                
            filename = os.path.join(folder, f"budgets_{date_str}.{fmt.lower()}")

            if fmt == "CSV":
                with open(filename, "w", newline="") as f_out:
                    writer = csv.writer(f_out)
                    writer.writerows(budgets)
            elif fmt == "JSON":
                json_data = [{"category": b[0], "amount": int(b[1])} for b in budgets]
                with open(filename, "w") as f_out:
                    json.dump(json_data, f_out, indent=4)
            
            console.print(f"[green]Budgets successfully exported to {filename}[/green]")
        except FileNotFoundError:
            console.print("[yellow]No budget file found to export.[/yellow]")
        except Exception as e:
            console.print(f"[bold red]An error occurred during budget export: {e}[/bold red]")


    if export_type == "Transactions" or export_type == "Both":
        export_transactions(destination_folder, export_format)
    
    if export_type == "Budgets" or export_type == "Both":
        export_budgets(destination_folder, export_format)


def import_data():
    """Imports transactions from a CSV file."""
    file_path = questionary.text("Enter the path to the CSV file to import:").ask()

    if not file_path or not os.path.exists(file_path):
        console.print("[bold red]Error: File not found.[/bold red]")
        return

    try:
        with open(file_path, "r") as f_in:
            reader = csv.reader(f_in)
            transactions_to_import = list(reader)

        if not transactions_to_import:
            console.print("[yellow]The selected file is empty.[/yellow]")
            return

        # Basic validation
        for row in transactions_to_import:
            if len(row) != 5:
                console.print(f"[bold red]Invalid row found: {row}. Each row must have 5 columns.[/bold red]")
                return
            # Could add more validation here (date format, amount is number, etc.)
        
        with open(TRANSACTION_FILE, "a", newline="") as f_out:
            writer = csv.writer(f_out)
            writer.writerows(transactions_to_import)
        
        console.print(f"[green]Successfully imported {len(transactions_to_import)} transactions.[/green]")

    except Exception as e:
        console.print(f"[bold red]An error occurred during import: {e}[/bold red]")


def backup_data():
    """Creates a timestamped zip backup of the data files."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename_base = os.path.join(BACKUP_DIR, f"finance_tracker_backup_{timestamp}")

    try:
        shutil.make_archive(backup_filename_base, 'zip', 'database')
        console.print(f"[green]Successfully created backup at {backup_filename_base}.zip[/green]")
    except Exception as e:
        console.print(f"[bold red]An error occurred during backup: {e}[/bold red]")


def reset_data():
    """Resets all transaction and budget data after confirmation."""
    console.print("[bold red]WARNING: This will delete all your financial data permanently.[/bold red]")
    confirmation = questionary.text(
        "To confirm, type 'DELETE' and press Enter:"
    ).ask()

    if confirmation == "DELETE":
        try:
            # Empty transactions.txt
            with open(TRANSACTION_FILE, "w") as f:
                pass 
            # Empty budgets.txt
            with open(BUDGET_FILE, "w") as f:
                pass
            console.print("[green]All data has been reset.[/green]")
        except Exception as e:
            console.print(f"[bold red]An error occurred during data reset: {e}[/bold red]")
    else:
        console.print("[yellow]Data reset cancelled.[/yellow]")
