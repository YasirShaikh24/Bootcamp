from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'message':'hello , world'}

api.add_resource(HelloWorld, '/helloworld')

if __name__ == '_main_':
    app.run(debug=True)

class HelloWorld(Resource):
    def get(self):
        return {'message':'hello , world'}
    
class HelloWorld(Resource):
    def get(self, name):
        return {'data':'hello, {}'.format(name)}

api.add_resource(HelloWorld, '/helloworld/')
api.add_resource(HelloWorld, '/helloworld/<string:name>')

if __name__ == '_main_':
    app.run(debug=True)
