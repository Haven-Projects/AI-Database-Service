few_shots = [
    {
        'Question': "How many items are currently in the inventory?",
        'SQLQuery': "SELECT SUM(quantity) FROM inventory;",
        'SQLResult': "Result of the SQL query",
        'Answer': 'e.g., 542'
    },
    {
        'Question': "What is the price and brand of the item with itemId 'ITM123'?",
        'SQLQuery': "SELECT price, brand FROM items WHERE itemId = 'ITM123';",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 19.99, Nike"
    },
    {
        'Question': "List all users who are admins.",
        'SQLQuery': "SELECT firstName, lastName, email FROM users WHERE isAdmin = 1;",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., John Doe, admin@example.com"
    },
    {
        'Question': "How many sales transactions happened in May 2025?",
        'SQLQuery': "SELECT COUNT(*) FROM transactions WHERE MONTH(date) = 5 AND YEAR(date) = 2025;",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 32"
    },
    {
        'Question': "What is the total revenue generated from all transactions?",
        'SQLQuery': "SELECT SUM(total) FROM transactions;",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 15432.50"
    },
    {
        'Question': "What was the total quantity sold for item 'ITM456'?",
        'SQLQuery': "SELECT SUM(quantity) FROM ledgerentries WHERE itemId = 'ITM456';",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., 87"
    },
    {
        'Question': "Show the names and prices of all items sold in transaction 'TXN789'.",
        'SQLQuery': """
SELECT i.name, le.priceSold 
FROM ledgerentries le 
JOIN items i ON le.itemId = i.itemId 
WHERE le.transactionId = 'TXN789';
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., T-shirt, 19.99"
    },
    {
        'Question': "List all items with less than 10 left in inventory.",
        'SQLQuery': """
SELECT i.name, inv.quantity 
FROM inventory inv 
JOIN items i ON inv.itemId = i.itemId 
WHERE inv.quantity < 10;
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., Cap, 7"
    },
    {
        'Question': "What is the email of the user who made transaction 'TXN101'?",
        'SQLQuery': """
SELECT u.email 
FROM transactions t 
JOIN users u ON t.userId = u.userId 
WHERE t.transactionId = 'TXN101';
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., customer@example.com"
    },
    {
        'Question': "Which items have never been sold?",
        'SQLQuery': """
SELECT i.itemId, i.name 
FROM items i 
LEFT JOIN ledgerentries le ON i.itemId = le.itemId 
WHERE le.itemId IS NULL;
""",
        'SQLResult': "Result of the SQL query",
        'Answer': "e.g., Mug"
    }
]