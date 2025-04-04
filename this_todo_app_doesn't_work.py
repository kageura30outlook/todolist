from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
date_format = '%Y-%m-%d'

# Modify the Todo model to include a 'status' column
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="not-started")  # New status column
    priority = db.Column(db.String(20),default="Low")

### Show tasks ###
@app.route("/", methods=["GET", "POST"])
def home():
    todo_list = Todo.query.all()

    # Pass the Todo list to the "index.html" template for display
    return render_template("index.html", todo_list=todo_list)

### Add a task ###
@app.route("/add", methods=["POST"])   
def add():
    # Get the deadline from the form and convert it to a datetime object
    deadline = request.form.get("deadline")
    if deadline:
        deadline = datetime.strptime(deadline, date_format)
    else:
        deadline = None
    
    # Get the title and status from the form
    title = request.form.get("title")
    status = request.form.get("status")  # Get the status from the form
    priority = request.form.get("priority")
    # Create a new Todo object with the provided data
    new_todo = Todo(title=title, deadline=deadline, status=status, priority=priority)
    db.session.add(new_todo)  # Add the new Todo to the session
    db.session.commit()  # Commit the session to save to the database
    return redirect(url_for("home"))  # Redirect back to the home page

### Delete a task ###
@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # Find the Todo by its ID
    db.session.delete(todo)  # Delete the Todo
    db.session.commit()  # Commit the deletion to the database
    return redirect(url_for("home"))  # Redirect back to the home page

### Update task status ###
@app.route("/update-status/<int:todo_id>", methods=["POST"])
def update_status(todo_id):
    todo = Todo.query.get(todo_id)  # Get the Todo object by ID
    todo.status = request.form.get("status")  # Update the status field
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for("home"))  # Redirect back to the home page

### Update task status ###
@app.route("/update-priority/<int:todo_id>", methods=["POST"])
def update_priority(todo_id):
    todo = Todo.query.get(todo_id)  # Get the Todo object by ID
    todo.priority = request.form.get("priority")  # Update the status field
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for("home"))  # Redirect back to the home page

@app.route("/filter", methods=["POST"])
def filter():
    status = request.form.get("status")  # Get the status from the form

    # If 'status' is selected as 'all', show all tasks
    if status == 'all' or not status:
        todo_list = Todo.query.all()
    else:
        todo_list = Todo.query.filter_by(status=status).all()

    return render_template("index.html", todo_list=todo_list)

@app.route("/filter_priority", methods=["POST"])
def filter_priority():
    priority = request.form.get("priority")

    if priority == "all" or not priority:
        todo_list = Todo.query.all()
    else:
        todo_list = Todo.query.filter_by(priority=priority).all()

    return render_template("index.html", todo_list=todo_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
