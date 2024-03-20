from cryptography.fernet import Fernet
import json
import os
import time

'''
    class Task - representation of a basic task
    id : unique id for each task, that will become in handy for deleting task if completed
    title : str, it's the title of the task, what should we do?
    content : list - elaborate to checkboxes what to do step by step (if there is more than one)
    completed : boolean - when a new task is added the value is False
'''
class Task:
    def __init__(self, id, title, content, completed=False):
        self.id = id
        self.title = title
        self.content = content
        self.completed = completed

class ToDoList:
    def __init__(self):
        self.tasksJSON = []
        self.unsaved_tasks = []

    def add_task(self, task):
        self.unsaved_tasks.append(task)

    def save_tasks(self, filename):
        with open(filename, 'a') as f:
            for task in self.unsaved_tasks:
                json.dump(vars(task), f)
                f.write('\n')  # Add newline character after each task
        print(f"SAVING {len(self.unsaved_tasks)} new tasks... ")
        time.sleep(2.5)
        print("OK")
        time.sleep(1)
        self.unsaved_tasks.clear() # after saving they are no longer needed as a copy

    def load_tasks(self, filename):
        self.tasksJSON.clear() # avoid duplicates
        if len(self.unsaved_tasks) > 0: # we've added a task but not saved it yet
            print(f'You have {len(self.unsaved_tasks)} new tasks that are not saved.')
            print(f'It\'s recommended to save.')
            choice = input('Type S/s for saving them or X/x to discard: ')
            if choice.lower() == 's':
                self.save_tasks(filename)
            elif choice.lower() == 'x':
                print(f'Deleting {len(self.unsaved_tasks)} unsaved tasks...')
                time.sleep(2.5)
                self.unsaved_tasks.clear()
                print('OK')
            else:
                print("Invalid choice, returning to main program...")
                time.sleep(1.5)
            
        with open(filename, 'r') as f:
            for line in f.readlines():
                task_data = json.loads(line)  # Parse JSON from line
                task = Task(**task_data)  # Create a Task object from the JSON data
                self.tasksJSON.append(task)  # Append the task to self.tasks
            

    def display_tasks(self):
        print("All Tasks:")
        time.sleep(1.5)
        for index, task in enumerate(self.tasksJSON, start=1):
            print(f'\tid: {task.id}')
            print(f"\t{index}. {task.title}")
            for section in task.content:
                print(f'\t\t* {section}')
            if task.completed:
                print(f'\t-- TASK IS COMPLETED --')
        self.tasksJSON.clear() # clear tasksJSON in order to avoid duplicates
        print("---------------------------------")
        print("---------------------------------")
    def mark_task_as_completed(self, filename, task_id):
        found = False
        try:
            with open(filename, 'r') as f:
                for line in f:
                    task = json.loads(line.strip())
                    if task.get('id') == task_id:
                        found = True
                        task['completed'] = True
                    self.tasksJSON.append(task)
                if not found:
                    print("Error: Task not found with the provided ID.")
                    time.sleep(1)
                    return
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error: Failed to update task completed status: {e}")

        #saving the new version
        with open(filename, 'w') as f:
            for task in self.tasksJSON:
                json.dump(task, f)
                f.write('\n')  # Add newline character after each task
        print("Task completed status updated to true successfully.")
        time.sleep(2)
        

    def delete_specific_task(self, filename, task_id):
        found = False
        with open(filename, 'r') as f:
            for line in f.readlines():
                task_data = json.loads(line.rstrip())  # Parse JSON from line
                if task_data.get('id') == task_id:
                    found = True
                    continue
                # Convert Task parsed object to dictionary
                task_dict = {
                    'id': task_data.get('id'),
                    'title': task_data.get('title'),
                    'content': task_data.get('content'),
                    'completed': task_data.get('completed')
                }
                self.tasksJSON.append(task_dict)  # Append the task to self.tasks
        if not found:
            print("Error: Task not found with the provided ID.")
            time.sleep(1)
            return
        # Save the updated tasks to the file
        with open(filename, 'w') as f:
            for task in self.tasksJSON:
                json.dump(task, f)
                f.write('\n')  # Add newline character after each task
        print("Deleted finished successfully")
        time.sleep(2)
        self.tasksJSON.clear()       
                

def main():
    todo_list = ToDoList()
    fileName = 'tasks.json'

    while True:
        print("\t1. Add a new task") # completed
        print("\t2. View all tasks") # completed
        print("\t3. Mark task as completed") # completed
        print("\t4. Delete task by id") # completed
        print("\t5. Save task(s)") # completed
        print("\t6. Quit") # completed

        choice = input("Enter your choice: ")

        if choice == '1': # ADD
            key = Fernet.generate_key()
            key = key.hex() # turn to hexadecimal string
            name = input("Enter task name/title: ")
            options = ['y','yes']
            contentList = []
            item = input("Describe what to do in this task --> ")
            while True:
                contentList.append(item)
                choice = input("Would you like to add more details to this task? y/n: ")
                if choice.lower() not in options:
                    break
                item = input("adding... --> ")
            task = Task(key, name, contentList)
            todo_list.add_task(task)
        elif choice == '2': # VIEW
            time.sleep(1)
            try:
                # get the size of file
                file_size = os.path.getsize('./tasks.json')
        
                # if file size is 0, it is empty
                if (file_size == 0):
                    print("There are no registered tasks in the app")
                    time.sleep(1)
                
                todo_list.load_tasks(fileName) 
            # if file does not exist, then exception occurs
            except FileNotFoundError as e:
                print("File NOT found")
                continue
            todo_list.display_tasks() # display tasks
        elif choice == '3': # Mark task as completed
            id = input("Please copy the id of the task in order to complete: ")
            todo_list.mark_task_as_completed(fileName, id)
        elif choice == '4': # Delete task by id
            id = input("Please copy the id of the task in order to delete: ")
            todo_list.delete_specific_task(fileName, id)
        elif choice == '5': # Save tasks to file
            todo_list.save_tasks('tasks.json')  
        elif choice == '6':
            print("- - - - Exiting - - - -")
            break
        else:
            print("Invalid choice. Please try again.")

    print("Goodbye!")

if __name__ == "__main__":
    main()
