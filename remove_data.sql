-- Run this to clear all data from tables (keeps structure intact)
-- WARNING: This will DELETE all data!

USE library_db;

-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;

-- Clear all tables
TRUNCATE TABLE Transactions;
TRUNCATE TABLE Members;
TRUNCATE TABLE Books;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'All data removed!' AS Status;
SELECT 'Tables are now empty. Run insert_sampledata.sql to add data again.' AS Note;
