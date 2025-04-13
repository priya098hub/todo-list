import sqlite3
import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")

        # UI elements
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.add_btn = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_btn.pack()

        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.pack(pady=10)

        self.delete_btn = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_btn.pack()

        # DB setup
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.setup_db()
        self.load_tasks()

    def setup_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        ''')
        try:
            self.cursor.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

        self.conn.commit()

    def add_task(self):
        title = self.task_entry.get().strip()
        if title == "":
            messagebox.showwarning("Warning", "Task cannot be empty")
            return

        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO tasks (title, created_at) VALUES (?, ?)", (title, timestamp))
        self.conn.commit()
        self.task_entry.delete(0, tk.END)
        self.load_tasks()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            return
        task_text = self.task_listbox.get(selected)
        task_id = int(task_text.split(".")[0])
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, title FROM tasks")
        for row in self.cursor.fetchall():
            self.task_listbox.insert(tk.END, f"{row[0]}. {row[1]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
