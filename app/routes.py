# app/routes.py
from flask import render_template, request, redirect, url_for
from app import app, db, socketio
from app.models import Task
from flask_socketio import emit

# Home route to view tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Route to create a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    assigned_to = request.form['assigned_to']
    new_task = Task(title=title, description=description, assigned_to=assigned_to)
    db.session.add(new_task)
    db.session.commit()

    # Emit a real-time event to update the client
    socketio.emit('new_task', {'id': new_task.id, 'title': new_task.title, 'assigned_to': new_task.assigned_to}, broadcast=True)

    return redirect(url_for('index'))

# Route to update task status
@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = request.form['status']
    db.session.commit()

    # Emit a real-time event to notify clients of the status change
    socketio.emit('task_updated', {'id': task.id, 'status': task.status}, broadcast=True)

    return redirect(url_for('index'))
