from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

# Define association tables
test_package_association = Table('test_package_association', db.Model.metadata,
    Column('test_id', Integer, ForeignKey('test.id')),
    Column('package_id', Integer, ForeignKey('package.id'))
)

test_parameter_association = Table('parameter_test_association', db.Model.metadata,
    Column('test_id', Integer, ForeignKey('test.id')),
    Column('parameter_id', Integer, ForeignKey('parameter.id'))
)

# Define other models
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place = db.Column(db.String(150))

    def to_dict(self):
        return {
            'id': self.id,
            'place': self.place
        }

class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    time = db.Column(db.DateTime(), default=datetime.now())
    showHide = db.Column(db.Integer, default=1) # 0 don't show, 1 show
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    tests = relationship("Test", secondary=test_parameter_association, back_populates="parameters")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time.strftime("%d/%m/%y %H/%M/%S"),
            'showHide': self.showHide,
            'price': self.price
        }

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime(), default=datetime.now)
    showHide = db.Column(db.Integer, default=1) # 0 don't show, 1 show
    packages = relationship("Package", secondary=test_package_association, back_populates="tests")
    parameters = relationship("Parameter", secondary=test_parameter_association, back_populates="tests")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'time': self.time.strftime("%d/%m/%y %H/%M/%S"),
            'showHide': self.showHide
        }

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime(), default=datetime.now)
    showHide= db.Column(db.Integer, default=1) # 0 don't show, 1 show
    tests = relationship("Test", secondary=test_package_association, back_populates="packages")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'time': self.time.strftime("%d/%m/%y %H/%M/%S"),
            'showHide': self.showHide
        }
