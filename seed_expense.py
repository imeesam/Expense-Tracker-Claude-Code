"""
Seed script to add realistic dummy expenses for a specific user.
Usage: python seed_expense.py <user_id> <count> <months>
Example: python seed_expense.py 1 50 6
"""
import sqlite3
import random
from datetime import datetime, timedelta
from database.db import get_db


# Category definitions with Indian context
CATEGORIES = {
    "Food": {"min": 50, "max": 800, "weight": 25, "descriptions": [
        "Lunch at office canteen", "Dinner at local restaurant", "Street food",
        "Groceries from weekly market", "Biryani from Paradise", "Chai and snacks",
        "Family dinner at hotel", "Tiffin service", "Pizza delivery", "Dosa at Udupi",
        "North Indian thali", "South Indian meal", "Fast food order", "Coffee at cafe",
        "Ice cream and desserts", "Breakfast at home", "Lunch box", "Evening snacks"
    ]},
    "Transport": {"min": 20, "max": 500, "weight": 15, "descriptions": [
        "Uber ride to office", "Auto fare to market", "Metro card recharge",
        "Bus pass monthly", "Fuel at petrol pump", "Ola cab to airport",
        "Local train ticket", "Bike service", "Taxi to railway station",
        "Rapido bike ride", "Car service and maintenance", "Parking fees",
        "Toll charges", "E-rickshaw fare", "Cycle repair"
    ]},
    "Bills": {"min": 200, "max": 3000, "weight": 12, "descriptions": [
        "Electricity bill payment", "Mobile recharge Airtel", "Jio postpaid bill",
        "Internet broadband bill", "DTH recharge Tata Sky", "Water bill",
        "Cooking gas cylinder", "House rent", "Maintenance charges",
        "Property tax", "Insurance premium", "Loan EMI"
    ]},
    "Health": {"min": 100, "max": 2000, "weight": 8, "descriptions": [
        "Medicine from pharmacy", "Doctor consultation fee", "Health checkup",
        "Gym membership monthly", "Yoga classes", "Physiotherapy session",
        "Blood test lab charges", "Dental cleaning", "Eye checkup and glasses",
        "Vitamin supplements", "First aid supplies", "Ayurvedic medicine"
    ]},
    "Entertainment": {"min": 100, "max": 1500, "weight": 10, "descriptions": [
        "Movie tickets PVR", "Netflix subscription", "Amazon Prime membership",
        "Cricket match tickets", "Concert entry pass", "Gaming cafe bill",
        "Book purchase", "Music streaming Spotify", "Weekend trip",
        "Amusement park visit", "Bowling alley", "Escape room experience"
    ]},
    "Shopping": {"min": 200, "max": 5000, "weight": 15, "descriptions": [
        "New kurta from Manyavar", "Jeans from Westside", "Saree from Nalli",
        "Shoes from Bata", "Watch from Titan showroom", "Mobile accessories",
        "Home decor items", "Kitchen utensils", "Bedding set", "School uniform",
        "Birthday gift", "Furniture from IKEA", "Electronics from Croma",
        "Jewellery from Kalyan", "Handbag from Tanishq"
    ]},
    "Other": {"min": 50, "max": 1000, "weight": 10, "descriptions": [
        "Donation to temple", "Gift for wedding", "Stationery items",
        "Newspaper subscription", "Magazine purchase", "Photocopy and printing",
        "Tailoring charges", "Shoe repair", "Key duplication",
        "Pet grooming", "Plant nursery purchase", "Hardware store items"
    ]}
}


def parse_arguments():
    """Parse command line arguments."""
    import sys

    if len(sys.argv) != 4:
        print("Usage: python seed_expense.py <user_id> <count> <months>")
        print("Example: python seed_expense.py 1 50 6")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
        count = int(sys.argv[2])
        months = int(sys.argv[3])
        return user_id, count, months
    except ValueError:
        print("Usage: python seed_expense.py <user_id> <count> <months>")
        print("Example: python seed_expense.py 1 50 6")
        print("Error: All arguments must be valid integers.")
        sys.exit(1)


def verify_user_exists(user_id):
    """Verify that the user exists in the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        print(f"No user found with id {user_id}.")
        sys.exit(1)

    return result["name"]


def generate_expenses(user_id, count, months):
    """Generate a list of expense records."""
    expenses = []

    # Build weighted category list for proportional distribution
    category_list = []
    for category, config in CATEGORIES.items():
        category_list.extend([category] * config["weight"])

    now = datetime.now()

    for _ in range(count):
        # Random date within the past 'months' months
        days_ago = random.randint(0, months * 30)
        expense_date = now - timedelta(days=days_ago)
        date_str = expense_date.strftime("%Y-%m-%d")

        # Select category based on weights
        category = random.choice(category_list)
        config = CATEGORIES[category]

        # Generate amount within category range
        amount = round(random.uniform(config["min"], config["max"]), 2)

        # Select random description
        description = random.choice(config["descriptions"])

        expenses.append((user_id, amount, category, date_str, description))

    return expenses


def insert_expenses(expenses):
    """Insert all expenses in a single transaction."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        for expense in expenses:
            cursor.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                expense
            )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        return False
    finally:
        conn.close()


def main():
    # Step 1: Parse arguments
    user_id, count, months = parse_arguments()

    # Step 2: Verify user exists
    user_name = verify_user_exists(user_id)
    print(f"Found user: {user_name} (ID: {user_id})")

    # Step 3: Generate expenses
    expenses = generate_expenses(user_id, count, months)

    # Calculate date range
    now = datetime.now()
    earliest_date = now - timedelta(days=months * 30)

    # Insert expenses
    if insert_expenses(expenses):
        print(f"\nSuccessfully inserted {count} expenses for user {user_id}")
        print(f"Date range: {earliest_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")

        # Step 4: Show sample of inserted records
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, amount, category, date, description FROM expenses WHERE user_id = ? ORDER BY RANDOM() LIMIT 5",
            (user_id,)
        )
        sample = cursor.fetchall()
        conn.close()

        print("\nSample of 5 inserted expenses:")
        print("-" * 80)
        for row in sample:
            print(f"  ID: {row['id']}, Rs.{row['amount']:.2f}, {row['category']}, {row['date']}, '{row['description']}'")
        print("-" * 80)
    else:
        print("Failed to insert expenses. Transaction rolled back.")


if __name__ == "__main__":
    main()
