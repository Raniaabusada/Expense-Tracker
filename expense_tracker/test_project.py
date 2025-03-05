import pytest
import sqlite3
from project import create_database, add_transaction, get_summary, DB_FILE

@pytest.fixture(scope="module")
def db_connection():
    """Fixture to provide a fresh database connection."""
    create_database()  
    conn = sqlite3.connect(DB_FILE)
    
    yield conn  
    
    conn.close()  

@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """Clear transactions before each test to ensure a clean database state."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")  
    cursor.execute("INSERT INTO transactions (date, category, amount) VALUES ('2024-02-25', 'Food', 12.50)")
    cursor.execute("INSERT INTO transactions (date, category, amount) VALUES ('2024-02-26', 'Transport', 5.00)")
    cursor.execute("INSERT INTO transactions (date, category, amount) VALUES ('2024-02-26', 'Food', 8.75)")
    conn.commit()
    conn.close()

def test_add_transaction(monkeypatch, db_connection):
    """Test adding a transaction by simulating user input."""
    
    user_inputs = iter(["2025-02-25", "Test Transaction", "50.00", "Food"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))  

    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count_before = cursor.fetchone()[0]

    add_transaction()  

    cursor.execute("SELECT COUNT(*) FROM transactions")
    count_after = cursor.fetchone()[0]

    assert count_after == count_before + 1  

def test_get_summary(capsys):
    """Test summary function output."""
    get_summary()
    captured = capsys.readouterr()
    assert "Total Expenses" in captured.out
    assert "Food" in captured.out
    assert "Transport" in captured.out
