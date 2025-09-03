import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                print(f"Error reading {self.filename}. Starting with empty todo list.")
                return []
        return []
    
    def save_todos(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.todos, file, indent=2, default=str)
        except IOError:
            print(f"Error saving to {self.filename}")
    
    def add_todo(self, task):
        if not task.strip():
            print("Task cannot be empty!")
            return False
        
        todo = {
            'id': len(self.todos) + 1,
            'task': task.strip(),
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.todos.append(todo)
        self.save_todos()
        print(f"✅ Added: '{task}'")
        return True
    
    def list_todos(self, show_completed=True):
        if not self.todos:
            print("📝 No todos yet! Add some tasks.")
            return
        
        print("\n" + "="*50)
        print("📋 YOUR TODO LIST")
        print("="*50)
        
        for todo in self.todos:
            if not show_completed and todo['completed']:
                continue
            
            status = "✅" if todo['completed'] else "❌"
            task = todo['task']
            created = todo['created_at']
            
            print(f"{status} [{todo['id']}] {task}")
            print(f"    Created: {created}")
        
        print("="*50)
    
    def complete_todo(self, todo_id):
        todo = self.find_todo(todo_id)
        if not todo:
            print(f"❌ Todo with ID {todo_id} not found!")
            return False
        
        if todo['completed']:
            print(f"✅ Todo '{todo['task']}' is already completed!")
            return True
        
        todo['completed'] = True
        todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_todos()
        print(f"🎉 Completed: '{todo['task']}'")
        return True
    
    def delete_todo(self, todo_id):
        todo = self.find_todo(todo_id)
        if not todo:
            print(f"❌ Todo with ID {todo_id} not found!")
            return False
        
        task = todo['task']
        self.todos = [t for t in self.todos if t['id'] != todo_id]
        self.save_todos()
        print(f"🗑️ Deleted: '{task}'")
        return True
    
    def find_todo(self, todo_id):
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def get_stats(self):
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo['completed'])
        pending = total - completed
        
        print("\n📊 STATISTICS")
        print("-" * 20)
        print(f"Total tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Completion rate: {completion_rate:.1f}%")
    
    def search_todos(self, keyword):
        keyword = keyword.lower()
        results = [todo for todo in self.todos if keyword in todo['task'].lower()]
        
        if not results:
            print(f"🔍 No todos found containing '{keyword}'")
            return
        
        print(f"\n🔍 Search results for '{keyword}':")
        print("-" * 30)
        for todo in results:
            status = "✅" if todo['completed'] else "❌"
            print(f"{status} [{todo['id']}] {todo['task']}")
    
    def clear_completed(self):
        completed_count = sum(1 for todo in self.todos if todo['completed'])
        
        if completed_count == 0:
            print("✅ No completed todos to clear!")
            return
        
        self.todos = [todo for todo in self.todos if not todo['completed']]
        self.save_todos()
        print(f"🧹 Cleared {completed_count} completed todos")

def show_menu():
    print("\n🌟 SIMPLE TODO APP 🌟")
    print("-" * 25)
    print("1. Add todo")
    print("2. List todos")
    print("3. List pending todos")
    print("4. Complete todo")
    print("5. Delete todo")
    print("6. Search todos")
    print("7. Show statistics")
    print("8. Clear completed")
    print("9. Exit")
    print("-" * 25)

def main():
    app = TodoApp()
    
    print("🎉 Welcome to Simple Todo App!")
    
    while True:
        show_menu()
        choice = input("Choose an option (1-9): ").strip()
        
        if choice == '1':
            task = input("Enter new task: ")
            app.add_todo(task)
        
        elif choice == '2':
            app.list_todos()
        
        elif choice == '3':
            app.list_todos(show_completed=False)
        
        elif choice == '4':
            try:
                todo_id = int(input("Enter todo ID to complete: "))
                app.complete_todo(todo_id)
            except ValueError:
                print("❌ Please enter a valid number!")
        
        elif choice == '5':
            try:
                todo_id = int(input("Enter todo ID to delete: "))
                app.delete_todo(todo_id)
            except ValueError:
                print("❌ Please enter a valid number!")
        
        elif choice == '6':
            keyword = input("Enter search keyword: ")
            app.search_todos(keyword)
        
        elif choice == '7':
            app.get_stats()
        
        elif choice == '8':
            app.clear_completed()
        
        elif choice == '9':
            print("👋 Goodbye! Thanks for using Todo App!")
            break
        
        else:
            print("❌ Invalid option! Please choose 1-9.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using Todo App!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the application.")