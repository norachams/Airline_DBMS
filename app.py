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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_table = request.form['table_name']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {selected_table}")
        data = cur.fetchall()
        cur.close()
        return render_template('table.html', table_name=selected_table, table_data=data)

    table_names = ['address', 'airline', 'airport', 'baggage', 'baggage_type', 'customer', 'economyclass', 'firstclass', 'flights', 'flights_duration', 'flight_status', 'gates', 'payment', 'seat','ticket']
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














''' 
# Define the routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/drop_tables")
def drop_tables():
    # Define the tables to drop
    tables = ["baggage_type", "address", "airline", "airport", "baggage", "customer", "economyclass", "firstclass", "flight_status", "flights_duration", "flights", "gates", "payment", "seat", "ticket"]
    
    # Drop the tables
    cursor = mysql.connection.cursor()
    for table in tables:
        cursor.execute("DROP TABLE IF EXISTS " + table)
    
    return render_template("message.html", message="Tables dropped successfully.")

# Route for creating tables
@app.route('/create-tables')
def create_tables():
    cursor = mysql.connection.cursor()

    # SQL queries to create tables

    baggage_type_query = "CREATE TABLE IF NOT EXISTS baggage_type (Baggage_Type VARCHAR(50), Fees VARCHAR(50))"
    address_query = "CREATE TABLE IF NOT EXISTS address (email VARCHAR(25) NOT NULL, postal_code VARCHAR(7) NOT NULL, province VARCHAR(25) NOT NULL, city VARCHAR(25) NOT NULL, street VARCHAR(25) NOT NULL, PRIMARY KEY (email))"
    airline_query = "CREATE TABLE IF NOT EXISTS airline (Airline_Name VARCHAR(25) NOT NULL, Country VARCHAR(25), PRIMARY KEY (Airline_Name))"
    airport_query = "CREATE TABLE IF NOT EXISTS airport (Airport_Name VARCHAR(40) NOT NULL, Departures VARCHAR(3) DEFAULT 'YYZ', Arrivals VARCHAR(3), PRIMARY KEY (Airport_Name))"
    baggage_query = "CREATE TABLE IF NOT EXISTS baggage (Baggage_ID VARCHAR(25) NOT NULL, Baggage_Type VARCHAR(25), Weight INT, PRIMARY KEY (Baggage_ID))"
    customer_query = "CREATE TABLE IF NOT EXISTS customer (First_name VARCHAR(25) NOT NULL, Last_name VARCHAR(25) NOT NULL, email VARCHAR(25) NOT NULL, customer_id INT NOT NULL, PRIMARY KEY (email,customer_id))"
    economyclass_query = "CREATE TABLE IF NOT EXISTS economyclass (Seat_num VARCHAR(3), Complementary_Drinks VARCHAR(25), Complementary_Meals VARCHAR(25), PRIMARY KEY (Seat_num), FOREIGN KEY (Seat_num) REFERENCES seat (Seat_num))"
    firstclass_query = "CREATE TABLE IF NOT EXISTS firstclass (Seat_num VARCHAR(3), Menu_Items VARCHAR(25), Beverage_Items VARCHAR(25), Gifts VARCHAR(25), PRIMARY KEY (Seat_num), FOREIGN KEY (Seat_num) REFERENCES seat (Seat_num))"
    flight_status_query = "CREATE TABLE IF NOT EXISTS flight_status (ticket_num VARCHAR(10) NOT NULL, flight_num VARCHAR(10) NOT NULL, flight_status VARCHAR(50) NOT NULL, PRIMARY KEY (ticket_num))"
    flights_duration_query = "CREATE TABLE IF NOT EXISTS flights_duration (Departure_Airport VARCHAR(50), Arrival_Airport VARCHAR(50), Flight_Duration VARCHAR(50))"
    flights_query = "CREATE TABLE IF NOT EXISTS flights (Flight_Num VARCHAR(50) NOT NULL, Airline VARCHAR(50), Departure_Time VARCHAR(50), Arrival_Time VARCHAR(50), Departure_Airport VARCHAR(50), Arrival_Airport VARCHAR(50), Plane_Type VARCHAR(50))"
    gates_query = "CREATE TABLE IF NOT EXISTS gates (Gate_ID VARCHAR(9) NOT NULL, Security_Check VARCHAR(50), PRIMARY KEY (Gate_ID), FOREIGN KEY (Security_Check) REFERENCES airport (Airport_Name))"
    payment_query = "CREATE TABLE IF NOT EXISTS payment (Method VARCHAR(25), Price VARCHAR(9), Booking_num VARCHAR(10) NOT NULL, PRIMARY KEY (Booking_num))"
    seat_query = "CREATE TABLE IF NOT EXISTS seat (Capacity INT, Seat_num VARCHAR(3) NOT NULL, Customer_email VARCHAR(45) NOT NULL, PRIMARY KEY (Seat_num,Customer_email))"
    ticket_query = "CREATE TABLE IF NOT EXISTS ticket (Ticket_num INT NOT NULL, Seat_num VARCHAR(4), Flight_num varchar(10),  Customer_id varchar(25), PRIMARY KEY (Ticket_num))"

    # Execute the queries
    cursor.execute(baggage_type_query)
    cursor.execute(address_query)
    cursor.execute(airline_query)
    cursor.execute(airport_query)
    cursor.execute(baggage_query)
    cursor.execute(customer_query)
    cursor.execute(economyclass_query)
    cursor.execute(firstclass_query)
    cursor.execute(flight_status_query)
    cursor.execute(flights_duration_query)
    cursor.execute(flights_query)
    cursor.execute(gates_query)
    cursor.execute(payment_query)
    cursor.execute(ticket_query)

    return "Tables created successfully!"
'''