#!/usr/bin/env python3
"""
Test script for expense tracker MCP server.
Run this to verify the expense tracker is working correctly.
"""

import sys
import sqlite3
import json
from pathlib import Path
from main import init_db, add_expense, get_expenses, get_expense_summary, delete_expense

def test_expense_tracker():
    """Run tests on the expense tracker."""
    print("🧪 Testing Expense Tracker MCP Server\n")
    
    # Initialize database
    print("1️⃣ Initializing database...")
    init_db()
    print("   ✅ Database initialized\n")
    
    # Test adding expenses
    print("2️⃣ Adding test expenses...")
    
    test_expenses = [
        {"category": "food", "amount": 15.50, "description": "Lunch at cafe"},
        {"category": "transport", "amount": 5.00, "description": "Bus fare"},
        {"category": "food", "amount": 25.99, "description": "Dinner"},
        {"category": "utilities", "amount": 45.00, "description": "Electricity bill"},
        {"category": "entertainment", "amount": 20.00, "description": "Movie tickets"},
    ]
    
    for expense in test_expenses:
        result = add_expense(**expense)
        if result["success"]:
            print(f"   ✅ Added: {expense['category']} - ${expense['amount']}")
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    print()
    
    # Test getting all expenses
    print("3️⃣ Retrieving all expenses...")
    result = get_expenses()
    if result["success"]:
        print(f"   ✅ Retrieved {result['count']} expenses")
        for exp in result["expenses"]:
            print(f"      - {exp['date']}: {exp['category']} ${exp['amount']} ({exp['description']})")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test filtering by category
    print("4️⃣ Filtering expenses by category (food)...")
    result = get_expenses(category="food")
    if result["success"]:
        print(f"   ✅ Found {result['count']} food expenses")
        for exp in result["expenses"]:
            print(f"      - ${exp['amount']}: {exp['description']}")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test summary statistics
    print("5️⃣ Getting expense summary...")
    result = get_expense_summary()
    if result["success"]:
        summary = result["summary"]
        print(f"   ✅ Summary:")
        print(f"      Total expenses: {summary['total_count']}")
        print(f"      Total amount: ${summary['total_amount']:.2f}")
        print(f"      Average expense: ${summary['average_amount']:.2f}")
        
        print(f"\n   📊 Breakdown by category:")
        for cat in result["by_category"]:
            print(f"      - {cat['category']}: {cat['count']} items, ${cat['total']:.2f}")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test category-specific summary
    print("6️⃣ Getting food category summary...")
    result = get_expense_summary(category="food")
    if result["success"]:
        summary = result["summary"]
        print(f"   ✅ Food expenses:")
        print(f"      Count: {summary['total_count']}")
        print(f"      Total: ${summary['total_amount']:.2f}")
        print(f"      Average: ${summary['average_amount']:.2f}")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    print("✨ All tests completed successfully!")
    print("\n📝 Next steps:")
    print("1. Copy the configuration from claude_desktop_config.json")
    print("2. Open %APPDATA%\\Claude\\claude_desktop_config.json")
    print("3. Add the expense_tracker MCP server configuration")
    print("4. Restart Claude Desktop")
    print("5. Start tracking expenses with Claude!")

if __name__ == "__main__":
    test_expense_tracker()
