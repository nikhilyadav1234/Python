import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("450x500")
        self.root.configure(bg="#f0f4f8")

        # Variables
        self.expenses = []

        # Create UI components
        self.create_widgets()
        self.load_expenses()  # Load expenses from file on startup

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Expense Tracker", font=("Arial", 18, "bold"), bg="#0d6efd", fg="white")
        title_label.pack(pady=15, fill=tk.X)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#f0f4f8")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Amount:", font=("Arial", 12), bg="#f0f4f8").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 12), width=22, bd=2, relief="solid")
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Category:", font=("Arial", 12), bg="#f0f4f8").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.category_entry = tk.Entry(input_frame, font=("Arial", 12), width=22, bd=2, relief="solid")
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Description:", font=("Arial", 12), bg="#f0f4f8").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.description_entry = tk.Entry(input_frame, font=("Arial", 12), width=22, bd=2, relief="solid")
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#f0f4f8")
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Expense", font=("Arial", 12), bg="#198754", fg="white", width=12, command=self.add_expense)
        add_button.grid(row=0, column=0, padx=5, pady=10)

        delete_button = tk.Button(button_frame, text="Delete Selected", font=("Arial", 12), bg="#dc3545", fg="white", width=12, command=self.delete_expense)
        delete_button.grid(row=0, column=1, padx=5, pady=10)

        clear_button = tk.Button(button_frame, text="Clear All", font=("Arial", 12), bg="#ffc107", fg="white", width=12, command=self.clear_all)
        clear_button.grid(row=0, column=2, padx=5, pady=10)

        # Expenses Treeview
        self.tree = ttk.Treeview(self.root, columns=("Amount", "Category", "Description"), show='headings', height=3)
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.column("Amount", width=100, anchor="center")
        self.tree.column("Category", width=100, anchor="center")
        self.tree.column("Description", width=150, anchor="center")
        self.tree.pack(pady=15, padx=10, fill=tk.X)

        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#e9ecef", fieldbackground="#e9ecef", foreground="#212529")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#0d6efd")

        # Total Expense Label
        self.total_label = tk.Label(self.root, text="Total Expenses: $0.00", font=("Arial", 11, "bold"), bg="#f0f4f8", fg="#198754")
        self.total_label.pack(pady=10)

        # Save Expenses Button
        save_button = tk.Button(self.root, text="Save Expenses", font=("Arial", 14), bg="#0d6efd", fg="white", command=self.save_expenses)
        save_button.pack(pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()
            description = self.description_entry.get().strip()

            if amount <= 0 or not category or not description:
                raise ValueError("Invalid input")

            # Add the expense to the list and Treeview
            self.expenses.append({"amount": amount, "category": category, "description": description})
            self.tree.insert("", "end", values=(amount, category, description))
            self.update_total()

            # Clear the input fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values.")

    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            # Remove the expense from the list
            index = self.tree.index(selected_item)
            del self.expenses[index]
            self.update_total()
        else:
            messagebox.showwarning("Warning", "Please select an expense to delete.")

    def clear_all(self):
        self.expenses.clear()  # Clear the expenses list
        self.tree.delete(*self.tree.get_children())  # Clear the treeview
        self.update_total()

    def update_total(self):
        total = sum(expense["amount"] for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")

    def save_expenses(self):
        with open("expenses.json", "w") as file:
            json.dump(self.expenses, file)
        messagebox.showinfo("Info", "Expenses saved successfully!")

    def load_expenses(self):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                self.expenses = json.load(file)
                for expense in self.expenses:
                    self.tree.insert("", "end", values=(expense["amount"], expense["category"], expense["description"]))
                self.update_total()

# Create the main application window
root = tk.Tk()
app = ExpenseTracker(root)

# Run the application
root.mainloop()






