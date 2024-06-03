import sqlite3

class Grocery:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.err = ""

    def ConnectDB(self):
        try:
            self.conn = sqlite3.connect("grocery.db")
            self.cur = self.conn.cursor()
            return "\n>>> Connected to database and Cursor created successfully <<<\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error establishing connection to the database: {str(e)} !!!\n"
            return self.err

    def CreateTable(self):
        try:
            # Creating three tables: bills, items, and stock
            bill_sql = """
            CREATE TABLE IF NOT EXISTS bills (
                billno INTEGER PRIMARY KEY, 
                date TEXT, 
                name TEXT, 
                no INTEGER
            )
            """
            item_sql = """
            CREATE TABLE IF NOT EXISTS items (
                itemid INTEGER PRIMARY KEY AUTOINCREMENT,
                billno INTEGER, 
                productname TEXT, 
                price INTEGER, 
                qty INTEGER,
                FOREIGN KEY (billno) REFERENCES bills (billno)
            )
            """
            stock_sql = """
            CREATE TABLE IF NOT EXISTS stock (
                productname TEXT PRIMARY KEY,
                amount_in_stock INTEGER,
                amount_sold INTEGER
            )
            """
            self.cur.execute(bill_sql)
            self.cur.execute(item_sql)
            self.cur.execute(stock_sql)
            return "\n>>> Tables created or opened (if already existing) successfully <<<\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error creating the tables: {str(e)} !!!\n"
            self.CloseDB()
            return self.err

    def InitializeStock(self):
        try:
            products = [
                "Idli&dosa batter","Toor dal(500g)","Wheat flour(1kg)","Peanuts(500g)","Tata salt(1pack)","Aachi chilli(100g)","Basmati Rice(5kg)","Quaker Oats(1kg)",
                "Eggs(dozen)","Freedom oil(1pack)","Fanta(250ml)","Frooti(300ml)","Chia seed(orange)","Maaza(1.2L)","Bingo Salted(1pack)","Kurkure(1pack)","Banana chips(1pack)",
                "Yippiee(8in1)","Kitkat(50g)","Dairy milk(52g)","Oreo(1pack)","Dark fantasy(1pack)","Mariegold(1pack)","Medimix(1pack)","Cintol(1pack)","Lux(1pack)",
                "Dove(1pack)","Dabur red(80g)","Colgate salt(42g)","Close-up(80g)"
            ]
            for product in products:
                sql = "INSERT OR IGNORE INTO stock (productname, amount_in_stock, amount_sold) VALUES (?, ?, ?)"
                self.cur.execute(sql, (product, 0, 0))
            self.conn.commit()
            return "\n>>> Stock initialized successfully <<<\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error initializing the stock: {str(e)} !!!\n"
            self.CloseDB()
            return self.err

    def UpdateStock(self, productname, quantity, is_selling=True):
        try:
            if is_selling:
                sql = """
                UPDATE stock 
                SET amount_in_stock = amount_in_stock - ?, 
                    amount_sold = amount_sold + ? 
                WHERE productname = ? AND amount_in_stock >= ?
                """
                self.cur.execute(sql, (quantity, quantity, productname, quantity))
            else:
                sql = "UPDATE stock SET amount_in_stock = amount_in_stock + ? WHERE productname = ?"
                self.cur.execute(sql, (quantity, productname))
            self.conn.commit()
            if self.cur.rowcount > 0:
                return "\n>>> Stock updated successfully <<<\n"
            else:
                return "\n!!! Insufficient stock or product not found !!!\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error updating the stock: {str(e)} !!!\n"
            self.CloseDB()
            return self.err

    def ViewStock(self):
        try:
            sql = "SELECT * FROM stock"
            self.cur.execute(sql)
            stock_data = self.cur.fetchall()
            stock_info = "\nCurrent Stock:\n"
            stock_info += "{:<20} {:<15} {:<15}\n".format("Product Name", "Amount in Stock", "Amount Sold")
            for item in stock_data:
                stock_info += "{:<20} {:<15} {:<15}\n".format(item[0], item[1], item[2])
            return stock_info
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error retrieving the stock data: {str(e)} !!!\n"
            self.CloseDB()
            return self.err

    def Save_details(self, b, d, n, no):
        try:
            sql = "INSERT INTO bills (billno, date, name, no) VALUES (?, ?, ?, ?)"
            self.cur.execute(sql, (b, d, n, no))
            self.conn.commit()
            return "\n>>> Details saved successfully <<<\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error inserting details into the database: {str(e)} !!!\n"
            self.CloseDB()
            return self.err

    def AddItem(self, b, pron, p, q):
        try:
            sql = "INSERT INTO items (billno, productname, price, qty) VALUES (?, ?, ?, ?)"
            self.cur.execute(sql, (b, pron, p, q))
            self.conn.commit()
            stock_update_msg = self.UpdateStock(pron, q)
            return "\n>>> Item added successfully <<<\n" + stock_update_msg
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error inserting item into the database: {str(e)} !!!\n"
            self.CloseDB()
            return self.err

    def DeleteItem(self, b, pron):
        try:
            sql = "DELETE FROM items WHERE billno = ? AND productname = ?"
            self.cur.execute(sql, (b, pron))
            self.conn.commit()
            if self.conn.total_changes > 0:
                return "\n>>> Item deleted successfully <<<\n"
            else:
                return "\n!!! No item to delete - check if the item ID is correct !!!\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error deleting item from the database: {str(e)} !!!\n"
            self.CloseDB()
            return self.err
    
    def GenerateBill(self, b):
        try:
            bill_sql = "SELECT * FROM bills WHERE billno = ?"
            self.cur.execute(bill_sql, (b,))
            bill_info = self.cur.fetchone()

            item_sql = "SELECT productname, price, qty FROM items WHERE billno = ?"
            self.cur.execute(item_sql, (b,))
            items = self.cur.fetchall()

            if bill_info:
                bill = f"Bill No: {bill_info[0]}\n"
                bill += f"Date: {bill_info[1]}\n"
                bill += f"Customer Name: {bill_info[2]}\n"
                bill += f"Customer Phone Number: {bill_info[3]}\n"
                bill += "\nItems:\n"
                bill += "{:<20} {:<10} {:<10} {:<10}\n".format("Product Name", "Price", "Quantity", "Total")

                total_price = 0
                for item in items:
                    item_total = item[1] * item[2]
                    bill += "{:<20} {:<10} {:<10} {:<10}\n".format(item[0], item[1], item[2], item_total)
                    total_price += item_total

                bill += "\nTotal Price: {}\n".format(total_price)
                return bill
            else:
                return "\n!!! There are no items in the bill with the given bill number !!!\n"
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error retrieving items from the bill: {str(e)} !!!\n"
            self.CloseDB()
            return self.err


    def DownloadBillHTML(self, b, file_path):
        bill_content = self.GenerateBill(b)
        if "!!!" not in bill_content:  # Check if there was an error in generating the bill
            try:
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Bill</title>
                    <style>
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                        }}
                        table, th, td {{
                            border: 1px solid black;
                        }}
                        th, td {{
                            padding: 8px;
                            text-align: left;
                        }}
                    </style>
                </head>
                <body>
                    <h2>Bill</h2>
                    <pre>{bill_content}</pre>
                </body>
                </html>
                """
                with open(file_path, 'w') as file:
                    file.write(html_content)
                return "\n>>> Bill downloaded successfully as HTML <<<\n"
            except IOError as e:
                return f"\n!!! There was an error writing the bill to an HTML file: {str(e)} !!!\n"
        else:
            return bill_content


    def CloseDB(self):
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            self.err = f"\n!!! There was an error closing the database: {str(e)} !!!\n"
            return self.err


