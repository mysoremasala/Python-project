from flask import Flask, render_template, request, redirect, url_for, session, flash
import MySQLdb

app = Flask(__name__)

app.secret_key = 'pythonproject24'

# Connect to the MySQL database
db = MySQLdb.connect(host="localhost", user="root", passwd="robloxfasds13yr_ver", db="pythonproject")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if Admin or User form was submitted
        if request.form.get('login-email'):  # Admin form
            return redirect(url_for('admin_dashboard'))
        elif request.form.get('signup-email'):  # User form
            return redirect(url_for('employee_dashboard'))
    
    return render_template('index.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Route for the Employee dashboard
@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('applyforaleavepage.html')

if __name__ == '__main__':
    app.run(debug=True)
