# pylint:disable=C0111,C0103

def order_rank_per_customer(db):
    query = '''
    SELECT o.OrderId, o.CustomerID, o.OrderDate,
    RANK() OVER(
    PARTITION BY o.CustomerID
    ORDER BY o.OrderDate) AS OrderRank
    FROM Orders o
    '''
    db.execute(query)
    r = db.fetchall()
    return r


def order_cumulative_amount_per_customer(db):
    query = '''
    SELECT o.OrderId, o.CustomerID, o.OrderDate,
    SUM(SUM(od.UnitPrice*od.Quantity)) OVER(
    PARTITION BY o.CustomerID
    ORDER BY o.OrderDate) AS OrderCumulativeAmount
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY o.OrderID
    '''
    db.execute(query)
    r = db.fetchall()
    return r
