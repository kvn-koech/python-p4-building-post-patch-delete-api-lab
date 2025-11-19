from app import app, db
from models import Bakery, BakedGood

with app.app_context():
    # Check if tables exist
    print("Tables in database:")
    print(db.engine.table_names())
    
    # Check bakeries
    bakeries = Bakery.query.all()
    print(f"Number of bakeries: {len(bakeries)}")
    
    # Check baked goods
    baked_goods = BakedGood.query.all()
    print(f"Number of baked goods: {len(baked_goods)}")