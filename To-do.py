import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import time
import threading

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root, width=40)
        self.task_listbox.pack(pady=10)

        self.remove_button = tk.Button(root, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        task_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Task", menu=task_menu)
        task_menu.add_command(label="Add Task", command=self.add_task)
        task_menu.add_command(label="Update Task", command=self.update_task)
        task_menu.add_command(label="View Tasks", command=self.view_tasks)
        task_menu.add_command(label="Remove Task", command=self.remove_task)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            now = datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            self.tasks.append({"task": task, "time": formatted_time, "reminder": None})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def update_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            current_task = self.tasks[selected_index[0]]["task"]
            updated_task = simpledialog.askstring("Update Task", f"Update task '{current_task}' to:")
            if updated_task:
                self.tasks[selected_index[0]]["task"] = updated_task
                self.update_task_listbox()

    def view_tasks(self):
        if not self.tasks:
            messagebox.showinfo("Tasks", "No tasks in the list.")
        else:
            task_text = "\n".join([f"{task['task']} ({task['time']})" for task in self.tasks])
            messagebox.showinfo("Tasks", task_text)

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['task']} ({task['time']})")

    def set_reminder(self, index):
        reminder_time = self.tasks[index]["reminder"]
        while reminder_time:
            current_time = datetime.now()
            if current_time >= reminder_time:
                messagebox.showinfo("Reminder", f"Reminder for task: {self.tasks[index]['task']}")
                self.tasks[index]["reminder"] = None
            time.sleep(1)

    def start_reminder_thread(self, index):
        thread = threading.Thread(target=self.set_reminder, args=(index,))
        thread.start()

    def add_reminder(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            reminder_time = simpledialog.askstring("Set Reminder", "Enter reminder time (HH:MM:SS):")
            if reminder_time:
                try:
                    hours, minutes, seconds = map(int, reminder_time.split(":"))
                    now = datetime.now()
                    reminder_datetime = now.replace(hour=hours, minute=minutes, second=seconds)
                    self.tasks[index]["reminder"] = reminder_datetime
                    self.start_reminder_thread(index)
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Invalid time format. Please use HH:MM:SS.")

def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
