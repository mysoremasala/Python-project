from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = 'pythonproject24'
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Models for Employees, Admins, and Leaves
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False)
    leave_type = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(100), nullable=False)
    end_date = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Admin Dashboard Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['login-email']
        password = request.form['login-password']
        
        # Fetch the admin from the database
        admin = Admin.query.filter_by(email=email).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['logged_in'] = True
            session['admin_name'] = admin.name  # Store admin name in session
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password')  # Error message if credentials are incorrect
            return redirect(url_for('login'))

    return render_template('index.html')

# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redirect to login if not logged in

    total_employees = Employee.query.count()
    total_admins = Admin.query.count()
    total_leaves = Leave.query.count()
    pending_leaves = 12  # Example placeholder, modify as needed
    approved_leaves = total_leaves  # Example
    
    return render_template('admin_dashboard.html', pending_leaves=pending_leaves, approved_leaves=approved_leaves, total_employees=total_employees, total_admins=total_admins)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('admin_name', None)
    return redirect(url_for('login'))

# Employee Section
@app.route('/emplist', methods=['GET', 'POST'])
def adsecemplist():
    if request.method == 'POST':
        name = request.form['employee-name']
        department = request.form['employee-department']
        position = request.form['employee-position']
        email = request.form['employee-email']
        
        new_employee = Employee(name=name, department=department, position=position, email=email)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('adsecemplist'))

    employees = Employee.query.all()
    return render_template('employee_section.html', employees=employees)

@app.route('/delete-employee/<int:id>')
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
    return redirect(url_for('adsecemplist'))

# Admin Management Section
# Admin Management Section
@app.route('/manage-admin', methods=['GET', 'POST'])
def admanage():
    if request.method == 'POST':
        name = request.form['admin-name']
        email = request.form['admin-email']
        password = request.form['admin-password']  # Get the password from the form

        # Hash the password before saving it
        password_hash = generate_password_hash(password)
        
        # Save the hashed password to the database
        new_admin = Admin(name=name, email=email, password_hash=password_hash)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('admanage'))

    admins = Admin.query.all()
    return render_template('manage_admin.html', admins=admins)

@app.route('/delete-admin/<int:id>')
def delete_admin(id):
    admin = Admin.query.get(id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
    return redirect(url_for('admanage'))

# Recent Leaves Section
@app.route('/recent-leaves')
def adrecent():
    leaves = Leave.query.all()
    return render_template('recent_leaves.html', leaves=leaves)



# Add leave functionality
@app.route('/add-leave', methods=['POST'])
def add_leave():
    employee_name = request.form['employee_name']
    leave_type = request.form['leave_type']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    reason = request.form['reason']

    new_leave = Leave(employee_name=employee_name, leave_type=leave_type, start_date=start_date, end_date=end_date, reason=reason)
    db.session.add(new_leave)
    db.session.commit()
    return redirect(url_for('adrecent'))


if __name__ == '__main__':
    app.run(debug=True)
