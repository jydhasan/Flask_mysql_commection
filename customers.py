from flask import Flask, render_template, request,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'excel'

mysql = MySQL(app)

# Create a 'customers' table if it doesn't exist
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=data)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
