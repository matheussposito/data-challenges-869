# pylint:disable=C0111,C0103

def get_average_purchase(db):
    # return the average amount spent per order for each customer
    # ordered by customer ID
    query = '''
        WITH mytable AS (
            SELECT
                od.OrderID , SUM(od.UnitPrice*od.Quantity) AS Total
            FROM OrderDetails od
            GROUP BY od.OrderID
        )
        SELECT
            o.CustomerId,
	        round(AVG(mytable.Total),2)
        FROM mytable
        JOIN Orders o ON mytable.OrderID = o.OrderID
        GROUP BY o.CustomerID
    '''
    db.execute(query)
    r = db.fetchall()
    return r

def get_general_avg_order(db):
    # return the average amount spent per order
    query = '''
        WITH mytable AS (
            SELECT
                od.OrderID , SUM(od.UnitPrice*od.Quantity) AS Total
            FROM OrderDetails od
            GROUP BY od.OrderID
        )
        SELECT
            AVG(mytable.Total)
        FROM mytable
    '''
    db.execute(query)
    r = db.fetchall()
    return r[0][0]

def best_customers(db):
    # return the customers who have an average purchase greater
    # than the general average purchase
    query = '''
        WITH mytable1 AS (
            SELECT
                od.OrderID , SUM(od.UnitPrice*od.Quantity) AS Total
            FROM OrderDetails od
            GROUP BY od.OrderID
        ),
        mytable2 AS (
            SELECT
                round(AVG(mytable1.Total),2) AS TotalAvg
            FROM mytable1
        ),
        mytable3 AS(
            SELECT
                o.CustomerId,
                round(AVG(mytable1.Total),2) AS CustAvg
            FROM Orders o
            JOIN mytable1 ON o.OrderID = mytable1.OrderID
            GROUP BY o.CustomerID
        )
        SELECT
            CustomerID,
            CustAvg
        FROM mytable3
        WHERE CustAvg > (SELECT TotalAvg FROM mytable2)
        ORDER BY CustAvg DESC
    '''
    db.execute(query)
    r = db.fetchall()
    return r

def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer
    # based on the total ordered amount in USD
    query = '''
        WITH prodtot AS (
            SELECT
                od.ProductID, o.CustomerID,
                SUM(od.UnitPrice*od.Quantity) AS ProdTotal
            FROM OrderDetails od
            JOIN Orders o ON o.OrderID = od.OrderID
            GROUP BY o.CustomerID, od.ProductID
            ORDER BY ProdTotal DESC
        )
        SELECT
            pt.CustomerID,
            pt.ProductID,
            MAX(pt.ProdTotal) AS OrderedAmount
        FROM prodtot pt
        GROUP BY pt.CustomerID
        ORDER BY OrderedAmount DESC
    '''
    db.execute(query)
    r = db.fetchall()
    return r

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive
    # orders of the same customer
    query = '''
        WITH mytable AS (
            SELECT
            o.CustomerID,
            o.OrderDate,
            RANK() OVER (PARTITION BY o.CustomerID ORDER BY o.CustomerID,
            o.OrderDate) AS OrderRank
        FROM Orders o
        ),
        tbl AS (
            SELECT m2.CustomerID, mytable.OrderDate AS PreviousOrder,
            m2.OrderDate AS NextOrder
            FROM mytable
            JOIN mytable m2 ON mytable.OrderRank = m2.OrderRank - 1 AND
            mytable.CustomerID = m2.CustomerID
            ORDER BY m2.CustomerID
        )
        SELECT
        CAST(ROUND(AVG(JULIANDAY(NextOrder) - JULIANDAY(PreviousOrder))) AS INT)
        AS AvgDays FROM tbl
    '''
    db.execute(query)
    r = db.fetchone()
    return r[0]
