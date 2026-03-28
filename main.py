import sqlite3
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(name='expense_tracker')

# Database setup - use /tmp/ for cloud deployment, fallback to local for development
DB_PATH = os.getenv("DB_PATH", "/tmp/expenses.db")


def ensure_directories():
    """Ensure database directory exists."""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create database directory: {e}", file=sys.stderr)


def init_db():
    """Initialize SQLite database with expenses table."""
    try:
        ensure_directories()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized successfully at {DB_PATH}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}", file=sys.stderr)
        return False


@mcp.tool
def add_expense(category: str, amount: float, description: str = "", date: str = None) -> dict:
    """
    Add a new expense to the database.
    
    Args:
        category: Expense category (e.g., 'food', 'transport', 'utilities')
        amount: Amount spent
        description: Optional description of the expense
        date: Date of expense (YYYY-MM-DD format, defaults to today)
    
    Returns:
        Dictionary with expense details and ID
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    if amount <= 0:
        return {"success": False, "error": "Amount must be greater than 0"}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (category, amount, description, date)
            VALUES (?, ?, ?, ?)
        ''', (category, amount, description, date))
        
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        
        return {
            "success": True,
            "id": expense_id,
            "category": category,
            "amount": amount,
            "description": description,
            "date": date,
            "message": f"Expense added successfully with ID {expense_id}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool
def get_expenses(category: str = None, limit: int = 50) -> dict:
    """
    Retrieve expenses from the database.
    
    Args:
        category: Optional filter by category
        limit: Maximum number of results (default: 50)
    
    Returns:
        List of expenses
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT * FROM expenses 
                WHERE category = ? 
                ORDER BY date DESC 
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT * FROM expenses 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        expenses = [dict(row) for row in rows]
        conn.close()
        
        return {
            "success": True,
            "count": len(expenses),
            "expenses": expenses
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool
def get_expense_summary(category: str = None, start_date: str = None, end_date: str = None) -> dict:
    """
    Get summary statistics for expenses.
    
    Args:
        category: Optional filter by category
        start_date: Optional start date (YYYY-MM-DD)
        end_date: Optional end date (YYYY-MM-DD)
    
    Returns:
        Summary with total, count, and average
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = 'SELECT COUNT(*) as count, SUM(amount) as total, AVG(amount) as average FROM expenses WHERE 1=1'
        params = []
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        # Get breakdown by category
        category_query = 'SELECT category, COUNT(*) as count, SUM(amount) as total FROM expenses WHERE 1=1'
        category_params = []
        
        if start_date:
            category_query += ' AND date >= ?'
            category_params.append(start_date)
        if end_date:
            category_query += ' AND date <= ?'
            category_params.append(end_date)
        
        category_query += ' GROUP BY category'
        
        cursor.execute(category_query, category_params)
        categories = cursor.fetchall()
        
        conn.close()
        
        return {
            "success": True,
            "summary": {
                "total_count": result[0] or 0,
                "total_amount": result[1] or 0.0,
                "average_amount": result[2] or 0.0
            },
            "by_category": [
                {"category": cat[0], "count": cat[1], "total": cat[2]}
                for cat in categories
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool
def delete_expense(expense_id: int) -> dict:
    """
    Delete an expense by ID.
    
    Args:
        expense_id: ID of the expense to delete
    
    Returns:
        Success status
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"Expense {expense_id} deleted successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool
def generate_test_data() -> dict:
    """
    Generate sample test data in the database.
    
    Populates the database with a variety of test expenses across different
    categories to help with testing and demonstration purposes.
    
    Returns:
        Success status with count of expenses added
    """
    try:
        test_expenses = [
            {"category": "food", "amount": 15.50, "description": "Lunch at cafe"},
            {"category": "transport", "amount": 5.00, "description": "Bus fare"},
            {"category": "food", "amount": 25.99, "description": "Dinner"},
            {"category": "utilities", "amount": 45.00, "description": "Electricity bill"},
            {"category": "entertainment", "amount": 20.00, "description": "Movie tickets"},
            {"category": "groceries", "amount": 87.50, "description": "Weekly groceries"},
            {"category": "transport", "amount": 12.00, "description": "Uber ride"},
            {"category": "entertainment", "amount": 15.99, "description": "Concert ticket"},
        ]
        
        added_count = 0
        added_expenses = []
        
        for expense in test_expenses:
            result = add_expense(**expense)
            if result["success"]:
                added_count += 1
                added_expenses.append({
                    "id": result["id"],
                    "category": result["category"],
                    "amount": result["amount"],
                    "description": result["description"]
                })
        
        return {
            "success": True,
            "count": added_count,
            "message": f"Successfully generated {added_count} test expenses",
            "expenses": added_expenses
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# Initialize database on module startup (ensures schema is created for cloud)
# ============================================================================
init_db()


if __name__ == "__main__":
    mcp.run()
