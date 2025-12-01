import sqlite3
from typing import Optional, Dict, List, Any

DB_PATH = "/content/support.db"

def get_db_connection():
    """Create a database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert SQLite row to dictionary."""
    return {key: row[key] for key in row.keys()}


# ============================================================
# REQUIRED MCP TOOL 1 — GET CUSTOMER
# ============================================================

def get_customer(customer_id: int) -> Dict[str, Any]:
    """Fetch customer by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        row = cur.fetchone()
        conn.close()

        if row:
            return {"success": True, "customer": row_to_dict(row)}
        else:
            return {"success": False, "error": f"Customer {customer_id} not found"}

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}


# ============================================================
# 🔹 REQUIRED MCP TOOL 2 — LIST CUSTOMERS
# ============================================================

def list_customers(status: Optional[str] = None, limit: Optional[int] = 50) -> Dict[str, Any]:
    """List customers optionally filtered by status."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if status:
            if status not in ["active", "disabled"]:
                return {"success": False, "error": "Status must be 'active' or 'disabled'"}
            query = "SELECT * FROM customers WHERE status = ? ORDER BY id LIMIT ?"
            cur.execute(query, (status, limit))
        else:
            query = "SELECT * FROM customers ORDER BY id LIMIT ?"
            cur.execute(query, (limit,))

        rows = cur.fetchall()
        conn.close()

        customers = [row_to_dict(r) for r in rows]
        return {"success": True, "count": len(customers), "customers": customers}

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}


# ============================================================
# REQUIRED MCP TOOL 3 — UPDATE CUSTOMER
# ============================================================

def update_customer(customer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update customer fields using a dynamic dictionary.
    Allowed fields must match the customers table.
    """
    allowed_fields = {"name", "email", "phone", "status"}

    # Filter invalid keys
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        return {"success": False, "error": "No valid fields to update"}

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check existence
        cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not cur.fetchone():
            conn.close()
            return {"success": False, "error": f"Customer {customer_id} not found"}

        # Build dynamic update query
        fields = ", ".join([f"{k} = ?" for k in updates.keys()])
        params = list(updates.values()) + [customer_id]

        query = f"UPDATE customers SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        cur.execute(query, params)
        conn.commit()

        # Return updated customer
        cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        updated = cur.fetchone()
        conn.close()

        return {"success": True, "customer": row_to_dict(updated)}

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}


# ============================================================
# REQUIRED MCP TOOL 4 — CREATE TICKET
# ============================================================

def create_ticket(customer_id: int, issue: str, priority: str = "medium") -> Dict[str, Any]:
    """Create a ticket for a customer."""
    if priority not in ["low", "medium", "high"]:
        return {"success": False, "error": "Priority must be low, medium, or high"}

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check customer exists
        cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not cur.fetchone():
            conn.close()
            return {"success": False, "error": f"Customer {customer_id} not found"}

        cur.execute("""
            INSERT INTO tickets (customer_id, issue, priority)
            VALUES (?, ?, ?)
        """, (customer_id, issue, priority))

        ticket_id = cur.lastrowid
        conn.commit()

        # Return created ticket
        cur.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cur.fetchone()
        conn.close()

        return {"success": True, "ticket": row_to_dict(row)}

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}


# ============================================================
# REQUIRED MCP TOOL 5 — GET CUSTOMER HISTORY
# ============================================================

def get_customer_history(customer_id: int) -> Dict[str, Any]:
    """Return all tickets for a given customer."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check customer exists
        cur.execute("SELECT id FROM customers WHERE id = ?", (customer_id,))
        if not cur.fetchone():
            conn.close()
            return {"success": False, "error": f"Customer {customer_id} not found"}

        # Fetch tickets
        cur.execute("SELECT * FROM tickets WHERE customer_id = ? ORDER BY created_at DESC", (customer_id,))
        rows = cur.fetchall()
        conn.close()

        history = [row_to_dict(r) for r in rows]
        return {"success": True, "count": len(history), "tickets": history}

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}
