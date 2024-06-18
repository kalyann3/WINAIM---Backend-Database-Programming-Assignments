from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from models import db, Customer, Contact, Opportunity, Interaction
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class CustomerResource(Resource):
    def get(self, customer_id=None):
        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                return jsonify(customer.as_dict())
            else:
                return {"error": "Customer not found"}, 404
        else:
            customers = Customer.query.all()
            return jsonify([customer.as_dict() for customer in customers])
    
    def post(self):
        data = request.json
        new_customer = Customer(**data)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.as_dict())
    
    def put(self, customer_id):
        data = request.json
        customer = Customer.query.get(customer_id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
            db.session.commit()
            return jsonify(customer.as_dict())
        else:
            return {"error": "Customer not found"}, 404
    
    def delete(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return '', 204
        else:
            return {"error": "Customer not found"}, 404

class ContactResource(Resource):
    def get(self, contact_id=None):
        if contact_id:
            contact = Contact.query.get(contact_id)
            if contact:
                return jsonify(contact.as_dict())
            else:
                return {"error": "Contact not found"}, 404
        else:
            contacts = Contact.query.all()
            return jsonify([contact.as_dict() for contact in contacts])
    
    def post(self):
        data = request.json
        new_contact = Contact(**data)
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(new_contact.as_dict())
    
    def put(self, contact_id):
        data = request.json
        contact = Contact.query.get(contact_id)
        if contact:
            for key, value in data.items():
                setattr(contact, key, value)
            db.session.commit()
            return jsonify(contact.as_dict())
        else:
            return {"error": "Contact not found"}, 404
    
    def delete(self, contact_id):
        contact = Contact.query.get(contact_id)
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return '', 204
        else:
            return {"error": "Contact not found"}, 404

class OpportunityResource(Resource):
    def get(self, opportunity_id=None):
        if opportunity_id:
            opportunity = Opportunity.query.get(opportunity_id)
            if opportunity:
                return jsonify(opportunity.as_dict())
            else:
                return {"error": "Opportunity not found"}, 404
        else:
            opportunities = Opportunity.query.all()
            return jsonify([opportunity.as_dict() for opportunity in opportunities])
    
    def post(self):
        data = request.json
        new_opportunity = Opportunity(**data)
        db.session.add(new_opportunity)
        db.session.commit()
        return jsonify(new_opportunity.as_dict())
    
    def put(self, opportunity_id):
        data = request.json
        opportunity = Opportunity.query.get(opportunity_id)
        if opportunity:
            for key, value in data.items():
                setattr(opportunity, key, value)
            db.session.commit()
            return jsonify(opportunity.as_dict())
        else:
            return {"error": "Opportunity not found"}, 404
    
    def delete(self, opportunity_id):
        opportunity = Opportunity.query.get(opportunity_id)
        if opportunity:
            db.session.delete(opportunity)
            db.session.commit()
            return '', 204
        else:
            return {"error": "Opportunity not found"}, 404

class InteractionResource(Resource):
    def get(self, interaction_id=None):
        if interaction_id:
            interaction = Interaction.query.get(interaction_id)
            if interaction:
                return jsonify(interaction.as_dict())
            else:
                return {"error": "Interaction not found"}, 404
        else:
            interactions = Interaction.query.all()
            return jsonify([interaction.as_dict() for interaction in interactions])
    
    def post(self):
        data = request.json
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M')
        new_interaction = Interaction(**data)
        db.session.add(new_interaction)
        db.session.commit()
        return jsonify(new_interaction.as_dict())
    
    def put(self, interaction_id):
        data = request.json
        interaction = Interaction.query.get(interaction_id)
        if interaction:
            for key, value in data.items():
                if key == 'date':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M')
                setattr(interaction, key, value)
            db.session.commit()
            return jsonify(interaction.as_dict())
        else:
            return {"error": "Interaction not found"}, 404
    
    def delete(self, interaction_id):
        interaction = Interaction.query.get(interaction_id)
        if interaction:
            db.session.delete(interaction)
            db.session.commit()
            return '', 204
        else:
            return {"error": "Interaction not found"}, 404

api.add_resource(CustomerResource, '/customers', '/customers/<int:customer_id>')
api.add_resource(ContactResource, '/contacts', '/contacts/<int:contact_id>')
api.add_resource(OpportunityResource, '/opportunities', '/opportunities/<int:opportunity_id>')
api.add_resource(InteractionResource, '/interactions', '/interactions/<int:interaction_id>')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
