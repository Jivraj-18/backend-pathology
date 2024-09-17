from flask import Flask
from flask_restful import Api
from Api.package import PackageApi
from Api.test import TestApi
from Api.parameter import ParameterApi
from Api.packageTest import PackageTestApi, SearchTestApi
from Api.testParameter import SearchParameterApi , TestParameterApi
import os 
from flask_cors import CORS
from database.model import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://pathology.vercel.app/"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join(os.getcwd(), 'database', 'path.sqlite3'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Disable modification tracking to suppress a warning
db.init_app(app)
with app.app_context():
    db.create_all()


api = Api(app)

# Add route for PackageApi
api.add_resource(PackageApi, '/package', '/package/<int:p_id>')
api.add_resource(TestApi, '/test', '/test/<int:p_id>')
api.add_resource(ParameterApi, '/parameter', '/parameter/<int:p_id>')
api.add_resource(PackageTestApi, '/package/<int:package_id>/test/<int:test_id>', '/package/<int:package_id>/test', '/package/<int:package_id>/tests')
api.add_resource(SearchTestApi, '/package/<int:package_id>/search')
api.add_resource(TestParameterApi, '/test/<int:package_id>/parameter/<int:test_id>', '/test/<int:package_id>/parameter', '/test/<int:package_id>/parameters')
api.add_resource(SearchParameterApi, '/test/<int:package_id>/search')

if __name__=="__main__":
    app.run()
    
