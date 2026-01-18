# Library Management System
# CBSE Class 12 Computer Science Project

import mysql.connector
import csv
from datetime import datetime, timedelta
from config import DB_CONFIG

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None


# ============================================================
# BOOK MANAGEMENT FUNCTIONS
# ============================================================

def add_book():
    """Add a new book to the library"""
    print("\n--- Add New Book ---")
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    publisher = input("Enter Publisher: ")
    year = input("Enter Publication Year: ")
    quantity = input("Enter Quantity: ")

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = """INSERT INTO Books (Title, Author, Publisher, Year, Quantity, Available)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (title, author, publisher, year, quantity, quantity))
        conn.commit()
        print(f"\n✓ Book '{title}' added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def view_books():
    """Display all books in the library"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT BookID, Title, Author, Quantity, Available FROM Books")
        books = cursor.fetchall()

        if not books:
            print("\nNo books in the library.")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Total':<8} {'Available':<8}")
        print("=" * 80)

        for book in books:
            print(f"{book[0]:<5} {book[1]:<30} {book[2]:<20} {book[3]:<8} {book[4]:<8}")

        print("=" * 80)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def search_book():
    """Search for a book by title or author"""
    print("\n--- Search Book ---")
    keyword = input("Enter title or author to search: ")

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = """SELECT BookID, Title, Author, Available
                   FROM Books
                   WHERE Title LIKE %s OR Author LIKE %s"""
        search_term = f"%{keyword}%"
        cursor.execute(query, (search_term, search_term))
        books = cursor.fetchall()

        if not books:
            print(f"\nNo books found matching '{keyword}'")
            return

        print("\n" + "-" * 60)
        print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'Available':<8}")
        print("-" * 60)

        for book in books:
            status = "Yes" if book[3] > 0 else "No"
            print(f"{book[0]:<5} {book[1]:<25} {book[2]:<20} {status:<8}")

        print("-" * 60)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def delete_book():
    """Delete a book from the library"""
    view_books()
    book_id = input("\nEnter Book ID to delete: ")

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Check if book has active issues
        cursor.execute("""SELECT COUNT(*) FROM Transactions
                         WHERE BookID = %s AND ReturnDate IS NULL""", (book_id,))
        active = cursor.fetchone()[0]

        if active > 0:
            print("\n✗ Cannot delete! This book is currently issued.")
            return

        cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("\n✓ Book deleted successfully!")
        else:
            print("\n✗ Book not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


# ============================================================
# MEMBER MANAGEMENT FUNCTIONS
# ============================================================

def add_member():
    """Add a new library member"""
    print("\n--- Add New Member ---")
    name = input("Enter Member Name: ")
    phone = input("Enter Phone Number: ")
    email = input("Enter Email: ")

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = "INSERT INTO Members (Name, Phone, Email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, phone, email))
        conn.commit()
        print(f"\n✓ Member '{name}' added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def view_members():
    """Display all library members"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MemberID, Name, Phone, JoinDate FROM Members")
        members = cursor.fetchall()

        if not members:
            print("\nNo members registered.")
            return

        print("\n" + "=" * 60)
        print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Join Date':<12}")
        print("=" * 60)

        for member in members:
            join_date = member[3].strftime('%Y-%m-%d') if member[3] else 'N/A'
            print(f"{member[0]:<5} {member[1]:<25} {member[2]:<15} {join_date:<12}")

        print("=" * 60)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


# ============================================================
# ISSUE AND RETURN FUNCTIONS
# ============================================================

def issue_book():
    """Issue a book to a member"""
    print("\n--- Issue Book ---")

    # Show available books
    view_books()
    book_id = input("\nEnter Book ID to issue: ")

    # Show members
    view_members()
    member_id = input("\nEnter Member ID: ")

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Check book availability
        cursor.execute("SELECT Title, Available FROM Books WHERE BookID = %s", (book_id,))
        book = cursor.fetchone()

        if book is None:
            print("\n✗ Book not found!")
            return

        if book[1] <= 0:
            print(f"\n✗ Sorry! '{book[0]}' is not available.")
            return

        # Check if member exists
        cursor.execute("SELECT Name FROM Members WHERE MemberID = %s", (member_id,))
        member = cursor.fetchone()

        if member is None:
            print("\n✗ Member not found!")
            return

        # Issue the book
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=14)  # 14 days loan period

        # Insert transaction
        cursor.execute("""INSERT INTO Transactions (BookID, MemberID, IssueDate, DueDate)
                         VALUES (%s, %s, %s, %s)""", (book_id, member_id, issue_date, due_date))

        # Update book availability
        cursor.execute("UPDATE Books SET Available = Available - 1 WHERE BookID = %s", (book_id,))

        conn.commit()

        print(f"\n✓ Book '{book[0]}' issued to {member[0]}")
        print(f"  Issue Date: {issue_date}")
        print(f"  Due Date: {due_date}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def return_book():
    """Return a book and calculate fine if overdue"""
    print("\n--- Return Book ---")

    # Show currently issued books
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Show issued books
        cursor.execute("""
            SELECT t.TransID, b.Title, m.Name, t.IssueDate, t.DueDate
            FROM Transactions t
            JOIN Books b ON t.BookID = b.BookID
            JOIN Members m ON t.MemberID = m.MemberID
            WHERE t.ReturnDate IS NULL
        """)
        issued = cursor.fetchall()

        if not issued:
            print("\nNo books are currently issued.")
            return

        print("\n" + "-" * 80)
        print(f"{'TransID':<8} {'Book':<25} {'Member':<20} {'Issue Date':<12} {'Due Date':<12}")
        print("-" * 80)

        for record in issued:
            print(f"{record[0]:<8} {record[1]:<25} {record[2]:<20} {record[3]} {record[4]}")

        print("-" * 80)

        trans_id = input("\nEnter Transaction ID to return: ")

        # Get transaction details
        cursor.execute("""SELECT BookID, DueDate FROM Transactions
                         WHERE TransID = %s AND ReturnDate IS NULL""", (trans_id,))
        trans = cursor.fetchone()

        if trans is None:
            print("\n✗ Invalid Transaction ID or book already returned.")
            return

        book_id = trans[0]
        due_date = trans[1]
        return_date = datetime.now().date()

        # Calculate fine (Rs. 2 per day if overdue)
        fine = 0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * 2  # Rs. 2 per day
            print(f"\n⚠ Book is {days_late} days overdue!")
            print(f"  Fine: Rs. {fine}")

        # Update transaction
        cursor.execute("""UPDATE Transactions
                         SET ReturnDate = %s, Fine = %s
                         WHERE TransID = %s""", (return_date, fine, trans_id))

        # Update book availability
        cursor.execute("UPDATE Books SET Available = Available + 1 WHERE BookID = %s", (book_id,))

        conn.commit()
        print("\n✓ Book returned successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def view_issued_books():
    """View all currently issued books"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.Title, m.Name, t.IssueDate, t.DueDate
            FROM Transactions t
            JOIN Books b ON t.BookID = b.BookID
            JOIN Members m ON t.MemberID = m.MemberID
            WHERE t.ReturnDate IS NULL
            ORDER BY t.DueDate
        """)
        issued = cursor.fetchall()

        if not issued:
            print("\nNo books are currently issued.")
            return

        print("\n" + "=" * 75)
        print(f"{'Book Title':<25} {'Issued To':<20} {'Issue Date':<12} {'Due Date':<12}")
        print("=" * 75)

        today = datetime.now().date()
        for record in issued:
            due = record[3]
            status = " (OVERDUE)" if due < today else ""
            print(f"{record[0]:<25} {record[1]:<20} {record[2]} {due}{status}")

        print("=" * 75)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


# ============================================================
# REPORTS
# ============================================================

def view_overdue_books():
    """View all overdue books"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        today = datetime.now().date()

        cursor.execute("""
            SELECT b.Title, m.Name, m.Phone, t.DueDate
            FROM Transactions t
            JOIN Books b ON t.BookID = b.BookID
            JOIN Members m ON t.MemberID = m.MemberID
            WHERE t.ReturnDate IS NULL AND t.DueDate < %s
            ORDER BY t.DueDate
        """, (today,))
        overdue = cursor.fetchall()

        if not overdue:
            print("\n✓ No overdue books!")
            return

        print("\n" + "=" * 75)
        print("OVERDUE BOOKS")
        print("=" * 75)
        print(f"{'Book':<25} {'Member':<20} {'Phone':<15} {'Due Date':<12}")
        print("-" * 75)

        for record in overdue:
            days_late = (today - record[3]).days
            print(f"{record[0]:<25} {record[1]:<20} {record[2]:<15} {record[3]} ({days_late} days)")

        print("=" * 75)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


# ============================================================
# FILE HANDLING - CSV EXPORT
# ============================================================

def export_books_to_csv():
    """Export all books to a CSV file"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT BookID, Title, Author, Publisher, Year, Quantity, Available FROM Books")
        books = cursor.fetchall()

        if not books:
            print("\nNo books to export.")
            return

        filename = "books_report.csv"

        # Open file and write data
        file = open(filename, 'w', newline='')
        writer = csv.writer(file)

        # Write header row
        writer.writerow(['BookID', 'Title', 'Author', 'Publisher', 'Year', 'Quantity', 'Available'])

        # Write data rows
        for book in books:
            writer.writerow(book)

        file.close()

        print(f"\n✓ Books exported to '{filename}' successfully!")
        print(f"  Total records: {len(books)}")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except IOError as err:
        print(f"File Error: {err}")
    finally:
        cursor.close()
        conn.close()


def export_members_to_csv():
    """Export all members to a CSV file"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MemberID, Name, Phone, Email, JoinDate FROM Members")
        members = cursor.fetchall()

        if not members:
            print("\nNo members to export.")
            return

        filename = "members_report.csv"

        # Open file and write data
        file = open(filename, 'w', newline='')
        writer = csv.writer(file)

        # Write header row
        writer.writerow(['MemberID', 'Name', 'Phone', 'Email', 'JoinDate'])

        # Write data rows
        for member in members:
            writer.writerow(member)

        file.close()

        print(f"\n✓ Members exported to '{filename}' successfully!")
        print(f"  Total records: {len(members)}")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except IOError as err:
        print(f"File Error: {err}")
    finally:
        cursor.close()
        conn.close()


# ============================================================
# MAIN MENU
# ============================================================

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 40)
    print("   LIBRARY MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Delete Book")
    print("-" * 40)
    print("5. Add Member")
    print("6. View All Members")
    print("-" * 40)
    print("7. Issue Book")
    print("8. Return Book")
    print("9. View Issued Books")
    print("10. View Overdue Books")
    print("-" * 40)
    print("11. Export Books to CSV")
    print("12. Export Members to CSV")
    print("-" * 40)
    print("0. Exit")
    print("=" * 40)


def main():
    """Main function - entry point"""
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            add_member()
        elif choice == '6':
            view_members()
        elif choice == '7':
            issue_book()
        elif choice == '8':
            return_book()
        elif choice == '9':
            view_issued_books()
        elif choice == '10':
            view_overdue_books()
        elif choice == '11':
            export_books_to_csv()
        elif choice == '12':
            export_members_to_csv()
        elif choice == '0':
            print("\nThank you for using Library Management System!")
            print("Goodbye!")
            break
        else:
            print("\n✗ Invalid choice! Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
