import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "data_explorer.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dataset_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER,
            row_data TEXT,
            FOREIGN KEY(dataset_id) REFERENCES datasets(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_dataset(name: str, description: str = None) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO datasets (name, description) VALUES (?, ?)",
        (name, description)
    )
    dataset_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return dataset_id

def insert_dataset_data(dataset_id: int, rows: list[dict]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    count = 0
    for row in rows:
        cursor.execute(
            "INSERT INTO dataset_data (dataset_id, row_data) VALUES (?, ?)",
            (dataset_id, json.dumps(row))
        )
        count += 1
    
    conn.commit()
    conn.close()
    return count
