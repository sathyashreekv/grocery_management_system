# from flask import Flask, request, render_template, send_file
# from trial_sqlite import Grocery

# app = Flask(__name__)

# def initialize_db():
#     dbobj = Grocery()
#     print(dbobj.ConnectDB())
#     print(dbobj.CreateTable())
#     print(dbobj.InitializeStock())  # Initialize stock items in the database

# initialize_db()  # Initialize the database when the app starts

# @app.route("/", methods=["GET", "POST"])
# def home():
#     dbobj = Grocery()
#     dbobj.ConnectDB()
#     stock_text = dbobj.ViewStock()
#     dbobj.CloseDB()
#     return render_template("index.html", g="", stock=stock_text, b="", d="", n="", no="", i="", p="", q="")

# @app.route("/update_stock", methods=["POST"])
# def update_stock():
#     item_name = request.form.get("stock_itemname")
#     quantity = request.form.get("stock_quantity")

#     dbobj = Grocery()
#     dbobj.ConnectDB()
#     gtext = dbobj.UpdateStock(item_name, int(quantity), is_selling=False)
#     stock_text = dbobj.ViewStock()
#     dbobj.CloseDB()

#     return render_template("index.html", g=gtext, stock=stock_text, b="", d="", n="", no="", i="", p="", q="")

# @app.route("/form_submit", methods=["POST"])
# def form_submit():
#     bill_no = request.form.get("billnumber")
#     bill_date = request.form.get("billdate")
#     cust_name = request.form.get("custid")
#     cust_mob = request.form.get("custno")
#     item_name = request.form.get("itemname")
#     price = request.form.get("price")
#     quant = request.form.get("quantity")
#     item_na = request.form.get("itemna")

#     dbobj = Grocery()
#     dbobj.ConnectDB()
#     gtext = ""
#     action = request.form.get("action_button")
#     if action == "Save Details":
#         gtext = dbobj.Save_details(int(bill_no), bill_date, cust_name, int(cust_mob))
#     elif action == "Add an Item":
#         gtext = dbobj.AddItem(int(bill_no), item_name, int(price), int(quant))
#     elif action == "Delete an Item":
#         gtext = dbobj.DeleteItem(int(bill_no), item_na)
#     elif action == "Generate Bill":
#         gtext = dbobj.GenerateBill(int(bill_no))
#     elif action == "Download Bill":
#         file_path = f'bill_{bill_no}.html'
#         gtext = dbobj.DownloadBillHTML(int(bill_no), file_path)
#         dbobj.CloseDB()
#         if "!!!" not in gtext:
#             return send_file(file_path, as_attachment=True)
#         return render_template("index.html", g=gtext, stock=dbobj.ViewStock(), b=bill_no, d=bill_date, n=cust_name, no=cust_mob, i=item_name, p=price, q=quant)

#     stock_text = dbobj.ViewStock()
#     dbobj.CloseDB()
#     return render_template("index.html", g=gtext, stock=stock_text, b=bill_no, d=bill_date, n=cust_name, no=cust_mob, i=item_name, p=price, q=quant)

# if __name__ == "__main__":
#     app.run(port=9001)
from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import logging
from trial_sqlite import Grocery

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

def initialize_db():
    dbobj = Grocery()
    logging.info(dbobj.ConnectDB())
    logging.info(dbobj.CreateTable())
    logging.info(dbobj.InitializeStock())  # Initialize stock items in the database

initialize_db()  # Initialize the database when the app starts

@app.route("/", methods=["GET", "POST"])
def home():
    dbobj = Grocery()
    dbobj.ConnectDB()
    stock_text = dbobj.ViewStock()
    dbobj.CloseDB()
    return render_template("index.html", g="", stock=stock_text, b="", d="", n="", no="", i="", p="", q="")

@app.route("/update_stock", methods=["POST"])
def update_stock():
    item_name = request.form.get("stock_itemname")
    quantity = request.form.get("stock_quantity")

    dbobj = Grocery()
    dbobj.ConnectDB()
    gtext = dbobj.UpdateStock(item_name, int(quantity), is_selling=False)
    stock_text = dbobj.ViewStock()
    dbobj.CloseDB()

    return render_template("index.html", g=gtext, stock=stock_text, b="", d="", n="", no="", i="", p="", q="")

@app.route("/form_submit", methods=["POST"])
def form_submit():
    bill_no = request.form.get("billnumber")
    bill_date = request.form.get("billdate")
    cust_name = request.form.get("custid")
    cust_mob = request.form.get("custno")
    item_name = request.form.get("itemname")
    price = request.form.get("price")
    quant = request.form.get("quantity")
    item_na = request.form.get("itemna")

    dbobj = Grocery()
    dbobj.ConnectDB()
    gtext = ""
    action = request.form.get("action_button")
    if action == "Save Details":
        gtext = dbobj.Save_details(int(bill_no), bill_date, cust_name, int(cust_mob))
    elif action == "Add an Item":
        gtext = dbobj.AddItem(int(bill_no), item_name, int(price), int(quant))
    elif action == "Delete an Item":
        gtext = dbobj.DeleteItem(int(bill_no), item_na)
    elif action == "Generate Bill":
        gtext = dbobj.GenerateBill(int(bill_no))
    elif action == "Download Bill":
        file_path = os.path.join('bills', f'bill_{bill_no}.html')
        gtext = dbobj.DownloadBillHTML(int(bill_no), file_path)
        dbobj.CloseDB()
        if "!!!" not in gtext:
            return send_file(file_path, as_attachment=True)
        return render_template("index.html", g=gtext, stock=dbobj.ViewStock(), b=bill_no, d=bill_date, n=cust_name, no=cust_mob, i=item_name, p=price, q=quant)
    elif action == "Clear":
        return redirect(url_for('home'))

    stock_text = dbobj.ViewStock()
    dbobj.CloseDB()
    return render_template("index.html", g=gtext, stock=stock_text, b=bill_no, d=bill_date, n=cust_name, no=cust_mob, i=item_name, p=price, q=quant)

if __name__ == "__main__":
    app.run(port=9001,debug=True)

