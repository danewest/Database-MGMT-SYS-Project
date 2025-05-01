import mysql.connector

def getCustomerReport(customerName):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="35yeZey53+01",
            database="CFG"
        )
        cursor = conn.cursor()

        query = """
        SELECT c.CustomerName, SUM(o1.QuotedPrice * o1.NumOrdered) AS TotalQuotedPrice
        FROM Customer c
        JOIN Orders o ON c.CustomerNum = o.CustomerNum
        JOIN OrderLine o1 ON o.OrderNum = o1.OrderNum
        WHERE c.CustomerName = %s
        GROUP BY c.CustomerName;
        """
        cursor.execute(query, (customerName,))
        res = cursor.fetchone()

        #if res:
        #    return {"CustomerName": res[0], "TotalQuotedPrice": float(res[1])}
        #else:
        #    return {"CustomerName": customerName, "TotalQuotedPrice": 0.0}

    except mysql.connector.Error as e:
        print("Database Error:", e)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()