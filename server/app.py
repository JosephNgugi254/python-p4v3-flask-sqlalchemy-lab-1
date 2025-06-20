# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def earthquake(id):
    result=Earthquake.query.filter(Earthquake.id==id).first()
    if result:
        return jsonify(result.to_dict()), 200
    else:
        
        return jsonify({'message': f'Earthquake {id} not found.'}), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude(magnitude):
    result=Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    count=len(result)
    return jsonify({"count":count,'quakes':[quake.to_dict() for quake in result]}),200

if __name__ == '__main__':
    app.run(port=5555, debug=True)