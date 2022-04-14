# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query = '''
        SELECT Orders.OrderID, Customers.ContactName, Employees.FirstName
        FROM Orders
        JOIN Customers ON Orders.CustomerID = Customers.CustomerID
        JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
    '''
    db.execute(query)
    res = db.fetchall()
    return res

def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query = '''
        SELECT c.ContactName, SUM(od.Quantity * od.UnitPrice) AS TotalAmount
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY c.ContactName
        ORDER BY TotalAmount
    '''
    db.execute(query)
    r = db.fetchall()
    return r

def best_employee(db):
    '''Implement the best_employee method to determine who's the best employee!
    By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like:
    ('FirstName', 'LastName', 6000 (the sum of all purchase)). The order of the
    information is irrelevant'''
    query = '''
        SELECT e.FirstName, e.LastName, SUM(od.Quantity * od.UnitPrice) AS TotalAmount
        FROM Orders o
        JOIN Employees e ON o.EmployeeID = e.EmployeeID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        GROUP BY e.EmployeeID
        ORDER BY TotalAmount DESC
    '''
    db.execute(query)
    r = db.fetchone()
    return r

def orders_per_customer(db):
    '''TO DO: return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    query='''
        SELECT c.ContactName, COUNT(o.OrderID) AS NumberOfOrders
        FROM Customers c
        LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
        GROUP BY c.ContactName
        ORDER BY NumberOfOrders
    '''
    db.execute(query)
    r = db.fetchall()
    return r
