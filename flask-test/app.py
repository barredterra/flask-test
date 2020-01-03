from flask import Flask
from flask import render_template
app = Flask(__name__)

LOCATIONS = [
    {
        "id": "1",
        "title": "Warehouse Leipzig"
    },
    {
        "id": "2",
        "title": "Warehouse Berlin"
    }
]

PRODUCTS = [
    {
        "id": "1",
        "title": "Apple"
    },
    {
        "id": "2",
        "title": "Pear"
    }
]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/product')
def get_product_list():
    return render_template("list.html", items=PRODUCTS)

@app.route('/product/<product_id>')
def get_product(product_id):
    product = list(filter(lambda location: location["id"]==product_id, PRODUCTS))[0]
    return render_template("single.html", doc=product)

@app.route('/location')
def get_location_list():
    return render_template("list.html", items=LOCATIONS)

@app.route('/location/<location_id>')
def get_location(location_id):
    location = list(filter(lambda location: location["id"]==location_id, LOCATIONS))[0]
    return render_template("single.html", doc=location)
