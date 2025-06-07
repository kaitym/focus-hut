from flask import Flask, render_template, request, redirect, url_for
from fhut import Task, load_tasks, save_tasks, delete_task
import os
from datetime import datetime

app = Flask(__name__)
NOTES_FILE = 'global_notes.txt'

@app.route('/', methods=['GET'])
def index():
    tasks = load_tasks()
    notes_content = ''
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            notes_content = f.read()
    return render_template('index.html', tasks=tasks, content=notes_content)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    name = request.form['name']
    category = request.form.get('category', '')
    task_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(task_id, name, category)
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/start_timer/<int:task_id>', methods=['POST'])
def start_timer(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.start_timer()
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/stop_timer/<int:task_id>', methods=['POST'])
def stop_timer(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.stop_timer()
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/reset_timer/<int:task_id>', methods=['POST'])
def reset_timer(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.reset_timer()
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/notes', methods=['POST'])
def notes():
    note = request.form['note'].strip()
    if note:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTES_FILE, 'a') as f:
            f.write(f"\n--- {timestamp} ---\n{note}\n")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
