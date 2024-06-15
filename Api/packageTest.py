from flask_restful import Resource
from database.model import db, Parameter, Test, test_package_association, Package
from flask import request
class PackageTestApi(Resource):
    
    def get(self, package_id):
        package = Package.query.filter_by(id = package_id).first()

        return [test.to_dict() for test in package.tests]
    def post(self, package_id):
        test_package_association_data = {
        'package_id': package_id,
        'test_id': request.json.get('test_id') ,
    }

        # Add the data to the association table
        db.session.execute(test_package_association.insert().values(**test_package_association_data))

        # Commit the session to persist the changes
        db.session.commit()

    def delete(self, package_id, test_id):
        test = Test.query.filter_by(id =  test_id).first()
        package = Package.query.filter_by(id = package_id).first()

        package.tests.remove(test)
        db.session.commit()
        


class SearchTestApi(Resource):
    def get(self, package_id):
        name = request.args.get('name', '')

        # Subquery to get the test IDs associated with the package
        subquery = db.session.query(test_package_association.c.test_id).filter(test_package_association.c.package_id == package_id).subquery()

        # Query to get tests not in the subquery
        tests = Test.query.filter(Test.name.ilike(f'%{name}%')).filter(Test.id.notin_(subquery)).limit(10).all()
        
        # Convert the results to dictionaries
        result = [test.to_dict() for test in tests]

        return result