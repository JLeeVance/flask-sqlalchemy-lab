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

# Add views here

@app.route('/earthquakes/<int:id>')
def get_quake(id):
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        body = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        status = 200
    else:
        body = {
            "message": f"Earthquake {id} not found."
        }
        status = 404

    return make_response(jsonify(body), status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_mag(magnitude):
    earthquakes_search = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()


    quake_dict = []
    count = 0
    for quake in earthquakes_search:
        count += 1
        quake_dict.append(
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            }
        )
    

    if earthquakes_search:
        body = {
            "count": count,
            "quakes": quake_dict
        }
        status = 200
    else:
        body = {
            "count": count,
            "quakes": quake_dict
        }
        status = 200
    
    return make_response(jsonify(body), status)
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
