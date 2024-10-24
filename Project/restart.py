from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import MySQLdb
import random
import pyrebase
from config import firebaseConfig


app = Flask(__name__)

app.secret_key = 'pythonproject24'

# Connect to the MySQL database
firebase = pyrebase.initialize_app(config=firebaseConfig)
auth = firebase.auth()
db = firebase.database()
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if Admin or User form was submitted
        if request.form.get('login-email'):  # Admin form
            return redirect('/admin_dashboard')
        elif request.form.get('signup-email'):  # User form
            return redirect('/employee_dashboard')
    
    return render_template('index.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@app.route('/employee_section')
def employee_section():
    data = db.child('employee').get().val()
    return render_template('admin/employee_section.html',employees=data)

@app.route('/manage_admin')
def manage_admin():
    return render_template('admin/manage_admin.html')

# Route for the Employee dashboard
@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee/emp_dashboard.html')

@app.route('/empstatus')
def empstatus():
    return render_template('employee/empstatus.html')

@app.route('/leave_form')
def leave_form():
    return render_template('employee/leave_form.html')


#ADD EMPLOYEE STAT
def generate_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

@app.route("/add_employee", methods=["POST"])
def add_emp():
    try:
        # Get form data
        name = request.form.get('employee-name')
        dept = request.form.get('employee-department')
        pos = request.form.get('employee-position')
        email = request.form.get('employee-email')

        # Check for missing fields
        if not all([name, dept, pos, email]):
            return jsonify({"message": "Missing fields"}), 400

        # Generate unique ID
        id = generate_id()

        # Create data object
        data = {
            "name": name,
            "department": dept,
            "position": pos,
            "email": email,
            "id": id
        }
        
        print(f"Adding employee: {data}")  # Log data being added

        # Assuming db is your Firebase database reference
        db.child("employee").child(id).set(data)

        print("Employee added successfully!")  # Log success message

        # Return JSON response to indicate success
        return redirect('/employee_section')

    except Exception as e:
        print(f"Error occurred while adding employee: {e}")  # More specific error logging
        return redirect('/employee_section')


if __name__ == '__main__':
    app.run(debug=True)
