few_shots = [
    {
        'Question': "How many items are currently in the inventory?",
        'SQLQuery': "SELECT SUM(quantity) FROM Inventory;",
        'SQLResult': "Result of the SQL query",
        'Answer': 'e.g., 542'
    },
    {
        'Question': "What is the price and brand of the item with itemId 'item-r7j4t5y4mbi0teuf'?",
        'SQLQuery': "SELECT price, brand FROM Items WHERE itemId = 'item-r7j4t5y4mbi0teuf';",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 200.00, Apple"
    },
    {
        'Question': "List all users who are admins.",
        'SQLQuery': "SELECT firstName, lastName, email FROM Users WHERE isAdmin = 1;",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., John Doe, admin@example.com"
    },
    {
        'Question': "How many sales transactions happened in May 2025?",
        'SQLQuery': "SELECT COUNT(*) FROM Transactions WHERE MONTH(date) = 5 AND YEAR(date) = 2025;",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 32"
    },
    {
        'Question': "What is the total revenue generated from all transactions?",
        'SQLQuery': "SELECT SUM(total) FROM Transactions;",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 15432.50"
    },
    {
        'Question': "What was the total quantity sold for item 'item-r7j4t5y4mbi0teuf'?",
        'SQLQuery': "SELECT SUM(quantity) FROM LedgerEntries WHERE itemId = 'item-r7j4t5y4mbi0teuf';",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 87"
    },
    {
        'Question': "Show the names and prices of all items sold in transaction 'txn123'.",
        'SQLQuery': """
SELECT i.name, le.priceSold 
FROM LedgerEntries le 
JOIN Items i ON le.itemId = i.itemId 
WHERE le.transactionId = 'txn123';
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., T-shirt, 19.99"
    },
    {
        'Question': "List all items with less than 10 left in inventory.",
        'SQLQuery': """
SELECT i.name, inv.quantity 
FROM Inventory inv 
JOIN Items i ON inv.itemId = i.itemId 
WHERE inv.quantity < 10;
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., Cap, 7"
    },
    {
        'Question': "What is the email of the user who made transaction 'txn101'?",
        'SQLQuery': """
SELECT u.email 
FROM Transactions t 
JOIN Users u ON t.userId = u.userId 
WHERE t.transactionId = 'txn101';
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., customer@example.com"
    },
    {
        'Question': "Which items have never been sold?",
        'SQLQuery': """
SELECT i.itemId, i.name 
FROM Items i 
LEFT JOIN LedgerEntries le ON i.itemId = le.itemId 
WHERE le.itemId IS NULL;
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., Mug"
    }
]