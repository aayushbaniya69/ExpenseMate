import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from PIL import Image, ImageTk

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("expense_mate.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    name TEXT,
    birthdate TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    date TEXT,
    expense TEXT,
    amount REAL,
    FOREIGN KEY (email) REFERENCES users(email)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES users(email)
);
""")
cursor.execute("PRAGMA table_info(loans)")
columns = [col[1] for col in cursor.fetchall()]  # Get column names

if "status" not in columns:  # If 'status' column doesn't exist, add it
    cursor.execute("""
        ALTER TABLE loans ADD COLUMN status TEXT DEFAULT 'Unpaid';
    """)
    conn.commit()

# Login/Signup Page
class LoginSignupPage:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpenseMate (Login / Signup)")
        self.root.geometry("800x600")
        self.root.resizable(0, 0)

        # Load the background image
        self.bg_image = Image.open(r"C:\Users\ASUS\Desktop\ExpenseMate\modern-background-connecting-lines-dots.jpg")  # Replace with your image path
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Label with the background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Stretch to fit the window

        # Load and resize the logo image
        self.logo_image = Image.open(r"C:\Users\ASUS\Desktop\ExpenseMate\Screenshot (55).png")  # Replace with your logo image path
        self.logo_image = self.logo_image.resize((340,140))  # Resize the logo image (adjust size as needed)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Create a Label with the resized logo image and position it on top
        self.logo_label = tk.Label(self.root, image=self.logo_photo, bg="#FFDAB9")  # Background color optional
        self.logo_label.place(x=600, y=30)  # Adjust x, y for positioning

        # Email and Password fields
        tk.Label(self.root, text="Email:", bg="#FFCC99", fg="black", font=("Arial", 10, "bold")).place(x=675, y=200, width=200, height=25)
        self.email_entry = tk.Entry(self.root, bg="#FFF5E1", fg="black", font=("Arial", 10))
        self.email_entry.place(x=675, y=230, width=200, height=25)

        tk.Label(self.root, text="Password:", bg="#FFCC99", fg="black", font=("Arial", 10, "bold")).place(x=675, y=270, width=200, height=25)
        self.password_entry = tk.Entry(self.root, show="*", bg="#FFF5E1", fg="black", font=("Arial", 10))
        self.password_entry.place(x=675, y=300, width=200, height=25)

        # Show/Hide Password Button
        self.show_password = tk.Button(self.root, text="Show", command=self.toggle_password_visibility, 
                                       bg="#FFE5B4", fg="black", font=("Arial", 9), relief="groove", borderwidth=1)
        self.show_password.place(x=880, y=300)

        # Buttons Styling Function
        def on_enter(e):
            e.widget.config(bg="#FFD700")  # Gold hover effect

        def on_leave(e):
            e.widget.config(bg=e.widget.default_bg)

        # Buttons for login/signup
        self.login_btn = tk.Button(self.root, text="Login", command=self.login, 
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                                   relief="flat", width=12, height=1)
        self.login_btn.place(x=725, y=340)
        self.login_btn.default_bg = "#4CAF50"
        self.login_btn.bind("<Enter>", on_enter)
        self.login_btn.bind("<Leave>", on_leave)

        self.signup_btn = tk.Button(self.root, text="Signup", command=self.open_signup_form, 
                                    bg="#007BFF", fg="white", font=("Arial", 10, "bold"), 
                                    relief="flat", width=12, height=1)
        self.signup_btn.place(x=725, y=380)
        self.signup_btn.default_bg = "#007BFF"
        self.signup_btn.bind("<Enter>", on_enter)
        self.signup_btn.bind("<Leave>", on_leave)

        # Delete Account Button
        self.delete_btn = tk.Button(self.root, text="Delete Account", command=self.open_delete_account_popup, 
                                    bg="#DC143C", fg="white", font=("Arial", 10, "bold"), 
                                    relief="flat", width=12, height=1)
        self.delete_btn.place(x=725, y=420)
        self.delete_btn.default_bg = "#DC143C"
        self.delete_btn.bind("<Enter>", on_enter)
        self.delete_btn.bind("<Leave>", on_leave)

    def toggle_password_visibility(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
            self.show_password.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.show_password.config(text="Show")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            self.root.destroy()
            Dashboard(email)
        else:
            messagebox.showerror("Error", "Login failed. Invalid email or password.")

    def open_signup_form(self):
        # Open a new window for signup form
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Signup Form")
        signup_window.geometry("500x350")
        signup_window.resizable(0,0)
        tk.Label(signup_window, text='Fill out the form with your details!', font=("Arial", 12)).pack()
        signup_window.iconbitmap(r"C:\Users\ASUS\Desktop\ExpenseMate\add-friend.ico")

        # Labels and Entries for signup form
        tk.Label(signup_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(signup_window)
        name_entry.pack(pady=5)

        tk.Label(signup_window, text="Birthdate (DD/MM/YYYY):").pack(pady=5)
        birthdate_entry = tk.Entry(signup_window)
        birthdate_entry.pack(pady=5)

        tk.Label(signup_window, text="Email:").pack(pady=5)
        email_entry = tk.Entry(signup_window)
        email_entry.pack(pady=5)

        tk.Label(signup_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(signup_window, show="*")
        password_entry.pack(pady=5)

        # Show/Hide Password Button
        show_password = tk.Button(signup_window, text="Show", command=lambda: self.toggle_password_visibility_signup(password_entry, show_password))
        show_password.place(x=320,y=238)

        # Button to submit signup form
        tk.Button(signup_window, text="Submit", command=lambda: self.signup(
            name_entry.get(), birthdate_entry.get(), email_entry.get(), password_entry.get(), signup_window
        )).pack(pady=10)

    def toggle_password_visibility_signup(self, password_entry, show_button):
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
            show_button.config(text="Hide")
        else:
            password_entry.config(show="*")
            show_button.config(text="Show")

    def signup(self, name, birthdate, email, password, window):
        if not all([name, birthdate, email, password]):
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                cursor.execute("INSERT INTO users (email, name, birthdate, password) VALUES (?, ?, ?, ?)",
                               (email, name, birthdate, password))
                conn.commit()
                messagebox.showinfo("Success", "Signup successful! Please login.")
                window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already exists. Please login.")
    
    def open_delete_account_popup(self):
        delete_popup = tk.Toplevel(self.root)
        delete_popup.title("Delete Account")
        delete_popup.geometry("300x150")

        tk.Label(delete_popup, text="Enter Email to Delete Account:").pack(pady=10)
        self.delete_email_entry = tk.Entry(delete_popup)
        self.delete_email_entry.pack(pady=5)

        tk.Button(delete_popup, text="Delete Account", command=self.delete_account).pack(pady=10)

    def delete_account(self):
        email_to_delete = self.delete_email_entry.get()
        if not email_to_delete:
            messagebox.showerror("Error", "Please enter the email to delete the account.")
        else:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email_to_delete,))
            user = cursor.fetchone()
            if user:
                cursor.execute("DELETE FROM users WHERE email = ?", (email_to_delete,))
                cursor.execute("DELETE FROM expenses WHERE email = ?", (email_to_delete,))
                conn.commit()
                messagebox.showinfo("Success", f"Account with email {email_to_delete} deleted successfully.")
            else:
                messagebox.showerror("Error", "Email not found. Please check the email and try again.")

# Dashboard Page
class Dashboard:
    def __init__(self, email):
        self.email = email
        self.dashboard_root = tk.Tk()
        self.dashboard_root.title("Dashboard")
        self.dashboard_root.geometry("1540x900")
        self.dashboard_root.iconbitmap(r"C:\Users\ASUS\Desktop\ExpenseMate\monitor.ico")
        self.dashboard_root.resizable(0, 0)

        # Load and set background image
        self.bg_image = Image.open(r"C:\Users\ASUS\Desktop\ExpenseMate\pexels-tamanna-rumee-52377920-8749133.jpg")
        self.bg_image = self.bg_image.resize((1540, 900))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.dashboard_root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.logo1_image = Image.open(r"C:\Users\ASUS\Desktop\ExpenseMate\Screenshot (55).png")  # Replace with your logo image path
        self.logo1_image = self.logo1_image.resize((340,140))  # Resize the logo image (adjust size as needed)
        self.logo1_photo = ImageTk.PhotoImage(self.logo1_image)

        # Create a Label with the resized logo image and position it on top
        self.logo1_label = tk.Label(self.dashboard_root, image=self.logo1_photo, bg="#FFDAB9")  # Background color optional
        self.logo1_label.place(x=600, y=30) 

        # Fetch user name for welcome message
        cursor.execute("SELECT name FROM users WHERE email = ?", (self.email,))
        user_name = cursor.fetchone()[0]
        welcome_message = f"Welcome, {user_name}!"

        tk.Label(
            self.dashboard_root,
            text=welcome_message,
            font=("Arial", 18, "bold"),
            bg="#FFD166",  # Warm yellow-orange
            fg="#333333",  # Darker text for contrast
            padx=5,
            pady=5
        ).place(x=30,y=30)

        # Expense Table with Styling
        self.tree = ttk.Treeview(
            self.dashboard_root,
            columns=("Date", "Expenses", "Amount"),
            show="headings",
            height=12
            
        )
        
        self.tree.heading("Date", text="Date (DD/MM)")
        self.tree.heading("Expenses", text="Expenses")
        self.tree.heading("Amount", text="Amount")

        # Style the table
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#FFF8E1", fieldbackground="#FFF8E1")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#FF9F1C", foreground="black")
        self.tree.place(x=50,y=370)

    
         # Loan Table
        self.loan_tree = ttk.Treeview(
            self.dashboard_root,
            columns=("Name", "Amount", "Type", "Date","Status"),
            show="headings",
            height=12
        )
        
        self.loan_tree.heading("Name", text="Person's Name")
        self.loan_tree.heading("Amount", text="Amount")
        self.loan_tree.heading("Type", text="Type")
        self.loan_tree.heading("Date", text="Date")
        self.loan_tree.heading("Status", text="Status")

        self.loan_tree.column("Name", width=150)
        self.loan_tree.column("Amount", width=150)
        self.loan_tree.column("Type", width=150)
        self.loan_tree.column("Date", width=150)
        self.loan_tree.column("Status", width=150)

        # Style the loan table
        style.configure("LoanTreeview", font=("Arial", 12), rowheight=25, background="#FFF8E1", fieldbackground="#FFF8E1")
        style.configure("LoanTreeview.Heading", font=("Arial", 13, "bold"), background="#8A2BE2", foreground="black")
        self.loan_tree.place(x=700,y=370)
        

        # Define button styles
        button_config = {
            "font": ("Arial", 12, "bold"),
            "width": 15,
            "height": 1,
            "bd": 3
        }

        # Add Buttons with new color scheme
        self.add_expense_btn = tk.Button(
            self.dashboard_root,
            text="➕ Add Expense",
            command=self.open_add_expense_form,
            bg="#FF9F1C", fg="white", **button_config
        )
        self.add_expense_btn.place(x=80, y=300)

        self.view_report_btn = tk.Button(
            self.dashboard_root,
            text="📊 View Report",
            command=self.view_report,
            bg="#118AB2", fg="white", **button_config
        )
        self.view_report_btn.place(x=272, y=300)

        self.delete_expense_btn = tk.Button(
            self.dashboard_root,
            text="🗑 Delete",
            command=self.open_delete_expense_form,
            bg="#EF476F", fg="white", **button_config
        )
        self.delete_expense_btn.place(x=490, y=715)

        self.logout_btn = tk.Button(
            self.dashboard_root,
            text="🔓 Logout",
            command=self.logout,
            bg="#FFD166", fg="black", **button_config
        )
        self.logout_btn.place(x=1300, y=30)
        self.loan_btn = tk.Button(
            self.dashboard_root,
            text="💰 Loan",
            command=self.open_loan_page,
            bg="#8A2BE2", fg="white", **button_config
        )
        self.loan_btn.place(x=750, y=300)
        self.mark_paid_btn = tk.Button(
           self.dashboard_root,
           text="✔️ Paid",
           command=self.open_paid_loan_form,  # Bind to the method that marks a loan as paid
           bg="#06D6A0", fg="white", **button_config
        )
        self.mark_paid_btn.place(x=1290, y=715)
        self.load_expenses()

        # Hover effects for buttons
        self.add_expense_btn.bind("<Enter>", lambda e: self.add_expense_btn.config(bg="#FF7F50"))
        self.add_expense_btn.bind("<Leave>", lambda e: self.add_expense_btn.config(bg="#FF9F1C"))

        self.view_report_btn.bind("<Enter>", lambda e: self.view_report_btn.config(bg="#0E6A90"))
        self.view_report_btn.bind("<Leave>", lambda e: self.view_report_btn.config(bg="#118AB2"))

        self.delete_expense_btn.bind("<Enter>", lambda e: self.delete_expense_btn.config(bg="#D72658"))
        self.delete_expense_btn.bind("<Leave>", lambda e: self.delete_expense_btn.config(bg="#EF476F"))

        self.logout_btn.bind("<Enter>", lambda e: self.logout_btn.config(bg="#FFC300"))
        self.logout_btn.bind("<Leave>", lambda e: self.logout_btn.config(bg="#FFD166"))

        self.loan_btn.bind("<Enter>", lambda e: self.loan_btn.config(bg="#6A1B9A"))
        self.loan_btn.bind("<Leave>", lambda e: self.loan_btn.config(bg="#8A2BE2"))

        self.mark_paid_btn.bind("<Enter>", lambda e: self.mark_paid_btn.config(bg="#2E8B57"))  # Darker green on hover  
        self.mark_paid_btn.bind("<Leave>", lambda e: self.mark_paid_btn.config(bg="#3CB371"))
    def open_loan_page(self):
        loan_window = tk.Toplevel(self.dashboard_root)
        loan_window.title("Loan Management")
        loan_window.geometry("600x400")
        loan_window.iconbitmap(r"C:\Users\ASUS\Desktop\ExpenseMate\loan.ico")

        tk.Label(loan_window, text="Person's Name:").pack(pady=5)
        name_entry = tk.Entry(loan_window)
        name_entry.pack(pady=5)

        tk.Label(loan_window, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(loan_window)
        amount_entry.pack(pady=5)

        tk.Label(loan_window, text="Type (Loan or Debt):").pack(pady=5)
        type_entry = tk.Entry(loan_window)
        type_entry.pack(pady=5)

        tk.Label(loan_window, text="Date (DD/MM):").pack(pady=5)
        date_entry = tk.Entry(loan_window)
        date_entry.pack(pady=5)

    # Button to submit loan form
        tk.Button(loan_window, text="Submit", command=lambda: self.add_loan(
        name_entry.get(), amount_entry.get(), type_entry.get(), date_entry.get(), loan_window
        )).pack(pady=5)

    def add_loan(self, name, amount, type_of_loan, date, window):
    
        if not name or not amount or not type_of_loan or not date:
           messagebox.showerror("Error", "All fields are required!")
           return

        try:
            amount = float(amount)  # Ensure amount is a valid number
        except ValueError:
          messagebox.showerror("Error", "Amount must be a valid number!")
          return

    # Insert into Treeview
        
        cursor.execute("INSERT INTO loans (email, name, amount, type, date,status) VALUES (?, ?, ?, ?, ?,?)",
                   (self.email, name, amount, type_of_loan, date,"Unpaid"))
        conn.commit()

        self.loan_tree.insert("", "end", values=(name, amount, type_of_loan, date, "Unpaid"))

        messagebox.showinfo("Success", "Loan added successfully!")
        window.destroy()
      
    def open_paid_loan_form(self):
        """Marks a loan as paid in the Treeview and database."""
        selected_item = self.loan_tree.selection()  # Get the selected item from the Treeview

        if not selected_item:
           messagebox.showerror("Error", "Please select a loan to mark as paid.")
           return
    
    # Get values from the selected row
        selected_loan = self.loan_tree.item(selected_item)
        loan_name = selected_loan['values'][0]  # Name of the person
        loan_amount = selected_loan['values'][1]  # Amount of the loan
        loan_type = selected_loan['values'][2]   # Type of the loan
        loan_date = selected_loan['values'][3]   # Date of the loan

    # Confirm mark as paid
        confirm = messagebox.askyesno("Confirm Paid", f"Are you sure this loan has been paid?\n\n"
                                                  f"Name: {loan_name}\nAmount: {loan_amount}\nType: {loan_type}\nDate: {loan_date}")
        if not confirm:
            return  # Exit if user doesn't confirm

    # Step 3: Update the loan's status in the database
        cursor.execute("UPDATE loans SET status = ? WHERE email = ? AND name = ? AND amount = ? AND type = ? AND date = ?",
                   ("Paid", self.email, loan_name, loan_amount, loan_type, loan_date))
        conn.commit()

    # Step 4: Update the Treeview to show the loan as paid
        self.loan_tree.item(selected_item, values=(loan_name, loan_amount, loan_type, loan_date, "Paid"))

        messagebox.showinfo("Success", "Loan marked as paid successfully!")

    def open_add_expense_form(self):
        # Open a new window for add expense form
        expense_window = tk.Toplevel(self.dashboard_root)
        expense_window.title("Add Expense")
        expense_window.geometry("400x300")
        expense_window.iconbitmap(r"C:\Users\ASUS\Desktop\ExpenseMate\spending.ico")

        # Labels and Entries for add expense form
        tk.Label(expense_window, text="Date (DD/MM):").pack(pady=5)
        date_entry = tk.Entry(expense_window)
        date_entry.pack(pady=5)

        tk.Label(expense_window, text="Expense Topic:").pack(pady=5)
        expense_entry = tk.Entry(expense_window)
        expense_entry.pack(pady=5)

        tk.Label(expense_window, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(expense_window)
        amount_entry.pack(pady=5)

        # Button to submit add expense form
        tk.Button(expense_window, text="Submit", command=lambda: self.add_expense(
            date_entry.get(), expense_entry.get(), amount_entry.get(), expense_window
        )).pack(pady=5)

    def add_expense(self, date, expense, amount, window):
       """Adds an expense to the Treeview and the database immediately (fixes duplicate saving)."""
       if not date or not expense or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return

       try:
            amount = float(amount)  # Ensure amount is a valid number
       except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return

        # Insert into database immediately to prevent duplicate saving
       cursor.execute("INSERT INTO expenses (email, date, expense, amount) VALUES (?, ?, ?, ?)",
                       (self.email, date, expense, amount))
       conn.commit()

        # Insert into Treeview
       self.tree.insert("", "end", values=(date, expense, amount))
       messagebox.showinfo("Success", "Expense added successfully!")
       window.destroy()

    def view_report(self):
        cursor.execute("SELECT date, expense, amount FROM expenses WHERE email = ?", (self.email,))
        expenses = cursor.fetchall()

        if not expenses:
            messagebox.showinfo("Report", "No expenses to display.")
        else:
            report = "Expense Report:\n"
            total_expenses = 0
            for date, expense, amount in expenses:
                report += f"Date: {date}, Expense: {expense}, Amount: {amount}\n"
                total_expenses += amount
            report += f"\nTotal Expenses: {total_expenses}"
            messagebox.showinfo("Report", report)

    def open_delete_expense_form(self):
        selected_item = self.tree.selection()  # Get selected item

        if not selected_item:
            messagebox.showerror("Error", "Please select an expense to delete!")
            return

        # Get selected expense details
        item_values = self.tree.item(selected_item, "values")
        if not item_values:
            messagebox.showerror("Error", "No valid expense selected!")
            return

        date, expense, amount = item_values  # Extract details

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{expense}'?")
        if confirm:
            # Remove from Treeview
            self.tree.delete(selected_item)

            # Remove from the database
            cursor.execute("DELETE FROM expenses WHERE email = ? AND date = ? AND expense = ? AND amount = ?",
                           (self.email, date, expense, amount))
            conn.commit()

            messagebox.showinfo("Success", f"Expense '{expense}' deleted successfully!")

    def load_expenses(self):
   
    # Load expenses
        cursor.execute("SELECT date, expense, amount FROM expenses WHERE email = ?", (self.email,))
        expenses = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())  # Clear existing data

        for date, expense, amount in expenses:
           self.tree.insert("", "end", values=(date, expense, amount))

    # Load loans
        cursor.execute("SELECT name, amount, type, date, status FROM loans WHERE email = ?", (self.email,))
        loans = cursor.fetchall()
        self.loan_tree.delete(*self.loan_tree.get_children())  # Clear existing data

        for name, amount, loan_type, date, status in loans:
           self.loan_tree.insert("", "end", values=(name, amount, loan_type, date, status))
    def logout(self):
        self.dashboard_root.destroy()
        root = tk.Tk()
        root.state('zoomed')
        LoginSignupPage(root)
        root.mainloop()
    

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.iconbitmap(r"C:\Users\ASUS\Desktop\ExpenseMate\salary.ico")
    LoginSignupPage(root)
    root.mainloop()