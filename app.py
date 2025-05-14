from flask import Flask, render_template, request, redirect
from focushut import Task, load_tasks, save_tasks

app = Flask(__name__)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    name = request.form['name']
    category = request.form.get('category', '')
    task_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(task_id, name, category)
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            break
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
