from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)

session_secret = os.environ.get('SESSION_SECRET')
if not session_secret:
    raise RuntimeError(
        'SESSION_SECRET environment variable must be set. '
        'For local development, you can set it in the Secrets tab. '
        'For production deployment, ensure it is configured in environment variables.'
    )

app.secret_key = session_secret

DATA_DIR = 'data'
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.json')
MOVEMENTS_FILE = os.path.join(DATA_DIR, 'movements.json')

os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    products = load_data(PRODUCTS_FILE)
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        products = load_data(PRODUCTS_FILE)
        product_id = request.form['product_id'].strip()
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        
        if any(p['product_id'] == product_id for p in products):
            flash('Product ID already exists!', 'error')
            return redirect(url_for('add_product'))
        
        products.append({
            'product_id': product_id,
            'name': name,
            'description': description
        })
        save_data(PRODUCTS_FILE, products)
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = load_data(PRODUCTS_FILE)
    product = next((p for p in products if p['product_id'] == product_id), None)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        product['name'] = request.form['name'].strip()
        product['description'] = request.form.get('description', '').strip()
        save_data(PRODUCTS_FILE, products)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/locations')
def locations():
    locations = load_data(LOCATIONS_FILE)
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        locations = load_data(LOCATIONS_FILE)
        location_id = request.form['location_id'].strip()
        name = request.form['name'].strip()
        address = request.form.get('address', '').strip()
        
        if any(l['location_id'] == location_id for l in locations):
            flash('Location ID already exists!', 'error')
            return redirect(url_for('add_location'))
        
        locations.append({
            'location_id': location_id,
            'name': name,
            'address': address
        })
        save_data(LOCATIONS_FILE, locations)
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_location.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    locations = load_data(LOCATIONS_FILE)
    location = next((l for l in locations if l['location_id'] == location_id), None)
    
    if not location:
        flash('Location not found!', 'error')
        return redirect(url_for('locations'))
    
    if request.method == 'POST':
        location['name'] = request.form['name'].strip()
        location['address'] = request.form.get('address', '').strip()
        save_data(LOCATIONS_FILE, locations)
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('edit_location.html', location=location)

@app.route('/movements')
def movements():
    movements = load_data(MOVEMENTS_FILE)
    products = load_data(PRODUCTS_FILE)
    locations = load_data(LOCATIONS_FILE)
    
    product_dict = {p['product_id']: p['name'] for p in products}
    location_dict = {l['location_id']: l['name'] for l in locations}
    
    for movement in movements:
        movement['product_name'] = product_dict.get(movement['product_id'], 'Unknown')
        movement['from_location_name'] = location_dict.get(movement['from_location'], '-') if movement['from_location'] else '-'
        movement['to_location_name'] = location_dict.get(movement['to_location'], '-') if movement['to_location'] else '-'
    
    movements.reverse()
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    products = load_data(PRODUCTS_FILE)
    locations = load_data(LOCATIONS_FILE)
    
    if request.method == 'POST':
        movements = load_data(MOVEMENTS_FILE)
        
        product_id = request.form['product_id']
        from_location = request.form.get('from_location', '').strip()
        to_location = request.form.get('to_location', '').strip()
        qty = int(request.form['qty'])
        
        if not from_location:
            from_location = None
        if not to_location:
            to_location = None
        
        if not from_location and not to_location:
            flash('At least one location (From or To) must be selected!', 'error')
            return redirect(url_for('add_movement'))
        
        movement_id = max([m['movement_id'] for m in movements], default=0) + 1
        
        movements.append({
            'movement_id': movement_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'from_location': from_location,
            'to_location': to_location,
            'product_id': product_id,
            'qty': qty
        })
        save_data(MOVEMENTS_FILE, movements)
        flash('Movement added successfully!', 'success')
        return redirect(url_for('movements'))
    
    return render_template('add_movement.html', products=products, locations=locations)

@app.route('/report')
def report():
    movements = load_data(MOVEMENTS_FILE)
    products = load_data(PRODUCTS_FILE)
    locations = load_data(LOCATIONS_FILE)
    
    balance = {}
    
    for movement in movements:
        product_id = movement['product_id']
        qty = movement['qty']
        from_loc = movement['from_location']
        to_loc = movement['to_location']
        
        if from_loc:
            key = f"{product_id}|{from_loc}"
            balance[key] = balance.get(key, 0) - qty
        
        if to_loc:
            key = f"{product_id}|{to_loc}"
            balance[key] = balance.get(key, 0) + qty
    
    product_dict = {p['product_id']: p['name'] for p in products}
    location_dict = {l['location_id']: l['name'] for l in locations}
    
    report_data = []
    for key, qty in balance.items():
        if qty != 0:
            product_id, location_id = key.split('|')
            report_data.append({
                'product_id': product_id,
                'product_name': product_dict.get(product_id, 'Unknown'),
                'location_id': location_id,
                'location_name': location_dict.get(location_id, 'Unknown'),
                'qty': qty
            })
    
    report_data.sort(key=lambda x: (x['product_name'], x['location_name']))
    
    return render_template('report.html', report_data=report_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
