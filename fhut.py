import json
import os
import time

# Task class holds all the task info
class Task:
    def __init__(self, task_id, name, category='', completed=False, start_time=None, elapsed_time=0):
        self.id = task_id
        self.name = name
        self.category = category
        self.completed = completed
        self.start_time = start_time
        self.elapsed_time = elapsed_time

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'completed': self.completed,
            'start_time': self.start_time,
            'elapsed_time': self.elapsed_time
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data['id'],
            name=data['name'],
            category=data.get('category', ''),
            completed=data.get('completed', False),
            start_time=data.get('start_time'),
            elapsed_time=data.get('elapsed_time', 0)
        )

    def get_elapsed(self):
        if self.start_time:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def start_timer(self):
        if not self.start_time:
            self.start_time = time.time()

    def stop_timer(self):
        if self.start_time:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None

    def reset_timer(self):
        self.start_time = None
        self.elapsed_time = 0

def load_tasks(filename='tasks.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data]
    else:
        return []

def save_tasks(tasks, filename='tasks.json'):
    with open(filename, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def delete_task(task_id, filename='tasks.json'):
    tasks = load_tasks(filename)
    tasks = [task for task in tasks if task.id != task_id]
    save_tasks(tasks, filename)
