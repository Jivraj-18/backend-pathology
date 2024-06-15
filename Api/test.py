from flask_restful import Resource
from database.model import db, Test

from flask import request

class TestApi(Resource):
    def get(self):
        t_id = request.args.get('t_id')
        if t_id == 'all':
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            pagination = Test.query.paginate(page=page, per_page=limit, error_out=False)
            tests = pagination.items
            return [test.to_dict() for test in tests], 200
        return Test.query.filter_by(id = t_id).first().to_dict()
    def post(self):
        
        if Test.query.filter_by(name = request.form.get('name')).first() == None : 
                
            package = Test(name = request.form.get('name'), price=request.form.get('price'))
            db.session.add(package)
            db.session.commit()
            print(package.id)
            return package.to_dict(), 200
        return "Package Already Exists",404
    def put(self, p_id):
        package = Test.query.filter_by(id= p_id).first()
        
        package.name = request.form.get('name')
        package.price = request.form.get('price')
        db.session.commit()
        return "updated", 200
        
    def delete(self, p_id):
        package = Test.query.filter_by(id = p_id).first()

        package.showHide = 1 if package.showHide == 0 else 0 
        db.session.commit()
        return "Updated successfully", 200