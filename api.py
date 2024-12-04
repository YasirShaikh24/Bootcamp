from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)
api = Api(app)

class Todos(db.Model):
    todo_id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return{
            "todo_id": self.todo_id,
            "task": self.task,
            "message": self.message
        }

# This two line of code is runned initially for the creation of the database 
with app.app_context():
    db.create_all()



class ToDoList(Resource):
    def get(self):
        todo = Todos.query.all()
        return[Todos.to_dict() for Todos in todo], 200  # This statement will call the to_dict() method in Todos class for json fromat
    def post(self):
        data = request.get_json()
        new_todo = Todos(
            task = data['task'],
            message = data['message']
        )
        db.session.add(new_todo)
        db.session.commit()
        return new_todo.to_dict(), 201
    
class ToDo(Resource):
    def get(self, todo_id):
        todo = Todos.query.get(todo_id)
        if todo:
            return todo.to_dict(), 200
        return 'Data Unavailable', 404
    
    def put(self, todo_id):
        data = request.get_json()
        todo = Todos.query.get(todo_id)
        if todo:
            todo.task = data.get('task', todo.task)
            todo.message = data.get('message', todo.message)
            db.session.commit()
            return todo.to_dict(), 200
        return '', 404

    def delete(self, todo_id):
        todo = Todos.query.get(todo_id)
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return '', 204
        return 'Unable to delete', 404


api.add_resource(ToDoList, '/todos')
api.add_resource(ToDo, '/todos/<int:todo_id>')
if __name__ == '__main__':
    app.run(debug=True)