# Day 6: Data Management

## Today's Goal
Implement robust data management features, allowing users to import, export, and manage their financial data.

## Learning Focus
- File I/O with different formats (CSV, JSON)
- Data serialization and deserialization
- User safety confirmations for destructive actions
- Working with file system paths and archives (zip)

## Fintech Concepts
- **Data Portability**: The ability for users to move their data between different services.
- **Data Backup & Recovery**: Ensuring data is safe and can be restored.
- **Data Integrity**: Maintaining the accuracy and consistency of data.

## Features to Build

### 1. Export Data
- Offer export options:
    - All transactions (CSV)
    - All transactions (JSON)
    - All budgets (CSV)
    - All budgets (JSON)
- Prompt the user for a destination folder to save the exported files.
- Files should be named with the current date (e.g., `transactions_2025-11-27.csv`).

### 2. Import Data
- Allow importing transactions from a CSV file.
- The CSV must have the correct columns (`date,type,category,description,amount`).
- The import should append to existing data, not overwrite.
- Provide clear feedback on how many transactions were imported.
- Handle potential errors in the CSV file gracefully (e.g., wrong number of columns, invalid amount).

### 3. Data Backup
- Create a single zip archive containing `transactions.txt` and `budgets.txt`.
- The backup file should be named with a timestamp (e.g., `finance_tracker_backup_20251127_103000.zip`).
- Save the backup to a `backups/` directory.

### 4. Reset Data
- Provide an option to completely wipe all transaction and budget data.
- This is a destructive action, so it requires a very clear confirmation prompt from the user (e.g., "Are you sure you want to delete all data? This cannot be undone. Type 'DELETE' to confirm.").
- If confirmed, empty `transactions.txt` and `budgets.txt`.

## Success Criteria

✅ Can export transactions to CSV and JSON.
✅ Can export budgets to CSV and JSON.
✅ Can import transactions from a CSV file.
✅ Can create a timestamped backup of all data.
✅ Can reset all data with a safety confirmation.
✅ All file operations are handled safely with error checking.
