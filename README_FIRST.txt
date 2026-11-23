SPENDWISE — EXPENSE TRACKER (WINDOWS QUICK START)
=================================================

FEATURES
- Add income and expenses with date, category, description and payment method.
- Dashboard for total income, total expenses and remaining balance.
- Expense category chart and income-vs-expense chart.
- Filter and review transactions.
- Delete an incorrect transaction.
- Download transaction records as CSV.
- Set a monthly budget and track spending against it.
- Records are saved locally in the project's data/transactions.csv file.

RUN THE APP
1. Extract the entire ZIP file to a normal folder, such as Desktop\SpendWise.
2. Install Python 3.10 or newer from https://www.python.org/downloads/
   Enable "Add Python to PATH" during installation if shown.
3. Open the extracted folder.
4. Double-click START_SPENDWISE.bat.
5. The first launch creates a virtual environment and installs the required packages.
   This needs an internet connection and may take a few minutes.
6. The app should open in your browser. If it does not, visit http://localhost:8501.

HOW TO USE
1. Open Add Transaction.
2. Choose Expense or Income.
3. Enter date, category, amount and description.
4. Click Save transaction.
5. View your totals and charts on Dashboard.
6. Open Budget to set a monthly spending limit.
7. Download a CSV backup from Transactions when needed.

DATA STORAGE
Your transaction records are stored on your own computer in:
data/transactions.csv
Do not delete this file if you want to keep your records. Download CSV backups regularly.
The monthly budget setting is held in the app session and may need to be entered again
after restarting the app.

TROUBLESHOOTING
- Python not recognized: install Python and enable Add Python to PATH.
- Browser did not open: visit http://localhost:8501 manually.
- Package install failed: check internet and run the BAT file again.
- Stop the app: focus the command window and press Ctrl+C.

PRIVACY AND SCOPE
- This app does not connect to a bank, payment provider or online account.
- Transaction data is saved locally in the project folder.
- This is a student project prototype, not accounting software or financial advice.
