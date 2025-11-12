import sqlite3

# -----------------------------
# 1️⃣ Connect to database
# -----------------------------
conn = sqlite3.connect('railway.db')
cursor = conn.cursor()

# -----------------------------
# 2️⃣ Create tables
# -----------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS trains (
    train_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    seats_available INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT NOT NULL,
    train_no INTEGER,
    FOREIGN KEY (train_no) REFERENCES trains(train_no)
)
''')

conn.commit()

# -----------------------------
# 3️⃣ Functions
# -----------------------------
def add_train():
    train_no = int(input("Enter train number: "))
    name = input("Enter train name: ")
    source = input("Enter source station: ")
    destination = input("Enter destination station: ")
    seats = int(input("Enter number of seats available: "))

    cursor.execute("INSERT INTO trains VALUES (?, ?, ?, ?, ?)", 
                   (train_no, name, source, destination, seats))
    conn.commit()
    print("✅ Train added successfully!\n")

def view_trains():
    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    print("\nAvailable Trains:")
    for t in trains:
        print(f"Train No: {t[0]}, Name: {t[1]}, From: {t[2]} → To: {t[3]}, Seats: {t[4]}")
    print()

def book_ticket():
    passenger_name = input("Enter passenger name: ")
    train_no = int(input("Enter train number to book: "))

    # Check seat availability
    cursor.execute("SELECT seats_available FROM trains WHERE train_no = ?", (train_no,))
    result = cursor.fetchone()
    if result is None:
        print("❌ Invalid train number!\n")
        return
    seats = result[0]

    if seats > 0:
        cursor.execute("INSERT INTO bookings (passenger_name, train_no) VALUES (?, ?)", 
                       (passenger_name, train_no))
        cursor.execute("UPDATE trains SET seats_available = seats_available - 1 WHERE train_no = ?", 
                       (train_no,))
        conn.commit()
        print("🎟️ Ticket booked successfully!\n")
    else:
        print("❌ No seats available!\n")

def view_bookings():
    cursor.execute('''
    SELECT b.booking_id, b.passenger_name, t.name, t.source, t.destination
    FROM bookings b JOIN trains t ON b.train_no = t.train_no
    ''')
    bookings = cursor.fetchall()
    print("\nAll Bookings:")
    for b in bookings:
        print(f"Booking ID: {b[0]}, Passenger: {b[1]}, Train: {b[2]} ({b[3]} → {b[4]})")
    print()

def cancel_booking():
    booking_id = int(input("Enter booking ID to cancel: "))

    # Find the train number for seat update
    cursor.execute("SELECT train_no FROM bookings WHERE booking_id = ?", (booking_id,))
    result = cursor.fetchone()
    if result is None:
        print("❌ Invalid booking ID!\n")
        return

    train_no = result[0]

    cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
    cursor.execute("UPDATE trains SET seats_available = seats_available + 1 WHERE train_no = ?", 
                   (train_no,))
    conn.commit()
    print("❎ Booking cancelled successfully!\n")

# -----------------------------
# 4️⃣ Menu System
# -----------------------------
def menu():
    while True:
        print("""
===== 🚆 RAILWAY MANAGEMENT SYSTEM =====
1. Add Train
2. View All Trains
3. Book Ticket
4. View All Bookings
5. Cancel Booking
6. Exit
""")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_train()
        elif choice == '2':
            view_trains()
        elif choice == '3':
            book_ticket()
        elif choice == '4':
            view_bookings()
        elif choice == '5':
            cancel_booking()
        elif choice == '6':
            print("👋 Exiting... Have a safe journey!")
            break
        else:
            print("❌ Invalid choice! Try again.\n")

# -----------------------------
# 5️⃣ Run Program
# -----------------------------
menu()

# Close the database
conn.close()
