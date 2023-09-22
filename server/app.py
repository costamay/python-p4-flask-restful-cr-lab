#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Define a parser to handle request parameters
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the plant')
parser.add_argument('image', type=str, required=True, help='Image URL of the plant')
parser.add_argument('price', type=float, required=True, help='Price of the plant')

class Plants(Resource):
    def get(self):
        response_body =[plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(response_body), 200)
    
    def post(self):
        # new_plant = Plant(
        #     name= request.form['name'],
        #     image= request.form['image'],
        #     price= request.form['price'],
        # )
        
        # Parse the request data
        args= parser.parse_args()
        
        # Create a new plant object
        new_plant = Plant(
            name=args['name'],
            image=args['image'],
            price=args['price']
        )
        print(new_plant)
        db.session.add(new_plant)
        db.session.commit()
        
        response_dict = new_plant.to_dict()
        print (response_dict)
        
        response = make_response(jsonify(response_dict), 201)
        
        return response
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        response_body = Plant.query.get(id).to_dict()
        return make_response(jsonify(response_body), 200)
    
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
