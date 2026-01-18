# 📚 Library Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A comprehensive Library Management System built as a CBSE Class 12 Computer Science Project**

*Demonstrating practical application of Python programming with MySQL database integration*

</div>

---

## 📖 About The Project

This Library Management System is a command-line application designed to streamline library operations. It provides a complete solution for managing books, members, and book transactions with features like issue/return tracking, fine calculation, and report generation.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📕 **Book Management** | Add, view, search, and delete books from the library catalog |
| 👥 **Member Management** | Register and manage library members with contact details |
| 📤 **Book Issue** | Issue books to members with automatic due date calculation (14 days) |
| 📥 **Book Return** | Return books with automatic overdue fine calculation (₹2/day) |
| ⏰ **Overdue Tracking** | View all overdue books with member contact information |
| 📊 **CSV Export** | Export books and members data to CSV files for reporting |

---

## 🛠️ Technologies Used

- **Programming Language**: Python 3.x
- **Database**: MySQL 8.0
- **Database Connector**: mysql-connector-python
- **File Handling**: CSV module for data export

---

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x ([Download Python](https://www.python.org/downloads/))
- MySQL 8.0 or higher ([Download MySQL](https://dev.mysql.com/downloads/))
- mysql-connector-python package

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

### Step 2: Install Required Package

```bash
pip install mysql-connector-python
```

### Step 3: Configure Database Credentials

Open `config.py` and update with your MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",  # ← Change this
    "database": "library_db"
}
```

### Step 4: Setup the Database

Open MySQL Command Line or MySQL Workbench and run:

```sql
SOURCE path/to/setup_database.sql;
```

Or copy and paste the contents of `setup_database.sql` directly into MySQL.

### Step 5: Run the Application

```bash
python main.py
```

---

## 💻 Usage

When you run the application, you'll see a menu-driven interface:

```
========================================
   LIBRARY MANAGEMENT SYSTEM
========================================
1. Add Book
2. View All Books
3. Search Book
4. Delete Book
----------------------------------------
5. Add Member
6. View All Members
----------------------------------------
7. Issue Book
8. Return Book
9. View Issued Books
10. View Overdue Books
----------------------------------------
11. Export Books to CSV
12. Export Members to CSV
----------------------------------------
0. Exit
========================================
```

Simply enter the number corresponding to the operation you want to perform.

---

## 🗄️ Database Schema

### Entity-Relationship Diagram

```
┌─────────────┐         ┌───────────────┐         ┌─────────────┐
│   Books     │         │ Transactions  │         │  Members    │
├─────────────┤         ├───────────────┤         ├─────────────┤
│ BookID (PK) │◄────────┤ BookID (FK)   │         │ MemberID(PK)│
│ Title       │         │ MemberID (FK) │────────►│ Name        │
│ Author      │         │ TransID (PK)  │         │ Phone       │
│ Publisher   │         │ IssueDate     │         │ Email       │
│ Year        │         │ DueDate       │         │ JoinDate    │
│ Quantity    │         │ ReturnDate    │         └─────────────┘
│ Available   │         │ Fine          │
└─────────────┘         └───────────────┘
```

### Table Structures

<details>
<summary><b>📕 Books Table</b></summary>

| Column    | Type         | Description                    |
|-----------|--------------|--------------------------------|
| BookID    | INT (PK)     | Unique identifier for book     |
| Title     | VARCHAR(200) | Book title                     |
| Author    | VARCHAR(100) | Author name                    |
| Publisher | VARCHAR(100) | Publisher name                 |
| Year      | INT          | Publication year               |
| Quantity  | INT          | Total copies in library        |
| Available | INT          | Currently available copies     |

</details>

<details>
<summary><b>👥 Members Table</b></summary>

| Column   | Type         | Description                      |
|----------|--------------|----------------------------------|
| MemberID | INT (PK)     | Unique identifier for member     |
| Name     | VARCHAR(100) | Member's full name               |
| Phone    | VARCHAR(15)  | Contact phone number             |
| Email    | VARCHAR(100) | Email address                    |
| JoinDate | DATE         | Membership registration date     |

</details>

<details>
<summary><b>📋 Transactions Table</b></summary>

| Column     | Type          | Description                        |
|------------|---------------|------------------------------------|
| TransID    | INT (PK)      | Unique transaction identifier      |
| BookID     | INT (FK)      | Reference to issued book           |
| MemberID   | INT (FK)      | Reference to member                |
| IssueDate  | DATE          | Date when book was issued          |
| DueDate    | DATE          | Expected return date (14 days)     |
| ReturnDate | DATE          | Actual return date (NULL if not)   |
| Fine       | DECIMAL(10,2) | Fine amount for late return        |

</details>

---

## 📸 Sample Output

```
================================================================================
ID    Title                          Author               Total    Available
================================================================================
1     The Alchemist                  Paulo Coelho         3        3
2     To Kill a Mockingbird          Harper Lee           2        2
3     1984                           George Orwell        2        2
4     Pride and Prejudice            Jane Austen          2        2
5     The Great Gatsby               F. Scott Fitzgerald  1        1
================================================================================
```

---

## 📁 Project Structure

```
library-management-system/
│
├── main.py              # Main application file with all functions
├── config.py            # Database configuration settings
├── setup_database.sql   # SQL script to create database and tables
├── README.md            # Project documentation
├── LICENSE              # MIT License
└── .gitignore           # Git ignore file
```

---

## 🔮 Future Enhancements

- [ ] GUI implementation using Tkinter or CustomTkinter
- [ ] User authentication and role-based access
- [ ] Book reservation system
- [ ] Email notifications for due dates
- [ ] Barcode/QR code scanning for books
- [ ] Advanced search and filtering options
- [ ] Dashboard with statistics and analytics

---

## 📝 Learning Outcomes

Through this project, the following concepts were implemented:

1. **Python Programming**
   - Functions and modular programming
   - Exception handling (try-except blocks)
   - String formatting and manipulation
   - Date and time operations

2. **MySQL Database**
   - Database and table creation
   - CRUD operations (Create, Read, Update, Delete)
   - JOIN queries for relational data
   - Foreign key relationships

3. **Python-MySQL Integration**
   - Database connectivity using mysql-connector-python
   - Parameterized queries for security
   - Transaction management (commit/rollback)

4. **File Handling**
   - CSV file writing
   - Report generation

---

## 👨‍💻 Author

**Class 12 Computer Science Project**

*Submitted as part of CBSE Class 12 Computer Science curriculum*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- CBSE for the Computer Science curriculum
- Python and MySQL documentation
- Teachers and mentors for guidance

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

*Made with ❤️ for Class 12 Computer Science*

</div>
