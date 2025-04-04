from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Vehicle, User
from datetime import datetime
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid email or password", "danger")  # Flash message for invalid login

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return redirect(url_for('view_vehicles'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash("This email is already registered.", "danger")
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password,
                        name=form.name.data, phone=form.phone.data,
                        address=form.address.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for('login'))

    
    return render_template('register.html', form=form)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        model = request.form['model']
        year = request.form['year']  # Extract year from the form
        odo_reading = request.form['odo_reading']  # Extract odometer reading from the form
        license_plate = request.form['license_plate']
        vin = request.form['vin']  # Extract VIN from the form

        existing_vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()

        if existing_vehicle:
            return "Error: License plate already exists!", 400
        
        vehicle = Vehicle(user_id=current_user.id,
                        model=model,
                        year=year,  
                        odo_reading=odo_reading,
                        license_plate=license_plate,
                        vin=vin)   
        db.session.add(vehicle)
        db.session.commit()
        flash("Vehicle Added Successfully", "success")

        return redirect(url_for('view_vehicles'))

    return render_template('add_vehicle.html')

@app.route('/view_vehicles')
def view_vehicles():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('view_vehicles.html', vehicles=vehicles)

@app.route('/delete_vehicle/<int:id>')
def delete_vehicle(id):
    vehicle_to_delete = Vehicle.query.get_or_404(id)
    try:
        db.session.delete(vehicle_to_delete)
        db.session.commit()
        
        return redirect(url_for('view_vehicles'))
    except:
        return "There was a error in deleting vehicle"

@app.route('/update_vehicle/<int:id>', methods=["GET", "POST"])
def update_vehicle(id):
    vehicle_to_update = Vehicle.query.get_or_404(id)
    
    if request.method == "POST":
        vehicle_to_update.cid = request.form['cid']
        vehicle_to_update.model = request.form['model']
        vehicle_to_update.year = int(request.form['year'])  # Convert to integer
        vehicle_to_update.odo_reading = int(request.form['odo_reading'])  # Convert to integer
        vehicle_to_update.license_plate = request.form['license_plate']
        vehicle_to_update.vin = request.form['vin']

        try:
            db.session.commit()
            return redirect(url_for('view_vehicles'))
        
        except:
            return 'There was an issue updating vehicle details'
    
    return render_template('update_vehicle.html', vehicle=vehicle_to_update)
