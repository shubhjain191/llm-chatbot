import sqlite3
import os

DATABASE_PATH = "customers.db"

def create_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"Removed existing database: {DATABASE_PATH}")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female')),
            location TEXT NOT NULL
        )
    """)
    
    return conn, cursor

def sample_data(cursor, conn):
    sample_customers = [
        ("Sneh Jain", "Male", "Mumbai"),
        ("Smit Jain", "Male", "Mumbai"),
        ("Khushi Jain", "Female", "Germany"),
        ("Sejal Jain", "Female", "Pune"),
        ("Shubh Jain", "Male", "Mumbai"),
        ("Isha Jain", "Female", "Pune"),
        ("Sanskar Jain", "Male", "Pune"),
        ("Aayush Jain", "Male", "Singapore"),
        ("Disha Jain", "Female", "Indore"),
        ("Bhumi Jain", "Female", "Mumbai"),
    ]
    
    cursor.executemany(
        "INSERT INTO customers (name, gender, location) VALUES (?, ?, ?)",
        sample_customers
    )
    
    conn.commit()
    print(f"Inserted {len(sample_customers)} sample customers")

def display_sample_data(cursor):
    cursor.execute("SELECT * FROM customers ORDER BY customer_id")
    customers = cursor.fetchall()
    
    print("=== Customer Database Contents ===")
    print("----------------------------------------")
    print("ID  | Name                | Gender   | Location")
    print("----------------------------------------")
    
    for customer in customers:
        customer_id, name, gender, location = customer
        print(f"{customer_id:3d} | {name:20} | {gender:8} | {location:12}")
    
    print("----------------------------------------")
    print(f"Total Records: {len(customers)}")

def location_summary(cursor):
    cursor.execute("""
        SELECT location, COUNT(*) as count, 
               SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) as male_count,
               SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) as female_count
        FROM customers 
        GROUP BY location 
        ORDER BY count DESC
    """)
    
    locations = cursor.fetchall()
    

    print("=== Customer Location Report ===")
    print("----------------------------------------")
    print("Location     | Total | Male | Female")
    print("----------------------------------------")
    for location, total, male, female in locations:
        print(f"{location:<12} | {total:>5} | {male:>4} | {female:>6}")
    print("----------------------------------------")

def main():
    print("Initializing LLM Chatbot Database...")
    print("----------------------------------------")
    
    try:
        conn, cursor = create_database()
        
        sample_data(cursor, conn)
        
        display_sample_data(cursor)
        location_summary(cursor)
        
        conn.close()
        
        print(f"Database successfully created: {DATABASE_PATH}")
        print("You can now run the FastAPI server")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()