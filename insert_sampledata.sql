-- Library Management System - Sample Data
-- Run this file AFTER setup_database.sql to add sample data
-- This is OPTIONAL - only for testing/demo purposes

USE library_db;

-- ============================================================
-- SAMPLE BOOKS (15 Books)
-- ============================================================

INSERT INTO Books (Title, Author, Publisher, Year, Quantity, Available) VALUES
-- Classic Literature
('The Alchemist', 'Paulo Coelho', 'HarperCollins', 1988, 3, 3),
('To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott', 1960, 2, 2),
('1984', 'George Orwell', 'Secker & Warburg', 1949, 3, 3),
('Pride and Prejudice', 'Jane Austen', 'T. Egerton', 1813, 2, 2),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 2, 2),

-- Indian Authors
('Wings of Fire', 'APJ Abdul Kalam', 'Universities Press', 1999, 4, 4),
('The God of Small Things', 'Arundhati Roy', 'IndiaInk', 1997, 2, 2),
('Train to Pakistan', 'Khushwant Singh', 'Chatto & Windus', 1956, 2, 2),

-- Science & Technology
('A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 1988, 2, 2),
('The Origin of Species', 'Charles Darwin', 'John Murray', 1859, 1, 1),

-- Modern Fiction
('Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Bloomsbury', 1997, 5, 5),
('The Hunger Games', 'Suzanne Collins', 'Scholastic', 2008, 3, 3),
('The Da Vinci Code', 'Dan Brown', 'Doubleday', 2003, 2, 2),

-- Self-Help
('Atomic Habits', 'James Clear', 'Avery', 2018, 3, 3),
('Rich Dad Poor Dad', 'Robert Kiyosaki', 'Warner Books', 1997, 2, 2);


-- ============================================================
-- SAMPLE MEMBERS (8 Members)
-- ============================================================

INSERT INTO Members (Name, Phone, Email) VALUES
('Rahul Sharma', '9876543210', 'rahul.sharma@email.com'),
('Priya Singh', '9876543211', 'priya.singh@email.com'),
('Amit Kumar', '9876543212', 'amit.kumar@email.com'),
('Sneha Patel', '9876543213', 'sneha.patel@email.com'),
('Vikram Reddy', '9876543214', 'vikram.reddy@email.com'),
('Ananya Gupta', '9876543215', 'ananya.gupta@email.com'),
('Rohan Mehta', '9876543216', 'rohan.mehta@email.com'),
('Kavya Nair', '9876543217', 'kavya.nair@email.com');


-- ============================================================
-- SAMPLE TRANSACTIONS (For demo - some overdue)
-- ============================================================

-- Issue some books (these will be currently issued - not returned)
INSERT INTO Transactions (BookID, MemberID, IssueDate, DueDate) VALUES
(1, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), DATE_ADD(DATE_SUB(CURDATE(), INTERVAL 10 DAY), INTERVAL 14 DAY)),
(3, 2, DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(DATE_SUB(CURDATE(), INTERVAL 5 DAY), INTERVAL 14 DAY)),
(6, 3, DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_ADD(DATE_SUB(CURDATE(), INTERVAL 20 DAY), INTERVAL 14 DAY)),
(11, 4, DATE_SUB(CURDATE(), INTERVAL 25 DAY), DATE_ADD(DATE_SUB(CURDATE(), INTERVAL 25 DAY), INTERVAL 14 DAY));

-- Update Available count for issued books
UPDATE Books SET Available = Available - 1 WHERE BookID IN (1, 3, 6, 11);

-- Some returned transactions (with fines for late returns)
INSERT INTO Transactions (BookID, MemberID, IssueDate, DueDate, ReturnDate, Fine) VALUES
(2, 5, DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 10 DAY), 12.00),
(4, 6, DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 6 DAY), DATE_SUB(CURDATE(), INTERVAL 7 DAY), 0.00);


SELECT 'Sample data inserted successfully!' AS Status;
SELECT CONCAT(COUNT(*), ' books added') AS Books FROM Books;
SELECT CONCAT(COUNT(*), ' members added') AS Members FROM Members;
SELECT CONCAT(COUNT(*), ' transactions added') AS Transactions FROM Transactions;
