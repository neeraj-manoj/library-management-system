-- Library Management System Database Setup
-- Run this file in MySQL to create the database and tables

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Books Table
CREATE TABLE IF NOT EXISTS Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200) NOT NULL,
    Author VARCHAR(100) NOT NULL,
    Publisher VARCHAR(100),
    Year INT,
    Quantity INT DEFAULT 1,
    Available INT DEFAULT 1
);

-- Members Table
CREATE TABLE IF NOT EXISTS Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    Email VARCHAR(100),
    JoinDate DATE DEFAULT (CURRENT_DATE)
);

-- Transactions Table (Issue/Return records)
CREATE TABLE IF NOT EXISTS Transactions (
    TransID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT NOT NULL,
    MemberID INT NOT NULL,
    IssueDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    Fine DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Database structure created successfully!
-- Run insert_sampledata.sql to add sample data (optional)
SELECT 'Database structure created!' AS Status;
