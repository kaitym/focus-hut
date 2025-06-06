import json 
import os 
import time

# Tasks class to hold task information (id, name, category, and whether it's completed)
class Task:
    def __init__(self, task_id, name, category='', completed=False, start_time=None, elapsed_time=0):
        self.id = task_id
        self.name = name 
        self.category = category 
        self.completed = completed

        #timer
        self.start_time = start_time
        self.elapsed_time = elapsed_time


    # Method to turn a Tasks into a dictionary (for the JSON file)
    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name,
            'category': self.category,
            'completed': self.completed,
            'start_time': self.start_time,
            'elapsed_time': self.elapsed_time
        }
    

    # Static method which creates a Task object from a dict. (from the JSON file)
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

    def stop_timer(self):
        if self.start_time:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None

    def start_timer(self):
        if not self.start_time:
            self.start_time = time.time()

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




if __name__ == '__main__':
    # Load any tasks from file (JSON)
    tasks = load_tasks()


    # Command-line menu for user with 4 options 
    while True:
        print("\n ==== FocusHut ====")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task complete")
        print("4. Timer options")
        print("5. Exit")


        # Prompt user to choose an option
        choice = input("Choose an option (1-5): ")

        # Opt 1: view all tasks (if any) and display their status
        if choice == '1':
            if not tasks:
                print("No tasks yet!")

            else:
                for task in tasks:
                    status = "✅" if task.completed else "❌"

                    print(f"[{status}] {task.id}: {task.name} ({task.category})")


        # Opt 2: add tasks to the file 
        elif choice == '2':
            name = input("Enter task name: ")
            category = input("Enter category (optional): ")
            task_id = max([task.id for task in tasks], default = 0) + 1
            new_task = Task(task_id=task_id, name=name, category=category)
            tasks.append(new_task)
            save_tasks(tasks)
            print(f"Tasks '{name}' added !")


        # Opt 3: mark a task as complete if it exists
        elif choice == '3':
            task_id = input("Enter the ID of the task to mark complete: ")
            found = False

            for task in tasks:
                if str(task.id) == task_id:
                    task.completed = True
                    save_tasks(tasks)
                    print(f"Task '{task.name}' marked complete !")
                    found = True
                    break
                
                if not found:
                    print("Task not found.")


        

        elif choice == '4':
            task_id = input("Enter the task ID for the timer: ")
            task = next((t for t in tasks if str(t.id) == task_id), None)

            if not task:
                print("Task not found.")
                continue

            while True:
                print("\n=== Timer Menu ===")
                print("a. Start timer")
                print("b. Stop timer")
                print("c. Reset timer")
                print("d. Show elapsed time")
                print("e. Back to main menu")

                timer_choice = input("Choose an option (a-e): ").lower()

                if timer_choice == 'a':
                    task.start_timer()
                    save_tasks(tasks)
                    print("Timer started.")

                elif timer_choice == 'b':
                    task.stop_timer()
                    save_tasks(tasks)
                    print("Timer stopped.")

                elif timer_choice == 'c':
                    task.reset_timer()
                    save_tasks(tasks)
                    print("Timer reset.")

                elif timer_choice == 'd':
                    seconds = task.get_elapsed()
                    mins = int(seconds // 60)
                    secs = int(seconds % 60)
                    print(f"Elapsed Time: {mins:02}:{secs:02}")

                elif timer_choice == 'e':
                    break

        # Opt 4: exit 
        elif choice == '5':
            save_tasks(tasks)
            print("Goodbye! Tasks saved.")
            break 


        # In case of invalid input
        else:
            print("Invalid option. Please choose 1-5")