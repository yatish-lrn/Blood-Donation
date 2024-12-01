import sqlite3

# Database setup
def initialize_database():
    conn = sqlite3.connect("blood_donation.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            treatment_status TEXT NOT NULL,
            disease_status TEXT NOT NULL,
            alcohol_consumption TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add donor information
def add_donor():
    name = input("Enter donor's name: ")
    age = int(input("Enter donor's age: "))
    gender = input("Enter donor's gender (Male/Female/Other): ")
    blood_group = input("Enter donor's blood group: ")
    treatment_status = input("Has the donor received any treatment? (yes/no): ").strip().lower()
    disease_status = input("Does the donor have any diseases? (yes/no): ").strip().lower()
    alcohol_consumption = input("Has the donor consumed alcohol? (yes/no): ").strip().lower()

    if treatment_status == "yes" or disease_status == "yes" or alcohol_consumption == "yes":
        print(f"Donor {name} is **not eligible** to donate blood due to health restrictions.")
    else:
        conn = sqlite3.connect("blood_donation.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donors (name, age, gender, blood_group, treatment_status, disease_status, alcohol_consumption)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, blood_group, treatment_status, disease_status, alcohol_consumption))
        conn.commit()
        conn.close()
        print(f"Donor {name} has been successfully added and is eligible to donate blood.")

# Display eligible donors
def display_eligible_donors():
    conn = sqlite3.connect("blood_donation.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, age, gender, blood_group 
        FROM donors 
        WHERE treatment_status = 'no' AND disease_status = 'no' AND alcohol_consumption = 'no'
    """)
    donors = cursor.fetchall()
    conn.close()

    if donors:
        print("\nList of eligible donors:")
        print(f"{'Name':<20}{'Age':<5}{'Gender':<10}{'Blood Group':<10}")
        print("-" * 45)
        for donor in donors:
            print(f"{donor[0]:<20}{donor[1]:<5}{donor[2]:<10}{donor[3]:<10}")
    else:
        print("\nNo eligible donors found.")

# Main menu
def main():
    initialize_database()
    while True:
        print("\n--- Blood Donation Application ---")
        print("1. Add Donor Information")
        print("2. Display Eligible Donors")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_donor()
        elif choice == "2":
            display_eligible_donors()
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
