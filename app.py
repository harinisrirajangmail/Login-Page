from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for simplicity
users = []
properties = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone_number': request.form['phone_number'],
            'password': request.form['password'],
            'user_type': request.form['user_type']
        }
        users.append(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            return redirect(url_for('dashboard', user_type=user['user_type']))
    return render_template('login.html')

@app.route('/dashboard/<user_type>')
def dashboard(user_type):
    if user_type == 'seller':
        return render_template('seller_dashboard.html', properties=properties)
    else:
        return render_template('buyer_dashboard.html', properties=properties)

@app.route('/post_property', methods=['GET', 'POST'])
def post_property():
    if request.method == 'POST':
        property = {
            'title': request.form['title'],
            'description': request.form['description'],
            'address': request.form['address'],
            'price': request.form['price'],
            'property_type': request.form['property_type'],
            'size': request.form['size'],
            'bedrooms': request.form['bedrooms'],
            'bathrooms': request.form['bathrooms'],
            'nearby_facilities': request.form['nearby_facilities'],
        }
        properties.append(property)
        return redirect(url_for('dashboard', user_type='seller'))
    return render_template('post_property.html')

@app.route('/interested/<int:property_id>')
def interested(property_id):
    property = properties[property_id]
    return render_template('property_detail.html', property=property)

if __name__ == '__main__':
    app.run(debug=True)
