from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def base():
    return render_template('applyforaleavepage.html')


@app.route('/recent-leaves')
def recent_leaves():
     return render_template('recent_leaves.html')
 
 
@app.route('/logout')
def logout():
     return render_template('index.html')
 

 
 
 
 
@app.route('/apply-leave', methods=['GET', 'POST'])
def apply_leave():
    if request.method == 'POST':
        leave_type = request.form.get('leave-type')
        other_reason = request.form.get('other-reason', '').strip()

        # Validate the form
        if leave_type == 'other' and not other_reason:
            flash('Please provide a reason for selecting "Other" leave type.', 'error')
            return redirect(url_for('apply_leave'))

        flash('Your leave request has been submitted successfully!', 'success')
        return redirect(url_for('base'))

    return render_template('leave_form.html')




    
if __name__ == '__main__':
    app.run(debug=True)
