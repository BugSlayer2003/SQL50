-- @setup
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL
);

INSERT INTO Customers (id, name, city) VALUES
  (1, 'Alice', 'Shanghai'),
  (2, 'Bob', 'Beijing'),
  (3, 'Celine', 'Shanghai');

-- @solution
SELECT
  city,
  COUNT(*) AS customer_count
FROM Customers
GROUP BY city
ORDER BY city;

-- @expected
city | customer_count
Beijing | 1
Shanghai | 2
