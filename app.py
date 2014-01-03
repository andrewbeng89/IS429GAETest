import webapp2
from webapp2_extras import json
from google.appengine.ext import ndb

class Todo(ndb.Model):
    id = ndb.FloatProperty()
    title = ndb.StringProperty()
    completed = ndb.BooleanProperty()

class GetTodosHandler(webapp2.RequestHandler):

    def get(self):
        todos = Todo.query().fetch(40)
        self.response.headers['Content-Type'] = 'application/json'
        result = []
        for todo in todos:
            result.append(todo.to_dict())
        self.response.write(json.encode(result))

class CreateTodosHandler(webapp2.RequestHandler):

    def post(self):
        json_form = json.decode(self.request.body)
        new_todo = Todo(id = json_form['id'],
            title = json_form['title'],
            completed = json_form['completed'])
        new_todo.put()
        self.response.headers['Content-Type'] = 'application/json'
        result = {
                'result': 'success'
            }
        self.response.write(json.encode(result))

class DeleteTodosHandler(webapp2.RequestHandler):

    def post(self):
        json_form = json.decode(self.request.body)
        id = json_form['id']
        q = Todo.query()
        q = q.filter(Todo.id == id)
        q.fetch(1)[0].key.delete()
        self.response.headers['Content-Type'] = 'application/json'
        result = {
                'result': 'success'
            }
        self.response.write(json.encode(result))

class UpdateTodosHandler(webapp2.RequestHandler):

    def post(self):
        json_form = json.decode(self.request.body)
        id = json_form['id']
        q = Todo.query()
        q = q.filter(Todo.id == id)
        todo = q.fetch(1)[0]
        if todo.completed == True:
            todo.completed = False
        else:
            todo.completed = True
        todo.put()
        self.response.headers['Content-Type'] = 'application/json'
        result = {
                'result': 'success'
            }
        self.response.write(json.encode(result))

application = webapp2.WSGIApplication([
    ('/api/get/todos', GetTodosHandler),
    ('/api/create/todos', CreateTodosHandler),
    ('/api/delete/todos', DeleteTodosHandler),
    ('/api/update/todos', UpdateTodosHandler)
], debug=True)