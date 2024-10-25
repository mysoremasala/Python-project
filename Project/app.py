from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
            session.pop('name', None)
            session['name'] = request.form.get('signup-email')  # Corrected assignment
            return redirect('/employee_dashboard')
    
    return render_template('index.html')



@app.route('/admin_dashboard')
def admin_dashboard():
    data = db.child("leaves").get().val()
    return render_template('admin/admin_dashboard.html', leaves = data)

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
    data = db.child("leaves").get().val()
    return render_template('employee/empstatus.html', leaves = data)

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
        name = session.get('name')
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


@app.route("/add_leave", methods=['POST'])
def add_leave():
    data = request.get_json()  # Get JSON data from the request
    if data:
        # Ensure all necessary data is present
        leave_type = data.get("type", "")
        employee_name = data.get("name", "")
        start_date = data.get("start", "")
        end_date = data.get("end", "")
        status = "not approved"
        id = generate_id()      # Save the data to Firebase
        leave_data = {
            "type": leave_type,
            "name": employee_name,
            "start": start_date,
            "end": end_date,
            "status":status,
            "id":id
        }
        
        db.child("leaves").child(id).set(leave_data)  # Use employee name as key or modify as needed
        return jsonify({"message": "Leave application submitted successfully!"}), 200

    return jsonify({"message": "Failed to submit leave application!"}), 400


@app.route("/approve_leave", methods=['POST'])
def app_leaves():
    data = request.get_json()  # Get JSON data from the request
    if data:
        leave_id = data.get("id", "")
        status = "approved"
        
        # Update the status in the database
        db.child("leaves").child(leave_id).child('status').set(status)  # Use leave_id instead of 'id'
        
        return jsonify({"message": "Leave application approved successfully!"}), 200

    return jsonify({"message": "Failed to approve leave application!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
