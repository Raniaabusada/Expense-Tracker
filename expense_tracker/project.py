import sqlite3
import datetime

DB_FILE = "expenses.db"

def create_database():
    """Creates the SQLite database and table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        category TEXT NOT NULL,
                        amount REAL NOT NULL
                      )''')
    conn.commit()
    conn.close()

def main():
    """Main function that provides a menu for the expense tracker."""
    create_database()

    while True:
        print("\nExpense Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Get Summary")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            get_summary()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def add_transaction():
    """Adds a new transaction to the SQLite database."""
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (Food, Rent, Transport, etc.): ")
    amount = float(input("Enter amount: "))

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
    conn.commit()
    conn.close()

    print("Transaction added successfully.")

def view_transactions():
    """Displays all transactions from the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    print("\nTransactions:")
    for row in rows:
        print(f"Date: {row[0]}, Category: {row[1]}, Amount: ${row[2]:.2f}")

def get_summary():
    """Generates a summary of total expenses and category-wise spending."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Total Expenses
    cursor.execute("SELECT SUM(amount) FROM transactions")
    total_spent = cursor.fetchone()[0] or 0

    # Category Breakdown
    cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
    category_summary = cursor.fetchall()
    
    conn.close()

    print(f"\nTotal Expenses: ${total_spent:.2f}")
    print("Category Breakdown:")
    for category, amount in category_summary:
        print(f"{category}: ${amount:.2f}")

if __name__ == "__main__":
    main()
