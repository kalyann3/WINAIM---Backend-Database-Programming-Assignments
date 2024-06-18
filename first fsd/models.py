from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    customer = db.relationship('Customer', back_populates='contacts')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

Customer.contacts = db.relationship('Contact', order_by=Contact.id, back_populates='customer')

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    customer = db.relationship('Customer', back_populates='opportunities')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

Customer.opportunities = db.relationship('Opportunity', order_by=Opportunity.id, back_populates='customer')

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    customer = db.relationship('Customer', back_populates='interactions')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

Customer.interactions = db.relationship('Interaction', order_by=Interaction.id, back_populates='customer')
