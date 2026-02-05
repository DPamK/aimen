#!/usr/bin/env python3
"""Product management script."""

import sqlite3
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "project.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_product(name, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO products (name, description) VALUES (?, ?)",
        (name, description)
    )
    product_id = cursor.lastrowid
    
    # Log history
    cursor.execute(
        "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
        ("product", product_id, "created", name)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {"id": product_id, "name": name, "description": description},
        "message": f"Product created with ID {product_id}"
    }

def list_products(status=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if status:
        cursor.execute(
            "SELECT id, name, description, status, created_at FROM products WHERE status = ?",
            (status,)
        )
    else:
        cursor.execute("SELECT id, name, description, status, created_at FROM products")
    
    products = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4]
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()
    
    return {
        "success": True,
        "data": products,
        "message": f"Found {len(products)} product(s)"
    }

def update_product(product_id, status=None, name=None, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if status:
        updates.append("status = ?")
        params.append(status)
    if name:
        updates.append("name = ?")
        params.append(name)
    if description:
        updates.append("description = ?")
        params.append(description)
    
    if not updates:
        return {"success": False, "error": "No updates specified"}
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(product_id)
    
    cursor.execute(
        f"UPDATE products SET {', '.join(updates)} WHERE id = ?",
        params
    )
    
    # Log history
    if status:
        cursor.execute(
            "INSERT INTO history (entity_type, entity_id, action, new_value) VALUES (?, ?, ?, ?)",
            ("product", product_id, "status_changed", status)
        )
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"Product {product_id} updated"
    }

def main():
    parser = argparse.ArgumentParser(description="Product management")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new product")
    create_parser.add_argument("--name", required=True, help="Product name")
    create_parser.add_argument("--description", help="Product description")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List products")
    list_parser.add_argument("--status", help="Filter by status")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a product")
    update_parser.add_argument("--id", type=int, required=True, help="Product ID")
    update_parser.add_argument("--status", help="New status")
    update_parser.add_argument("--name", help="New name")
    update_parser.add_argument("--description", help="New description")
    
    args = parser.parse_args()
    
    try:
        if args.command == "create":
            result = create_product(args.name, args.description)
        elif args.command == "list":
            result = list_products(args.status)
        elif args.command == "update":
            result = update_product(args.id, args.status, args.name, args.description)
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
