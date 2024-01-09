#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):

    def get(self):
        
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        
        response = make_response(
            response_dict,
            200,
        )

        return response

api.add_resource(Home, '/')

class Newsletters(Resource):

    def get(self):
        
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

    def post(self):
        
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):

    def get(self, id):

        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response
    
    def patch(self, id):
        nltr = Newsletter.query.filter_by(id=id).first();
        if (nltr == None):
            return make_response(f"404 Error: Newsletter with id {id} not found!", 404);
        
        if (0 < len(request.form)):
            for attr in request.form:
                setattr(nltr, attr, request.form.get(attr));
        else:
            for attr in request.json:
                setattr(nltr, attr, request.json[attr]);
        
        db.session.add(nltr);
        db.session.commit();
        
        return make_response(nltr.to_dict(), 200);

    def delete(self, id):
        nltr = Newsletter.query.filter_by(id=id).first();
        if (nltr == None):
            return make_response(f"404 Error: Newsletter with id {id} not found!", 404);
        db.session.delete(nltr);
        db.session.commit();
        return make_response({"message": "record successfully deleted"}, 200);


api.add_resource(NewsletterByID, '/newsletters/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)