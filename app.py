from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '19930712'
app.config['MYSQL_DB'] = 'a3'

mysql = MySQL(app)

# Defining the main route of the application
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handling POST requests
    if request.method == 'POST':
        # Extracting the selected table name from the request form
        selected_table = request.form['table_name']
        # Creating a cursor object to execute SQL queries
        cur = mysql.connection.cursor()
        # Executing the SELECT query for the selected table
        cur.execute(f"SELECT * FROM {selected_table}")
        # Fetching all the data from the selected table
        data = cur.fetchall()
        # Closing the cursor object
        cur.close()
        # Rendering the 'table.html' template with the selected table name and its data
        return render_template('table.html', table_name=selected_table, table_data=data)

    # Handling GET requests
    # Listing all the available table names
    table_names = ['address', 'airline', 'airport', 'baggage', 'baggage_type', 'customer', 'economyclass', 'firstclass', 'flights', 'flights_duration', 'flight_status', 'gates', 'payment', 'seat', 'ticket']
    # Rendering the 'index.html' template with the available table names
    return render_template('index.html', table_names=table_names)


@app.route('/insert/<string:table_name>', methods=['GET', 'POST'])
def insert(table_name):
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO {table_name} (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('index'))

    return render_template('insert.html', table_name=table_name)


@app.route('/delete/<string:table_name>/<string:id_data>', methods=['GET'])
def delete(table_name, id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/update/<string:table_name>', methods=['POST', 'GET'])
def update(table_name):
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute(f"""
        UPDATE {table_name} SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)










