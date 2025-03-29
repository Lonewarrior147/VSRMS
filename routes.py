from flask import Flask, render_template, request, redirect, url_for
from models import db, Vehicle, Repair
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        owner_name = request.form['owner_name']
        model = request.form['model']
        license_plate = request.form['license_plate']
        purchase_date = datetime.strptime(request.form['purchase_date'],'%Y-%m-%d')

        existing_vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()

        if existing_vehicle:
            return "Error: License plate already exists!", 400

        vehicle = Vehicle(owner_name=owner_name, model=model, license_plate=license_plate, purchase_date=purchase_date)
        db.session.add(vehicle)
        db.session.commit()

        return redirect(url_for('view_vehicles'))

    return render_template('add_vehicle.html')

@app.route('/view_vehicles')
def view_vehicles():
    vehicles = Vehicle.query.all()
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
        vehicle_to_update.license_plate = request.form['license_plate']
        vehicle_to_update.owner_name = request.form['owner_name']
        vehicle_to_update.model = request.form['model']
        vehicle_to_update.purchase_date = request.form['purchase_date']

        try:
            db.session.commit()
            return redirect(url_for('view_vehicles'))
        
        except:
            return 'These was an issue updating vehicle details'
    else:
        return render_template('update_vehicle.html', vehicle=vehicle_to_update)
