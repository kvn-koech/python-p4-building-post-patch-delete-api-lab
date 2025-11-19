from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    response = make_response(jsonify(bakeries_serialized), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_serialized = bakery.to_dict()
        response = make_response(jsonify(bakery_serialized), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [bg.to_dict() for bg in baked_goods]
    response = make_response(jsonify(baked_goods_serialized), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        baked_good_serialized = baked_good.to_dict()
        response = make_response(jsonify(baked_good_serialized), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        return jsonify({'error': 'No baked goods found'}), 404

# POST route for creating new baked goods
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # Get form data
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')
    
    # Validate required fields
    if not name or not price or not bakery_id:
        return jsonify({'error': 'Missing required fields: name, price, bakery_id'}), 400
    
    # Create new baked good
    try:
        baked_good = BakedGood(
            name=name,
            price=float(price),
            bakery_id=int(bakery_id)
        )
        db.session.add(baked_good)
        db.session.commit()
        
        # Return the created baked good as JSON
        baked_good_serialized = baked_good.to_dict()
        response = make_response(jsonify(baked_good_serialized), 201)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# PATCH route for updating bakeries
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    if not bakery:
        return jsonify({'error': 'Bakery not found'}), 404
    
    # Get form data
    name = request.form.get('name')
    
    if name:
        bakery.name = name
        try:
            db.session.commit()
            bakery_serialized = bakery.to_dict()
            response = make_response(jsonify(bakery_serialized), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No name provided'}), 400

# DELETE route for deleting baked goods
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    
    if not baked_good:
        return jsonify({'error': 'Baked good not found'}), 404
    
    try:
        db.session.delete(baked_good)
        db.session.commit()
        return jsonify({'message': 'Baked good successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)