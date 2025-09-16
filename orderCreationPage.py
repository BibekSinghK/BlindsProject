import customtkinter as ctk
from customer import Customer
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class OrderCreationPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        self.conn = sqlite3.connect("blinds_app.db")
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")    
    
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=0)

        name_label = ctk.CTkLabel(frame, text="Customer Name:", font=("Helvetica", 20))
        name_label.pack(pady=(0, 10))

        self.customer_name_entry = ctk.CTkEntry(frame, width=300, height=40, placeholder_text="Enter customer name")
        self.customer_name_entry.pack(pady=(0, 20))

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)

        back_btn = ctk.CTkButton(button_frame, text="Back", width=150,
                                 command=lambda: self.master.show_frame(self.master.welcome_page))
        back_btn.pack(side="left", padx=10)

        next_btn = ctk.CTkButton(button_frame, text="Next", width=150, command=self.on_next)
        next_btn.pack(side="left", padx=10)
    
    def customer_exists(self, name):
        self.cursor.execute("SELECT 1 FROM customers WHERE name = ?;", (name,))
        return self.cursor.fetchone() is not None
    
    def on_next(self):
        customer_name = self.customer_name_entry.get().strip()
        if customer_name == "":
            messagebox.showwarning("Warning", "Please enter a customer name!")
        elif self.customer_exists(customer_name):
            messagebox.showwarning("Warning", "Customer name already exists!")
        else:
            customer_id = self.master.db.add_customer(customer_name)
            self.master.curr_customer = Customer(customer_name, customer_id)
            self.customer_name_entry.delete(0, "end")
            self.master.show_frame(self.master.blind_creation_page)