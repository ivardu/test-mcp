# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for managing expenses with SQLite database backend. Integrates seamlessly with Claude Desktop to help you track and analyze spending.

## Features

- **Add Expenses**: Record expenses with category, amount, description, and date
- **Query Expenses**: Retrieve expenses with optional filtering by category
- **Expense Summary**: Get detailed statistics and breakdown by category
- **Delete Expenses**: Remove expense entries
- **SQLite Storage**: Persistent local database

## Installation & Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Run the MCP Server

```bash
uv run fastmcp dev main.py
```

## Available Tools

### `add_expense`
Add a new expense to the database.

**Parameters:**
- `category` (string, required): Expense category (e.g., 'food', 'transport', 'utilities', 'entertainment')
- `amount` (float, required): Amount spent
- `description` (string, optional): Additional details
- `date` (string, optional): Date in YYYY-MM-DD format (defaults to today)

**Example:**
```json
{
  "category": "food",
  "amount": 15.50,
  "description": "Lunch at cafe",
  "date": "2026-03-27"
}
```

### `get_expenses`
Retrieve expenses from the database.

**Parameters:**
- `category` (string, optional): Filter by specific category
- `limit` (integer, optional): Maximum number of results (default: 50)

**Example:**
```json
{
  "category": "food",
  "limit": 10
}
```

### `get_expense_summary`
Get summary statistics for expenses.

**Parameters:**
- `category` (string, optional): Filter by specific category
- `start_date` (string, optional): Start date (YYYY-MM-DD)
- `end_date` (string, optional): End date (YYYY-MM-DD)

**Example:**
```json
{
  "start_date": "2026-03-01",
  "end_date": "2026-03-31"
}
```

### `delete_expense`
Delete an expense by ID.

**Parameters:**
- `expense_id` (integer, required): ID of the expense to delete

## Claude Desktop Integration

### Configuration

1. **Locate the config file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**

```json
{
  "mcpServers": {
    "expense_tracker": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "python",
        "D:\\Agentic AI\\Claude\\MCP\\main.py"
      ]
    }
  }
}
```

**Note for Windows users:** Use forward slashes (`/`) or double backslashes (`\\`) in the path.

3. **Restart Claude Desktop** to apply changes

### Usage with Claude Desktop

Once configured, you can:
- Ask Claude to add an expense: "Add a $20 grocery expense"
- Query your expenses: "Show me all my food expenses"
- Get summaries: "What's my total spending this month?"
- Analyze patterns: "Compare my spending by category"

## Database Schema

The SQLite database includes an `expenses` table with:
- `id`: Primary key (auto-increment)
- `category`: Expense category
- `amount`: Amount spent
- `description`: Optional description
- `date`: Date of expense (YYYY-MM-DD)
- `created_at`: Timestamp of database entry

## Example Usage with Claude

```
User: Add a $45.99 restaurant expense for dinner last night
Claude: [Uses add_expense tool to record the expense]

User: How much did I spend on food this month?
Claude: [Uses get_expense_summary to calculate totals]

User: Show me my top spending categories
Claude: [Analyzes the data and presents a breakdown]
```

## Troubleshooting

**MCP Server won't start:**
```bash
uv run fastmcp dev main.py
```

**Database errors:**
- Ensure the project directory is writable
- Delete `expenses.db` to reset the database

**Claude Desktop not connecting:**
1. Check the config path is correct
2. Verify the command path in `claude_desktop_config.json`
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for error messages

## License

MIT
