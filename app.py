import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables with meaningful defaults
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')  # Changed default to 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'admin')  # Changed default to 'admin'
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'mydb')  # Changed default to 'mydb'

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            );
            ''')
            mysql.connection.commit()
        except Exception as e:
            print(f"Error creating table: {str(e)}")
        finally:
            cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')

    # Validate the input
    if not new_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
        return jsonify({'message': new_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    app.run(host='0.0.0.0', port=5000, debug=True)
