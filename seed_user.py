"""
Seed script to add a random Indian user to the database.
"""
import sqlite3
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

DATABASE_PATH = "spendly.db"


def get_db():
    """Opens a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Common Indian first names (mixed gender)
FIRST_NAMES = [
    # North Indian
    "Rahul", "Rohan", "Priya", "Neha", "Amit", "Deepak", "Sneha", "Pooja",
    "Rajesh", "Kavita", "Suresh", "Meera", "Vikram", "Anjali", "Manoj", "Ritu",
    # South Indian
    "Arjun", "Lakshmi", "Karthik", "Divya", "Venkat", "Swathi", "Ravi", "Anita",
    "Krishnan", "Meenakshi", "Balaji", "Ramya", "Srinivas", "Kavya", "Mohan", "Rekha",
    # East/West Indian
    "Sourav", "Rituparna", "Arijit", "Sunita", "Rahul", "Pranav", "Ankita", "Nilesh",
    "Prajakta", "Siddharth", "Rupali", "Ashwin", "Manisha", "Prasad", "Usha"
]

LAST_NAMES = [
    # Common North Indian
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Yadav", "Patel", "Reddy",
    "Malhotra", "Kapoor", "Chopra", "Bhatia", "Sethi", "Bansal", "Agarwal",
    # Common South Indian
    "Iyer", "Nair", "Menon", "Rao", "Naidu", "Reddy", "Pillai", "Krishnan",
    "Subramanian", "Venkatesh", "Hegde", "Kamath", "Shenoy", "Bhat",
    # Common East/West Indian
    "Banerjee", "Chatterjee", "Mukherjee", "Das", "Dutta", "Joshi", "Deshmukh",
    "Kulkarni", "Patil", "Shinde", "Jadhav", "Pawar", "Mehta", "Shah", "Desai"
]


def generate_indian_name():
    """Generate a random Indian name."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"


def generate_email_from_name(name):
    """Generate an email from the name with random 2-3 digit suffix."""
    first, last = name.lower().split(" ", 1)
    suffix = random.randint(10, 999)
    return f"{first}.{last}{suffix}@gmail.com"


def check_email_exists(email):
    """Check if an email already exists in the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def main():
    # Generate a unique user
    max_attempts = 100
    attempt = 0

    while attempt < max_attempts:
        name = generate_indian_name()
        email = generate_email_from_name(name)

        if not check_email_exists(email):
            break

        attempt += 1
    else:
        print(f"Failed to generate unique email after {max_attempts} attempts.")
        return

    # Hash the password
    password = "password123"
    password_hash = generate_password_hash(password)

    # Get current datetime
    created_at = datetime.now().isoformat()

    # Insert the user
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, created_at)
        )
        conn.commit()
        user_id = cursor.lastrowid
        print(f"User created successfully!")
        print(f"  id: {user_id}")
        print(f"  name: {name}")
        print(f"  email: {email}")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
