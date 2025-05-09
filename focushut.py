import json 
import os 

# Tasks class to hold task information (id, name, category, and whether it's completed)
class Task:
    def __init__(self, task_id, name, category='', completed=False):
        self.id = task_id
        self.name = name 
        self.category = category 
        self.completed = completed


    # Method to turn a Tasks into a dictionary (for the JSON file)
    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name,
            'category': self.category,
            'completed': self.completed
        }
    

    # Static method which creates a Task object from a dict. (from the JSON file)
    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data['id'],
            name=data['name'],
            category=data.get('category', ''),
            completed=data.get('completed', False)
        )
    

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




if __name__ == '__main__':
    tasks = load_tasks()

    print(f"Loaded {len(tasks)} tasks.")

    new_task = Task(task_id=len(tasks) + 1, name='Test Task', category='Test Category')
    tasks.append(new_task)

    save_tasks(tasks)

    print("Added and saved a test task")
