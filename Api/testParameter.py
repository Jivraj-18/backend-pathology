from flask_restful import Resource
from database.model import db, Parameter, Test, test_parameter_association, Package
from flask import request
class TestParameterApi(Resource):
    
    def get(self, package_id):
        package = Test.query.filter_by(id = package_id).first()

        return [test.to_dict() for test in package.parameters]
    def post(self, package_id):
        test_package_association_data = {
        'test_id': package_id,
        'parameter_id': request.json.get('parameter_id') ,
    }

        # Add the data to the association table
        db.session.execute(test_parameter_association.insert().values(**test_package_association_data))

        # Commit the session to persist the changes
        db.session.commit()

    def delete(self, package_id, test_id):
        test = Parameter.query.filter_by(id =  test_id).first()
        package = Test.query.filter_by(id = package_id).first()

        package.parameters.remove(test)
        db.session.commit()
        


class SearchParameterApi(Resource):
    def get(self, package_id):
        name = request.args.get('name', '')

        # Subquery to get the test IDs associated with the package
        subquery = db.session.query(test_parameter_association.c.parameter_id).filter(test_parameter_association.c.test_id == package_id).subquery()

        # Query to get tests not in the subquery
        tests = Parameter.query.filter(Parameter.name.ilike(f'%{name}%')).filter(Parameter.id.notin_(subquery)).limit(10).all()
        
        # Convert the results to dictionaries
        result = [test.to_dict() for test in tests]

        return result