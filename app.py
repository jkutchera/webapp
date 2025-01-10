from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Database connection details
server = 'gloscolinvoiceserver.database.windows.net'
database = 'InvoiceDatabase'
username = 'InvoiceAdmin'
password = '9&8EJB#uibgd'
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM InvoiceTracker')
    invoices = cursor.fetchall()
    conn.close()
    return render_template('index.html', invoices=invoices)

@app.route('/add', methods=['POST'])
def add_invoice():
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    invoice_date = request.form['invoice_date']
    invoice_number = request.form['invoice_number']
    description = request.form['description']
    try:
        invoice_total = float(request.form['invoice_total'])  # Convert to numeric
    except ValueError:
        return "Invalid input for Invoice Total", 400  # Return an error for invalid input

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO InvoiceTracker (CustomerName, CustomerAddress, InvoiceDate, InvoiceNumber, Description, InvoiceTotal) '
        'VALUES (?, ?, ?, ?, ?, ?)',
        (customer_name, customer_address, invoice_date, invoice_number, description, invoice_total)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_invoice(id):
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    invoice_date = request.form['invoice_date']
    invoice_number = request.form['invoice_number']
    description = request.form['description']
    invoice_total = request.form['invoice_total']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE InvoiceTracker SET CustomerName = ?, CustomerAddress = ?, InvoiceDate = ?, InvoiceNumber = ?, Description = ?, InvoiceTotal = ? '
        'WHERE InvoiceID = ?',
        (customer_name, customer_address, invoice_date, invoice_number, description, invoice_total, id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_invoice(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM InvoiceTracker WHERE InvoiceID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
